from wlc import Weblate, WeblateException
from prometheus_client.core import GaugeMetricFamily
from weblate_exporter.logger import log
from requests.exceptions import ConnectionError


class WeblateMetrics:
    """
    The data class which parses raw metrics from Weblate described here:

    https://docs.weblate.org/en/latest/admin/install.html?highlight=metrics#monitoring-weblate

    and represents them in a prometheus format.

    Example of metrics:

        weblate_exporter_app_units
        weblate_exporter_app_units_translated
        ....
        ....

    Celery queues stored as weblate_exporter_app_celery_queues metric
    with an additional label weblate_celery_queue_name.

    """

    def __init__(self, raw_metrics: dict = {}, additional_labels: dict = {}):
        self.metrics_prefix = "weblate_exporter_app"
        labels_names = ["name"]
        labels_values = [raw_metrics["name"]]

        for k, v in additional_labels.items():
            labels_names.append(k)
            labels_values.append(v)

        self.data = {
            f"{self.metrics_prefix}_up": GaugeMetricFamily(
                f"{self.metrics_prefix}_up",
                "weblate application is up",
                labels=["name"],
            ),
        }

        for metric, value in raw_metrics.items():
            if metric != "name":
                metric_name = f"{self.metrics_prefix}_{metric}"
                if metric == "celery_queues":
                    self.data[metric_name] = GaugeMetricFamily(
                        metric_name,
                        "",
                        labels=labels_names + ["weblate_celery_queue_name"],
                    )

                    for queue_label, queue_value in raw_metrics[metric].items():
                        self.data[metric_name].add_metric(
                            labels_values + [queue_label], queue_value
                        )
                else:
                    self.data[metric_name] = GaugeMetricFamily(
                        metric_name,
                        "",
                        labels=labels_names,
                    )
                    self.data[metric_name].add_metric(labels_values, value)


class WeblateCollector:
    """
    The custom prometheus collector which fetches metrics data from Weblate instance and
    store them in prometheus format. Instance of the class is used by a prometheus client registry.

    https://github.com/prometheus/client_python#custom-collectors
    """

    def __init__(
        self,
        api_url: str,
        api_key: str = None,
    ):
        """
        :param api_url: Weblate API root endpoint, i.e. http://weblate:8080/api/
                        Notice, that you should use '/' as a trailing slash.

                    More information about Weblate API here: https://docs.weblate.org/en/latest/api.html
        :param api_key: authorization token which described here https://docs.weblate.org/en/latest/api.html?highlight=token#authentication-and-generic-parameters
        """

        self.api_key = api_key
        self.api_url = api_url
        self._raw_metrics = {}
        self._wlc = Weblate(key=api_key, url=api_url)
        self.metrics = None

    def _fetch_raw_metrics(self) -> None:
        try:
            log.debug(f"Try to fetch metrics from: {self.api_url}")
            self._raw_metrics = self._wlc.get("metrics/")
            self._raw_metrics["up"] = 1
        except (WeblateException, ConnectionError) as error:
            log.warning(f"Can't fetch metrics from weblate: {error}")
            self._raw_metrics = {"up": 0, "name": "unknown"}
        finally:
            log.debug(f"Fetched raw metrics: {self._raw_metrics}")

    def collect(self):
        self._fetch_raw_metrics()
        self.metrics = WeblateMetrics(
            self._raw_metrics, additional_labels={"weblate_api_url": self.api_url}
        )
        for metric in self.metrics.data.values():
            yield metric
