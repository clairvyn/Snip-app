# Snip – Master Plan (The Big Map)

This document is your high-level roadmap. It shows the four phases of development and where Snip sits at any time. When you feel lost, open this file first.

---

## The Four Phases

| Phase | Name | What It Means | Status |
|-------|------|---------------|--------|
| **1** | **The Shell** | The app exists, looks like Snip, and runs end-to-end with fake data. Users can upload a screenshot, click Process, and see example results. No real AI yet. | ✅ Done |
| **2** | **The Brain** | Real AI (vision/OCR) reads the screenshot and extracts real subscription names, prices, and billing periods. The numbers users see come from their actual screenshot. | 🔜 Next |
| **3** | **The Product** | Snip feels finished: clear copy, export options, error handling, and polish so it’s something you’d be comfortable showing to a real user or investor. | ⏳ Later |
| **4** | **The Launch** | Market-ready: hosting, reliability, legal/privacy, and whatever you need to open the doors to real users (landing page, waitlist, or first launch). | ⏳ Later |

---

## Phase 1 – The Shell ✅

**Goal:** Prove the flow and the UI before spending time on AI.

- [x] Streamlit app with title “Snip”
- [x] File uploader (PNG/JPG) for subscription screenshots
- [x] Image preview so users confirm the right screenshot
- [x] “Process” button (explicit user action)
- [x] Dummy AI that returns fake subscriptions
- [x] Results: table + estimated yearly total
- [x] Sidebar for OpenAI API key (for Phase 2)
- [x] `requirements.txt` and runnable app

**You are here when:** You can run the app, upload any image, click Process, and see fake subscription data and a total.

---

## Phase 2 – The Brain 🔜

**Goal:** Replace fake data with real extraction from the screenshot.

- [ ] Call a vision-capable API (e.g. OpenAI Vision) with the uploaded image
- [ ] Prompt/parse so the model returns: subscription name, price, billing period
- [ ] Normalize and validate (e.g. monthly vs yearly, same service different tiers)
- [ ] Show real results in the same table + yearly total
- [ ] Handle errors: bad image, no subscriptions found, API failure — with clear user messages
- [ ] Loading state so users know the AI is working
- [ ] API key: use sidebar key securely (no logging, no exposure)

**You are here when:** A real subscription screenshot yields real names and numbers in the app.

---

## Phase 3 – The Product ⏳

**Goal:** Make Snip feel like a real product, not a prototype.

- [ ] Onboarding / “How it works” (short, above the fold)
- [ ] Clear error messages and suggestions (e.g. “Use a clearer screenshot”)
- [ ] Export: download list and/or total (CSV or copy-paste)
- [ ] Visual polish: spacing, typography, maybe a simple brand look
- [ ] Optional: “Try again” or “Upload another” without losing context
- [ ] Copy and tone consistent with “mass-market subscription audit tool”

**You are here when:** You’d be comfortable putting this in front of a friend or early tester and saying “this is Snip.”

---

## Phase 4 – The Launch ⏳

**Goal:** Get Snip in front of real users in a sustainable way.

- [ ] Hosting: run Snip somewhere stable (e.g. Streamlit Cloud, a VPS, or another host)
- [ ] Reliability: basic uptime, timeouts, and error handling so the app doesn’t “break” silently
- [ ] Privacy & terms: what you do with screenshots and data (e.g. not stored, or stored briefly), and a simple terms/privacy note if needed
- [ ] Landing / distribution: how people find Snip (landing page, waitlist, or direct link)
- [ ] Optional: analytics or feedback so you know how people use it and where it fails

**You are here when:** Someone can discover Snip, use it, and you’re confident it’s “market ready” by your definition.

---

## How to Use This Map

- **Feeling lost?** Read this file. Then open `app.py` and check the comment at the top — it will say which phase the code is in.
- **Planning the day?** Pick one phase and work from the checklist above (and from `PRD.md` for detail).
- **Tracking progress?** Log what you did in `Sprint_Log.md` (by hour or by session).

All of this lives in the same repo so the “Big Co” docs and the code stay in sync.
