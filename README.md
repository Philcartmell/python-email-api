# Python Email API

A FastAPI-based email service that provides a RESTful API for sending emails via SMTP. The application supports both plain text and HTML email content with comprehensive validation and error handling.

## Features

- **RESTful API**: Simple HTTP endpoints for email operations
- **Email Validation**: Comprehensive validation using Pydantic models
- **SMTP Integration**: Configurable SMTP server support
- **Development Mode**: Skip actual email sending for testing
- **Error Handling**: Proper HTTP status codes and error messages
- **Clean Architecture**: Modular design with separated concerns

## Project Structure

```
python-email-api/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── models/
│   ├── __init__.py
│   └── email_request.py   # EmailRequest Pydantic model
├── config/
│   ├── __init__.py
│   └── email_config.py    # EmailConfig class
└── services/
    ├── __init__.py
    └── email_service.py   # EmailService class
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-email-api
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your SMTP credentials:
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   SKIP_EMAIL_SENDING=false
   ```

## Running the Application

### Development Mode

```bash
python main.py
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints

#### Send Email
- **POST** `/send-email`
- **Description**: Send an email via SMTP
- **Request Body**:
  ```json
  {
    "to": ["recipient@example.com", "another@example.com"],
    "from_email": "sender@example.com",
    "subject": "Test Email",
    "plain_body": "This is the plain text body",
    "html_body": "<h1>This is the HTML body</h1>"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Email sent successfully",
    "status": "success"
  }
  ```

#### Health Check
- **GET** `/health`
- **Description**: Check API health status
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SMTP_HOST` | SMTP server hostname | - | Yes |
| `SMTP_PORT` | SMTP server port | 587 | No |
| `SMTP_USERNAME` | SMTP username | - | Yes |
| `SMTP_PASSWORD` | SMTP password | - | Yes |
| `SKIP_EMAIL_SENDING` | Skip actual email sending (development) | false | No |

### SMTP Providers

#### Gmail
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

#### Outlook/Hotmail
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
```

#### Custom SMTP Server
```env
SMTP_HOST=your-smtp-server.com
SMTP_PORT=587
SMTP_USERNAME=your-username
SMTP_PASSWORD=your-password
```

## Development

### Development Mode

Set `SKIP_EMAIL_SENDING=true` in your `.env` file to skip actual email sending during development. This allows you to test the API without sending real emails.

### Testing the API

You can test the API using curl:

```bash
curl -X POST "http://localhost:8000/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["test@example.com"],
    "from_email": "sender@example.com",
    "subject": "Test Email",
    "plain_body": "This is a test email",
    "html_body": "<h1>Test Email</h1><p>This is a test email</p>"
  }'
```

## Error Handling

The API returns appropriate HTTP status codes:

- **200**: Email sent successfully
- **400**: Bad request (validation errors)
- **500**: Internal server error

### Example Error Response

```json
{
  "detail": "At least one recipient is required"
}
```

## Testing

The project includes comprehensive test suites to ensure reliability and validation.

### Test Structure

```
tests/
├── __init__.py
├── test_email_request_validation.py    # Model validation tests
└── test_api_validation.py              # API endpoint tests
```

### Test Categories

#### **Model Validation Tests** (`test_email_request_validation.py`)
Tests the Pydantic EmailRequest model validation:

- ✅ **Valid email requests** - Ensures proper data acceptance
- ✅ **Empty recipients validation** - Tests required recipient validation
- ✅ **Empty subject validation** - Ensures subject is not empty
- ✅ **Empty plain body validation** - Ensures body content is required
- ✅ **Invalid email format validation** - Tests email format validation
- ✅ **Missing required fields** - Tests required field validation
- ✅ **Whitespace trimming** - Ensures proper whitespace handling
- ✅ **Multiple recipients** - Tests bulk recipient handling

#### **API Endpoint Tests** (`test_api_validation.py`)
Tests the FastAPI endpoints with various scenarios:

- ✅ **Valid requests** - Tests successful email sending
- ✅ **Validation errors** - Tests HTTP 422 responses for invalid data
- ✅ **Missing fields** - Tests required field validation
- ✅ **Invalid JSON** - Tests malformed request handling
- ✅ **Wrong content type** - Tests content type validation
- ✅ **Health endpoint** - Tests `/healthz` endpoint functionality

### Running Tests

#### **Install Test Dependencies**
```bash
pip install -r requirements.txt
```

#### **Run All Tests**
```bash
# Run all tests with verbose output
pytest -v

# Run all tests with coverage
pytest -v --cov=.

# Run tests with detailed output
pytest -v -s
```

#### **Run Specific Test Files**
```bash
# Run only model validation tests
pytest tests/test_email_request_validation.py -v

# Run only API validation tests
pytest tests/test_api_validation.py -v
```

#### **Run Specific Test Classes**
```bash
# Run only EmailRequest validation tests
pytest tests/test_email_request_validation.py::TestEmailRequestValidation -v

# Run only API validation tests
pytest tests/test_api_validation.py::TestEmailAPIValidation -v
```

#### **Run Specific Test Methods**
```bash
# Run a specific test method
pytest tests/test_email_request_validation.py::TestEmailRequestValidation::test_valid_email_request -v
```

#### **Run Tests with Markers**
```bash
# Run only validation tests (if you add markers)
pytest -m validation -v
```

### Test Coverage

```bash
# Install coverage if not already installed
pip install coverage

# Run tests with coverage
pytest --cov=. --cov-report=html --cov-report=term-missing

# View HTML coverage report
open htmlcov/index.html
```

### CI/CD Pipeline Commands

For automated testing in CI/CD pipelines:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with exit code on failure
pytest -v --tb=short

# Run tests with coverage report
pytest -v --cov=. --cov-report=term-missing

# Run tests and generate JUnit XML for CI
pytest -v --junitxml=test-results.xml
```

### Test Configuration

Create a `pytest.ini` file in your project root for custom test configuration:

```ini
[tool.pytest.ini_options]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    validation: marks tests as validation tests
    integration: marks tests as integration tests
```

### Expected Test Results

All tests should pass with the following coverage:

- ✅ **Model Validation**: 100% coverage of EmailRequest validation logic
- ✅ **API Validation**: 100% coverage of endpoint validation scenarios
- ✅ **Error Handling**: Comprehensive testing of error scenarios
- ✅ **Edge Cases**: Testing of boundary conditions and edge cases

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications
- **python-dotenv**: Load environment variables from .env files
- **python-multipart**: Handle multipart form data
- **pytest**: Testing framework for Python
- **httpx**: HTTP client for testing FastAPI applications
- **email-validator**: Email validation for Pydantic models

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For support and questions, please open an issue in the repository.
