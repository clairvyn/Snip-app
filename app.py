import io
from dataclasses import dataclass
from typing import List, Optional

import streamlit as st
from PIL import Image


@dataclass
class SubscriptionItem:
    name: str
    price: float
    period: str  # e.g. "month" or "year"


def dummy_ai_analyze_subscriptions(image: Image.Image, api_key: Optional[str]) -> List[SubscriptionItem]:
    """
    Dummy function (no real AI yet).
    Returns fake subscription data so you can see how the UI will look.
    """
    # Note: api_key is unused here on purpose (dummy mode)
    return [
        SubscriptionItem(name="Spotify", price=10.99, period="month"),
        SubscriptionItem(name="Netflix", price=15.49, period="month"),
        SubscriptionItem(name="iCloud+", price=2.99, period="month"),
        SubscriptionItem(name="Duolingo", price=83.99, period="year"),
    ]


def yearly_cost(item: SubscriptionItem) -> float:
    if item.period.lower().startswith("month"):
        return item.price * 12
    return item.price


def render_upload_and_process():
    st.title("Snip")
    st.write("Upload a screenshot of your phone’s **Subscriptions** page and click **Process**.")

    uploaded = st.file_uploader("Upload a screenshot (PNG or JPG)", type=["png", "jpg", "jpeg"])

    if not uploaded:
        st.info("Add a screenshot to get started.")
        return

    # Read image bytes once
    image_bytes = uploaded.getvalue()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    st.subheader("Preview")
    st.image(image, caption=f"Uploaded: {uploaded.name}", use_container_width=True)

    process = st.button("Process", type="primary")
    if not process:
        return

    with st.spinner("Analyzing (dummy mode)..."):
        items = dummy_ai_analyze_subscriptions(image=image, api_key=st.session_state.get("openai_api_key"))

    st.subheader("Estimated subscriptions (dummy)")

    rows = []
    for it in items:
        rows.append(
            {
                "Name": it.name,
                "Price": f"${it.price:.2f}",
                "Billing": it.period,
                "Estimated yearly cost": f"${yearly_cost(it):.2f}",
            }
        )

    st.table(rows)

    total_yearly = sum(yearly_cost(i) for i in items)
    st.metric("Estimated yearly total", f"${total_yearly:.2f}")
    st.caption("This is dummy data for now. Next step is hooking up real OCR + AI extraction.")


def main():
    st.set_page_config(page_title="Snip", page_icon="✂️", layout="centered")

    st.sidebar.header("Settings")
    st.sidebar.write("Add your OpenAI key here (not used yet in dummy mode).")
    st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        key="openai_api_key",
        placeholder="sk-...",
    )

    render_upload_and_process()


if __name__ == "__main__":
    main()
