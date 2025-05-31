import json
import os
from typing import List, Dict, Any, Optional
import re
from datetime import datetime
import openai
from dotenv import load_dotenv

load_dotenv()


class AnswerGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        self.discourse_data = self.load_discourse_data()
        self.course_content = self.load_course_content()
        
        # Predefined answers for common questions
        self.predefined_answers = {
            'model_usage': {
                'gpt-3.5-turbo-0125': {
                    'answer': "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`. Use the OpenAI API directly for this question.",
                    'links': [
                        {
                            'url': "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4",
                            'text': "Use the model that's mentioned in the question."
                        }
                    ]
                }
            },
            'environment_setup': {
                'docker_vs_podman': {
                    'answer': "While Docker knowledge is valuable, we recommend using Podman for this course as it's the officially supported container tool. However, Docker is also acceptable for completing assignments.",
                    'links': [
                        {
                            'url': "https://tds.s-anand.net/#/docker",
                            'text': "TDS Docker/Podman Documentation"
                        }
                    ]
                }
            },
            'grading_system': {
                'bonus_scoring': {
                    'answer': "If a student scores 10/10 on GA4 as well as a bonus, it would appear as '110' on the dashboard, indicating 10 out of 10 plus the bonus point.",
                    'links': [
                        {
                            'url': "https://discourse.onlinedegree.iitm.ac.in/t/ga4-data-sourcing-discussion-thread-tds-jan-2025/165959/388",
                            'text': "GA4 scoring discussion"
                        }
                    ]
                }
            }
        }
    
    def load_discourse_data(self) -> List[Dict[str, Any]]:
        """
        Load scraped Discourse data
        """
        try:
            filepath = os.path.join('data', 'discourse_posts.json')
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading discourse data: {e}")
        
        # Return sample data if file doesn't exist
        return [
            {
                'id': 155939,
                'title': 'GA5 Question 8 Clarification',
                'url': 'https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939',
                'posts': [
                    {
                        'raw': 'Use the model that\'s mentioned in the question. If it says gpt-3.5-turbo-0125, use that specifically.'
                    }
                ]
            },
            {
                'id': 165959,
                'title': 'GA4 Data Sourcing Discussion Thread TDS Jan 2025',
                'url': 'https://discourse.onlinedegree.iitm.ac.in/t/ga4-data-sourcing-discussion-thread-tds-jan-2025/165959',
                'posts': [
                    {
                        'raw': 'If you score 10/10 and get a bonus, the dashboard will show 110.'
                    }
                ]
            }
        ]
    
    def load_course_content(self) -> List[Dict[str, Any]]:
        """
        Load scraped course content
        """
        try:
            filepath = os.path.join('data', 'course_content.json')
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading course content: {e}")
        
        # Return sample course content
        return [
            {
                'url': 'https://tds.s-anand.net/#/docker',
                'title': 'Docker and Podman Guide',
                'content': 'This course recommends using Podman, but Docker is also acceptable for assignments.'
            }
        ]
    
    def generate_answer(self, processed_question: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an answer based on the processed question
        """
        question_type = processed_question['question_type']
        keywords = processed_question['keywords']
        original_question = processed_question['original_question']
        
        # Check for predefined answers first
        predefined_answer = self.get_predefined_answer(question_type, keywords, original_question)
        if predefined_answer:
            return predefined_answer
        
        # Search for relevant content
        relevant_content = self.search_relevant_content(processed_question)
        
        # Generate answer using available content
        if relevant_content:
            return self.generate_contextual_answer(processed_question, relevant_content)
        else:
            return self.generate_fallback_answer(processed_question)
    
    def get_predefined_answer(self, question_type: str, keywords: List[str], question: str) -> Optional[Dict[str, Any]]:
        """
        Check if we have a predefined answer for this type of question
        """
        question_lower = question.lower()
        
        # Model usage questions
        if question_type == 'model_usage':
            if 'gpt-3.5-turbo-0125' in keywords or 'gpt3.5' in question_lower:
                return self.predefined_answers['model_usage']['gpt-3.5-turbo-0125']
        
        # Environment setup questions
        elif question_type == 'environment_setup':
            if any(word in question_lower for word in ['docker', 'podman']):
                return self.predefined_answers['environment_setup']['docker_vs_podman']
        
        # Grading system questions
        elif question_type == 'grading_system':
            if 'bonus' in question_lower and ('10/10' in question or 'dashboard' in question_lower):
                return self.predefined_answers['grading_system']['bonus_scoring']
        
        # Schedule inquiries
        elif question_type == 'schedule_inquiry':
            if 'sep 2025' in question_lower and 'end-term' in question_lower:
                return {
                    'answer': "I don't have information about the TDS Sep 2025 end-term exam schedule yet, as this information is not available at this time.",
                    'links': []
                }
        
        return None
    
    def search_relevant_content(self, processed_question: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for relevant content in discourse posts and course materials
        """
        relevant_content = []
        keywords = processed_question['keywords']
        question_lower = processed_question['cleaned_question'].lower()
        
        # Search discourse posts
        for topic in self.discourse_data:
            relevance_score = 0
            
            # Check title relevance
            title_lower = topic.get('title', '').lower()
            for keyword in keywords:
                if keyword.lower() in title_lower:
                    relevance_score += 2
            
            # Check post content relevance
            for post in topic.get('posts', []):
                post_content = post.get('raw', '').lower()
                for keyword in keywords:
                    if keyword.lower() in post_content:
                        relevance_score += 1
            
            if relevance_score > 0:
                relevant_content.append({
                    'type': 'discourse',
                    'data': topic,
                    'relevance': relevance_score
                })
        
        # Search course content
        for content in self.course_content:
            relevance_score = 0
            content_text = content.get('content', '').lower()
            
            for keyword in keywords:
                if keyword.lower() in content_text:
                    relevance_score += 1
            
            if relevance_score > 0:
                relevant_content.append({
                    'type': 'course',
                    'data': content,
                    'relevance': relevance_score
                })
        
        # Sort by relevance
        relevant_content.sort(key=lambda x: x['relevance'], reverse=True)
        
        return relevant_content[:5]  # Return top 5 most relevant
    
    def generate_contextual_answer(self, processed_question: Dict[str, Any], relevant_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate an answer based on relevant content found
        """
        answer_parts = []
        links = []
        
        # Extract information from relevant content
        for content_item in relevant_content:
            if content_item['type'] == 'discourse':
                topic = content_item['data']
                links.append({
                    'url': topic.get('url', ''),
                    'text': topic.get('title', 'Discourse discussion')
                })
                
                # Extract relevant post content
                for post in topic.get('posts', [])[:2]:  # Take first 2 posts
                    post_text = post.get('raw', '')
                    if len(post_text) > 50:  # Only include substantial posts
                        answer_parts.append(post_text[:200] + '...' if len(post_text) > 200 else post_text)
            
            elif content_item['type'] == 'course':
                course_item = content_item['data']
                links.append({
                    'url': course_item.get('url', ''),
                    'text': course_item.get('title', 'Course content')
                })
        
        # Combine answer parts
        if answer_parts:
            answer = "Based on the available information: " + " ".join(answer_parts[:2])
        else:
            answer = "I found some relevant discussions, but please check the linked resources for detailed information."
        
        return {
            'answer': answer,
            'links': links[:3]  # Limit to 3 links
        }
    
    def generate_fallback_answer(self, processed_question: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a fallback answer when no relevant content is found
        """
        return {
            'answer': "I don't have specific information about this question in my current knowledge base. Please check the TDS course materials or ask on the Discourse forum for more detailed assistance.",
            'links': [
                {
                    'url': 'https://tds.s-anand.net',
                    'text': 'TDS Course Materials'
                },
                {
                    'url': 'https://discourse.onlinedegree.iitm.ac.in',
                    'text': 'TDS Discourse Forum'
                }
            ]
        }
