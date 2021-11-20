WEBLATE_EXPORTER_IMAGE_NAME ?= loktionovam/weblate_exporter
WEBLATE_EXPORTER_IMAGE_TAG ?= dev

lint:
	python -m black --check weblate_exporter tests

test-apps: lint
	python -m pytest --cov-report=html --cov-report=term --cov=weblate_exporter tests/apps -v

fmt:
	python -m black weblate_exporter tests

build-images:
	docker build --build-arg VERSION=$(WEBLATE_EXPORTER_IMAGE_TAG) -t $(WEBLATE_EXPORTER_IMAGE_NAME):$(WEBLATE_EXPORTER_IMAGE_TAG) .

test-images:
	python -m pytest tests/images -v

all: test-apps build-images test-images

.PHONY: test-apps fmt lint build-images test-images all
