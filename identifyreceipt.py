# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 22:27:41 2026

@author: sheng
"""

#!/usr/bin/env python3
"""
Receipt Total Extractor
Uses Claude's vision API to analyze a receipt image and extract the total amount.

Usage:
    python receipt_reader.py <path_to_receipt_image>

Requirements:
    pip install anthropic
    export ANTHROPIC_API_KEY="your-api-key"
"""

import anthropic
import base64
import sys
import os
import re
from pathlib import Path


def load_image_as_base64(image_path: str) -> tuple[str, str]:
    """Load an image file and return base64-encoded data and media type."""
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Determine media type from extension
    ext = path.suffix.lower()
    media_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }

    media_type = media_type_map.get(ext)
    if not media_type:
        raise ValueError(f"Unsupported image format: {ext}. Use JPG, PNG, GIF, or WebP.")

    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    return image_data, media_type


def extract_receipt_total(image_path: str) -> dict:
    """
    Analyze a receipt image and extract the total amount.

    Args:
        image_path: Path to the receipt image file.

    Returns:
        A dict with 'total', 'currency', 'raw_response', and 'confidence'.
    """
    # Load and encode the image
    image_data, media_type = load_image_as_base64(image_path)

    # Initialize the Anthropic client
    # Automatically uses ANTHROPIC_API_KEY environment variable
    client = anthropic.Anthropic()

    # Send the image to Claude for analysis
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "Please analyze this receipt image and extract the total amount due. "
                            "Look for labels like 'Total', 'Grand Total', 'Amount Due', 'Balance Due', or similar. "
                            "Respond in this exact format:\n\n"
                            "TOTAL: <amount>\n"
                            "CURRENCY: <currency symbol or code>\n"
                            "CONFIDENCE: <high/medium/low>\n"
                            "NOTES: <any relevant notes, e.g. if multiple totals found, tax info, etc.>\n\n"
                            "If you cannot find a total amount, respond with TOTAL: NOT_FOUND and explain in NOTES."
                        ),
                    },
                ],
            }
        ],
    )

    raw_response = message.content[0].text

    # Parse the structured response
    result = {
        "total": None,
        "currency": None,
        "confidence": None,
        "notes": None,
        "raw_response": raw_response,
    }

    for line in raw_response.splitlines():
        if line.startswith("TOTAL:"):
            total_str = line.split(":", 1)[1].strip()
            if total_str != "NOT_FOUND":
                # Remove currency symbols and commas for clean numeric value
                result["total"] = re.sub(r"[^\d.,]", "", total_str) or total_str
                result["total_display"] = total_str  # Keep original for display
        elif line.startswith("CURRENCY:"):
            result["currency"] = line.split(":", 1)[1].strip()
        elif line.startswith("CONFIDENCE:"):
            result["confidence"] = line.split(":", 1)[1].strip()
        elif line.startswith("NOTES:"):
            result["notes"] = line.split(":", 1)[1].strip()

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python receipt_reader.py <path_to_receipt_image>")
        print("Example: python receipt_reader.py receipt.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable is not set.")
        print("Set it with: export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)

    print(f"Analyzing receipt: {image_path}")
    print("-" * 40)

    result = extract_receipt_total(image_path)

    # Display results
    if result["total"]:
        display = result.get("total_display", result["total"])
        currency = result["currency"] or ""
        print(f"✅ Total Amount Found: {currency} {display}".strip())
        print(f"   Confidence: {result['confidence'] or 'N/A'}")
    else:
        print("❌ Could not extract total amount from receipt.")

    if result["notes"]:
        print(f"   Notes: {result['notes']}")

    print("-" * 40)
    print("Full response from Claude:")
    print(result["raw_response"])

    return result


if __name__ == "__main__":
    main()