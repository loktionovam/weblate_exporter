import sys
import weblate_exporter.cli as cli


try:
    sys.exit(cli.main())
except KeyboardInterrupt:
    sys.exit(1)
