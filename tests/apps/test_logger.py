from unittest import TestCase, mock
import os
import importlib
import weblate_exporter.logger


class TestLogger(TestCase):
    def test_log(self):
        importlib.reload(weblate_exporter.logger)
        log = weblate_exporter.logger.log
        self.assertEqual(20, log.level)

        with self.assertLogs(logger=log, level=log.level) as cm:
            log.info("info message")
            log.warning("warn message")
        self.assertEqual(
            cm.output,
            [
                "INFO:weblate_exporter:info message",
                "WARNING:weblate_exporter:warn message",
            ],
        )

    @mock.patch.dict(os.environ, {"DEBUG": "1"})
    def test_log_debug(self):
        importlib.reload(weblate_exporter.logger)
        log = weblate_exporter.logger.log
        self.assertEqual(10, log.level)

        with self.assertLogs(logger=log, level=log.level) as cm:
            log.info("info message")
            log.warning("warn message")
            log.debug("debug message")
        self.assertEqual(
            cm.output,
            [
                "INFO:weblate_exporter:info message",
                "WARNING:weblate_exporter:warn message",
                "DEBUG:weblate_exporter:debug message",
            ],
        )
