# Kigali Business Directory — Bulk Flowcode Generator

**Flowcode International Innovation Fellowship Rwanda 2026**
Tabitha Aluel | Mondiant Initiative × Flowcode

---

## What This Is

A Python application that takes a list of Kigali businesses and automatically generates a branded Flowcode (QR code) for each one in bulk using the Flowcode Enterprise API.

Built as the API Innovation Project for Weeks 3–4 of the fellowship. It demonstrates programmatic asset creation at scale using the `AddCodesToBatch` endpoint — the same capability used by Fortune 500 companies to deploy thousands of codes across physical locations.

---

## The Rwanda Context

Most small businesses in Kigali — market stalls, cafes, tour operators, cooperatives — have no digital presence that customers can reach from a physical touchpoint. A Flowcode on a stall, counter, or poster changes that instantly. This tool lets anyone generate codes for an entire directory of businesses in one run, ready to print and deploy.

---

## What It Does

1. Reads a CSV of businesses (name, category, URL or WhatsApp link)
2. Authenticates with the Flowcode API
3. Creates a Flow using the Scan-to-URL template
4. Bulk-adds all businesses as individual Flowcodes via `AddCodesToBatch`
5. Downloads a QR image for each business
6. Saves a summary CSV mapping every business to its short URL and QR file

---

## Project Structure

```
kigali_directory/
├── main.py              # Main pipeline — run this
├── auth.py              # Bearer token authentication
├── flowcode_api.py      # All Flowcode API calls
├── generator.py         # QR image downloader
├── businesses.csv       # Sample input: 15 Kigali businesses
├── config.example.py    # Credentials template (copy to config.py)
├── requirements.txt     # Python dependencies
└── output/              # Generated QR images + summary.csv (created on run)
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Tabitha2005/Flowcode-Project.git
cd Flowcode-Project
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your credentials**
```bash
cp config.example.py config.py
```
Then open `config.py` and fill in your `CLIENT_ID`, `CLIENT_SECRET`, `ORG_ID`, and `WORKSPACE_ID` from the Flowcode platform.

---

## Usage

**Demo mode** (no credentials needed — great for testing):
```bash
python main.py --demo
```

**Live mode** (requires real credentials in config.py):
```bash
python main.py
```

**Use your own business list:**
```bash
python main.py --input my_businesses.csv
python main.py --input my_businesses.csv --demo
```

---

## Input CSV Format

```csv
name,category,url
Inzora Rooftop Cafe,Restaurant,https://wa.me/250788000001
Kimironko Market Crafts,Market,https://wa.me/250788000002
Kigali Serena Hotel,Hospitality,https://www.serenahotels.com/kigali
```

| Column | Required | Description |
|--------|----------|-------------|
| name | Yes | Business name (used as code name and filename) |
| category | Yes | Sector (Restaurant, Market, Tourism, etc.) |
| url | Yes | Destination URL or WhatsApp link |

---

## Output

After running, the `output/` folder contains:

- One `.png` QR code image per business
- `summary.csv` — full mapping of business name, category, URL, Flowcode short URL, code ID, and image file path

---

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `POST /identity/resources/auth/v1/api-token` | Get bearer token |
| `POST /brands.v1.BrandsService/GetDefaultBrandKit` | Get brand kit ID |
| `POST /links.v1.LinksService/ListDomains` | Get active domain |
| `POST /bundles.v1.BundleService/CreateSuite` | Create a Flow from template |
| `POST /codes.v3.CodeService/AddCodesToBatch` | Bulk create Flowcodes |
| `GET /flowcode-generator/v1/flowcode` | Download QR images |

---

## Fellowship Context

This project was built during Weeks 3–4 of the Flowcode International Innovation Fellowship Rwanda 2026, a partnership between [Flowcode](https://www.flowcode.com) and the [Mondiant Initiative](https://mondiantinitiative.org).

The fellowship places four Computer Science fellows in Kigali to find product-market fit for Flowcode in Rwanda and the wider East African region.
