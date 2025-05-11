# tools.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_web_page(url: str, headers: Optional[Dict[str, str]] = None) -> Optional[str]:
    """
    Fetches the content of a web page.
    
    Args:
        url (str): The URL of the web page to fetch.
        headers (Optional[Dict[str, str]]): Optional HTTP headers.
        
    Returns:
        Optional[str]: The HTML content of the page if successful, None otherwise.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info(f"Successfully fetched URL: {url}")
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return None

def parse_html_for_data(html_content: str, parser: str = 'html.parser') -> Optional[BeautifulSoup]:
    """
    Parses HTML content using BeautifulSoup.
    
    Args:
        html_content (str): The HTML content to parse.
        parser (str): The parser to use (default is 'html.parser').
        
    Returns:
        Optional[BeautifulSoup]: Parsed BeautifulSoup object if successful, None otherwise.
    """
    try:
        soup = BeautifulSoup(html_content, parser)
        logger.info("HTML content parsed successfully.")
        return soup
    except Exception as e:
        logger.error(f"Error parsing HTML content: {e}")
        return None

def extract_data_from_html(soup: BeautifulSoup, selector: str) -> List[str]:
    """
    Extracts data from HTML using a CSS selector.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content.
        selector (str): CSS selector string.
        
    Returns:
        List[str]: List of extracted text data.
    """
    try:
        elements = soup.select(selector)
        data = [element.get_text(strip=True) for element in elements]
        logger.info(f"Extracted {len(data)} elements using selector '{selector}'.")
        return data
    except Exception as e:
        logger.error(f"Error extracting data with selector '{selector}': {e}")
        return []

def fetch_and_parse(url: str, selector: str, headers: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Fetches a web page and extracts data based on a CSS selector.
    
    Args:
        url (str): URL of the web page.
        selector (str): CSS selector for data extraction.
        headers (Optional[Dict[str, str]]): Optional HTTP headers.
        
    Returns:
        List[str]: Extracted data list.
    """
    html = fetch_web_page(url, headers)
    if html:
        soup = parse_html_for_data(html)
        if soup:
            return extract_data_from_html(soup, selector)
    return []

def generate_plot(data: List[float], title: str = "Data Plot") -> Optional[str]:
    """
    Generates a bar plot from numerical data.
    
    Args:
        data (List[float]): List of numerical values.
        title (str): Title of the plot.
        
    Returns:
        Optional[str]: Path to saved plot image if successful, None otherwise.
    """
    try:
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(data)), data)
        plt.title(title)
        plt.xlabel("Index")
        plt.ylabel("Value")
        image_path = "output_plot.png"
        plt.savefig(image_path)
        plt.close()
        logger.info(f"Plot saved to {image_path}")
        return image_path
    except Exception as e:
        logger.error(f"Error generating plot: {e}")
        return None

def create_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Creates a pandas DataFrame from a list of dictionaries.
    
    Args:
        data (List[Dict[str, Any]]): List of data records.
        
    Returns:
        pd.DataFrame: The resulting DataFrame.
    """
    try:
        df = pd.DataFrame(data)
        logger.info("DataFrame created successfully.")
        return df
    except Exception as e:
        logger.error(f"Error creating DataFrame: {e}")
        return pd.DataFrame()

def generate_report(df: pd.DataFrame, report_title: str = "Research Report") -> str:
    """
    Generates a simple textual report from a DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame containing report data.
        report_title (str): Title of the report.
        
    Returns:
        str: The report as a string.
    """
    try:
        report = f"{report_title}\n\n"
        report += df.describe().to_string()
        logger.info("Report generated successfully.")
        return report
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return "Failed to generate report."

def save_text_report(report: str, filename: str = "research_report.txt") -> bool:
    """
    Saves a text report to a file.
    
    Args:
        report (str): The report content.
        filename (str): The filename to save the report.
        
    Returns:
        bool: True if saved successfully, False otherwise.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"Report saved to {filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving report to {filename}: {e}")
        return False

def generate_presentation(slides: List[Dict[str, str]], filename: str = "presentation.pptx") -> bool:
    """
    Placeholder function for generating a presentation.
    (Implementation would use a library like python-pptx)
    
    Args:
        slides (List[Dict[str, str]]): List of slides with title and content.
        filename (str): Output filename.
        
    Returns:
        bool: True if presentation is created successfully.
    """
    # Placeholder implementation
    try:
        # Implementation would go here
        logger.info(f"Generated presentation with {len(slides)} slides.")
        return True
    except Exception as e:
        logger.error(f"Error generating presentation: {e}")
        return False

def narrate_text(text: str) -> bool:
    """
    Placeholder function for narration.
    (Implementation would interface with TTS services)
    
    Args:
        text (str): Text to narrate.
        
    Returns:
        bool: True if narration succeeded.
    """
    # Placeholder implementation
    try:
        # Implementation would go here
        logger.info("Narration completed.")
        return True
    except Exception as e:
        logger.error(f"Error during narration: {e}")
        return False