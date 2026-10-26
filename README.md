# Banking UI & API Test Automation Framework

A Python-based test automation framework for testing a banking web application. It uses **pytest** and **Playwright** to exercise browser UI workflows and API endpoints, with reusable page objects, API clients, fixtures, and test data.

## Coverage

The test suite includes UI and API checks for:

- User registration and login
- Bank account workflows
- Transactions and payment flows
- Contacts, likes, and user-related endpoints
- End-to-end workflows that combine API setup or validation with browser interactions

The repository also includes QA planning artifacts: an API inventory, test cases, a test plan, and a requirements traceability matrix.

## Tech stack

- Python
- pytest
- Playwright (Chromium)
- Requests through Playwright's API request context
- JSON Schema validation
- Faker for generated test data
- Allure results configuration

## Prerequisites

1. Python 3.10 or later (use a version supported by the pinned dependencies).
2. The banking application under test running locally:
   - Web UI: `http://localhost:3000`
   - API: `http://localhost:3001`
3. Playwright's Chromium browser installed.

The application itself is not included in this repository. Start its UI and API services before running the tests. If your application uses different addresses, update the URLs in the test fixtures and page setup before execution.

## Installation

Clone the repository and enter its directory:

```bash
git clone https://github.com/Joshva-Jashper/banking-ui-api-test-framework.git
cd banking-ui-api-test-framework
```

Create and activate a virtual environment, then install the pinned dependencies and Chromium:

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirement.txt
playwright install chromium
```

## Running tests

Run the full test suite:

```bash
pytest
```

Run only UI or API tests:

```bash
pytest tests/test_ui
pytest tests/test_api
```

Run tests selected by marker:

```bash
pytest -m ui
pytest -m api
pytest -m smoke
pytest -m e2e
```

The pytest configuration selects Chromium, enables verbose output, and configures screenshots, videos, traces, and Allure result output for test runs. Failure artifacts and reports are written under the configured `report/` paths.

## Project structure

```text
auth/                 Browser storage-state files used by test fixtures
pages/
  pages_api/          API client wrappers
  pages_ui/           Page-object classes for UI workflows
test_data/            Test data builders and JSON data
tests/
  test_api/           API and API/UI end-to-end tests
  test_ui/            Browser UI tests
utils/                Shared utilities
API_Inventory.xlsx    API inventory
BRS_and_Test_Plan.docx Business requirements and test plan
QA_Test_Cases.xlsx    QA test cases
RTM.xlsx              Requirements traceability matrix
pytest.ini            pytest options and markers
requirement.txt       Pinned Python dependencies
```

## Test markers

Markers declared in `pytest.ini` include `ui`, `api`, `smoke`, `e2e`, and `no_auth`. Use `pytest -m <marker>` to select tests by marker.

## Reports and debugging

The pytest configuration stores Allure result files in `report/allure_result` and retains screenshots, videos, and Playwright traces on failure. Review these artifacts when investigating a failed test. Allure result files can be rendered with the Allure command-line tool if it is installed.


## Current known limitation

One API/UI end-to-end transaction validation test is marked `xfail` because its transaction is not currently reflected in the UI. The test is expected to fail until that behavior is resolved.
