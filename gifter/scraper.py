"""Scrape Unilever brand info from https://www.unilever.com/brands/view-all-brands/."""


from __future__ import annotations

import json
from pathlib import Path

import requests
from loguru import logger

ROOT = Path(".")


def parse_country(name):
    """Turns "South Africa (Hellmann's)" into "South Africa"."""
    return name.split(" (")[0]


def main():
    """Run the script."""
    # Get the data
    session = requests.Session()
    i = 1
    data_list = []
    while True:
        url = f"https://www.unilever.com/brands/view-all-brands/index.json?page={i}"
        logger.info(f"Querying page {i} (URL {url})")
        response = session.get(url)

        # Stop if bad response
        if not response.ok:
            break
        items = response.json()["listing"]["items"]
        # Stop if no items returned
        if not items:
            break
        data_list += items
        i += 1

    # Process the data
    data = []
    for item in data_list:
        data.append(
            {
                "title": item["title"],
                "summary": item["summary"],
                "image": item["image"],
                "countries": list(
                    {parse_country(country["text"]) for country in item["countries"]},
                ),
            },
        )

    # Save to ./data/processed/data.json
    with open(ROOT / "data" / "processed" / "data.json", "w", encoding="utf-8") as filepath:
        json.dump(data, filepath)


if __name__ == "__main__":
    main()
