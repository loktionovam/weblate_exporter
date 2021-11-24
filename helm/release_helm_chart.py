#!/usr/bin/env python3

import os
import subprocess

import yaml

script_path = os.path.dirname(os.path.abspath(__file__))
chart_path = os.path.join(script_path, "charts/weblate-exporter")
chart_info_path = os.path.join(chart_path, "Chart.yaml")

app_version = os.environ.get("WEBLATE_EXPORTER_IMAGE_TAG", "v0.1.0")
chart_version = app_version.strip("v")

with open(chart_info_path) as chart_info_fh:
    chart_info = yaml.load(chart_info_fh, Loader=yaml.FullLoader)

chart_info["version"] = chart_version
chart_info["appVersion"] = app_version

with open(chart_info_path, mode="w") as chart_info_fh:
    yaml.dump(chart_info, chart_info_fh)

helm_package_output = subprocess.check_output(
    [
        "helm",
        "package",
        chart_path,
    ]
)
