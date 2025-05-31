import requests
import json
import os
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import time


class TDSCourseScraper:
    def __init__(self):
        self.base_url = "https://tds.s-anand.net"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TDS-Virtual-TA/1.0'
        })
    
    def scrape_course_content(self) -> List[Dict[str, Any]]:
        """
        Scrape TDS course content from the main site
        """
        content = []
        
        try:
            # Get the main page
            response = self.session.get(self.base_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract main content sections
            main_content = {
                'url': self.base_url,
                'title': 'TDS Course Main Page',
                'content': soup.get_text(strip=True),
                'sections': []
            }
            
            # Look for navigation links or content sections
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href') # type: ignore
                if href and (href.startswith('#') or href.startswith('/')): # type: ignore
                    section_url = urljoin(self.base_url, href)
                    section_content = self.scrape_section(section_url, link.get_text(strip=True))
                    if section_content:
                        main_content['sections'].append(section_content)
            
            content.append(main_content)
            
        except requests.RequestException as e:
            print(f"Error scraping course content: {e}")
        
        return content
    
    def scrape_section(self, url: str, title: str) -> Dict[str, Any]:
        """
        Scrape a specific section of the course
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return {
                'url': url,
                'title': title,
                'content': soup.get_text(strip=True)
            }
            
        except requests.RequestException as e:
            print(f"Error scraping section {url}: {e}")
            return None # type: ignore
    
    def save_data(self, content: List[Dict[str, Any]], filename: str = "course_content.json"):
        """
        Save scraped course content to JSON file
        """
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        print(f"Saved course content to {filepath}")


def main():
    scraper = TDSCourseScraper()
    
    # Scrape course content
    content = scraper.scrape_course_content()
    
    # Save the data
    scraper.save_data(content)
    
    print(f"Course scraping completed. Found {len(content)} content sections.")


if __name__ == "__main__":
    main()
