import subprocess
from unittest import TestCase
import pytest
import json
from time import sleep


@pytest.mark.usefixtures("host")
class TestRequirements(TestCase):
    """
    Check the requirements for running the bot are set up in the Docker image
    correctly
    """

    def setUp(self):
        super(TestRequirements, self).setUp()

    def test_weblate_exporter_port(self):
        self.assertTrue(self.host.socket("tcp://0.0.0.0:9867").is_listening)

    def test_weblate_exporter_process(self):
        """
        Check that exactly one python process launched
        and it is non-root process
        """
        process = self.host.process.get(comm="python")
        self.assertEqual("weblate_", process.user)
        self.assertEqual("nogroup", process.group)

    def test_weblate_exporter_logs(self):
        """
        Test that weblate exporter write logs in json format
        """
        sleep(2)
        log_entry = (
            subprocess.check_output(
                ["docker", "logs", self.host.backend.name], stderr=subprocess.STDOUT
            )
            .decode()
            .split("\n")[0]
        )
        parsed_log_entry = json.loads(log_entry)
        self.assertEqual("INFO", parsed_log_entry["levelname"])
        self.assertEqual("weblate_exporter", parsed_log_entry["name"])
