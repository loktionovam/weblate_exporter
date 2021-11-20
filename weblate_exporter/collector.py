from wlc import Weblate, WeblateException
from prometheus_client.core import GaugeMetricFamily
from weblate_exporter.logger import log
import flatdict
from requests.exceptions import ConnectionError


class WeblateMetrics:
    def __init__(self, raw_metrics: dict = {}):
        self.metrics_prefix = "weblate_exporter_app"
        self._flattened_raw_metrics = flatdict.FlatDict(raw_metrics, delimiter=":")
        self.data = {
            f"{self.metrics_prefix}_up": GaugeMetricFamily(
                f"{self.metrics_prefix}_up",
                "weblate application is up",
                labels=["name"],
            ),
        }

        labels = [self._flattened_raw_metrics["name"]]

        for metric in self._flattened_raw_metrics.keys():

            if metric != "name":
                metric_name = f"{self.metrics_prefix}_{metric}"
                self.data[metric_name] = GaugeMetricFamily(
                    metric_name,
                    "",
                    labels=["name"],
                )
                value = self._flattened_raw_metrics[metric]
            self.data[metric_name].add_metric(labels, value)


class WeblateCollector:
    def __init__(
        self,
        api_url: str,
        api_key: str = None,
    ):
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
        self.metrics = WeblateMetrics(self._raw_metrics)
        for metric in self.metrics.data.values():
            yield metric
