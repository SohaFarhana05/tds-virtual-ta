#!/usr/bin/env python3
"""
Complete scraper script that combines both discourse and course content scraping.
This is the bonus script that can scrape Discourse posts across a date range.
"""

import argparse
from datetime import datetime
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.discourse_scraper import DiscoursePostsScraper
from scraper.course_scraper import TDSCourseScraper


def main():
    parser = argparse.ArgumentParser(description="Scrape TDS Discourse posts and course content")
    parser.add_argument(
        '--start-date', 
        default='2025-01-01',
        help='Start date for scraping (YYYY-MM-DD format, default: 2025-01-01)'
    )
    parser.add_argument(
        '--end-date',
        default='2025-04-14', 
        help='End date for scraping (YYYY-MM-DD format, default: 2025-04-14)'
    )
    parser.add_argument(
        '--discourse-only',
        action='store_true',
        help='Only scrape Discourse posts'
    )
    parser.add_argument(
        '--course-only',
        action='store_true',
        help='Only scrape course content'
    )
    
    args = parser.parse_args()
    
    # Validate dates
    try:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
        
        if start_date >= end_date:
            print("❌ Start date must be before end date")
            return 1
            
    except ValueError as e:
        print(f"❌ Invalid date format: {e}")
        print("Please use YYYY-MM-DD format")
        return 1
    
    print("🕷️  TDS Data Scraper")
    print("===================")
    print(f"📅 Date range: {args.start_date} to {args.end_date}")
    
    success = True
    
    # Scrape Discourse posts
    if not args.course_only:
        print("\n📰 Scraping Discourse posts...")
        try:
            discourse_scraper = DiscoursePostsScraper()
            topics = discourse_scraper.scrape_tds_topics(args.start_date, args.end_date)
            discourse_scraper.save_data(topics)
            print(f"✅ Scraped {len(topics)} Discourse topics")
        except Exception as e:
            print(f"❌ Error scraping Discourse: {e}")
            success = False
    
    # Scrape course content
    if not args.discourse_only:
        print("\n📚 Scraping course content...")
        try:
            course_scraper = TDSCourseScraper()
            content = course_scraper.scrape_course_content()
            course_scraper.save_data(content)
            print(f"✅ Scraped {len(content)} course content sections")
        except Exception as e:
            print(f"❌ Error scraping course content: {e}")
            success = False
    
    if success:
        print("\n🎉 Scraping completed successfully!")
        print("📁 Data saved to data/ directory")
        return 0
    else:
        print("\n⚠️  Scraping completed with some errors")
        return 1


if __name__ == "__main__":
    exit(main())
