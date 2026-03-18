import requests

DATAGOV_BASE = "https://data.gov.il/api/3/action"
CBS_BASE = "https://api.cbs.gov.il/index/time-series/search"


def get_recent_packages(limit=50):
    """Return a list of the most recently modified datasets from data.gov.il."""
    url = f"{DATAGOV_BASE}/package_search"
    params = {
        "rows": limit,
        "sort": "metadata_modified desc",
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    results = resp.json().get("result", {}).get("results", [])
    return results


def get_package_details(package_id):
    """Return full metadata for a single dataset."""
    url = f"{DATAGOV_BASE}/package_show"
    resp = requests.get(url, params={"id": package_id}, timeout=15)
    resp.raise_for_status()
    return resp.json().get("result", {})


def get_cbs_recent(limit=20):
    """Return recently updated time-series from the CBS (הלמ״ס) API."""
    params = {
        "lang": "he",
        "skip": 0,
        "take": limit,
        "orderBy": "lastUpdate",
    }
    try:
        resp = requests.get(CBS_BASE, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json().get("data", [])
    except Exception:
        return []
