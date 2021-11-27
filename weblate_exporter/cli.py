import os
import sys
import time
import configargparse
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from weblate_exporter.collector import WeblateCollector
from weblate_exporter.logger import log


def parse_args(args):
    parser = configargparse.ArgParser(
        description="Weblate exporter args weblate address, api key and weblate exporter port",
        default_config_files=["/etc/weblate_exporter.yaml"],
    )

    parser.add("-c", "--config", help="config filename", is_config_file=True)

    parser.add(
        "-s",
        "--weblate_api_url",
        metavar="weblate_api_url",
        required=False,
        help="Weblate API URL",
        default=os.environ.get("WEBLATE_API_URL", "http://weblate:8080/api/"),
    )
    parser.add(
        "--weblate_api_key",
        metavar="weblate_api_key",
        required=False,
        help="weblate api key",
        default=os.environ.get("WEBLATE_API_KEY"),
    )
    parser.add(
        "-p",
        "--weblate_exporter_bind_port",
        metavar="weblate_exporter_bind_port",
        required=False,
        type=int,
        help="Listen to this port",
        default=int(os.environ.get("WEBLATE_EXPORTER_BIND_PORT", "9867")),
    )

    return parser.parse_args(args)


def run_exporter(args):
    log.info(f"Start weblate exporter for: {args.weblate_api_url}")
    collector = WeblateCollector(
        api_url=args.weblate_api_url,
        api_key=args.weblate_api_key,
    )
    REGISTRY.register(collector)

    start_http_server(args.weblate_exporter_bind_port)
    log.info(f"Serving at port: {args.weblate_exporter_bind_port}")
    while True:
        time.sleep(1)


def main():

    args = parse_args(sys.argv[1:])
    run_exporter(args)


if __name__ == "__main__":
    main()
