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

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications
- **python-dotenv**: Load environment variables from .env files
- **python-multipart**: Handle multipart form data

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
