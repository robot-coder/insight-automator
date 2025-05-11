# README.md

# Automated Research Report Generation System

This project implements an agent-based system utilizing LlamaIndex to perform automated research report generation, including data collection, analysis, visualization, and presentation. The system integrates multiple Python tools and interacts with MCP servers for advanced web automation and data retrieval capabilities.

## Features

- Modular design with dedicated tools for data scraping, processing, and visualization
- Integration with MCP servers for web automation and complex interactions
- Automated generation of research reports with visualizations and narration
- Extensible architecture for adding new tools and capabilities

## Requirements

Ensure you have the following libraries installed:

- llama_index
- mcp_server_sdk
- playwright
- requests
- beautifulsoup4
- matplotlib
- pandas

You can install the required libraries using:

```bash
pip install -r requirements.txt
```

## Files

- `main.py`: Entry point for orchestrating the research report generation process.
- `tools.py`: Contains various utility functions for data collection, processing, and visualization.
- `mcp_integration.py`: Handles interactions with MCP servers for web automation and advanced capabilities.
- `requirements.txt`: Lists all dependencies.

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the main script:

```bash
python main.py
```

## Structure Overview

- `main.py`: Coordinates the overall workflow, invoking tools and MCP interactions.
- `tools.py`: Implements functions such as data scraping, analysis, plotting, and report formatting.
- `mcp_integration.py`: Manages web automation tasks like browsing, data extraction, and interaction with MCP servers.

## Example Workflow

1. Collect data from web sources using MCP automation.
2. Process and analyze data with pandas.
3. Generate visualizations with matplotlib.
4. Compile findings into a report.
5. Use MCP to create presentation slides and narrate the report.

## Error Handling

The system includes error handling to manage network issues, data inconsistencies, and automation failures, ensuring robustness during execution.

## License

This project is for educational and research purposes. Feel free to modify and extend as needed.

---

# main.py

```python
import asyncio
from llama_index import GPTIndex
from tools import collect_data, analyze_data, generate_visualizations, compile_report
from mcp_integration import automate_web_tasks

def main() -> None:
    """
    Main function to orchestrate the automated research report generation.
    """
    try:
        # Step 1: Collect data via MCP automation
        data = asyncio.run(automate_web_tasks())
        if not data:
            print("Data collection failed.")
            return

        # Step 2: Analyze data
        analysis_results = analyze_data(data)

        # Step 3: Generate visualizations
        visualizations = generate_visualizations(analysis_results)

        # Step 4: Compile report
        report_path = compile_report(analysis_results, visualizations)

        # Optional: Use MCP to create presentation and narration
        asyncio.run(automate_web_tasks(presentation=True, report_path=report_path))

        print("Research report generation completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
```

# tools.py

```python
from typing import Any, Dict, List
import pandas as pd
import matplotlib.pyplot as plt
import os

def collect_data() -> pd.DataFrame:
    """
    Placeholder function for data collection.
    Replace with actual data scraping and processing logic.
    """
    # Example: Create dummy data
    data = {
        'Category': ['A', 'B', 'C', 'D'],
        'Values': [23, 45, 12, 37]
    }
    df = pd.DataFrame(data)
    return df

def analyze_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze the collected data.
    """
    analysis = {
        'summary': df.describe().to_dict(),
        'correlations': df.corr().to_dict()
    }
    return analysis

def generate_visualizations(analysis: Dict[str, Any]) -> List[str]:
    """
    Generate visualizations based on analysis.
    Returns list of file paths to saved images.
    """
    image_paths = []

    # Example: Bar plot of Values
    df = pd.DataFrame(analysis['summary'])
    plt.figure()
    df.loc['mean'].plot(kind='bar')
    plt.title('Average Values')
    filename = 'visualization_mean.png'
    plt.savefig(filename)
    image_paths.append(filename)
    plt.close()

    # Additional visualizations can be added here

    return image_paths

def compile_report(analysis: Dict[str, Any], images: List[str]) -> str:
    """
    Compile the analysis and visualizations into a report.
    Returns the path to the generated report.
    """
    report_path = 'research_report.html'
    with open(report_path, 'w') as f:
        f.write('<html><head><title>Research Report</title></head><body>')
        f.write('<h1>Automated Research Report</h1>')
        f.write('<h2>Analysis Summary</h2>')
        f.write('<pre>{}</pre>'.format(analysis))
        f.write('<h2>Visualizations</h2>')
        for img in images:
            f.write(f'<img src="{img}" alt="{img}"><br>')
        f.write('</body></html>')
    return report_path
```

# mcp_integration.py

```python
import asyncio
from typing import Optional, Dict, Any
from mcp_server_sdk import MCPClient
from playwright.async_api import async_playwright

async def automate_web_tasks(presentation: bool = False, report_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Automate web tasks using MCP server and Playwright.
    If presentation is True, create presentation slides and narration.
    """
    try:
        # Initialize MCP client
        async with MCPClient() as mcp:
            # Example: Open a webpage and perform actions
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto('https://example.com')
                # Perform web automation tasks here
                # e.g., scrape data, interact with elements

                # Placeholder: Extract page title
                title = await page.title()

                await browser.close()

            # If presentation is requested, create slides and narration
            if presentation and report_path:
                # Placeholder for creating presentation
                # e.g., generate slides from report and add narration
                pass

            # Return collected data or status
            return {'title': title}

    except Exception as e:
        print(f"Error during MCP automation: {e}")
        return None
```