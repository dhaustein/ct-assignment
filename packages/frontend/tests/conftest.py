import pytest
from playwright.sync_api import Page, sync_playwright, Browser
from packages.frontend.tests.pages.timestamp_page import TimestampConverterPage
from typing import Generator
import os

# TODO the value should be fetched from a configuration file
# expects playwright browser server to run in a container
PLAYWRIGHT_WS_ENDPOINT = "ws://0.0.0.0:19323"
PLAYWRIGHT_TRACING = True

@pytest.fixture(scope="session")
def chromium_browser() -> Generator[Browser, None, None]:
    """
    Main browser fixture that connects to the running browser server
    in container.
    """
    with sync_playwright() as p:
        browser = p.chromium.connect(PLAYWRIGHT_WS_ENDPOINT)
        yield browser
        browser.close()

@pytest.fixture
def page(chromium_browser: Browser, request) -> Generator[Page, None, None]:
    """
    Overrides the default 'page' fixture to create a new page for each test
    from the session-scoped browser.
    """
    context = chromium_browser.new_context()
    page = context.new_page()

    if PLAYWRIGHT_TRACING:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    if PLAYWRIGHT_TRACING:
        # TODO do not hardcore the trace dir path
        # TODO abstract tmpo dir so that it works on different OS-es
        trace_dir = "/tmp/playwright_traces"
        os.makedirs(trace_dir, exist_ok=True)

        test_name = request.node.name.replace("::", "_").replace("[", "_").replace("]", "_")
        trace_path = f"{trace_dir}/{test_name}_trace.zip"

        context.tracing.stop(path=trace_path)

    page.close()
    context.close()


@pytest.fixture
def timestamp_converter_page(page: Page) -> TimestampConverterPage:
    """
    Fixture to provide an instance of the TimestampConverterPage.

    Uses customized Page
    """
    return TimestampConverterPage(page)
