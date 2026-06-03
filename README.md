# 📄 Hati AI — Kenya Document Explainer in Swahili

> *Hati* (Swahili) = document, certificate, official paper

Upload any Kenya government document — land title, tax notice, court summons, employment contract — and get a plain Swahili explanation of what it means, what you need to do, and what your rights are.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hatiai.streamlit.app)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

## The Problem

Kenya's legal, financial, and administrative documents are written in dense English that excludes millions of Kiswahili-dominant citizens from understanding their own rights and obligations. A land dispute, a KRA notice, or an employment contract can change someone's life — they deserve to understand what they're signing.

## Research Basis

Based on multimodal document-grounded conversational AI methodology (arXiv:2502.09843, MuDoC, Georgia Tech). Extended for low-resource language contexts.

## Features

| Feature | Description |
|---------|-------------|
| 📤 Upload | PDF or image of any Kenya document |
| 🔍 Explain | Plain Swahili summary of key points |
| ✅ Actions | What you need to do (and by when) |
| ⚠️ Rights | Your legal rights in this situation |
| ❓ Ask | Follow-up questions about the document |

## Architecture

```
Document (PDF/image) → Gemini Vision API → Structured Swahili explanation
                              ↓
                    Kenya legal context + domain knowledge
```

## Quickstart

```bash
git clone https://github.com/gabrielmahia/hati-ai
cd hati-ai
pip install -r requirements.txt
streamlit run app.py
```

## Disclaimer

Hati AI provides AI-generated explanations for educational purposes only. Not legal advice. For legal matters, consult a qualified advocate.

---

*Part of the gabrielmahia.ai East Africa civic tech portfolio*
