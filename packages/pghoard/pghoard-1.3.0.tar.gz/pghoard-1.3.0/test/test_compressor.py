"""
pghoard

Copyright (c) 2015 Ohmu Ltd
See LICENSE for details
"""
# pylint: disable=attribute-defined-outside-init
from .base import PGHoardTestCase, CONSTANT_TEST_RSA_PUBLIC_KEY, CONSTANT_TEST_RSA_PRIVATE_KEY
from .test_wal import wal_header_for_file
from io import BytesIO
from pghoard.compressor import CompressorThread
from pghoard.rohmu import IO_BLOCK_SIZE
from pghoard.rohmu.compressor import snappy
from queue import Queue
import lzma
import os
import pytest


class TestXlog:
    def __init__(self, path, name, mode):
        """Create a random or zero file resembling a valid xlog, bigger than block size, with a valid header."""
        self.path = os.path.join(path, name)
        self.path_partial = self.path + ".partial"
        self.contents = wal_header_for_file(name)
        if mode == "random":
            self.contents += os.urandom(IO_BLOCK_SIZE * 2)
        elif mode == "zero":
            zeros = (IO_BLOCK_SIZE * 2 - 32) * b"\x00"
            self.contents += os.urandom(16) + zeros + os.urandom(16)

        with open(self.path, "wb") as out:
            out.write(self.contents)
            self.size = out.tell()


class Compression(PGHoardTestCase):
    algorithm = None

    def compress(self, data):
        raise NotImplementedError

    def decompress(self, data):
        raise NotImplementedError

    def setup_method(self, method):
        super().setup_method(method)
        self.config = self.config_template()
        self.config["backup_sites"][self.test_site] = {
            "encryption_key_id": None,
            "encryption_keys": {
                "testkey": {
                    "public": CONSTANT_TEST_RSA_PUBLIC_KEY,
                    "private": CONSTANT_TEST_RSA_PRIVATE_KEY
                },
            },
            "object_storage": {
                "storage_type": "s3",
            },
            "pg_version": 90500,
        }
        self.config["compression"]["algorithm"] = self.algorithm
        self.compression_queue = Queue()
        self.transfer_queue = Queue()
        self.incoming_path = os.path.join(self.temp_dir, self.test_site, "xlog")
        os.makedirs(self.incoming_path)
        self.handled_path = os.path.join(self.config["backup_location"], self.test_site, "xlog")
        os.makedirs(self.handled_path)

        self.compressor = CompressorThread(config=self.config,
                                           compression_queue=self.compression_queue,
                                           transfer_queue=self.transfer_queue)
        self.compressor.start()

    def teardown_method(self, method):
        self.compressor.running = False
        self.compression_queue.put({"type": "QUIT"})
        self.compressor.join()
        super().teardown_method(method)

    def test_get_event_type(self):
        # Rename from .partial to final should be recognized
        event = {
            "full_path": "/out/00000001000000000000000C",
            "src_path": "/tmp/00000001000000000000000C.partial",
            "type": "MOVE",
        }
        assert self.compressor.get_event_filetype(event) == "xlog"
        # Rename from non-partial suffix is not recognized
        event["src_path"] += "xyz"
        assert self.compressor.get_event_filetype(event) is None
        # "CLOSE_WRITE" doesn't consider src_path
        del event["src_path"]
        event["type"] = "CLOSE_WRITE"
        assert self.compressor.get_event_filetype(event) == "xlog"
        # other event types are ignored
        event["type"] = "NAKKI"
        assert self.compressor.get_event_filetype(event) is None

        # Timeline history files are handled the same way (do they actually ever have .partial?)
        event = {
            "full_path": "/xlog/0000000A.history",
            "src_path": "/tmp/0000000A.history.partial",
            "type": "MOVE",
        }
        assert self.compressor.get_event_filetype(event) == "timeline"
        event["src_path"] += "xyz"
        assert self.compressor.get_event_filetype(event) is None
        del event["src_path"]
        event["type"] = "CLOSE_WRITE"
        assert self.compressor.get_event_filetype(event) == "timeline"

        event = {
            "full_path": "/data/base.tar",
            "type": "CLOSE_WRITE",
        }
        assert self.compressor.get_event_filetype(event) == "basebackup"

    def test_compress_fileobj(self):
        ifile = TestXlog(self.incoming_path, "00000001000000000000000C", "random")
        with open(ifile.path, "rb") as input_obj, BytesIO() as output_obj:
            orig_len, compr_len = self.compressor.compress_fileobj(
                input_obj=input_obj,
                output_obj=output_obj,
                compression_algorithm=self.algorithm)
            assert output_obj.tell() == compr_len
            assert len(output_obj.getvalue()) == compr_len
            assert orig_len == ifile.size

    def test_compress_to_file_xlog(self):
        ifile = TestXlog(self.incoming_path, "00000001000000000000000C", "random")
        self._test_compress_to_file("xlog", ifile.size, ifile.path, ifile.path_partial)

    def test_compress_to_file_history(self):
        file_path = os.path.join(self.incoming_path, "0000000F.history")
        contents = "\n".join("# FOOBAR {}".format(n) for n in range(10)) + "\n"
        contents = contents.encode("ascii")
        with open(file_path, "wb") as out:
            out.write(contents)
            file_size = out.tell()

        self._test_compress_to_file("timeline", file_size, file_path, file_path + ".partial")

    def _test_compress_to_file(self, filetype, file_size, file_path, file_path_partial):
        self.compression_queue.put({
            "type": "MOVE",
            "src_path": file_path_partial,
            "full_path": file_path,
        })
        transfer_event = self.transfer_queue.get(timeout=1.0)
        expected = {
            "filetype": filetype,
            "local_path": file_path.replace(self.incoming_path, self.handled_path),
            "metadata": {
                "compression-algorithm": self.algorithm,
                "compression-level": 0,
                "original-file-size": file_size,
                "pg-version": 90500,
            },
            "site": self.test_site,
        }
        for key, value in expected.items():
            assert transfer_event[key] == value

    def test_compress_to_memory(self):
        ifile = TestXlog(self.incoming_path, "00000001000000000000000C", "random")
        self.compression_queue.put({
            "compress_to_memory": True,
            "delete_file_after_compression": False,
            "full_path": ifile.path,
            "src_path": ifile.path_partial,
            "type": "MOVE",
        })
        expected = {
            "callback_queue": None,
            "filetype": "xlog",
            "local_path": ifile.path,
            "metadata": {
                "compression-algorithm": self.algorithm,
                "compression-level": 0,
                "original-file-size": ifile.size,
                "pg-version": 90500,
            },
            "site": self.test_site,
        }
        transfer_event = self.transfer_queue.get(timeout=1.0)
        for key, value in expected.items():
            assert transfer_event[key] == value

        assert self.decompress(transfer_event["blob"]) == ifile.contents

    def test_compress_encrypt_to_memory(self):
        ifile = TestXlog(self.incoming_path, "00000001000000000000000C", "random")
        self.compressor.config["backup_sites"][self.test_site]["encryption_key_id"] = "testkey"
        event = {
            "compress_to_memory": True,
            "delete_file_after_compression": False,
            "full_path": ifile.path,
            "src_path": ifile.path_partial,
            "type": "MOVE",
        }
        self.compressor.handle_event(event, filetype="xlog")
        expected = {
            "callback_queue": None,
            "filetype": "xlog",
            "local_path": ifile.path,
            "metadata": {
                "compression-algorithm": self.algorithm,
                "compression-level": 0,
                "encryption-key-id": "testkey",
                "original-file-size": ifile.size,
                "pg-version": 90500,
            },
            "site": self.test_site,
        }
        transfer_event = self.transfer_queue.get(timeout=1.0)
        for key, value in expected.items():
            assert transfer_event[key] == value

    def test_archive_command_compression(self):
        zero = TestXlog(self.incoming_path, "00000001000000000000000D", "zero")
        callback_queue = Queue()
        event = {
            "callback_queue": callback_queue,
            "compress_to_memory": True,
            "delete_file_after_compression": False,
            "full_path": zero.path,
            "src_path": zero.path_partial,
            "type": "CLOSE_WRITE",
        }
        transfer_event = self.compression_queue.put(event)
        transfer_event = self.transfer_queue.get(timeout=1.0)
        expected = {
            "callback_queue": callback_queue,
            "filetype": "xlog",
            "local_path": zero.path,
            "metadata": {
                "compression-algorithm": self.algorithm,
                "compression-level": 0,
                "original-file-size": zero.size,
                "pg-version": 90500,
            },
            "site": self.test_site,
        }
        for key, value in expected.items():
            assert transfer_event[key] == value

        assert self.decompress(transfer_event["blob"]) == zero.contents

    def test_decompression_event(self):
        ifile = TestXlog(self.incoming_path, "00000001000000000000000A", "random")
        callback_queue = Queue()
        local_filepath = os.path.join(self.temp_dir, "00000001000000000000000A")
        self.compression_queue.put({
            "blob": self.compress(ifile.contents),
            "callback_queue": callback_queue,
            "filetype": "xlog",
            "local_path": local_filepath,
            "metadata": {
                "compression-algorithm": self.algorithm,
                "compression-level": 0,
                "original-file-size": ifile.size,
                "pg-version": 90500,
            },
            "site": self.test_site,
            "type": "DECOMPRESSION",
        })
        callback_queue.get(timeout=1.0)
        assert os.path.exists(local_filepath) is True
        with open(local_filepath, "rb") as fp:
            assert fp.read() == ifile.contents

    def test_decompression_decrypt_event(self):
        ifile = TestXlog(self.incoming_path, "00000001000000000000000E", "random")
        output_obj = BytesIO()
        with open(ifile.path, "rb") as input_obj:
            self.compressor.compress_fileobj(
                input_obj=input_obj,
                output_obj=output_obj,
                compression_algorithm=self.config["compression"]["algorithm"],
                compression_level=self.config["compression"]["level"],
                rsa_public_key=CONSTANT_TEST_RSA_PUBLIC_KEY)
        callback_queue = Queue()
        local_filepath = os.path.join(self.temp_dir, "00000001000000000000000E")
        self.compression_queue.put({
            "blob": output_obj.getvalue(),
            "callback_queue": callback_queue,
            "filetype": "xlog",
            "local_path": local_filepath,
            "metadata": {
                "compression-algorithm": self.algorithm,
                "compression-level": 0,
                "encryption-key-id": "testkey",
                "original-file-size": ifile.size,
                "pg-version": 90500,
            },
            "site": self.test_site,
            "type": "DECOMPRESSION",
        })
        callback_queue.get(timeout=1.0)
        assert os.path.exists(local_filepath) is True
        with open(local_filepath, "rb") as fp:
            assert fp.read() == ifile.contents


class TestLzmaCompression(Compression):
    algorithm = "lzma"

    def compress(self, data):
        return lzma.compress(data)

    def decompress(self, data):
        return lzma.decompress(data)


@pytest.mark.skipif(not snappy, reason="snappy not installed")
class TestSnappyCompression(Compression):
    algorithm = "snappy"

    def compress(self, data):
        return snappy.StreamCompressor().compress(data)

    def decompress(self, data):
        return snappy.StreamDecompressor().decompress(data)
