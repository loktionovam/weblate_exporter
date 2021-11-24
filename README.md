# Weblate prometheus exporter

[![weblate prometheus exporter](https://github.com/loktionovam/weblate_exporter/actions/workflows/ci.yml/badge.svg)](https://github.com/loktionovam/weblate_exporter/actions/workflows/ci.yml)

[![codecov](https://codecov.io/gh/loktionovam/weblate_exporter/branch/main/graph/badge.svg?token=3OWCAKRWEA)](https://codecov.io/gh/loktionovam/weblate_exporter)

Prometheus exporter for Weblate server metrics ([Weblate metrics described here](https://docs.weblate.org/en/latest/api.html))

Supported versions:

* Weblate >= 4.9

## Building and running

### Prerequisites

* docker engine >= 20.10
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
