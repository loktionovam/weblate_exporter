from weblate_exporter.cli import parse_args, run_exporter
from unittest import TestCase, mock
from multiprocessing import Process
from tests.apps.test_collector import METRICS, API_URL
import os
import responses
import requests
from time import sleep

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


class TestCLI(TestCase):
    def setUp(self):
        responses.mock.start()
        responses.add(responses.GET, API_URL + "metrics/", json=METRICS, status=200)
        responses.add_passthru("http://127.0.0.1:9867/metrics")

    def tearDown(self):
        """Disable responses."""
        responses.mock.stop()
        responses.mock.reset()

    def test_parse_args_config(self):
        config_path = os.path.join(DATA_DIR, "config.yaml")
        args = parse_args(["--config", config_path])
        assert args.weblate_exporter_bind_port == 9867
        assert args.weblate_api_url == "http://test-weblate:8080/api/"
        assert args.weblate_api_key == "test_weblate_api_key"

    @mock.patch.dict(
        os.environ,
        {
            "WEBLATE_API_URL": "http://env-test-weblate:8080/api/",
            "WEBLATE_API_KEY": "env_test_weblate_api_key",
            "WEBLATE_EXPORTER_BIND_PORT": "9868",
        },
    )
    def test_parse_args_env(self):
        args = parse_args([])

        assert args.weblate_exporter_bind_port == 9868
        assert args.weblate_api_url == "http://env-test-weblate:8080/api/"
        assert args.weblate_api_key == "env_test_weblate_api_key"

    def test_run_exporter(self):
        args = parse_args(["--weblate_api_url", API_URL])

        p = Process(target=run_exporter, args=(args,))
        try:
            p.start()
            sleep(1)
            response = requests.get("http://127.0.0.1:9867/metrics")
            self.assertEqual(200, response.status_code)
        finally:
            p.terminate()
            p.join()
