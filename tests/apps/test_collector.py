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
                "weblate_exporter_app_units",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )
        self.assertEqual(
            8,
            self.registry.get_sample_value(
                "weblate_exporter_app_units_translated",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )
        self.assertEqual(
            10,
            self.registry.get_sample_value(
                "weblate_exporter_app_users",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )
        self.assertEqual(
            30,
            self.registry.get_sample_value(
                "weblate_exporter_app_changes",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )
        self.assertEqual(
            2,
            self.registry.get_sample_value(
                "weblate_exporter_app_projects",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )
        self.assertEqual(
            5,
            self.registry.get_sample_value(
                "weblate_exporter_app_components",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )
        self.assertEqual(
            15,
            self.registry.get_sample_value(
                "weblate_exporter_app_translations",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )
        self.assertEqual(
            20,
            self.registry.get_sample_value(
                "weblate_exporter_app_languages",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )
        self.assertEqual(
            7,
            self.registry.get_sample_value(
                "weblate_exporter_app_checks",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )
        self.assertEqual(
            6,
            self.registry.get_sample_value(
                "weblate_exporter_app_configuration_errors",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )
        self.assertEqual(
            2,
            self.registry.get_sample_value(
                "weblate_exporter_app_suggestions",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )
        self.assertEqual(
            15,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues",
                {
                    "name": "Devel",
                    "weblate_api_url": "http://weblate:8080/api/",
                    "weblate_celery_queue_name": "memory",
                },
            ),
        )
        self.assertEqual(
            10,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues",
                {
                    "name": "Devel",
                    "weblate_api_url": "http://weblate:8080/api/",
                    "weblate_celery_queue_name": "notify",
                },
            ),
        )
        self.assertEqual(
            7,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues",
                {
                    "name": "Devel",
                    "weblate_api_url": "http://weblate:8080/api/",
                    "weblate_celery_queue_name": "celery",
                },
            ),
        )
        self.assertEqual(
            7,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues",
                {
                    "name": "Devel",
                    "weblate_api_url": "http://weblate:8080/api/",
                    "weblate_celery_queue_name": "translate",
                },
            ),
        )
        self.assertEqual(
            1,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues",
                {
                    "name": "Devel",
                    "weblate_api_url": "http://weblate:8080/api/",
                    "weblate_celery_queue_name": "backup",
                },
            ),
        )
        self.assertEqual(
            1,
            self.registry.get_sample_value(
                "weblate_exporter_app_up",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/api/"},
            ),
        )

    def test_collect_non_200(self):
        self.registry = CollectorRegistry(auto_describe=True)
        self.collector = WeblateCollector(api_url=WRONG_API_URL)
        self.registry.register(self.collector)

        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_units",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/wrong_api/"},
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_units_translated",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/wrong_api/"},
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_users",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/wrong_api/"},
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_changes",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/wrong_api/"},
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_projects",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/wrong_api/"},
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_components",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/wrong_api/"},
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_translations",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/wrong_api/"},
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_languages",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/wrong_api/"},
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_checks",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/wrong_api/"},
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_configuration_errors",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/wrong_api/"},
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_suggestions",
                {"name": "Devel", "weblate_api_url": "http://weblate:8080/wrong_api/"},
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues",
                {
                    "name": "Devel",
                    "weblate_api_url": "http://weblate:8080/wrong_api/",
                    "weblate_celery_queue_name": "memory",
                },
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues",
                {
                    "name": "Devel",
                    "weblate_api_url": "http://weblate:8080/wrong_api/",
                    "weblate_celery_queue_name": "notify",
                },
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues",
                {
                    "name": "Devel",
                    "weblate_api_url": "http://weblate:8080/wrong_api/",
                    "weblate_celery_queue_name": "celery",
                },
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues",
                {
                    "name": "Devel",
                    "weblate_api_url": "http://weblate:8080/wrong_api/",
                    "weblate_celery_queue_name": "translate",
                },
            ),
        )
        self.assertEqual(
            None,
            self.registry.get_sample_value(
                "weblate_exporter_app_celery_queues",
                {
                    "name": "Devel",
                    "weblate_api_url": "http://weblate:8080/wrong_api/",
                    "weblate_celery_queue_name": "backup",
                },
            ),
        )

        self.assertEqual(
            0,
            self.registry.get_sample_value(
                "weblate_exporter_app_up",
                {
                    "name": "unknown",
                    "weblate_api_url": "http://weblate:8080/wrong_api/",
                },
            ),
        )
