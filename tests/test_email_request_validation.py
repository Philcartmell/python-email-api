import pytest
from pydantic import ValidationError
from models.email_request import EmailRequest

class TestEmailRequestValidation:
    """Test cases for EmailRequest model validation"""
    
    def test_valid_email_request(self):
        """Test valid email request passes validation"""
        valid_data = {
            "to": ["test@example.com", "user@example.com"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "Test plain body content"
        }
        
        email_request = EmailRequest(**valid_data)
        assert email_request.to == ["test@example.com", "user@example.com"]
        assert email_request.from_email == "sender@example.com"
        assert email_request.subject == "Test Subject"
        assert email_request.plain_body == "Test plain body content"
        assert email_request.html_body is None
    
    def test_valid_email_request_with_html(self):
        """Test valid email request with HTML body"""
        valid_data = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "Test plain body",
            "html_body": "<h1>Test HTML</h1>"
        }
        
        email_request = EmailRequest(**valid_data)
        assert email_request.html_body == "<h1>Test HTML</h1>"
    
    def test_empty_recipients_list_validation_error(self):
        """Test that empty recipients list raises ValidationError"""
        invalid_data = {
            "to": [],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "Test body"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            EmailRequest(**invalid_data)
        
        assert "At least one recipient is required" in str(exc_info.value)
    
    def test_none_recipients_list_validation_error(self):
        """Test that None recipients list raises ValidationError"""
        invalid_data = {
            "to": None,
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "Test body"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            EmailRequest(**invalid_data)
    
    def test_empty_subject_validation_error(self):
        """Test that empty subject raises ValidationError"""
        invalid_data = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "",
            "plain_body": "Test body"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            EmailRequest(**invalid_data)
        
        assert "Subject cannot be empty" in str(exc_info.value)
    
    def test_whitespace_only_subject_validation_error(self):
        """Test that whitespace-only subject raises ValidationError"""
        invalid_data = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "   ",
            "plain_body": "Test body"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            EmailRequest(**invalid_data)
        
        assert "Subject cannot be empty" in str(exc_info.value)
    
    def test_empty_plain_body_validation_error(self):
        """Test that empty plain body raises ValidationError"""
        invalid_data = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": ""
        }
        
        with pytest.raises(ValidationError) as exc_info:
            EmailRequest(**invalid_data)
        
        assert "Plain body cannot be empty" in str(exc_info.value)
    
    def test_whitespace_only_plain_body_validation_error(self):
        """Test that whitespace-only plain body raises ValidationError"""
        invalid_data = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "   "
        }
        
        with pytest.raises(ValidationError) as exc_info:
            EmailRequest(**invalid_data)
        
        assert "Plain body cannot be empty" in str(exc_info.value)
    
    def test_invalid_email_format_validation_error(self):
        """Test that invalid email format raises ValidationError"""
        invalid_data = {
            "to": ["invalid-email"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "Test body"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            EmailRequest(**invalid_data)
    
    def test_invalid_from_email_format_validation_error(self):
        """Test that invalid from email format raises ValidationError"""
        invalid_data = {
            "to": ["test@example.com"],
            "from_email": "invalid-from-email",
            "subject": "Test Subject",
            "plain_body": "Test body"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            EmailRequest(**invalid_data)
    
    def test_missing_required_fields_validation_error(self):
        """Test that missing required fields raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            EmailRequest(
                to=["test@example.com"],
                subject="Test Subject"
                # Missing from_email and plain_body
            )
    
    def test_subject_trimming(self):
        """Test that subject whitespace is trimmed"""
        data = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "  Test Subject  ",
            "plain_body": "Test body"
        }
        
        email_request = EmailRequest(**data)
        assert email_request.subject == "Test Subject"
    
    def test_plain_body_trimming(self):
        """Test that plain body whitespace is trimmed"""
        data = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "  Test body  "
        }
        
        email_request = EmailRequest(**data)
        assert email_request.plain_body == "Test body"
    
    def test_multiple_valid_recipients(self):
        """Test multiple valid recipients"""
        data = {
            "to": ["user1@example.com", "user2@example.com", "user3@example.com"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "Test body"
        }
        
        email_request = EmailRequest(**data)
        assert len(email_request.to) == 3
        assert "user1@example.com" in email_request.to
        assert "user2@example.com" in email_request.to
        assert "user3@example.com" in email_request.to
