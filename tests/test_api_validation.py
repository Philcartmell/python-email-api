import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

class TestEmailAPIValidation:
    """Test cases for email API endpoint validation"""
    
    def setup_method(self):
        """Setup test client and mock environment"""
        self.client = TestClient(app)
        
        # Mock environment variables for testing
        self.env_patcher = patch.dict(os.environ, {
            "SMTP_HOST": "test-smtp.com",
            "SMTP_PORT": "587",
            "SMTP_USERNAME": "test@example.com",
            "SMTP_PASSWORD": "test-password",
            "SKIP_EMAIL_SENDING": "true"
        })
        self.env_patcher.start()
    
    def teardown_method(self):
        """Clean up after each test"""
        self.env_patcher.stop()
    
    def test_valid_email_request_success(self):
        """Test valid email request returns 200"""
        valid_payload = {
            "to": ["test@example.com", "user@example.com"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "Test body content"
        }
        
        with patch("services.email_service.EmailService.send_email") as mock_send:
            mock_send.return_value = True
            
            response = self.client.post("/send-email", json=valid_payload)
            
            assert response.status_code == 200
            assert response.json()["status"] == "success"
            assert "Email sent successfully" in response.json()["message"]
    
    def test_valid_email_request_with_html_success(self):
        """Test valid email request with HTML body returns 200"""
        valid_payload = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "Test body content",
            "html_body": "<h1>Test HTML</h1>"
        }
        
        with patch("services.email_service.EmailService.send_email") as mock_send:
            mock_send.return_value = True
            
            response = self.client.post("/send-email", json=valid_payload)
            
            assert response.status_code == 200
            assert response.json()["status"] == "success"
    
    def test_empty_recipients_validation_error(self):
        """Test empty recipients list returns 422"""
        invalid_payload = {
            "to": [],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "Test body"
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
        assert "At least one recipient is required" in str(response.json())
    
    def test_empty_subject_validation_error(self):
        """Test empty subject returns 422"""
        invalid_payload = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "",
            "plain_body": "Test body"
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
        assert "Subject cannot be empty" in str(response.json())
    
    def test_whitespace_only_subject_validation_error(self):
        """Test whitespace-only subject returns 422"""
        invalid_payload = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "   ",
            "plain_body": "Test body"
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
        assert "Subject cannot be empty" in str(response.json())
    
    def test_empty_plain_body_validation_error(self):
        """Test empty plain body returns 422"""
        invalid_payload = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": ""
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
        assert "Plain body cannot be empty" in str(response.json())
    
    def test_whitespace_only_plain_body_validation_error(self):
        """Test whitespace-only plain body returns 422"""
        invalid_payload = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "   "
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
        assert "Plain body cannot be empty" in str(response.json())
    
    def test_invalid_email_format_validation_error(self):
        """Test invalid email format returns 422"""
        invalid_payload = {
            "to": ["invalid-email"],
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "Test body"
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
    
    def test_invalid_from_email_format_validation_error(self):
        """Test invalid from email format returns 422"""
        invalid_payload = {
            "to": ["test@example.com"],
            "from_email": "invalid-from-email",
            "subject": "Test Subject",
            "plain_body": "Test body"
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
    
    def test_missing_required_fields_validation_error(self):
        """Test missing required fields returns 422"""
        invalid_payload = {
            "to": ["test@example.com"],
            "subject": "Test Subject"
            # Missing from_email and plain_body
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
    
    def test_missing_to_field_validation_error(self):
        """Test missing to field returns 422"""
        invalid_payload = {
            "from_email": "sender@example.com",
            "subject": "Test Subject",
            "plain_body": "Test body"
            # Missing to field
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
    
    def test_missing_from_email_field_validation_error(self):
        """Test missing from_email field returns 422"""
        invalid_payload = {
            "to": ["test@example.com"],
            "subject": "Test Subject",
            "plain_body": "Test body"
            # Missing from_email field
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
    
    def test_missing_subject_field_validation_error(self):
        """Test missing subject field returns 422"""
        invalid_payload = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "plain_body": "Test body"
            # Missing subject field
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
    
    def test_missing_plain_body_field_validation_error(self):
        """Test missing plain_body field returns 422"""
        invalid_payload = {
            "to": ["test@example.com"],
            "from_email": "sender@example.com",
            "subject": "Test Subject"
            # Missing plain_body field
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
    
    def test_multiple_validation_errors(self):
        """Test multiple validation errors returns 422"""
        invalid_payload = {
            "to": [],
            "from_email": "invalid-email",
            "subject": "",
            "plain_body": ""
        }
        
        response = self.client.post("/send-email", json=invalid_payload)
        
        assert response.status_code == 422
    
    def test_health_endpoint(self):
        """Test health endpoint returns 200"""
        response = self.client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_invalid_json_format(self):
        """Test invalid JSON format returns 422"""
        response = self.client.post("/send-email", 
                                  data="invalid json",
                                  headers={"Content-Type": "application/json"})
        
        assert response.status_code == 422
    
    def test_wrong_content_type(self):
        """Test wrong content type returns 422"""
        response = self.client.post("/send-email", 
                                  data="some data",
                                  headers={"Content-Type": "text/plain"})
        
        assert response.status_code == 422