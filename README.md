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

- **Swagger UI**: `http://localhost:8000/docs` (if enabled via `ENABLE_SWAGGER=true`)

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
| `ENABLE_SWAGGER` | Enable Swagger UI documentation | false | No |


## Development

### Development Mode

Set `SKIP_EMAIL_SENDING=true` in your `.env` file to skip actual email sending during development. This allows you to test the API without sending real emails.

### Swagger Documentation

Swagger UI documentation is disabled by default for security. To enable it for development:

1. Set `ENABLE_SWAGGER=true` in your `.env` file
2. Restart the application
3. Access the documentation at `http://localhost:8000/docs`

**Note**: ReDoc is permanently disabled and cannot be enabled.

### Testing the API

You can test the API using curl:

```bash
curl -X POST "http://localhost:8000/email" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["test@example.com"],
    "from_email": "sender@example.com",
    "subject": "Test Email",
    "plain_body": "This is a test email",
    "html_body": "<h1>Test Email</h1><p>This is a test email</p>"
  }'
```

## Using the API from Python

### Example Python Script

Here's a complete example of how to call the email API from another Python script:

#### **Dependencies**
```bash
pip install requests
```

#### **Basic Email Sending Script**
```python
import requests
import json
from typing import List, Optional

class EmailAPIClient:
    """Client for interacting with the Email API"""
    
    def __init__(self, base_url: str = "http://localhost:8000", token: str):
        self.base_url = base_url
        self.email_endpoint = f"{base_url}/email"
        self.health_endpoint = f"{base_url}/healthz"
        self.token = token
    
    def send_email(self, 
                   to: List[str], 
                   from_email: str, 
                   subject: str, 
                   plain_body: str, 
                   html_body: Optional[str] = None) -> dict:
        """
        Send an email via the API
        
        Args:
            to: List of recipient email addresses
            from_email: Sender email address
            subject: Email subject
            plain_body: Plain text body content
            html_body: Optional HTML body content
            
        Returns:
            dict: API response
        """
        payload = {
            "to": to,
            "from_email": from_email,
            "subject": subject,
            "plain_body": plain_body
        }
        
        if html_body:
            payload["html_body"] = html_body
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        
        try:
            response = requests.post(
                self.email_endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            error_detail = "Unknown error"
            try:
                error_response = response.json()
                error_detail = error_response.get("detail", "Unknown error")
            except:
                pass
            raise Exception(f"HTTP Error {response.status_code}: {error_detail}")
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def check_health(self) -> dict:
        """Check API health status"""
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = requests.get(self.health_endpoint, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Health check failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Initialize the client with token
    email_client = EmailAPIClient("http://localhost:8000", token="your-api-token-here")
    
    try:
        # Check API health
        print("Checking API health...")
        health = email_client.check_health()
        print(f"API Status: {health.get('status', 'unknown')}")
        
        # Send a simple email
        print("\nSending email...")
        result = email_client.send_email(
            to=["recipient@example.com"],
            from_email="sender@example.com",
            subject="Test Email from Python Script",
            plain_body="This is a test email sent from a Python script using the Email API.",
            html_body="<h1>Test Email</h1><p>This is a test email sent from a Python script using the Email API.</p>"
        )
        print(f"Email sent successfully: {result}")
        
        # Send email to multiple recipients
        print("\nSending email to multiple recipients...")
        result = email_client.send_email(
            to=["user1@example.com", "user2@example.com", "user3@example.com"],
            from_email="sender@example.com",
            subject="Bulk Email Test",
            plain_body="This email was sent to multiple recipients.",
            html_body="<h2>Bulk Email Test</h2><p>This email was sent to multiple recipients.</p>"
        )
        print(f"Bulk email sent successfully: {result}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
```

#### **Advanced Usage Example**
```python
import requests
import json
from datetime import datetime
from typing import List, Optional, Dict, Any

class AdvancedEmailAPIClient:
    """Advanced client with additional features"""
    
    def __init__(self, base_url: str = "http://localhost:8000", token: str):
        self.base_url = base_url
        self.email_endpoint = f"{base_url}/email"
        self.health_endpoint = f"{base_url}/healthz"
        self.token = token
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "EmailAPIClient/1.0"
        })
        
        self.session.headers["Authorization"] = f"Bearer {token}"
    
    def send_email_with_template(self, 
                                to: List[str], 
                                from_email: str, 
                                subject: str, 
                                template_name: str, 
                                template_vars: Dict[str, Any]) -> dict:
        """Send email using a template with variables"""
        
        # Simple template system (you can expand this)
        templates = {
            "welcome": {
                "plain_body": f"Welcome {template_vars.get('name', 'User')}! Your account has been created.",
                "html_body": f"<h1>Welcome {template_vars.get('name', 'User')}!</h1><p>Your account has been created.</p>"
            },
            "notification": {
                "plain_body": f"Notification: {template_vars.get('message', 'No message')}",
                "html_body": f"<h2>Notification</h2><p>{template_vars.get('message', 'No message')}</p>"
            }
        }
        
        template = templates.get(template_name, templates["notification"])
        
        return self.send_email(
            to=to,
            from_email=from_email,
            subject=subject,
            plain_body=template["plain_body"],
            html_body=template["html_body"]
        )
    
    def send_email(self, 
                   to: List[str], 
                   from_email: str, 
                   subject: str, 
                   plain_body: str, 
                   html_body: Optional[str] = None) -> dict:
        """Send an email via the API"""
        
        payload = {
            "to": to,
            "from_email": from_email,
            "subject": subject,
            "plain_body": plain_body
        }
        
        if html_body:
            payload["html_body"] = html_body
        
        try:
            response = self.session.post(
                self.email_endpoint,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            error_detail = "Unknown error"
            try:
                error_response = response.json()
                error_detail = error_response.get("detail", "Unknown error")
            except:
                pass
            raise Exception(f"HTTP Error {response.status_code}: {error_detail}")
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def check_health(self) -> dict:
        """Check API health status"""
        try:
            response = self.session.get(self.health_endpoint, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Health check failed: {str(e)}")
    
    def send_bulk_emails(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Send multiple emails in batch"""
        results = []
        
        for email_data in emails:
            try:
                result = self.send_email(**email_data)
                results.append({"success": True, "result": result, "email": email_data})
            except Exception as e:
                results.append({"success": False, "error": str(e), "email": email_data})
        
        return results

# Example usage
if __name__ == "__main__":
    # Initialize the advanced client with token
    email_client = AdvancedEmailAPIClient("http://localhost:8000", token="your-api-token-here")
    
    try:
        # Check API health
        print("Checking API health...")
        health = email_client.check_health()
        print(f"API Status: {health.get('status', 'unknown')}")
        
        # Send email with template
        print("\nSending welcome email with template...")
        result = email_client.send_email_with_template(
            to=["newuser@example.com"],
            from_email="noreply@example.com",
            subject="Welcome to Our Service",
            template_name="welcome",
            template_vars={"name": "John Doe"}
        )
        print(f"Welcome email sent: {result}")
        
        # Send bulk emails
        print("\nSending bulk emails...")
        bulk_emails = [
            {
                "to": ["user1@example.com"],
                "from_email": "sender@example.com",
                "subject": "Bulk Email 1",
                "plain_body": "This is bulk email 1"
            },
            {
                "to": ["user2@example.com"],
                "from_email": "sender@example.com",
                "subject": "Bulk Email 2",
                "plain_body": "This is bulk email 2"
            }
        ]
        
        bulk_results = email_client.send_bulk_emails(bulk_emails)
        for i, result in enumerate(bulk_results):
            if result["success"]:
                print(f"Bulk email {i+1} sent successfully")
            else:
                print(f"Bulk email {i+1} failed: {result['error']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
```

#### **Error Handling Example**
```python
import requests
import json
from typing import List, Optional

def send_email_with_retry(to: List[str], 
                         from_email: str, 
                         subject: str, 
                         plain_body: str, 
                         html_body: Optional[str] = None,
                         token: str,
                         max_retries: int = 3) -> dict:
    """Send email with retry logic"""
    
    for attempt in range(max_retries):
        try:
            payload = {
                "to": to,
                "from_email": from_email,
                "subject": subject,
                "plain_body": plain_body
            }
            
            if html_body:
                payload["html_body"] = html_body
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            response = requests.post(
                "http://localhost:8000/email",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 422:
                # Validation error - don't retry
                error_detail = "Validation error"
                try:
                    error_response = response.json()
                    error_detail = error_response.get("detail", "Validation error")
                except:
                    pass
                raise Exception(f"Validation Error: {error_detail}")
            elif response.status_code >= 500:
                # Server error - retry
                print(f"Server error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    raise Exception(f"Server error after {max_retries} attempts: {e}")
            else:
                # Other HTTP error - don't retry
                raise Exception(f"HTTP Error {response.status_code}: {e}")
        
        except requests.exceptions.RequestException as e:
            print(f"Request error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise Exception(f"Request failed after {max_retries} attempts: {e}")
        
        # Wait before retry
        import time
        time.sleep(2 ** attempt)  # Exponential backoff
    
    raise Exception("Max retries exceeded")

# Example usage
if __name__ == "__main__":
    try:
        result = send_email_with_retry(
            to=["recipient@example.com"],
            from_email="sender@example.com",
            subject="Test Email with Retry",
            plain_body="This email was sent with retry logic.",
            html_body="<h1>Test Email with Retry</h1><p>This email was sent with retry logic.</p>",
            token="your-api-token-here"
        )
        print(f"Email sent successfully: {result}")
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
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
