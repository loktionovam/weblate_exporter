import pytest
import subprocess
import os
import testinfra

WEBLATE_EXPORTER_IMAGE_NAME = os.environ.get(
    "WEBLATE_EXPORTER_IMAGE_NAME", "loktionovam/weblate_exporter"
)
WEBLATE_EXPORTER_IMAGE_TAG = os.environ.get("WEBLATE_EXPORTER_IMAGE_TAG", "dev")


# scope='session' uses the same container for all the tests;
# scope='function' uses a new container per test function.
@pytest.fixture(scope="class")
def host(request):
    # run a container
    docker_id = (
        subprocess.check_output(
            [
                "docker",
                "run",
                "-d",
                f"{WEBLATE_EXPORTER_IMAGE_NAME}:{WEBLATE_EXPORTER_IMAGE_TAG}",
            ]
        )
        .decode()
        .strip()
    )
    # return a testinfra connection to the container
    host = testinfra.get_host("docker://" + docker_id)
    request.cls.host = host
    yield host
    # at the end of the test suite, destroy the container
    subprocess.check_call(["docker", "rm", "-f", docker_id])
