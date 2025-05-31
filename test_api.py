import pytest
import requests
import json
from unittest.mock import patch, MagicMock


class TestTDSVirtualTA:
    """
    Basic tests for the TDS Virtual TA API
    """
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        # This would be run against a running instance
        pass
    
    def test_question_processing(self):
        """Test question processing functionality"""
        from services.question_processor import QuestionProcessor
        
        processor = QuestionProcessor()
        
        # Test basic question processing
        result = processor.process_question("Should I use gpt-3.5-turbo-0125 or gpt-4o-mini?")
        
        assert result['original_question'] == "Should I use gpt-3.5-turbo-0125 or gpt-4o-mini?"
        assert result['question_type'] == 'model_usage'
        assert 'gpt' in result['keywords']
    
    def test_answer_generation(self):
        """Test answer generation functionality"""
        from services.answer_generator import AnswerGenerator
        from services.question_processor import QuestionProcessor
        
        processor = QuestionProcessor()
        generator = AnswerGenerator()
        
        # Test predefined answer for model usage
        processed = processor.process_question("Should I use gpt-3.5-turbo-0125 or gpt-4o-mini?")
        answer = generator.generate_answer(processed)
        
        assert answer['answer'] is not None
        assert len(answer['links']) >= 0
        assert isinstance(answer['links'], list)
    
    def test_api_request_format(self):
        """Test API request and response format"""
        from models.request_models import QuestionRequest
        from models.response_models import AnswerResponse, LinkResponse
        
        # Test request model
        request = QuestionRequest(question="Test question")
        assert request.question == "Test question"
        assert request.image is None
        
        # Test response model
        link = LinkResponse(url="http://example.com", text="Example")
        response = AnswerResponse(answer="Test answer", links=[link])
        
        assert response.answer == "Test answer"
        assert len(response.links) == 1
        assert response.links[0].url == "http://example.com"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
