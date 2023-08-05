from datetime import datetime
import json
import shutil
import tempfile
import textwrap

import pytz
import responses
from mock import patch
from six.moves.urllib import parse
from tabulate import tabulate

from hatcher.core.url_templates import URLS
from hatcher.core.utils import compute_sha256
from hatcher.errors import ChecksumMismatchError
from hatcher.testing import (
    unittest, runtime_from_metadata,
    RUNTIME_CPYTHON_2_7_10_RH5_X86_64_METADATA,
)
from hatcher.tests.common import MainTestingMixin, patch_repository
from hatcher.cli import main, utils


class TestRuntimeMetadataMain(MainTestingMixin, unittest.TestCase):

    def setUp(self):
        MainTestingMixin.setUp(self)
        self.initial_args = ['--api-version', '1',
                             '--url', 'brood-dev.invalid', 'runtimes',
                             'metadata']
        self.final_args = [self.organization, self.repository, 'rh5-x86_64',
                           'cpython', '2.7.10+1']

    @patch_repository
    def test_runtime_metadata(self, Repository):
        # Given
        expected = {
            "abi": "gnu",
            "build_revision": "2.1.0-dev570",
            "filename": "cpython-2.7.10+1-rh5_x86_64-gnu.runtime",
            "implementation": "cpython",
            "language_version": "2.7.10",
            "metadata_version": "1.0",
            "platform": "rh5-x86_64",
            "sha256": "81ec4d15bd8b131c80eb72cb0f5222846e306bb3f1dd8ce572ffbe859ace1608",  # noqa
            "version": "2.7.10+1"
        }
        repository, platform_repo = self._mock_repository_class(Repository)
        runtime_metadata = platform_repo.runtime_metadata
        runtime_metadata.return_value = expected

        # When
        result = self.runner.invoke(
            main.hatcher,
            args=self.initial_args + self.final_args,
        )

        # Then
        self.assertRepositoryConstructedCorrectly(Repository)
        runtime_metadata.assert_called_once_with('cpython', '2.7.10+1')
        self.assertEqual(json.loads(result.output), expected)
        self.assertEqual(result.exit_code, 0)


class TestUploadRuntimeMain(MainTestingMixin, unittest.TestCase):

    def setUp(self):
        MainTestingMixin.setUp(self)
        self.platform = 'rh5_x86_64'
        self.host = host = 'http://brood-dev.invalid'
        self.initial_args = ['--api-version', '1',
                             '--url', host, 'runtimes', 'upload']
        self.final_args = [self.organization, self.repository]

    def _upload_runtime(self, filepath=None, force=False,
                        verify=False, debug=False):
        initial_args = self.initial_args
        if force:
            initial_args = initial_args + ['--force']
        if verify:
            initial_args = initial_args + ['--verify']
        if debug:
            initial_args = ['--debug'] + initial_args
        with self.runner.isolated_filesystem() as tempdir:
            if filepath is None:
                metadata = RUNTIME_CPYTHON_2_7_10_RH5_X86_64_METADATA
                filepath = runtime_from_metadata(tempdir, metadata)

            result = self.runner.invoke(
                main.hatcher,
                args=initial_args + self.final_args + [filepath],
            )

        return filepath, result

    @responses.activate
    def test_without_force(self):
        # Given
        upload_url = '{host}{uri}'.format(
            host=self.host,
            uri=URLS.v1.data.runtimes.upload.format(
                organization_name=self.organization,
                repository_name=self.repository,
                platform=self.platform,
            ),
        )
        responses.add(
            responses.POST,
            upload_url,
            status=204,
        )

        # When
        with patch.object(
                utils, 'get_localtime') as get_localtime:
            now = datetime(2016, 2, 9, 10, 29, 7, tzinfo=pytz.utc)
            get_localtime.return_value = now.astimezone(
                pytz.timezone('Europe/Helsinki'))
            filename, result = self._upload_runtime(force=False)

        # Given
        expected_output = textwrap.dedent("""\
        Runtime upload  {filename}
        Server          {server}
        Repository      {organization}/{repository}
        Time            {time}
        """).format(
            filename=filename,
            server=self.host,
            organization=self.organization,
            repository=self.repository,
            time='2016-02-09 12:29:07 EET (+0200)',
        )

        # Then
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, expected_output)
        self.assertEqual(len(responses.calls), 1)
        upload_request, = responses.calls

        parsed = parse.urlsplit(upload_request.request.url)
        used_upload_url = parse.urlunsplit(parsed[:3] + ('', ''))
        self.assertEqual(used_upload_url, upload_url)
        self.assertEqual(parsed[3], 'overwrite=False')

    @responses.activate
    def test_with_force(self):
        # Given
        upload_url = '{host}{uri}'.format(
            host=self.host,
            uri=URLS.v1.data.runtimes.upload.format(
                organization_name=self.organization,
                repository_name=self.repository,
                platform=self.platform,
            ),
        )
        responses.add(
            responses.POST,
            upload_url,
            status=204,
        )

        # When
        with patch.object(
                utils, 'get_localtime') as get_localtime:
            now = datetime(2016, 2, 9, 10, 29, 7, tzinfo=pytz.utc)
            get_localtime.return_value = now.astimezone(
                pytz.timezone('Europe/Helsinki'))
            filename, result = self._upload_runtime(force=True)

        # Given
        expected_output = textwrap.dedent("""\
        Runtime upload  {filename}
        Server          {server}
        Repository      {organization}/{repository}
        Time            {time}
        """).format(
            filename=filename,
            server=self.host,
            organization=self.organization,
            repository=self.repository,
            time='2016-02-09 12:29:07 EET (+0200)',
        )

        # Then
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, expected_output)
        self.assertEqual(len(responses.calls), 1)
        upload_request, = responses.calls

        parsed = parse.urlsplit(upload_request.request.url)
        used_upload_url = parse.urlunsplit(parsed[:3] + ('', ''))
        self.assertEqual(used_upload_url, upload_url)
        self.assertEqual(parsed[3], 'overwrite=True')

    @responses.activate
    def test_upload_no_verify(self):
        # Given
        upload_url = '{host}{uri}'.format(
            host=self.host,
            uri=URLS.v1.data.runtimes.upload.format(
                organization_name=self.organization,
                repository_name=self.repository,
                platform=self.platform,
            ),
        )
        responses.add(
            responses.POST,
            upload_url,
            status=200,
        )

        # When
        filename, result = self._upload_runtime()

        # Then
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(responses.calls), 1)
        upload_request, = responses.calls

        parsed = parse.urlsplit(upload_request.request.url)
        used_upload_url = parse.urlunsplit(parsed[:3] + ('', ''))
        self.assertEqual(used_upload_url, upload_url)

    @responses.activate
    def test_upload_verify_no_upstream(self):
        # Given
        metadata_url = '{host}{uri}'.format(
            host=self.host,
            uri=URLS.v1.metadata.artefacts.runtimes.format(
                organization_name=self.organization,
                repository_name=self.repository,
                platform=self.platform,
                implementation='cpython',
                version='2.7.10+1',
            ),
        )
        responses.add(
            responses.GET,
            metadata_url,
            status=404,
        )

        upload_url = '{host}{uri}'.format(
            host=self.host,
            uri=URLS.v1.data.runtimes.upload.format(
                organization_name=self.organization,
                repository_name=self.repository,
                platform=self.platform,
            ),
        )
        responses.add(
            responses.POST,
            upload_url,
            status=200,
        )

        # When
        filename, result = self._upload_runtime(verify=True)

        # Then
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(responses.calls), 2)
        metadata_request, upload_request = responses.calls
        self.assertEqual(metadata_request.request.url, metadata_url)

        parsed = parse.urlsplit(upload_request.request.url)
        used_upload_url = parse.urlunsplit(parsed[:3] + ('', ''))
        self.assertEqual(used_upload_url, upload_url)

    @responses.activate
    def test_upload_verify_valid(self):
        # Given
        tempdir = tempfile.mkdtemp(prefix='hatcher-')
        try:
            metadata = RUNTIME_CPYTHON_2_7_10_RH5_X86_64_METADATA
            filepath = runtime_from_metadata(tempdir, metadata)
            sha256 = compute_sha256(filepath)
            server_metadata = {
                'sha256': sha256,
            }

            metadata_url = '{host}{uri}'.format(
                host=self.host,
                uri=URLS.v1.metadata.artefacts.runtimes.format(
                    organization_name=self.organization,
                    repository_name=self.repository,
                    platform=self.platform,
                    implementation='cpython',
                    version='2.7.10+1',
                ),
            )
            responses.add(
                responses.GET,
                metadata_url,
                content_type='application/json',
                status=200,
                body=json.dumps(server_metadata),
            )

            # When
            filename, result = self._upload_runtime(
                filepath=filepath, verify=True)

            # Then
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(len(responses.calls), 1)
            metadata_request, = responses.calls
            self.assertEqual(metadata_request.request.url, metadata_url)
        finally:
            shutil.rmtree(tempdir)

    @responses.activate
    def test_upload_verify_checksum_failure(self):
        # Given
        server_metadata = {
            'sha256': 'invalid sha256',
        }

        metadata_url = '{host}{uri}'.format(
            host=self.host,
            uri=URLS.v1.metadata.artefacts.runtimes.format(
                organization_name=self.organization,
                repository_name=self.repository,
                platform=self.platform,
                implementation='cpython',
                version='2.7.10+1',
            ),
        )
        responses.add(
            responses.GET,
            metadata_url,
            content_type='application/json',
            status=200,
            body=json.dumps(server_metadata),
        )

        # When
        ## Use --debug so that we can assert on the actual exception
        ## raised rather than a SystemExit from the Exception handler
        filename, result = self._upload_runtime(verify=True, debug=True)

        # Then
        self.assertIsInstance(result.exception, ChecksumMismatchError)
        self.assertEqual(result.exit_code, -1)
        self.assertEqual(len(responses.calls), 1)
        metadata_request, = responses.calls
        self.assertEqual(metadata_request.request.url, metadata_url)

    @responses.activate
    def test_upload_verify_error(self):
        # Given
        error = 'An error'

        metadata_url = '{host}{uri}'.format(
            host=self.host,
            uri=URLS.v1.metadata.artefacts.runtimes.format(
                organization_name=self.organization,
                repository_name=self.repository,
                platform=self.platform,
                implementation='cpython',
                version='2.7.10+1',
            ),
        )
        responses.add(
            responses.GET,
            metadata_url,
            content_type='application/json',
            status=400,
            body=json.dumps({'error': error})
        )

        # When
        filename, result = self._upload_runtime(verify=True)

        # Then
        self.assertIsInstance(result.exception, SystemExit)
        self.assertEqual(result.exit_code, -1)
        self.assertTrue(result.output.strip().endswith(error))
        self.assertEqual(len(responses.calls), 1)
        metadata_request, = responses.calls
        self.assertEqual(metadata_request.request.url, metadata_url)


class TestDownloadRuntimeMain(MainTestingMixin, unittest.TestCase):

    def setUp(self):
        MainTestingMixin.setUp(self)
        self.initial_args = ['--api-version', '1',
                             '--url', 'brood-dev.invalid', 'runtimes',
                             'download']
        self.final_args = [self.organization, self.repository, self.platform]

    @patch_repository
    def test_download(self, Repository):
        # Given
        args = ['cpython', '2.7.10+1', 'destination']
        repository, platform_repo = self._mock_repository_class(Repository)
        iter_download_runtime = platform_repo.iter_download_runtime
        iter_download_runtime.return_value = 0, []

        # When
        result = self.runner.invoke(
            main.hatcher,
            args=self.initial_args + self.final_args + args,
        )

        # Then
        self.assertRepositoryConstructedCorrectly(Repository)
        iter_download_runtime.assert_called_once_with(*args)
        self.assertEqual(result.exit_code, 0)


class TestListRuntimesMain(MainTestingMixin, unittest.TestCase):

    @patch_repository
    def test_list_runtimes(self, Repository):
        # Given
        runtimes = [
            ('cpython', '2.7.10+1'),
            ('cpython', '3.4.3+1'),
        ]
        headers = ['Runtime', 'Version']
        expected = '{0}\n'.format(tabulate(runtimes, headers=headers))

        repository, platform_repo = self._mock_repository_class(Repository)
        list_runtimes = platform_repo.list_runtimes
        list_runtimes.return_value = runtimes

        args = ['--api-version', '1',
                '--url', 'brood-dev.invalid', 'runtimes', 'list',
                self.organization, self.repository, self.platform]

        # When
        result = self.runner.invoke(main.hatcher, args=args)

        # Then
        self.assertRepositoryConstructedCorrectly(Repository)
        list_runtimes.assert_called_once_with()
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, expected)
