"""
Snip - Subscription Audit Tool
Phase 2: THE BRAIN (Real AI Vision Extraction)

This version uses OpenAI GPT-4 Vision to read real subscription screenshots
and extract service names, prices, and billing periods.
"""

import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import json

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Snip - Subscription Audit",
    page_icon="✂️",
    layout="centered"
)

# ============================================================================
# SIDEBAR (API KEY INPUT)
# ============================================================================

st.sidebar.header("⚙️ Settings")
st.sidebar.markdown("""
**You need an OpenAI API key to use Snip.**

Get one here: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

⚠️ Your key is only used for this session and never stored.
""")

api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-proj-..."
)

st.sidebar.markdown("---")
st.sidebar.caption("Snip v0.2 - Phase 2 (The Brain)")

# ============================================================================
# MAIN APP
# ============================================================================

st.title("✂️ Snip")
st.subheader("Find out how much you're spending on subscriptions")

st.markdown("""
**How it works:**
1. Take a screenshot of your phone's Subscriptions page (Settings → Apple ID → Subscriptions on iPhone)
2. Upload it here
3. We'll show you the total yearly cost

*Your screenshot is sent to OpenAI for analysis only. We don't store it.*
""")

st.markdown("---")

# ============================================================================
# AI VISION FUNCTION (THE BRAIN)
# ============================================================================

def extract_subscriptions_ai(image, api_key):
    """
    Sends the uploaded image to OpenAI Vision and extracts subscription data.
    
    Args:
        image: PIL Image object
        api_key: OpenAI API key string
    
    Returns: 
        List of dicts like [{"name": "Netflix", "price": 15.99, "period": "monthly"}]
    """
    
    # Convert PIL image to base64 (OpenAI needs this format)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    # Call OpenAI Vision API
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Vision-capable model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """You are analyzing a screenshot of a phone's subscription list (like iPhone Settings → Subscriptions or Android equivalent).

Extract ALL subscriptions you see. For each one, identify:
- Service name (e.g. "Netflix", "Spotify Premium", "YouTube Premium")
- Price (numeric only, e.g. 15.99)
- Billing period (either "monthly" or "yearly")

Return ONLY valid JSON in this exact format with no other text:
[
  {"name": "Netflix", "price": 15.99, "period": "monthly"},
  {"name": "Spotify Premium", "price": 9.99, "period": "monthly"}
]

If you see no subscriptions, return: []

Important:
- Extract the ACTUAL price shown (don't guess)
- If billing period is unclear, assume "monthly"
- Ignore free trials unless a price is shown
- Return ONLY the JSON array, no markdown, no explanations"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000,
            temperature=0  # Make it consistent
        )
        
        # Parse the AI's response
        result_text = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if AI added them
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
        
        # Parse JSON
        subscriptions = json.loads(result_text)
        
        # Validate structure
        for sub in subscriptions:
            if not all(key in sub for key in ["name", "price", "period"]):
                st.warning(f"⚠️ Skipping invalid entry: {sub}")
                subscriptions.remove(sub)
        
        return subscriptions
        
    except json.JSONDecodeError:
        st.error("❌ AI returned invalid data. Try a clearer screenshot.")
        return []
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Check that your API key is correct and you have billing set up at platform.openai.com")
        return []


# ============================================================================
# FILE UPLOAD
# ============================================================================

uploaded_file = st.file_uploader(
    "Upload your subscription screenshot",
    type=["png", "jpg", "jpeg"],
    help="Take a screenshot of your Subscriptions page (Settings → Apple ID → Subscriptions on iPhone)"
)

if uploaded_file is not None:
    # Show preview
    image = Image.open(uploaded_file)
    st.image(image, caption="Your screenshot", use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # PROCESS BUTTON
    # ========================================================================
    
    if st.button("🔍 Process Screenshot", type="primary", use_container_width=True):
        
        # Validate API key
        if not api_key:
            st.error("⚠️ **Please enter your OpenAI API key in the sidebar first.**")
            st.info("👈 Look for the Settings section on the left")
            st.stop()
        
        # Show loading state
        with st.spinner("🧠 AI is reading your screenshot... (this takes ~10 seconds)"):
            subscriptions = extract_subscriptions_ai(image, api_key)
        
        # Handle no results
        if not subscriptions or len(subscriptions) == 0:
            st.warning("⚠️ **No subscriptions found.**")
            st.info("""
            **Tips for better results:**
            - Make sure the screenshot clearly shows subscription names and prices
            - Try the iPhone Subscriptions page: Settings → [Your Name] → Subscriptions
            - Ensure text is readable (not blurry or too small)
            """)
            st.stop()
        
        # ====================================================================
        # SHOW RESULTS
        # ====================================================================
        
        st.success(f"✅ Found {len(subscriptions)} subscription(s)")
        
        # Display table
        st.subheader("Your Subscriptions")
        
        # Format for display
        for sub in subscriptions:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{sub['name']}**")
            with col2:
                st.write(f"${sub['price']:.2f}")
            with col3:
                st.write(sub['period'])
        
        st.markdown("---")
        
        # Calculate yearly total
        yearly_total = 0
        for sub in subscriptions:
            if sub['period'].lower() == 'monthly':
                yearly_total += sub['price'] * 12
            elif sub['period'].lower() == 'yearly':
                yearly_total += sub['price']
            else:
                yearly_total += sub['price'] * 12  # Assume monthly if unclear
        
        # Show total with emphasis
        st.subheader("💰 Total Yearly Spending")
        st.metric(
            label="Estimated annual cost",
            value=f"${yearly_total:,.2f}",
            delta=None
        )
        
        st.caption("*This is an estimate based on current prices and billing periods.*")
        
        # Optional: Show breakdown
        with st.expander("📊 See monthly breakdown"):
            monthly_total = sum(
                sub['price'] if sub['period'].lower() == 'monthly' 
                else sub['price'] / 12 
                for sub in subscriptions
            )
            st.write(f"**Average monthly cost:** ${monthly_total:.2f}")
            st.write(f"**Average daily cost:** ${monthly_total / 30:.2f}")

else:
    # Empty state
    st.info("👆 Upload a screenshot to get started")
    
    # Show example
    with st.expander("💡 What kind of screenshot should I upload?"):
        st.markdown("""
        **iPhone:**
        1. Open Settings
        2. Tap your name at the top
        3. Tap "Subscriptions"
        4. Take a screenshot (Volume Up + Power button)
        
        **Android:**
        1. Open Google Play Store
        2. Tap your profile icon
        3. Tap "Payments & subscriptions" → "Subscriptions"
        4. Take a screenshot
        
        The screenshot should clearly show:
        - Service names
        - Prices
        - Billing periods (monthly/yearly)
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.caption("Made with ✂️ by Snip | Your data is processed via OpenAI and not stored")