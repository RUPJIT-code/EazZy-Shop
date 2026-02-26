"""
debug_scraper.py  -  Run this to diagnose scraping issues
Usage: python debug_scraper.py <url>
Example: python debug_scraper.py "https://dl.flipkart.com/s/2kmUe8NNNN"
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from scraper import (
    SCRAPER_API_KEY, _is_short, resolve_url,
    _scraperapi_html, _scraperapi_structured,
    _direct_fetch, _blocked, _json_ld, _og,
    _price, _extract_price_from_scripts, _extract_image_from_scripts
)
from bs4 import BeautifulSoup

def debug(url):
    print(f"\n{'='*65}")
    print(f"DEBUG SCRAPER")
    print(f"{'='*65}")
    print(f"Input URL : {url}")
    print(f"ScraperAPI: {'SET ✅  key=' + SCRAPER_API_KEY[:8] + '...' if SCRAPER_API_KEY else 'MISSING ❌'}")
    print(f"Is short  : {_is_short(url)}")

    # Step 1: Resolve
    print(f"\n--- STEP 1: Resolve URL ---")
    resolved = resolve_url(url)
    print(f"Resolved  : {resolved}")

    # Step 2: Fetch with ScraperAPI
    print(f"\n--- STEP 2: ScraperAPI HTML fetch ---")
    resp = _scraperapi_html(resolved, render=False, timeout=40)
    if resp:
        print(f"Status    : {resp.status_code}")
        print(f"Size      : {len(resp.content)} bytes")
        print(f"Blocked?  : {_blocked(resp.text)}")

        soup = BeautifulSoup(resp.text, "html.parser")
        ld_t, ld_p, ld_i = _json_ld(soup)
        og_t, og_p, og_i = _og(soup)
        sp = _extract_price_from_scripts(resp.text)
        si = _extract_image_from_scripts(resp.text)

        print(f"\n  JSON-LD  title : {ld_t}")
        print(f"  JSON-LD  price : {ld_p}")
        print(f"  JSON-LD  image : {ld_i}")
        print(f"  OG       title : {og_t}")
        print(f"  OG       price : {og_p}")
        print(f"  OG       image : {og_i}")
        print(f"  Script   price : {sp}")
        print(f"  Script   image : {si}")

        # Show first 2000 chars of HTML for inspection
        print(f"\n--- HTML PREVIEW (first 2000 chars) ---")
        print(resp.text[:2000])
    else:
        print("ScraperAPI HTML fetch FAILED")

    # Step 3: Structured endpoint (Amazon only)
    if "amazon" in resolved.lower():
        print(f"\n--- STEP 3: ScraperAPI Structured (Amazon) ---")
        struct = _scraperapi_structured(resolved, timeout=40)
        if struct:
            import json
            print(json.dumps(struct, indent=2)[:1000])
        else:
            print("Structured endpoint returned nothing")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else input("Enter URL: ").strip()
    debug(url)
