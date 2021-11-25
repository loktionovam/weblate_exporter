#!/usr/bin/env python3

import collections.abc
import os
import subprocess
import ruamel.yaml

"""
The script patches Chart.yaml, values.yaml by current version of an application
and creates a helm chart package.
"""

script_path = os.path.dirname(os.path.abspath(__file__))
chart_path = os.path.join(script_path, "charts/weblate-exporter")
chart_info_path = os.path.join(chart_path, "Chart.yaml")

chart_values_path = os.path.join(chart_path, "values.yaml")

app_version = os.environ.get("WEBLATE_EXPORTER_IMAGE_TAG", "v0.1.0")
app_image = os.environ.get("WEBLATE_EXPORTER_IMAGE_NAME", "loktionovam/weblate_exporter")
chart_version = app_version.strip("v")


# Update nested dict based on https://stackoverflow.com/a/3233356
def update_dict(src_dict: dict = {}, patch_dict: dict = {}) -> dict:
    for k, v in patch_dict.items():
        if isinstance(v, collections.abc.Mapping):
            src_dict[k] = update_dict(src_dict.get(k, {}), v)
        else:
            src_dict[k] = v
    return src_dict


def patch_yaml_file(yaml_file_path: str = "", patch_dict: dict = {}) -> None:
    print(f"Apply patch: {patch_dict} to {yaml_file_path}")
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    with open(yaml_file_path) as yaml_fh:
        yaml_values = yaml.load(yaml_fh)

    patched_yaml_values = update_dict(yaml_values, patch_dict)
    with open(yaml_file_path, "w") as yaml_fh:
        yaml.dump(patched_yaml_values, yaml_fh)


patch_yaml_file(
    yaml_file_path=chart_info_path,
    patch_dict={
        "version": chart_version,
        "appVersion": app_version
    })

patch_yaml_file(
    yaml_file_path=chart_values_path,
    patch_dict={
        "image": {
            "repository": app_image,
            "tag": app_version,
        }
    })


# helm_package_output = subprocess.check_output(
#     [
#         "helm",
#         "package",
#         chart_path,
#     ]
# ).decode().strip()
#
# print(helm_package_output)
