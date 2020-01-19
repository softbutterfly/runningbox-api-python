import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [("Authorization", "Bearer runningbox_api_key")],
    }
