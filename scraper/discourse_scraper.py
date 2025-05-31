import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()


class DiscoursePostsScraper:
    def __init__(self):
        self.base_url = os.getenv('DISCOURSE_BASE_URL', 'https://discourse.onlinedegree.iitm.ac.in')
        self.api_key = os.getenv('DISCOURSE_API_KEY')
        self.username = os.getenv('DISCOURSE_USERNAME')
        
    def get_headers(self):
        headers = {
            'User-Agent': 'TDS-Virtual-TA/1.0',
            'Accept': 'application/json'
        }
        if self.api_key and self.username:
            headers['Api-Key'] = self.api_key
            headers['Api-Username'] = self.username
        return headers
    
    def scrape_tds_topics(self, start_date: str = "2025-01-01", end_date: str = "2025-04-14") -> List[Dict[str, Any]]:
        """
        Scrape TDS-related topics from Discourse
        """
        topics = []
        page = 0
        
        print(f"Scraping TDS topics from {start_date} to {end_date}")
        
        while True:
            try:
                # Search for TDS-related topics
                search_url = f"{self.base_url}/search.json"
                params = {
                    'q': 'TDS OR "Tools in Data Science" after:{start_date} before:{end_date}',
                    'page': page
                }
                
                response = requests.get(search_url, params=params, headers=self.get_headers())
                response.raise_for_status()
                
                data = response.json()
                
                if not data.get('posts'):
                    break
                
                for post_data in data['posts']:
                    topic_id = post_data.get('topic_id')
                    if topic_id:
                        topic_detail = self.get_topic_detail(topic_id)
                        if topic_detail:
                            topics.append(topic_detail)
                
                page += 1
                time.sleep(1)  # Rate limiting
                
                if page >= 10:  # Limit to avoid too many requests
                    break
                    
            except requests.RequestException as e:
                print(f"Error scraping page {page}: {e}")
                break
        
        return topics
    
    def get_topic_detail(self, topic_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific topic
        """
        try:
            topic_url = f"{self.base_url}/t/{topic_id}.json"
            response = requests.get(topic_url, headers=self.get_headers())
            response.raise_for_status()
            
            topic_data = response.json()
            
            # Extract relevant information
            topic_info = {
                'id': topic_data.get('id'),
                'title': topic_data.get('title'),
                'url': f"{self.base_url}/t/{topic_data.get('slug')}/{topic_data.get('id')}",
                'created_at': topic_data.get('created_at'),
                'posts': []
            }
            
            # Extract posts
            for post in topic_data.get('post_stream', {}).get('posts', []):
                post_info = {
                    'id': post.get('id'),
                    'post_number': post.get('post_number'),
                    'username': post.get('username'),
                    'created_at': post.get('created_at'),
                    'cooked': post.get('cooked'),  # HTML content
                    'raw': self.extract_text_from_html(post.get('cooked', ''))
                }
                topic_info['posts'].append(post_info)
            
            return topic_info
            
        except requests.RequestException as e:
            print(f"Error getting topic {topic_id}: {e}")
            return None
    
    def extract_text_from_html(self, html_content: str) -> str:
        """
        Extract plain text from HTML content
        """
        if not html_content:
            return ""
        
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(strip=True)
    
    def save_data(self, topics: List[Dict[str, Any]], filename: str = "discourse_posts.json"):
        """
        Save scraped data to JSON file
        """
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(topics, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(topics)} topics to {filepath}")


def main():
    scraper = DiscoursePostsScraper()
    
    # Scrape TDS topics from Jan 1, 2025 to Apr 14, 2025
    topics = scraper.scrape_tds_topics("2025-01-01", "2025-04-14")
    
    # Save the data
    scraper.save_data(topics)
    
    print(f"Scraping completed. Found {len(topics)} topics.")


if __name__ == "__main__":
    main()
