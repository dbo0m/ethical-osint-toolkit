from urllib.parse import quote

from modules.utils import load_config, safe_request


def evaluate_presence(platform: dict, status_code: int, payload) -> str:
    if status_code in platform.get("valid_statuses", [200]):
        if isinstance(payload, list) and len(payload) == 0:
            return "not_found"
        if isinstance(payload, dict):
            if payload.get("message") in ("Not Found", "not found", "Not Found 404"):
                return "not_found"
            if payload.get("error") == "Not Found":
                return "not_found"
        return "found"

    if status_code == 404:
        return "not_found"

    if status_code in (403, 429):
        return "blocked"

    return "unknown"


def check_username(username: str, timeout: int = 10):
    username = (username or "").strip()
    if not username:
        raise ValueError("Username is required.")

    config = load_config()
    platforms = config.get("social_platforms", [])

    results = []

    for platform in platforms:
        url = platform["pattern"].format(username=quote(username))
        try:
            response = safe_request(url, timeout=timeout)
            content_type = response.headers.get("Content-Type", "").lower()

            if "application/json" in content_type:
                payload = response.json()
            else:
                payload = response.text

            status = evaluate_presence(platform, response.status_code, payload)
            results.append({
                "platform": platform["name"],
                "url": url,
                "status_code": response.status_code,
                "result": status
            })
        except Exception as exc:
            results.append({
                "platform": platform["name"],
                "url": url,
                "status_code": "error",
                "result": "error",
                "error": str(exc)
            })

    return results
