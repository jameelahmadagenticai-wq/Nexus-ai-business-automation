from agents.tools.web_search import web_search
from agents.tools.send_email import send_email
from agents.tools.query_db import query_db
from agents.tools.scrape_url import scrape_url


TOOL_REGISTRY = {

    "web_search": {
        "function": web_search,
        "description": "Search the web for information",
        "schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string"
                }
            },
            "required": ["query"]
        }
    },

    "send_email": {
        "function": send_email,
        "description": "Send professional emails",
        "schema": {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string"
                },
                "subject": {
                    "type": "string"
                },
                "body": {
                    "type": "string"
                }
            },
            "required": [
                "recipient",
                "subject",
                "body"
            ]
        }
    },

    "query_db": {
        "function": query_db,
        "description": "Query PostgreSQL database",
        "schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string"
                }
            },
            "required": ["query"]
        }
    },

    "scrape_url": {
        "function": scrape_url,
        "description": "Scrape website content",
        "schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string"
                }
            },
            "required": ["url"]
        }
    }
}