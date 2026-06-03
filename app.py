import streamlit as st
import urllib.request
import json
import base64

st.set_page_config(page_title="Hati AI — Eleza Hati yako", page_icon="📄", layout="centered")

st.markdown("""<style>
.main { background: #0a0f1a; color: #e8eaf6; }
.stApp { background: #0a0f1a; }
.hati-card {
    background: #0d1a3b; border: 1px solid #1e3a6e;
    border-radius: 10px; padding: 14px 18px; margin: 8px 0;
}
.stButton > button {
    background: #1565c0; color: white; border: none;
    border-radius: 8px; padding: 10px 24px; font-weight: 700; width: 100%;
}
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")

def explain_document(file_bytes: bytes, mime_type: str, question: str = "") -> str:
    if not API_KEY:
        return "❌ API key not configured."
    b64 = base64.b64encode(file_bytes).decode()
    prompt = question if question else (
        "Eleza hati hii kwa Kiswahili rahisi. Toa:\n"
        "1. Muhtasari: Hati hii ni nini na inasema nini?\n"
        "2. Hatua za kuchukua: Ninapaswa kufanya nini?\n"
        "3. Tarehe muhimu: Kuna muda wowote wa mwisho?\n"
        "4. Haki zangu: Haki zangu katika hali hii ni nini?\n"
        "5. Tahadhari: Kuna hatari yoyote ninayopaswa kujua?"
    )
    body = {
        "contents": [{"role": "user", "parts": [
            {"inline_data": {"mime_type": mime_type, "data": b64}},
            {"text": prompt}
        ]}],
        "systemInstruction": {"parts": [{"text": (
            "Wewe ni mshauri wa hati za kisheria na serikali kwa wananchi wa Kenya. "
            "Eleza hati kwa Kiswahili wazi na rahisi. "
            "Sema ukweli — kama hujui kitu fulani, sema hivyo na umpeleke kwa mtaalamu. "
            "Usitoe ushauri wa kisheria rasmi — eleza tu maana ya hati."
        )}]},
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1000}
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    try:
        req = urllib.request.Request(
            url, data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=45) as r:
            d = json.loads(r.read())
            return d["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Hitilafu: {e}"

st.markdown("# 📄 Hati AI")
st.markdown("**Eleza Hati yako kwa Kiswahili**")
st.caption("Pakia hati yoyote ya serikali au kisheria — tutaeleza kwa lugha rahisi.")

uploaded = st.file_uploader(
    "Pakia hati (PDF au picha)",
    type=["pdf", "png", "jpg", "jpeg"],
    help="Mfano: Ardhini, Notisi ya KRA, Mkataba wa kazi, Hati ya mahakama"
)

if uploaded:
    st.success(f"✅ Hati imepakiwa: {uploaded.name}")
    mime = "application/pdf" if uploaded.name.endswith(".pdf") else f"image/{uploaded.name.split('.')[-1]}"
    file_bytes = uploaded.read()

    if "doc_explanation" not in st.session_state:
        st.session_state.doc_explanation = ""

    if st.button("🔍 Eleza Hati Hii", key="explain_btn"):
        with st.spinner("Ninasoma na kuelewa hati yako..."):
            result = explain_document(file_bytes, mime)
            st.session_state.doc_explanation = result

    if st.session_state.doc_explanation:
        st.markdown("### Maelezo ya Hati Yako")
        st.markdown(f"""<div class="hati-card">{st.session_state.doc_explanation.replace(chr(10), '<br>')}</div>""",
                    unsafe_allow_html=True)

        st.markdown("### ❓ Una swali zaidi?")
        followup = st.text_input("Uliza swali kuhusu hati hii:", placeholder="Mfano: Ninaweza kupinga notisi hii?")
        if st.button("💬 Uliza", key="followup_btn") and followup:
            with st.spinner("Ninafikiri..."):
                ans = explain_document(file_bytes, mime, followup)
            st.markdown(f"""<div class="hati-card">{ans.replace(chr(10), '<br>')}</div>""", unsafe_allow_html=True)
else:
    st.info("👆 Pakia hati yako ili tuanze.")

st.markdown("---")
st.caption("⚠️ Hati AI ni kwa madhumuni ya elimu tu. Si ushauri wa kisheria rasmi. Kwa mambo ya kisheria, wasiliana na wakili aliyeidhinishwa. | Hati AI v1.0")
