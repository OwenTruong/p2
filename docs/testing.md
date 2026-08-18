# Testing Setup

SpaceBnB uses **pytest** for unit, HTTP/router, and integration testing.

## 1. Install Test Dependencies

From the project root, activate the project's Python virtual environment and install pytest:

``` bash
pip install pytest
```

------------------------------------------------------------------------

## 2. Run Tests from the Project Root

Unit and HTTP tests should be run from the **root of the repository**.

Running tests from the root ensures that Python resolves shared packages and service modules using the expected project structure.

### Run All Unit/HTTP Tests

``` bash
bash scripts/test/run_tests.sh
```

### Run Unit Tests

For a specific service:

``` bash
python -m pytest services/auth_service/tests/unit
```


### Run HTTP / Route Tests

``` bash
python -m pytest services/auth_service/tests/http
```


### Run a Specific Test File

``` bash
python -m pytest services/auth_service/tests/http/test_auth_routes.py
```

### Run a Specific Test

``` bash
python -m pytest services/auth_service/tests/http/test_auth_routes.py::test_register_returns_409_when_email_exists
```

### Verbose Output

Use `-v` to display individual test names:

``` bash
python -m pytest -v
```

For additional debugging information:

``` bash
python -m pytest -vv
```

------------------------------------------------------------------------

## 3. Test Types

### Unit Tests

Unit tests validate individual classes or functions in isolation.

External dependencies such as repositories, API clients, and other services should normally be mocked.

``` text
ReservationService
    ├── Mock ReservationRepository
    └── Mock ListingClient
```

Unit tests should not require Docker, databases, or running microservices.

### HTTP / Route Tests

HTTP tests validate the FastAPI HTTP layer using `TestClient`.

These tests verify:

- Request validation
- HTTP status codes
- Response bodies
- Dependency injection
- Application exception handling

Service dependencies should generally be mocked so the test focuses on HTTP behavior.

### Integration Tests

Integration tests verify multiple real components working together:

``` text
HTTP request
    ↓
FastAPI
    ↓
Service
    ↓
Repository
    ↓
PostgreSQL
```

They can also verify communication between multiple SpaceBnB services.

Because integration tests require infrastructure such as databases and containers, run them using the project's integration test script.

------------------------------------------------------------------------

## 4. Run Integration Tests

Run the integration test script from the project root:

``` bash
./scripts/<integration-test-script>
```

The script is responsible for preparing the required test environment, running the integration tests, and cleaning up afterward.

If the script is not executable:

``` bash
chmod +x ./scripts/<integration-test-script>
```

Then run it again.

------------------------------------------------------------------------

## Quick Reference

| Test              | Command                                          |
|-------------------|--------------------------------------------------|
| Unit & HTTP tests | `bash scripts/test/run_tests.sh`                 |
| Unit tests        | `python -m pytest services/<service>/tests/unit` |
| HTTP tests        | `python -m pytest services/<service>/tests/http` |
| Specific file     | `python -m pytest <path-to-test-file>`           |
| Specific test     | `python -m pytest <file>::<test_name>`           |
| Verbose output    | `python -m pytest -v`                            |
| Integration tests | `./scripts/<integration-test-script>`            |

## Important

Always run unit and HTTP pytest commands from the **repository root**.

Prefer:

``` bash
python -m pytest ...
```

rather than:

``` bash
pytest ...
```

Using `python -m pytest` ensures pytest runs through the active Python interpreter and generally avoids import/path inconsistencies between environments.
