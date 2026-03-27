"""Developed by Senior Engineer @multilogin-automation

Multilogin X Local API + Playwright sample integration.
"""

import os
import requests
import time
from playwright.sync_api import sync_playwright

MLX_BASE = "http://127.0.0.1:35000"


def create_profile(name):
    payload = {
        "name": name,
        "os": "win",
        "browser": "chromium",
        "options": {
            "navigator": {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            "proxy": {"mode": "direct"}
        }
    }
    r = requests.post(f"{MLX_BASE}/profile", json=payload)
    r.raise_for_status()
    return r.json()["id"]


def launch_profile(profile_id):
    r = requests.post(f"{MLX_BASE}/profile/{profile_id}/launch")
    r.raise_for_status()
    return r.json()["wsEndpoint"]


def close_profile(profile_id):
    requests.post(f"{MLX_BASE}/profile/{profile_id}/stop")


def main():
    print("[Multilogin X] Starting migration-friendly multi-login example")
    profile_name = "SessionBox-Bridge-Profile"

    profile_id = create_profile(profile_name)
    print(f"Created profile {profile_id} (legacy-session safety)")

    ws_endpoint = launch_profile(profile_id)
    print(f"Profile launched with WebSocket endpoint {ws_endpoint}")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_endpoint)
        page = browser.new_page()
        page.goto("https://example.com")
        print("Page title:", page.title())
        page.screenshot(path="example_ml_test.png")
        browser.close()

    close_profile(profile_id)
    print("Profile stopped and context cleaned, ready for 24/7 high reliability")


if __name__ == "__main__":
    main()