import json
import os
from pathlib import Path
from typing import Any, Dict

import requests


def load_config() -> Dict[str, Any]:
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / "config.json"
    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def safe_request(url: str, timeout: int = 10, headers: Dict[str, str] | None = None):
    config = load_config()
    default_headers = {
        "User-Agent": config.get("user_agent", "OSINT-Tool/1.0"),
        "Accept": "application/json, text/plain, */*"
    }
    if headers:
        default_headers.update(headers)

    try:
        response = requests.get(
            url,
            headers=default_headers,
            timeout=timeout,
            allow_redirects=True
        )
        return response
    except requests.exceptions.Timeout:
        raise TimeoutError(f"Connection timed out for URL: {url}")
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Request failed for URL: {url}: {exc}")


def get_hibp_api_key() -> str:
    config = load_config()
    env_name = config.get("hibp_api_key_env", "HIBP_API_KEY")
    return os.getenv(env_name, "").strip()
