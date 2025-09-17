import pytest
from pytest import FixtureRequest
from playwright.sync_api import Page, sync_playwright, Browser
from packages.frontend.tests.pages.timestamp_page import TimestampConverterPage
from typing import Generator
import os

# If PLAYWRIGHT_WS_ENDPOINT is set, we connect to a remote server (for local)
# otherwise  launch a local browser instance (used in CI)
PLAYWRIGHT_WS_ENDPOINT = os.environ.get("PLAYWRIGHT_WS_ENDPOINT")
# tracing is disabled by default
PLAYWRIGHT_TRACING = os.environ.get("PLAYWRIGHT_TRACING", "False").lower() == "True"


@pytest.fixture(scope="session")
def chromium_browser() -> Generator[Browser, None, None]:
    """
    Main browser fixture.

    If the PLAYWRIGHT_WS_ENDPOINT environment variable is set, this fixture
    connects to a remote Playwright browser server. This is used for local
    testing with the 'make test-ui' command.

    If the environment variable is not set, it launches a new local browser
    instance, used in CI container where the browsers are available directly.

    The browser is closed automatically when the session ends.

    Returns:
        Generator[Browser, None, None]: A generator yielding a Playwright Browser
                                       instance.
    """
    with sync_playwright() as p:
        if PLAYWRIGHT_WS_ENDPOINT:
            browser = p.chromium.connect(PLAYWRIGHT_WS_ENDPOINT)
        else:
            browser = p.chromium.launch()

        yield browser

        browser.close()


@pytest.fixture
def page(chromium_browser: Browser, request: FixtureRequest) -> Generator[Page, None, None]:
    """
    Overrides the default 'page' fixture to create a new page for each test
    from the session-scoped browser.

    Creates a new browser context and page for each test, with optional tracing
    enabled.

    The context and page are automatically cleaned up after the test.
    When tracing is enabled, trace files are saved to a temporary directory.

    Args:
        chromium_browser (Browser): The session-scoped browser instance.
        request: The pytest request object containing test metadata.

    Returns:
        Generator[Page, None, None]: A generator yielding a Playwright Page
                                    instance for the test.
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
    Fixture to provide an instance of the TimestampConverterPage
    that wraps the provided Playwright Page.

    Args:
        page (Page): The Playwright Page instance to wrap.

    Returns:
        TimestampConverterPage: An instance of the TimestampConverterPage
                               page object for interacting with the timestamp
                               converter interface.
    """
    return TimestampConverterPage(page)
