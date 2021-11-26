# Weblate prometheus exporter

[![weblate prometheus exporter](https://github.com/loktionovam/weblate_exporter/actions/workflows/ci.yml/badge.svg)](https://github.com/loktionovam/weblate_exporter/actions/workflows/ci.yml)

[![codecov](https://codecov.io/gh/loktionovam/weblate_exporter/branch/main/graph/badge.svg?token=3OWCAKRWEA)](https://codecov.io/gh/loktionovam/weblate_exporter)

Prometheus exporter for Weblate server metrics ([Weblate metrics described here](https://docs.weblate.org/en/latest/api.html))

Supported versions:

* Weblate >= 4.9

Basic metrics
| Metric                                      | Type  | Description                                                                                                      | Labels |
|---------------------------------------------|-------|------------------------------------------------------------------------------------------------------------------|--------|
| `weblate_exporter_app_up`                   | Gauge | Weblate application is running up                                                                                | `name` |
| `weblate_exporter_app_units`                | Gauge | Total number of [units](https://docs.weblate.org/en/latest/api.html?highlight=units#units)                       | `name` |
| `weblate_exporter_app_units_translated`     | Gauge | Number of translated [units](https://docs.weblate.org/en/latest/api.html?highlight=units#units)                  | `name` |
| `weblate_exporter_app_users`                | Gauge | Number of weblate users                                                                                          | `name` |
| `weblate_exporter_app_changes`              | Gauge | Number of [translation changes](https://docs.weblate.org/en/latest/api.html?highlight=changes#get--api-changes-) | `name` |
| `weblate_exporter_app_projects`             | Gauge | Number of [projects](https://docs.weblate.org/en/latest/user/translating.html#translation-projects)              | `name` |
| `weblate_exporter_app_components`           | Gauge | Number of [components](https://docs.weblate.org/en/latest/admin/projects.html#component)                         | `name` |
| `weblate_exporter_app_translations`         | Gauge | Number of [translations](https://docs.weblate.org/en/latest/api.html?highlight=units#translations)               | `name` |
| `weblate_exporter_app_languages`            | Gauge | Number of [used languages](https://docs.weblate.org/en/latest/api.html?highlight=units#languages)                | `name` |
| `weblate_exporter_app_configuration_errors` | Gauge | Number of [configuration errors](https://docs.weblate.org/en/latest/api.html?highlight=units#metrics)            | `name` |
| `weblate_exporter_app_suggestions`          | Gauge | Number of pending [suggestions](https://docs.weblate.org/en/latest/api.html?highlight=units#metrics)             | `name` |

Metrics below describes lengths of various celery queues, see [Background tasks using Celery](https://docs.weblate.org/en/latest/admin/install.html#celery)
| Metric                                         | Type  | Labels |
|------------------------------------------------|-------|--------|
| `weblate_exporter_app_celery_queues:memory`    | Gauge | `name` |
| `weblate_exporter_app_celery_queues:notify`    | Gauge | `name` |
| `weblate_exporter_app_celery_queues:celery"`   | Gauge | `name` |
| `weblate_exporter_app_celery_queues:translate` | Gauge | `name` |
| `weblate_exporter_app_celery_queues:backup`    | Gauge | `name` |

## Building and running

### Prerequisites

* docker engine >= 20.10
* helm >= 3.7.1
* helm-docs >= 1.5.0
* make
* python >= 3.10 (used by tests only)
* python3-venv (used by tests only)

### Setup an environment for developing and testing

* Install prerequisites for developing and testing:

  ```shell
  sudo apt-get install python3-venv
  python3 -m venv venv
  source venv/bin/activate
  python -m pip install --upgrade pip

  # Install for tests only
  pip install -r requirements-test.txt

  # Install for developing
  pip install -r requirements-dev.txt
  ```

### Build and test a docker image

* Set up an image name and tag (optional):

    ```shell
    export WEBLATE_EXPORTER_IMAGE_NAME=yourname/weblate_exporter
    export WEBLATE_EXPORTER_IMAGE_TAG=0.1.0
    ```

* Build and test the image:

    ```shell
    make build-images
    make test-images
    ```

### Run the weblate_exporter

#### Helm

* Add weblate-exporter helm repository:

  ```shell
    helm repo add weblate-exporter https://raw.githubusercontent.com/loktionovam/weblate_exporter/gh-pages/
    helm repo update
  ```

* Search available weblate-exporter helm charts:

  ```shell
    helm search repo --versions weblate-exporter

    NAME                             	CHART VERSION	APP VERSION	DESCRIPTION
    weblate-exporter/weblate-exporter	0.3.2        	v0.3.2     	Weblate prometheus metrics exporter

  ```

* Deploy new helm release:

  ```shell
  helm install weblate-exporter weblate-exporter/weblate-exporter \
    --version 0.3.2 \
    --set config.weblateAPIUrl="http://weblate.example.com:8080/api/" \
    --set config.weblateAPIKey="secret_api_key"

    helm test weblate-exporter
  ```

#### Docker

* Running using environment variables:

  ```shell
    docker run -p 9867:9867  -d -e WEBLATE_API_URL=http://weblate.example.com/api/ -e WEBLATE_API_KEY=secret_api_key yourname/weblate_exporter:0.1.0

    # Get the metrics
    curl http://localhost:9867/metrics/
  ```

* Running using a configuration file:

  ```shell
    mv config.yaml.example weblate_exporter.yaml

    # Setup weblate_api_url and weblate_api_key variables in weblate_exporter.yaml

    cat weblate_exporter.yaml                                                                                                                                                                                                              ─╯
    ---
    weblate_api_url: http://weblate.example.com/api/
    weblate_api_key: secret_api_key
    weblate_exporter_port: 9867

    # Run weblate_exporter docker container:
    docker run -p 9867:9867  -d -v $(pwd)/weblate_exporter.yaml:/etc/weblate_exporter.yaml  yourname/weblate_exporter:0.1.0

    # Get the metrics
    curl http://localhost:9867/metrics/

  ```

## Developing and testing weblate exporter

* Install prerequisites [as described here](#setup-an-environment-for-developing-and-testing) and activate python virtual environment
* Format the code and run tests:

  ```shell
  make fmt
  make test-apps
  ```
