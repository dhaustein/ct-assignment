from playwright.sync_api import Page

class TimestampConverterPage:
    """
    Page Object for the Unix Timestamp Converter page.

    This class provides methods to interact with the timestamp converter web page,
    including navigation, input filling, and result retrieval.

    Args:
        page (Page): The Playwright Page object for browser interaction.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = "https://helloacm.com/tools/unix-timestamp-converter/"  # TODO extract to config file

        # Locators
        self.timestamp_input = page.locator("#timestamp_1")
        self.converted_date_output = page.locator("#beijing_time_1")
        self.date_input = page.locator("#beijing_time_2")
        self.converted_timestamp_output = page.locator("#timestamp_2")
        self.current_timestamp = page.locator("#cur_timestamp")
        self.current_date = page.locator("#cur_date")
        self.convert_to_date_button = page.locator(
            "h2:has-text('Convert Unix TimeStamp to Date String') + p input[value*='Convert']"
        )
        self.convert_to_timestamp_button = page.locator(
            "h2:has-text('Convert Date String to TimeStamp') + p input[value*='Convert']"
        )

    def navigate(self) -> None:
        """
        Navigate to the timestamp converter page.

        Returns:
            None
        """
        self.page.goto(self.url)

    def convert_timestamp_to_date(self, timestamp: str) -> None:
        """
        Fills in the timestamp input and triggers the conversion.

        Args:
            timestamp (str): The Unix timestamp to convert to a date string.

        Returns:
            None
        """
        self.timestamp_input.fill(timestamp)
        self.convert_to_date_button.click()

    def convert_date_to_timestamp(self, date_string: str) -> None:
        """
        Fills in the date input and triggers the conversion.

        Args:
            date_string (str): The date string to convert to a Unix timestamp.

        Returns:
            None
        """
        self.date_input.fill(date_string)
        self.convert_to_timestamp_button.click()

    def get_converted_date(self) -> str:
        """
        Returns the value of the converted date output field.

        Returns:
            str: The converted date string from the output field.
        """
        return self.converted_date_output.input_value()

    def get_converted_timestamp(self) -> str:
        """
        Returns the value of the converted timestamp output field.

        Returns:
            str: The converted Unix timestamp from the output field.
        """
        return self.converted_timestamp_output.input_value()

    def get_current_timestamp(self) -> str | None:
        """
        Returns the text content of the current timestamp element.

        Returns:
            str | None: The current Unix timestamp displayed on the page,
                       or None if the element is not found or has no content.
        """
        return self.current_timestamp.text_content()

    def get_current_date(self) -> str | None:
        """
        Returns the text content of the current date element.

        Returns:
            str | None: The current date string displayed on the page,
                       or None if the element is not found or has no content.
        """
        return self.current_date.text_content()
