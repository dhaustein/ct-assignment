# Future Strategy & Improvements

This document outlines a strategy for future improvements to the testing process
and the API itself, focusing on scalability, reliability, and maintainability.

## Scalability

* **CI/CD Pipeline:** Implement a CI/CD pipeline (e.g., GitHub Actions, GitLab CI,
Jenkins) that includes automated stages for linting, unit testing, contract testing,
integration testing, and building artifacts.

* **Contract Testing:** Introduce contract testing for interactions between
services using a tool like Pact. The API provider would publish a contract,
and consumers (like the frontend) would test against it. This ensures that
changes in one service do not break the contract expected by another,
preventing integration issues.

* **Centralized Test Environments:** Utilize containerization (including devcontainers)
to create consistent, reproducible development and testing environments
for all services. This simplifies onboarding and ensures uniformity across the team.

* **Shared Test Libraries:** Develop and maintain shared libraries for
common testing utilities, such as test data generation, API clients,
and result reporting frameworks.

## Reliability

* **Isolate Tests:** Ensure that tests are independent and can run in any order.
Avoid dependencies between test cases to improve stability and parallel execution.

* **Smart Waits in E2E Tests:** Avoid fixed waits (e.g., `sleep(5)`) in all tests.
Instead, use explicit waits that check for a specific condition,
such as an element becoming visible or a network request completing.
Playwright has robust auto-waiting capabilities that should be leveraged for this.

* **Flaky Test Detection:** Configure CI pipelines to automatically re-run
failed tests a limited number of times and to identify and report flaky tests
that pass and fail intermittently.

* **Unit Tests:** As this project is a test suite for an external service,
it currently lacks a unit testing layer for the service itself.
Implementing unit tests would provide faster, more granular feedback during development.

* **E2E Test Scope:** E2E tests are expensive to write and maintain and can be brittle.
They should be used sparingly to verify critical end-to-end user journeys.
The majority of testing should focus on lower-level API and component tests,
which are faster and more stable.

## API & Test Process Improvements

* **Property-Based Testing:** For functions that handle a wide range of inputs,
like timestamp conversion, property-based testing (using libraries like `hypothesis` for Python)
could be highly effective. Tools like `schemathesis` can also be used to test
an API's adherence to its OpenAPI/Swagger specification.

* **Code Coverage Analysis:** Integrate code coverage analysis to identify untested
parts of the codebase and guide testing efforts.

* **RESTful Error Handling:** The API currently returns a `200 OK` status
with a payload of `false` for invalid input. This is non-standard.
The API should use appropriate HTTP status codes (e.g., `400 Bad Request`)
to indicate client errors.

* **Explicit API Behavior:** The API's behavior regarding timezones and 12/24-hour
formats is implicit and should be explicitly defined in the API specification.
Ideally, the API would consistently handle and declare its timezone
(e.g., by accepting and returning UTC).
