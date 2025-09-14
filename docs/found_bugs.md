# Found Bugs

* **Inconsistent 12h/24h Format Handling:** The API inconsistently handles
the 12h/24h format, particularly at noon and midnight.
  ```
  00:00:00 UTC (midnight) is converted to "2023-01-01 12:00:00"
  01:00:00 UTC is converted to "2023-01-01 01:00:00"
  12:00:00 UTC (noon) is also converted to "2023-01-01 12:00:00"
  ```

* **Missing Zero-Padding in Frontend:** The frontend does not zero-pad
single-digit time units in the conversion results.
  ```
  Timestamp:  1582934400
  Expected:   2020-02-29 00:00:00
  Actual:     2020-02-29 0:0:00
  ```

* **Missing Timezone Information:** The API response does not include timezone
information, making the returned time ambiguous.

* **`cached` Parameter Ineffective:** The `cached` API parameter appears to
have no effect on response behavior or caching.

* **Incorrect Leap Day Handling:** A non-existent leap day timestamp is
converted to the following day instead of the preceding one.
  ```
  Timestamp:  1677625200  # Represents 2023-02-29 00:00:00, which does not exist
  Expected:   2023-02-28 23:00:00
  Actual:     2023-03-01 0:0:00
  ```

* **Poor Invalid Input Handling in Frontend:** The frontend does not handle
invalid input gracefully, displaying `NaN` instead of a user-friendly error message.

* **Limited Testability of HTML Structure:** The HTML structure lacks
test-specific identifiers (e.g., `data-testid` attributes), which makes
E2E tests more brittle and harder to maintain.
