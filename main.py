"""
Kigali Business Directory - Bulk Flowcode Generator
Flowcode International Innovation Fellowship Rwanda 2026
Tabitha Aluel | Mondiant Initiative

Usage:
    python main.py                  # live mode (requires real credentials in config.py)
    python main.py --demo           # demo mode (no credentials needed)
    python main.py --input my.csv   # use a custom CSV file
"""

import argparse
import csv
import os
import sys
from datetime import datetime

import auth
import flowcode_api
import generator


OUTPUT_DIR = "output"
FLOW_NAME = f"Kigali Business Directory - {datetime.now().strftime('%Y-%m-%d')}"


def load_businesses(csv_path):
    businesses = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            category = row.get("category", "").strip()
            url = row.get("url", "").strip()
            if name and url:
                businesses.append({"name": name, "category": category, "url": url})
    return businesses


def save_summary(results, output_dir):
    summary_path = os.path.join(output_dir, "summary.csv")
    with open(summary_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["business_name", "category", "url", "short_url", "code_id", "qr_file"])
        writer.writeheader()
        writer.writerows(results)
    return summary_path


def run_demo(businesses):
    print("\n[DEMO MODE] Running with mock data — no API calls made.\n")

    print("Step 1: Getting brand kit... DEMO_BRAND_KIT_ID")
    print("Step 2: Getting domain...   DEMO_DOMAIN_ID")
    print("Step 3: Creating flow...    DEMO_SUITE_ID")
    print(f"        Batch ID:           DEMO_BATCH_ID")
    print(f"\nStep 4: Adding {len(businesses)} businesses as Flowcodes in bulk...")

    codes = flowcode_api.demo_bulk_add_codes(businesses)

    results = []
    print("\nStep 5: Saving QR placeholders to output/\n")
    for i, (code, business) in enumerate(zip(codes, businesses)):
        qr_file = generator.demo_save_placeholder(business["name"], OUTPUT_DIR)
        results.append({
            "business_name": business["name"],
            "category": business["category"],
            "url": business["url"],
            "short_url": code["shortUrl"],
            "code_id": code["id"],
            "qr_file": qr_file,
        })
        print(f"  [{i+1:02d}] {business['name']:<35} -> {code['shortUrl']}")

    summary_path = save_summary(results, OUTPUT_DIR)
    print(f"\n[OK] Done. {len(results)} codes generated.")
    print(f"[OK] Summary saved to: {summary_path}")
    print("\nWhen you have real API credentials, update config.py and run without --demo.\n")


def run_live(businesses):
    print("\n[LIVE MODE] Connecting to Flowcode API...\n")

    print("Step 1: Authenticating...")
    token, refresh_token = auth.get_bearer_token()
    print("        Bearer token obtained.")

    print("Step 2: Getting default brand kit...")
    brand_kit_id = flowcode_api.get_default_brand_kit(token)
    print(f"        Brand Kit ID: {brand_kit_id}")

    print("Step 3: Getting active domain...")
    domain_id = flowcode_api.list_domains(token)
    print(f"        Domain ID: {domain_id or 'using default'}")

    print(f"Step 4: Creating flow '{FLOW_NAME}'...")
    suite_id, batch_id = flowcode_api.create_suite(token, brand_kit_id, domain_id, FLOW_NAME)
    print(f"        Suite ID: {suite_id}")
    print(f"        Batch ID: {batch_id}")

    print(f"\nStep 5: Adding {len(businesses)} businesses as Flowcodes in bulk...")
    codes = flowcode_api.bulk_add_codes(token, batch_id, businesses)
    print(f"        {len(codes)} codes created.")

    results = []
    print("\nStep 6: Downloading QR code images to output/\n")
    for i, (code, business) in enumerate(zip(codes, businesses)):
        short_url = code.get("shortUrl", "")
        design_config = code.get("codeDesign", {}).get("config", {})
        try:
            qr_file = generator.download_qr_image(short_url, design_config, business["name"], OUTPUT_DIR)
        except Exception as e:
            print(f"  [WARN] Could not download image for {business['name']}: {e}")
            qr_file = "download_failed"

        results.append({
            "business_name": business["name"],
            "category": business["category"],
            "url": business["url"],
            "short_url": short_url,
            "code_id": code.get("id", ""),
            "qr_file": qr_file,
        })
        print(f"  [{i+1:02d}] {business['name']:<35} -> {short_url}")

    summary_path = save_summary(results, OUTPUT_DIR)
    print(f"\n[OK] Done. {len(results)} Flowcodes generated.")
    print(f"[OK] QR images saved to: {OUTPUT_DIR}/")
    print(f"[OK] Summary saved to:   {summary_path}\n")


def main():
    parser = argparse.ArgumentParser(description="Kigali Business Directory - Bulk Flowcode Generator")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode without real API credentials")
    parser.add_argument("--input", default="businesses.csv", help="Path to input CSV file (default: businesses.csv)")
    args = parser.parse_args()

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("=" * 55)
    print("  Kigali Business Directory — Bulk Flowcode Generator")
    print("  Flowcode Fellowship Rwanda 2026 | Tabitha Aluel")
    print("=" * 55)

    if not os.path.exists(args.input):
        print(f"\n[ERROR] Input file not found: {args.input}")
        sys.exit(1)

    businesses = load_businesses(args.input)
    if not businesses:
        print("\n[ERROR] No valid businesses found in the CSV.")
        sys.exit(1)

    print(f"\nLoaded {len(businesses)} businesses from '{args.input}'")

    if args.demo:
        run_demo(businesses)
    else:
        run_live(businesses)


if __name__ == "__main__":
    main()
