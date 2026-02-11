# Snip – Product Requirements Document (PRD)

**Product:** Snip – subscription audit via screenshot  
**Definition of “Market Ready”:** A first-time user can find Snip, upload a subscriptions screenshot, get an accurate spending total, and optionally export the list — without hitting broken flows or confusion. The app is hosted, stable enough for light use, and clear about privacy.

This document lists **every feature Snip must have** before we call it Market Ready. Use it for prioritization and to avoid scope creep.

---

## 1. Core Experience

| ID | Feature | Description | Phase |
|----|---------|-------------|--------|
| F1 | **Upload screenshot** | User can upload one image (PNG/JPG) of their phone’s Subscriptions (or similar) page. | Shell ✅ |
| F2 | **Preview before process** | After upload, user sees the image so they can confirm it’s the right screenshot. | Shell ✅ |
| F3 | **Process on demand** | A single clear action (e.g. “Process” button) runs the analysis. No auto-run on upload. | Shell ✅ |
| F4 | **Real extraction** | AI/vision reads the screenshot and extracts: subscription name, price, billing period (month/year). | Brain |
| F5 | **Results table** | Display extracted subscriptions in a table: name, price, billing period. | Shell ✅ (dummy) / Brain (real) |
| F6 | **Yearly total** | Show one number: estimated total spend per year (normalize monthly to yearly where needed). | Shell ✅ / Brain |
| F7 | **Loading state** | While AI runs, user sees a spinner or message (e.g. “Analyzing…”). | Brain |

---

## 2. Inputs & Configuration

| ID | Feature | Description | Phase |
|----|---------|-------------|--------|
| F8 | **API key input** | User can enter an OpenAI (or chosen provider) API key; used only for vision/API calls, not logged or stored beyond session. | Shell ✅ (UI) / Brain (wired) |
| F9 | **Key validation** | If key is missing or invalid when Process is clicked, show a clear message (e.g. “Please add your API key in the sidebar”). | Brain |
| F10 | **Image validation** | If file is not an image or is corrupted, show a friendly error and ask for a new upload. | Brain / Product |

---

## 3. Errors & Edge Cases

| ID | Feature | Description | Phase |
|----|---------|-------------|--------|
| F11 | **No subscriptions found** | If AI finds nothing in the image, show a clear message and suggest retrying with a clearer or different screenshot. | Brain |
| F12 | **API / network errors** | On timeout or API failure, show a short, non-technical message and suggest trying again. | Brain |
| F13 | **Partial results** | If only some subscriptions are detected, show what we have and note that the list might be incomplete. | Product (optional but nice) |

---

## 4. Onboarding & Clarity

| ID | Feature | Description | Phase |
|----|---------|-------------|--------|
| F14 | **Value proposition** | Above the fold: one line explaining what Snip does (e.g. “Upload a screenshot of your subscriptions — we’ll tell you how much you’re spending.”). | Product |
| F15 | **How it works** | Short copy (1–3 bullets or one paragraph) on what to upload and what they’ll get (list + yearly total). | Product |
| F16 | **Empty state** | When no file is uploaded, show a clear prompt (e.g. “Add a screenshot to get started”) instead of a blank screen. | Shell ✅ |

---

## 5. Export & Sharing

| ID | Feature | Description | Phase |
|----|---------|-------------|--------|
| F17 | **Export list** | User can download the subscription list (e.g. CSV) or copy a summary (names + prices + total). | Product |
| F18 | **Copy total** | At minimum, user can easily copy the yearly total (e.g. copy button or selectable text). | Product |

---

## 6. Trust & Privacy

| ID | Feature | Description | Phase |
|----|---------|-------------|--------|
| F19 | **Privacy note** | Short note on how screenshots are used (e.g. “Sent to AI for reading only; we don’t store your images”). | Product / Launch |
| F20 | **No key logging** | API key is never logged, printed, or sent anywhere except the chosen AI provider. | Brain |
| F21 | **Session-only key** | Key lives only in session (or client-side); not written to disk or database by default. | Brain |

---

## 7. Reliability & Launch

| ID | Feature | Description | Phase |
|----|---------|-------------|--------|
| F22 | **Hosted app** | Snip runs on a stable host (e.g. Streamlit Cloud, VPS) so users can open it via a URL. | Launch |
| F23 | **Timeout handling** | If the AI call takes too long, show a timeout message and suggest retry. | Brain / Product |
| F24 | **Graceful degradation** | On critical failure, show a generic “Something went wrong” and retry option rather than a raw stack trace. | Product |

---

## 8. Polish (Feels Like a Product)

| ID | Feature | Description | Phase |
|----|---------|-------------|--------|
| F25 | **Consistent branding** | One clear product name (Snip), one icon or logo, consistent tone in copy. | Product |
| F26 | **Readable layout** | Enough spacing, readable font sizes, and a layout that works on desktop (and optionally mobile). | Product |
| F27 | **Clear CTAs** | Primary action (Process, Upload) is obvious; secondary actions (e.g. export) are findable. | Product |

---

## Summary: Must-Have for Market Ready

Before calling Snip **Market Ready**, every feature in sections **1–7** should be satisfied at least in a minimal form. Section **8** is polish that makes it feel like a real product; you can ship with a subset and improve later.

**Quick checklist**

- [ ] F1–F7: Core flow works with real AI and clear totals  
- [ ] F8–F10: Key and image handling are safe and clear  
- [ ] F11–F13: Errors and edge cases have user-friendly messages  
- [ ] F14–F16: New users understand what to do  
- [ ] F17–F18: User can take their data out (export/copy)  
- [ ] F19–F21: Privacy and key handling are trustworthy  
- [ ] F22–F24: App is hosted and fails gracefully  
- [ ] F25–F27: Feels like a product, not a prototype  

Use this PRD with `Master_Plan.md` and `Sprint_Log.md` to decide what to build next and to track progress toward Market Ready.
