import dns.resolver
import whois

from modules.utils import get_hibp_api_key, safe_request


def resolve_dns(domain: str):
    domain = domain.strip().lower()
    results = {
        "domain": domain,
        "A": [],
        "AAAA": [],
        "MX": [],
        "NS": [],
        "TXT": []
    }

    try:
        results["A"] = [str(r) for r in dns.resolver.resolve(domain, "A")]
    except Exception:
        pass

    try:
        results["AAAA"] = [str(r) for r in dns.resolver.resolve(domain, "AAAA")]
    except Exception:
        pass

    try:
        results["MX"] = [str(r.exchange) for r in dns.resolver.resolve(domain, "MX")]
    except Exception:
        pass

    try:
        results["NS"] = [str(r) for r in dns.resolver.resolve(domain, "NS")]
    except Exception:
        pass

    try:
        results["TXT"] = [str(r) for r in dns.resolver.resolve(domain, "TXT")]
    except Exception:
        pass

    return results


def whois_lookup(domain: str):
    try:
        data = whois.query(domain)
        return {
            "domain_name": data.domain_name,
            "registrar": getattr(data, "registrar", None),
            "creation_date": str(getattr(data, "creation_date", None)),
            "expiration_date": str(getattr(data, "expiration_date", None)),
            "last_updated": str(getattr(data, "last_updated", None)),
            "name_servers": list(getattr(data, "name_servers", [])),
            "status": getattr(data, "status", None)
        }
    except Exception as exc:
        return {"error": f"WHOIS lookup failed: {exc}"}


def check_email_breach(email: str, timeout: int = 10):
    email = (email or "").strip()
    if not email:
        raise ValueError("Email is required.")

    api_key = get_hibp_api_key()
    if not api_key:
        return {
            "status": "disabled",
            "message": "HIBP API key is not configured. Set HIBP_API_KEY in environment variables."
        }

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "hibp-api-key": api_key,
        "User-Agent": "OSINT-Tool/1.0"
    }

    try:
        response = safe_request(url, timeout=timeout, headers=headers)
        if response.status_code == 404:
            return {
                "status": "not_found",
                "message": "No public breach record found for this email.",
                "breaches": []
            }

        if response.status_code == 200:
            breaches = response.json()
            return {
                "status": "breached",
                "message": "Public breaches found.",
                "breaches": breaches
            }

        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text[:500]
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc)
        }
