import gzip
import hashlib
import io
import json
import os
import shutil
import tempfile

import requests
import responses

from hatcher.testing import unittest
from ..auth import BroodBearerTokenAuth
from ..brood_url_handler import BroodURLHandler
from ..utils import compute_sha256


def _compress_data(buf):
    zbuf = io.BytesIO()
    gz = gzip.GzipFile(None, 'wb', 9, zbuf)
    try:
        gz.write(buf)
    finally:
        gz.close()
    return zbuf.getvalue()


class TestBroodURLHandler(unittest.TestCase):

    @responses.activate
    def test_bearer_token_auth(self):
        # Given
        token = 'token'
        url_handler = BroodURLHandler.from_auth(
            'http://brood-dev',
            auth=BroodBearerTokenAuth(token),
        )
        self.auth_header = None

        def callback(request):
            self.auth_header = request.headers.get('Authorization')
            return (200, {}, '')

        responses.add_callback(
            responses.GET,
            '{scheme}://{host}/'.format(
                scheme=url_handler.scheme,
                host=url_handler.host,
            ),
            callback,
        )

        # When
        url_handler.get('/')

        # Then
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(self.auth_header, 'Bearer {0}'.format(token))

    @responses.activate
    def test_session_injection(self):
        # Given
        expected = {'User-Agent': 'dummy'}
        session = requests.Session()
        session.headers = expected.copy()

        self.headers = None

        def callback(request):
            self.headers = request.headers.copy()
            return (200, {}, '')

        # When
        url_handler = BroodURLHandler.from_session(
            'http://brood-dev', session)

        # Then
        self.assertIs(url_handler._session, session)

        # Given
        responses.add_callback(
            responses.GET,
            '{scheme}://{host}/'.format(
                scheme=url_handler.scheme,
                host=url_handler.host,
            ),
            callback,
        )

        # When
        url_handler.get('/')

        # Then
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(self.headers, expected)

    def _compressed_payload_factory(self, json_dict, strip_header=False):
        def callback(request):
            encodings_string = request.headers.get("accept-encoding")
            encodings = [p.strip() for p in encodings_string.split(",")]
            if "gzip" in encodings:
                payload = _compress_data(json.dumps(json_dict).encode("utf8"))
                if strip_header:
                    headers = {}
                else:
                    headers = {"Content-Encoding": "gzip"}
            else:
                payload = json_dict
            return (200, headers, payload)
        return callback

    @responses.activate
    def test_get_json_compressed_simple(self):
        # Given
        r_data = {"key": "value"}
        session = requests.Session()

        responses.add_callback(
            responses.GET, "http://brood-dev/json",
            self._compressed_payload_factory(r_data),
        )

        url_handler = BroodURLHandler.from_session(
            'http://brood-dev', session)

        # When
        data = url_handler.get_json("/json")

        # Then
        self.assertEqual(data, r_data)

        # Given
        session = requests.Session()
        session.headers.update({"Accept-Encoding": ""})

        # When
        data = url_handler.get_json("/json")

        # Then
        self.assertEqual(data, r_data)

    @responses.activate
    def test_get_json_compressed_stripped_header(self):
        # Given
        r_data = {"key": "value"}
        session = requests.Session()

        responses.add_callback(
            responses.GET, "http://brood-dev/json",
            self._compressed_payload_factory(r_data, strip_header=True),
        )

        url_handler = BroodURLHandler.from_session(
            'http://brood-dev', session)

        # When
        data = url_handler.get_json("/json")

        # Then
        self.assertEqual(data, r_data)

        # Given
        session = requests.Session()
        session.headers.update({"Accept-Encoding": ""})

        # When
        data = url_handler.get_json("/json")

        # Then
        self.assertEqual(data, r_data)


class TestDownloadFile(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='hatcher-download-test-')
        self.host = 'http://brood-dev'
        self.url_handler = BroodURLHandler.from_auth(self.host)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @responses.activate
    def test_download_file_exists(self):
        # Given
        data = 'body'.encode('ascii')
        filename = 'test-1.2.3-1.egg'
        path = os.path.join(self.temp_dir, filename)

        with open(path, 'wb') as fh:
            fh.write(data)

        sha256 = compute_sha256(path)
        uri = '{0}/'.format(self.host)

        expected_content_length = len(data)

        def get_response(request):
            headers = {
                'Content-Length': str(expected_content_length),
                'Content-Disposition': 'attachment; filename="{0}"'.format(
                    filename),
                'Content-Type': 'application/octet-stream',
            }
            return (200, headers, 'body'.encode('ascii'))

        responses.add_callback(
            responses.GET, uri,
            callback=get_response,
        )

        # When
        content_length, download_iter = self.url_handler.iter_download(
            '/', self.temp_dir, sha256)

        content_chunks = [v for v in download_iter]

        # Then
        self.assertEqual(content_length, expected_content_length)
        self.assertEqual(content_chunks, [content_length])

        with open(path, 'rb') as fh:
            downloaded_data = fh.read()
        self.assertEqual(downloaded_data, data)

    @responses.activate
    def test_download_file_exists_not_redownloaded(self):
        ## This test is the same as test_download_file_exists, but uses
        ## a bad body value to assert that the file is not re-downloaded
        ## and therefore changed.
        # Given
        data = 'body'.encode('ascii')
        filename = 'test-1.2.3-1.egg'
        path = os.path.join(self.temp_dir, filename)

        with open(path, 'wb') as fh:
            fh.write(data)

        sha256 = compute_sha256(path)
        uri = '{0}/'.format(self.host)

        expected_content_length = len(data)

        def get_response(request):
            headers = {
                'Content-Length': str(expected_content_length),
                'Content-Disposition': 'attachment; filename="{0}"'.format(
                    filename),
                'Content-Type': 'application/octet-stream',
            }
            ### Bad body value here.
            return (200, headers, 'nono'.encode('ascii'))

        responses.add_callback(
            responses.GET, uri,
            callback=get_response,
        )

        # When
        content_length, download_iter = self.url_handler.iter_download(
            '/', self.temp_dir, sha256)

        content_chunks = [v for v in download_iter]

        # Then
        self.assertEqual(content_length, expected_content_length)
        self.assertEqual(content_chunks, [content_length])

        with open(path, 'rb') as fh:
            downloaded_data = fh.read()
        self.assertEqual(downloaded_data, data)

    @responses.activate
    def test_download_file_exists_bad_sha(self):
        # Given
        data = 'nono'.encode('ascii')
        bad_data = 'body'.encode('ascii')
        filename = 'test-1.2.3-1.egg'
        path = os.path.join(self.temp_dir, filename)

        with open(path, 'wb') as fh:
            fh.write(bad_data)

        sha256 = hashlib.sha256(data).hexdigest()
        uri = '{0}/'.format(self.host)

        expected_content_length = len(data)

        def get_response(request):
            headers = {
                'Content-Length': str(expected_content_length),
                'Content-Disposition': 'attachment; filename="{0}"'.format(
                    filename),
                'Content-Type': 'application/octet-stream',
            }
            return (200, headers, 'nono'.encode('ascii'))

        responses.add_callback(
            responses.GET, uri,
            callback=get_response,
        )

        # When
        content_length, download_iter = self.url_handler.iter_download(
            '/', self.temp_dir, sha256)

        content_chunks = [v for v in download_iter]

        # Then
        self.assertEqual(content_length, expected_content_length)
        self.assertEqual(content_chunks, [content_length])

        with open(path, 'rb') as fh:
            downloaded_data = fh.read()
        self.assertEqual(downloaded_data, data)
