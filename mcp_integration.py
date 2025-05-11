import requests
from typing import Any, Dict, Optional
from mcp_server_sdk import MCPClient, MCPError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPIntegration:
    """
    A class to handle interactions with the MCP server for advanced capabilities such as web automation.
    """

    def __init__(self, server_url: str, api_key: str) -> None:
        """
        Initialize the MCPIntegration instance.

        Args:
            server_url (str): The URL of the MCP server.
            api_key (str): The API key for authentication.
        """
        self.server_url = server_url
        self.api_key = api_key
        self.client: Optional[MCPClient] = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """
        Initialize the MCP client with the server URL and API key.
        """
        try:
            self.client = MCPClient(server_url=self.server_url, api_key=self.api_key)
            logger.info("MCP client initialized successfully.")
        except MCPError as e:
            logger.error(f"Failed to initialize MCP client: {e}")
            self.client = None

    def perform_web_automation(self, url: str, actions: Dict[str, Any]) -> Optional[str]:
        """
        Perform web automation tasks via MCP server.

        Args:
            url (str): The URL to automate.
            actions (Dict[str, Any]): A dictionary describing actions to perform.

        Returns:
            Optional[str]: The result or output from the automation, or None if failed.
        """
        if not self.client:
            logger.error("MCP client is not initialized.")
            return None
        try:
            response = self.client.execute_web_automation(url=url, actions=actions)
            logger.info(f"Web automation performed successfully for {url}.")
            return response.get('result')
        except MCPError as e:
            logger.error(f"Error during web automation: {e}")
            return None

    def fetch_web_content(self, url: str) -> Optional[str]:
        """
        Fetch web page content using MCP server's web automation capabilities.

        Args:
            url (str): The URL of the web page to fetch.

        Returns:
            Optional[str]: The HTML content of the page or None if failed.
        """
        actions = {
            "action": "fetch_page",
            "parameters": {
                "url": url
            }
        }
        return self.perform_web_automation(url, actions)

    def close(self) -> None:
        """
        Close the MCP client connection if necessary.
        """
        if self.client:
            try:
                self.client.close()
                logger.info("MCP client connection closed.")
            except MCPError as e:
                logger.error(f"Error closing MCP client: {e}")