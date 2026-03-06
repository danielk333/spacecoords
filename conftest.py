import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--include_download",
        action="store_true", default=False, help="Do tests that need to download files",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "need_download: tests that need to download large files")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--include_download"):
        skip_tests = pytest.mark.skip(reason="Needs to download large files")
        for item in items:
            if "need_download" in item.keywords:
                item.add_marker(skip_tests)

