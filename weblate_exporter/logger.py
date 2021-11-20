import logging
import os
from pythonjsonlogger import jsonlogger

DEBUG = int(os.environ.get("DEBUG", "0"))
log = logging.getLogger("weblate_exporter")
log.setLevel(logging.DEBUG if DEBUG else logging.INFO)

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

if DEBUG:
    log.debug(f"Current log level is {logging.getLevelName(log.level)}")
