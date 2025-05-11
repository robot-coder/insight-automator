# main.py

import asyncio
import logging
from typing import Any, Dict, List, Optional

from llama_index import GPTIndex, ServiceContext, LLMPredictor
from tools import generate_research_topics, analyze_data, create_presentation, narrate_report
from mcp_integration import MCPClient
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchAgent:
    """
    An agent-based system to perform automated research report generation,
    including data collection, analysis, presentation creation, and narration.
    """

    def __init__(self, mcp_server_url: str):
        """
        Initialize the ResearchAgent with MCP server URL.
        """
        self.mcp_client = MCPClient(mcp_server_url)
        self.service_context = self._create_service_context()

    def _create_service_context(self) -> ServiceContext:
        """
        Create and return a ServiceContext for llama_index.
        """
        try:
            predictor = LLMPredictor()
            return ServiceContext.from_defaults(llm_predictor=predictor)
        except Exception as e:
            logger.error(f"Error creating service context: {e}")
            raise

    def fetch_web_data(self, url: str) -> str:
        """
        Fetch web page content from the given URL.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()
            logger.info(f"Fetched data from {url}")
            return text_content
        except requests.RequestException as e:
            logger.error(f"Error fetching data from {url}: {e}")
            return ""

    def generate_research_report(self, topic: str) -> Dict[str, Any]:
        """
        Perform research on the given topic and generate a report.
        """
        try:
            # Step 1: Generate research subtopics
            subtopics = generate_research_topics(topic)
            logger.info(f"Generated subtopics: {subtopics}")

            # Step 2: Collect data for each subtopic
            data_frames = []
            for subtopic in subtopics:
                url = f"https://en.wikipedia.org/wiki/{subtopic.replace(' ', '_')}"
                page_content = self.fetch_web_data(url)
                df = analyze_data(page_content)
                data_frames.append(df)

            # Step 3: Combine data
            combined_data = pd.concat(data_frames, ignore_index=True)

            # Step 4: Generate visualizations
            fig = plt.figure()
            combined_data['value'].plot(kind='bar')
            plt.title(f"Data Analysis for {topic}")
            plt.savefig("analysis_plot.png")
            plt.close()

            # Step 5: Create presentation
            presentation_path = create_presentation(topic, "analysis_plot.png")

            # Step 6: Generate narration
            narration = narrate_report(topic, combined_data)

            # Step 7: Compile report
            report = {
                "topic": topic,
                "subtopics": subtopics,
                "data": combined_data,
                "visualization": "analysis_plot.png",
                "presentation": presentation_path,
                "narration": narration
            }
            return report
        except Exception as e:
            logger.error(f"Error generating report for {topic}: {e}")
            return {}

    def run(self, main_topic: str):
        """
        Main execution method to generate report and interact with MCP server.
        """
        try:
            report = self.generate_research_report(main_topic)
            # Send report to MCP server for further processing or storage
            self.mcp_client.send_report(report)
            logger.info("Report successfully sent to MCP server.")
        except Exception as e:
            logger.error(f"Error running agent: {e}")

async def main():
    """
    Entry point for asynchronous execution.
    """
    agent = ResearchAgent(mcp_server_url="http://localhost:8000")
    main_topic = "Artificial Intelligence in Healthcare"
    agent.run(main_topic)

if __name__ == "__main__":
    asyncio.run(main())