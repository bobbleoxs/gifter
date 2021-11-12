"""Streamlit app for displaying the Gifter frontend application."""
from __future__ import annotations

import json
from itertools import chain
from pathlib import Path

import streamlit as st
from num2words import num2words


@st.cache
def load_data(root: Path) -> dict:
    """Load data from local directory."""
    with open(root / "data" / "processed" / "data.json", encoding="utf-8") as filepath:
        return json.load(filepath)


def unique_ordered_list(list_of_lists: list[list]) -> set:
    """Flatten & unique-ify."""
    unique_items = set(chain(*list_of_lists))
    return sorted(list(unique_items))


def get_unavailable_products(home, destination):
    """Extract brands that are in `home` but not available in `destination`."""
    return sorted(
        (
            brand
            for brand in data
            if (
                home in brand["countries"]
                and destination not in brand["countries"]
                and "Global brands" not in brand["countries"]
            )
        ),
        key=lambda d: d["title"],
    )


if __name__ == "__main__":
    data = load_data(Path("."))
    countries = unique_ordered_list([brand["countries"] for brand in data])

    st.title("🎁  Gifter 🌻")
    option_home = st.selectbox(label="Home Country", options=countries, index=0)
    option_recipient = st.selectbox(label="Recipient Country", options=countries, index=1)
    if option_home == option_recipient:
        st.write("⚠️  Don't be selfish, you can't gift to yourself!")

    else:

        gifts = get_unavailable_products(home=option_home, destination=option_recipient)
        total = num2words(len(gifts)).replace("-", " ").title()

        st.subheader(f"💙  {total} brands found 💙")
        st.write(
            f"The following brands are available in **{option_home}**"
            f" but not in **{option_recipient}**.",
        )

        n_cols = 3

        indexes = list(range(len(gifts)))
        index_groups = [indexes[i : i + n_cols] for i in range(0, len(indexes), n_cols)]
        for group in index_groups:
            with st.container():
                cols = st.columns(n_cols)
                for index in group:
                    gift = gifts[index]
                    markdown = f"""
                        ### {gift['title']}
                        <img src="https://www.unilever.com/{gift['image']}" width="160"/>
                        <br/><br/>
                        {gift['summary']}
                        <br/><br/>
                    """
                    cols[index % n_cols].markdown(markdown, unsafe_allow_html=True)

        st.balloons()
