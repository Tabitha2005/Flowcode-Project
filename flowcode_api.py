import requests
from config import API_BASE, ORG_ID, WORKSPACE_ID, SCAN_TO_URL_BUNDLE_ID


def _headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def get_default_brand_kit(token):
    response = requests.post(
        f"{API_BASE}/brands.v1.BrandsService/GetDefaultBrandKit",
        headers=_headers(token),
        json={"orgId": ORG_ID, "workspaceId": WORKSPACE_ID},
    )
    response.raise_for_status()
    return response.json()["brandKit"]["id"]


def list_domains(token):
    response = requests.post(
        f"{API_BASE}/links.v1.LinksService/ListDomains",
        headers=_headers(token),
        json={"orgId": ORG_ID, "workspaceId": WORKSPACE_ID},
    )
    response.raise_for_status()
    items = response.json().get("items", [])
    # Return first active domain, or None to use default
    for item in items:
        if item.get("status") == "DOMAIN_STATUS_ACTIVE":
            return item["id"]
    return None


def create_suite(token, brand_kit_id, domain_id, flow_name):
    payload = {
        "orgId": ORG_ID,
        "workspaceId": WORKSPACE_ID,
        "bundleId": SCAN_TO_URL_BUNDLE_ID,
        "brandKitId": brand_kit_id,
        "name": flow_name,
        "state": "ASSET_STATE_ACTIVE",
        "config": {
            "code_batch-1": {
                "metadata": {"url": "https://mondiantinitiative.org"},
                "metadataSchema": "{\"type\":\"object\",\"properties\":{\"url\":{\"type\":\"string\",\"title\":\"Destination URL\",\"description\":\"\"},\"businessName\":{\"type\":\"string\",\"title\":\"Business Name\",\"description\":\"\"},\"category\":{\"type\":\"string\",\"title\":\"Category\",\"description\":\"\"}},\"required\":[]}",
                "position": {},
            },
            "external_destination-1": {
                "appendUtmParameters": True,
                "url": "{{ .request.url }}",
                "type": "EXTERNAL_DESTINATION_TYPE_URL",
            },
        },
    }
    if domain_id:
        payload["domain"] = domain_id

    response = requests.post(
        f"{API_BASE}/bundles.v1.BundleService/CreateSuite",
        headers=_headers(token),
        json=payload,
    )
    response.raise_for_status()
    suite = response.json()["suite"]
    suite_id = suite["id"]
    batch_id = suite["assets"]["code_batch-1"]["assetId"]
    return suite_id, batch_id


def bulk_add_codes(token, batch_id, businesses):
    """
    businesses: list of dicts with keys: name, category, url
    Returns list of code objects from the API
    """
    requests_payload = [
        {
            "name": b["name"],
            "metadata": {
                "url": b["url"],
                "businessName": b["name"],
                "category": b["category"],
            },
        }
        for b in businesses
    ]

    response = requests.post(
        f"{API_BASE}/codes.v3.CodeService/AddCodesToBatch",
        headers=_headers(token),
        json={
            "orgId": ORG_ID,
            "workspaceId": WORKSPACE_ID,
            "batchId": batch_id,
            "requests": requests_payload,
        },
    )
    response.raise_for_status()
    return response.json().get("codes", [])


# --- Demo mode mocks ---

def demo_get_brand_kit():
    return "DEMO_BRAND_KIT_ID"


def demo_list_domains():
    return "DEMO_DOMAIN_ID"


def demo_create_suite(flow_name):
    return "DEMO_SUITE_ID", "DEMO_BATCH_ID"


def demo_bulk_add_codes(businesses):
    codes = []
    for i, b in enumerate(businesses):
        codes.append({
            "id": f"DEMO_CODE_{i+1}",
            "name": b["name"],
            "shortUrl": f"https://flowsto.com/r/demo{i+1:03d}",
            "codeDesign": {"config": {}},
        })
    return codes
