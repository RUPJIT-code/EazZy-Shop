# EazZy Shop – Setup & Scraping Guide

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Open: http://localhost:5000

---

## Why Scraping Sometimes Fails

Amazon and Flipkart actively block automated scrapers using:
- Cloudflare bot-protection
- Device fingerprinting
- CAPTCHA challenges

This app uses **three scraping strategies**, tried in order:

| # | Strategy | Notes |
|---|----------|-------|
| 1 | `cloudscraper` | Bypasses Cloudflare; free; works ~60-70% of the time |
| 2 | `requests` with realistic headers | Works when sites don't fingerprint |
| 3 | ScraperAPI proxy | ~99% success rate; free tier = 5,000 req/month |

---

## Get a Free ScraperAPI Key (Recommended)

1. Sign up at **https://www.scraperapi.com/** (no credit card needed)
2. Copy your API key
3. Set it before running the server:

**Linux / Mac:**
```bash
export SCRAPER_API_KEY=your_key_here
python app.py
```

**Windows CMD:**
```cmd
set SCRAPER_API_KEY=your_key_here
python app.py
```

**Windows PowerShell:**
```powershell
$env:SCRAPER_API_KEY="your_key_here"
python app.py
```

---

## Project Structure

```
EazZy Shop/
├── app.py              ← Flask backend (run this)
├── scraper.py          ← All scraping logic (Amazon + Flipkart)
├── requirements.txt    ← Python dependencies
├── data.csv            ← Product dataset for trending/budget features
├── users.csv           ← User accounts (auto-created)
├── README.md           ← This file
└── static/
    ├── login.html      ← Login / signup page
    └── index.html      ← Main app
```

---

## Supported URL Formats

| Platform | Supported Formats |
|----------|------------------|
| Amazon   | `amazon.in/dp/ASIN`, `amazon.in/product-name/dp/ASIN`, `amzn.in/...`, `amzn.to/...` |
| Flipkart | `flipkart.com/.../p/...`, `fkrt.cc/...`, `fkrt.it/...`, `dl.flipkart.com/...` |

Short links (amzn.in, fkrt.cc, etc.) are automatically resolved.

---

## Troubleshooting

**"Could not extract product details"**
→ The site blocked the scraper. Set a `SCRAPER_API_KEY` to fix this.

**"Please paste an Amazon.in or Flipkart product link"**
→ Make sure the URL contains `amazon.in` or `flipkart.com` (Indian sites only).

**Short link doesn't resolve**
→ Try copying the full product URL from the browser address bar instead.

**Price shows as null**
→ The product page loaded but price wasn't found (common on out-of-stock items).
