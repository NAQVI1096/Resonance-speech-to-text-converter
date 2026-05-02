import streamlit as st
import requests

st.set_page_config(
    page_title="Resonance | AI Audio Transcription",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a beautiful, structured dashboard layout
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    
    h1 {
        font-weight: 800;
        color: #f8f9fa;
        padding-bottom: 0.5rem;
    }
    
    h2, h3 {
        font-weight: 600;
        color: #e9ecef;
    }
    
    .output-card {
        background-color: #1a1c23;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #2d3139;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-top: 15px;
        min-height: 180px;
    }
    
    .output-card h4 {
        color: #4da8da;
        margin-top: 0;
        margin-bottom: 15px;
        font-size: 1.15rem;
        border-bottom: 1px solid #2d3139;
        padding-bottom: 12px;
        font-weight: 600;
    }
    
    .output-text {
        color: #e2e8f0;
        font-size: 1.1rem;
        line-height: 1.7;
    }

    /* Style Streamlit Tabs to look like modern UI */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
        padding-top: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 0;
        border: none;
        border-bottom: 2px solid transparent;
        padding-bottom: 10px;
        color: #8b949e;
        font-size: 1.1rem;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        color: #f8f9fa !important;
        border-bottom: 2px solid #4da8da !important;
        background-color: transparent !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .dev-credit {
        color: #8b949e;
        font-size: 0.95rem;
        font-weight: 400;
        text-align: center;
        padding-top: 30px;
        margin-top: 30px;
        border-top: 1px solid #2d3139;
    }
    
    .stRadio > div {
        gap: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("Configure your output preferences below.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### Translation")
    target_language = st.selectbox(
        "Select Target Language",
        options=[
            "English Only (No Translation)",
            "Hindi (hi)",
            "Urdu (ur)",
            "French (fr)",
            "Spanish (es)",
            "German (de)",
            "Chinese (zh)"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("""
    <div class="dev-credit">
        Developed by<br>
        <b style="color: #c9d1d9; font-size: 1.1rem;">Syed Muhammad Zeeshan</b>
    </div>
    """, unsafe_allow_html=True)

# ----------------- MAIN CONTENT -----------------
st.title("🎙️ Resonance")

# Create Tabs
tab_studio, tab_about = st.tabs(["🎙️ Studio", "ℹ️ About Project"])

# ----------------- TAB 1: STUDIO -----------------
with tab_studio:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    audio_file_to_process = None

    with col1:
        st.markdown("### 1. Audio Source")
        source_type = st.radio("Choose Input Method:", ["📁 Upload File", "🎙️ Record Microphone"], horizontal=True, label_visibility="collapsed")
        
        if source_type == "📁 Upload File":
            uploaded_file = st.file_uploader("Upload your audio file", type=["wav", "mp3", "flac", "ogg", "aac", "m4a", "wma"])
            if uploaded_file:
                audio_file_to_process = uploaded_file
        else:
            recorded_audio = st.audio_input("Record your voice")
            if recorded_audio:
                audio_file_to_process = recorded_audio

    with col2:
        st.markdown("### 2. Audio Preview")
        if audio_file_to_process:
            st.audio(audio_file_to_process, format='audio/wav')
            st.success("Audio loaded successfully!")
        else:
            st.info("Upload or record an audio file to preview it here.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Process Button
    process_col, _, _ = st.columns([1, 1, 1])
    with process_col:
        process_btn = st.button("🚀 Process Audio", use_container_width=True, type="primary")

    if process_btn:
        if audio_file_to_process is not None:
            st.markdown("---")
            st.markdown("### Results")
            
            with st.spinner("Analyzing and transcribing audio..."):
                file_name = getattr(audio_file_to_process, "name", "recorded_audio.wav")
                files = {"audio_file": (file_name, audio_file_to_process.getvalue(), "audio/wav")}
                try:
                    # Call Backend for Transcription
                    response = requests.post("http://127.0.0.1:8000/transcribe", files=files)
                    if response.status_code == 200:
                        res_json = response.json()
                        if "error" in res_json:
                            st.error(f"Backend Error: {res_json['error']}")
                        else:
                            transcription = res_json.get("transcription", "")
                            lang_code = None
                            if target_language != "English Only (No Translation)":
                                lang_code = target_language.split("(")[-1].replace(")", "")
                            
                            # Layout: Side-by-side if translation is enabled, else full width
                            if lang_code:
                                out_col1, out_col2 = st.columns(2)
                                
                                with out_col1:
                                    st.markdown(f"""
                                    <div class="output-card">
                                        <h4>📝 Original Transcription</h4>
                                        <div class="output-text">{transcription}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                with out_col2:
                                    with st.spinner(f"Translating to {lang_code}..."):
                                        data = {"text": transcription, "target_lang": lang_code}
                                        res_trans = requests.post("http://127.0.0.1:8000/translate", data=data)
                                        
                                        if res_trans.status_code == 200:
                                            trans_json = res_trans.json()
                                            if "error" in trans_json:
                                                st.error(f"Translation Error: {trans_json['error']}")
                                            else:
                                                translation = trans_json.get("translation", "")
                                                st.markdown(f"""
                                                <div class="output-card">
                                                    <h4 style="color: #a78bfa;">🌍 Translation ({target_language.split(' ')[0]})</h4>
                                                    <div class="output-text">{translation}</div>
                                                </div>
                                                """, unsafe_allow_html=True)
                                        else:
                                            st.error("Error communicating with translation service.")
                            else:
                                st.markdown(f"""
                                <div class="output-card">
                                    <h4>📝 Transcription</h4>
                                    <div class="output-text">{transcription}</div>
                                </div>
                                """, unsafe_allow_html=True)

                    else:
                        st.error("Error communicating with transcription service.")
                except requests.exceptions.ConnectionError:
                    st.error("🚨 Could not connect to the backend server. Is it running on http://127.0.0.1:8000?")
        else:
            st.warning("⚠️ Please upload or record an audio file first before processing.")

# ----------------- TAB 2: ABOUT -----------------
with tab_about:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### System Architecture")
    st.markdown("This application leverages state-of-the-art Deep Learning models to provide robust speech recognition and machine translation in a completely localized pipeline.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_about1, col_about2 = st.columns(2)
    
    with col_about1:
        st.info("🎙️ **Speech-to-Text Engine**")
        st.markdown("""
        - Powered by **HuggingFace Speech2Text**
        - Automatically resamples standard audio formats (WAV, MP3, FLAC) to 16kHz
        - Optimized for high accuracy transcription across varying audio qualities.
        """)
        
    with col_about2:
        st.success("🌍 **Machine Translation Engine**")
        st.markdown("""
        - Powered by **Meta M2M100**
        - Supports direct many-to-many multilingual translation without relying on English as a pivot.
        - Low CPU memory usage configuration enabled for efficient inference.
        """)
        
    st.markdown("---")
    st.markdown("### Developer")
    st.markdown("""
    **Syed Muhammad Zeeshan**  
    Designed as a sophisticated End-to-End Deep Learning application, decoupling the AI Inference backend (FastAPI) from the user interface (Streamlit) for high scalability.
    """)
