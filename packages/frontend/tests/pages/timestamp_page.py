from playwright.sync_api import Page

class TimestampConverterPage:
    """
    Page Object for the Unix Timestamp Converter page.
    """

    def __init__(self, page: Page):
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

    def navigate(self):
        """
        Navigate to the timestamp converter page.
        """
        self.page.goto(self.url)

    def convert_timestamp_to_date(self, timestamp: str):
        """
        Fills in the timestamp input and triggers the conversion.
        """
        self.timestamp_input.fill(timestamp)
        self.convert_to_date_button.click()

    def convert_date_to_timestamp(self, date_string: str):
        """
        Fills in the date input and triggers the conversion.
        """
        self.date_input.fill(date_string)
        self.convert_to_timestamp_button.click()

    def get_converted_date(self) -> str:
        """
        Returns the value of the converted date output field.
        """
        return self.converted_date_output.input_value()

    def get_converted_timestamp(self) -> str:
        """
        Returns the value of the converted timestamp output field.
        """
        return self.converted_timestamp_output.input_value()

    def get_current_timestamp(self) -> str | None:
        """
        Returns the text content of the current timestamp element.
        """
        return self.current_timestamp.text_content()

    def get_current_date(self) -> str | None:
        """
        Returns the text content of the current date element.
        """
        return self.current_date.text_content()
