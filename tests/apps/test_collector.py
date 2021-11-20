from unittest import TestCase
import responses
from weblate_exporter.collector import WeblateCollector
from prometheus_client.core import CollectorRegistry

API_URL = "http://weblate:8080/api/"
WRONG_API_URL = "http://weblate:8080/wrong_api/"

METRICS = {
    "units": 15,
    "units_translated": 8,
    "users": 10,
    "changes": 30,
    "projects": 2,
    "components": 5,
    "translations": 15,
    "languages": 20,
    "checks": 7,
    "configuration_errors": 6,
    "suggestions": 2,
    "celery_queues": {
        "memory": 15,
        "notify": 10,
        "celery": 7,
        "translate": 7,
        "backup": 1,
    },
    "name": "Devel",
}


class TestWeblateCollector(TestCase):
    def setUp(self):
        responses.mock.start()
        responses.add(responses.GET, API_URL + "metrics/", json=METRICS, status=200)
        responses.add(responses.GET, WRONG_API_URL + "metrics/", status=404)

    def tearDown(self):
        """Disable responses."""
        responses.mock.stop()
        responses.mock.reset()

    def test_collect_200(self):
        self.registry = CollectorRegistry(auto_describe=True)
        self.collector = WeblateCollector(api_url=API_URL)
        self.registry.register(self.collector)

        self.assertEqual(
            15,
            self.registry.get_sample_value(
                "weblate_exporter_app_units", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            8,
            self.registry.get_sample_value(
                "weblate_exporter_app_units_translated", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            10,
            self.registry.get_sample_value(
                "weblate_exporter_app_users", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            30,
            self.registry.get_sample_value(
                "weblate_exporter_app_changes", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            2,
            self.registry.get_sample_value(
                "weblate_exporter_app_projects", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            5,
            self.registry.get_sample_value(
                "weblate_exporter_app_components", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            15,
            self.registry.get_sample_value(
                "weblate_exporter_app_translations", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            20,
            self.registry.get_sample_value(
                "weblate_exporter_app_languages", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            7,
            self.registry.get_sample_value(
                "weblate_exporter_app_checks", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            6,
            self.registry.get_sample_value(
                "weblate_exporter_app_configuration_errors", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            2,
            self.registry.get_sample_value(
                "weblate_exporter_app_suggestions", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            15,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues:memory", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            10,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues:notify", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            7,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues:celery", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            7,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues:translate", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            1,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues:backup", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            1,
            self.registry.get_sample_value(
                "weblate_exporter_app_up", {"name": "Devel"}
            ),
        )

    def test_collect_non_200(self):
        self.registry = CollectorRegistry(auto_describe=True)
        self.collector = WeblateCollector(api_url=WRONG_API_URL)
        self.registry.register(self.collector)

        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_units", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_units_translated", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_users", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_changes", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_projects", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_components", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_translations", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_languages", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_checks", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_configuration_errors", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_suggestions", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues:memory", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues:notify", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues:celery", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues:translate", {"name": "Devel"}
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues:backup", {"name": "Devel"}
            ),
        )

        self.assertEqual(
            0,
            self.registry.get_sample_value(
                "weblate_exporter_app_up", {"name": "unknown"}
            ),
        )
