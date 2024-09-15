import gpt.tools as tools

FUNCTIONS_MAP = {
    "wikipedia_search_tool": tools.wikipedia_search_tool,
    "duckduckgo_search_tool": tools.duckduckgo_search_tool,
    "website_scraping_tool": tools.website_scraping_tool,
}

FUNCTIONS = [
    {
        "type": "function",
        "function": {
            "name": "wikipedia_search_tool",
            "description": """
                Use this tool to do your research.
                It takes a query as an argument and returns the search results.
                """,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query is the topic you want to find in Wikipedia.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "duckduckgo_search_tool",
            "description": """
                Use this tool to do your research.
                It takes a query as an argument and returns the search results.
                """,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query is the topic you want to find in DuckDuckGo.",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "website_scraping_tool",
            "description": """
                Visit websites and extract their content with this tool.
                It takes a url as an argument and returns the content.
                """,
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the website you want to scrape.",
                    },
                },
                "required": ["url"],
            },
        },
    },
]