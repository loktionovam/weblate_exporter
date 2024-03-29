WEBLATE_EXPORTER_IMAGE_NAME ?= loktionovam/weblate_exporter
WEBLATE_EXPORTER_IMAGE_TAG ?= $(shell ./get_version.sh)
GIT_BRANCH_NAME := $(shell git branch  --show-current)
export

lint:
	python -m black --check weblate_exporter tests

test-apps: lint
	python -m pytest --cov-report=xml --cov-report=term --cov=weblate_exporter tests/apps -v

fmt:
	python -m black weblate_exporter tests

build-images:
	docker build --build-arg VERSION=$(WEBLATE_EXPORTER_IMAGE_TAG) -t $(WEBLATE_EXPORTER_IMAGE_NAME):$(WEBLATE_EXPORTER_IMAGE_TAG) .

test-images:
	python -m pytest tests/images -v

push-images:
	docker push $(WEBLATE_EXPORTER_IMAGE_NAME):$(WEBLATE_EXPORTER_IMAGE_TAG)

build-charts:
	helm lint helm/charts/weblate-exporter
	helm/release_helm_chart.py

changelog:
ifeq ($(GIT_BRANCH_NAME), main)
	@echo "Current branch is $(GIT_BRANCH_NAME), create changelog"
	gitchangelog > CHANGELOG.md
else
	@echo "Current branch is $(GIT_BRANCH_NAME), skipping to update CHANGELOG.md"
endif

all: test-apps build-images test-images build-charts

.PHONY: test-apps fmt lint build-images test-images push-images build-charts all
