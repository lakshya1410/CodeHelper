import streamlit as st
from PIL import Image
import base64
import os

def set_page_style():
    """Apply colorful styling to the Streamlit app with dark theme optimization"""
    st.markdown("""
    <style>
        /* Modern typography */
        html, body, [class*="css"] {
            font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
        }
        
        /* Dark theme optimized background colors */
        .stApp {
            background-color: #111827;
            color: #F1F5F9;
        }
        
        /* Vibrant header styling */
        .main-header {
            font-family: 'Inter', 'Segoe UI', sans-serif;
            color: #3B82F6;
            text-align: center;
            padding-bottom: 24px;
            font-size: 2.4rem;
            font-weight: 700;
            text-shadow: 0px 0px 10px rgba(59, 130, 246, 0.3);
            letter-spacing: -0.5px;
        }
        
        /* Text styling with dark theme optimization */
        p, li {
            font-size: 1rem !important;
            color: #E2E8F0 !important;
            line-height: 1.7 !important;
            font-weight: 400 !important;
        }
        
        /* Sidebar text */
        .sidebar-text {
            font-size: 0.95rem !important;
            color: #E2E8F0 !important;
            line-height: 1.6 !important;
            font-weight: 400 !important;
        }
        
        /* Colorful tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            border-bottom: 1px solid #374151;
            padding-bottom: 6px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 45px;
            white-space: pre-wrap;
            border-radius: 6px 6px 0px 0px;
            padding: 8px 16px;
            background-color: #1F2937;
            font-weight: 500;
            font-size: 0.95rem;
            border: 1px solid transparent;
            border-bottom: none;
            color: #D1D5DB;
        }
        .stTabs [aria-selected="true"] {
            background-color: #3B82F6 !important;
            color: white !important;
            border: 1px solid #60A5FA !important;
            border-bottom: none !important;
            position: relative;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }
        .stTabs [aria-selected="true"]:after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            right: 0;
            height: 1px;
            background: #3B82F6;
        }
        
        /* Dark theme text area styling */
        .stTextArea textarea {
            border-radius: 6px;
            border: 1px solid #4B5563;
            font-size: 1rem !important;
            padding: 12px !important;
            background-color: #1F2937;
            color: #F1F5F9;
            box-shadow: 0 1px 2px rgba(0,0,0,0.3);
            transition: all 0.2s;
        }
        .stTextArea textarea:focus {
            border-color: #60A5FA;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
        }
        
        /* Vibrant button styling */
        .stButton>button {
            background-color: #3B82F6;
            color: white;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 500;
            font-size: 0.95rem;
            border: none;
            transition: all 0.2s;
            box-shadow: 0 4px 6px rgba(59, 130, 246, 0.25);
        }
        .stButton>button:hover {
            background-color: #2563EB;
            transform: translateY(-1px);
            box-shadow: 0 6px 10px rgba(59, 130, 246, 0.4);
        }
        
        /* Success message styling */
        .success-message {
            background-color: #064E3B;
            padding: 12px;
            border-radius: 6px;
            border-left: 3px solid #10B981;
            margin: 12px 0;
            color: #D1FAE5;
        }
        
        /* Colorful info card */
        .info-card {
            background-color: #1E3A8A;
            background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%);
            padding: 20px;
            border-radius: 8px;
            margin: 16px 0;
            border: 1px solid #3B82F6;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
        }
        
        .info-card p {
            font-size: 1rem !important;
            color: #E0E7FF !important;
            line-height: 1.6 !important;
        }
        
        /* Gradient response box styling */
        .response-box {
            background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
            padding: 20px;
            border-radius: 8px;
            margin: 12px 0;
            border: 1px solid #3B82F6;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* Section header */
        .section-header {
            color: #60A5FA;
            padding-bottom: 8px;
            margin: 20px 0 12px 0;
            font-weight: 600;
            border-bottom: 1px solid #374151;
            font-size: 1.1rem;
        }
        
        /* File uploader */
        .stFileUploader {
            margin: 12px 0;
        }
        .stFileUploader > div {
            background-color: #1F2937;
            border-color: #4B5563;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #111827;
        }
        
        /* Colorful model card styling */
        .model-card {
            padding: 10px;
            border-radius: 6px;
            text-align: center;
            margin-bottom: 12px;
            border: 1px solid #3B82F6;
            background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%);
            transition: all 0.2s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
        .model-card:hover {
            box-shadow: 0 6px 12px rgba(59, 130, 246, 0.3);
            transform: translateY(-2px);
        }
        
        /* Stats styling */
        .stat-value {
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            color: #60A5FA !important;
            text-align: center;
        }
        
        .stat-label {
            font-weight: 500 !important;
            color: #9CA3AF !important;
            text-align: center;
            font-size: 0.85rem !important;
        }

        /* Code editor and output */
        pre {
            background-color: #1F2937;
            color: #E2E8F0;
            border-radius: 6px;
            border: 1px solid #374151;
        }

        code {
            color: #60A5FA;
        }

        .streamlit-expanderHeader {
            color: #E2E8F0 !important;
            font-weight: 500;
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1F2937;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #4B5563;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #60A5FA;
        }
        
        /* Input fields for dark theme */
        .stSelectbox div[data-baseweb="select"] {
            background-color: #1F2937;
            border-radius: 6px;
            border-color: #4B5563;
            color: #F1F5F9;
        }
        
        /* Spinner */
        .stSpinner > div {
            border-color: #3B82F6 transparent transparent transparent;
        }
        
        /* Slider for temperature control */
        .stSlider div[data-baseweb="slider"] > div {
            background-color: #374151;
        }
        .stSlider div[data-baseweb="slider"] div[role="progressbar"] {
            background-color: #3B82F6;
        }
        .stSlider div[data-baseweb="slider"] div[role="slider"] {
            background-color: #60A5FA;
            border-color: #60A5FA;
            box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
        }
        
        /* Model settings card */
        .settings-card {
            background: linear-gradient(135deg, #1E3A8A 0%, #1F2937 100%);
            padding: 15px;
            border-radius: 8px;
            margin: 12px 0;
            border: 1px solid #3B82F6;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Stats container */
        .stats-container {
            background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            margin-top: 10px;
            border: 1px solid #3B82F6;
        }
    </style>
    """, unsafe_allow_html=True)

def add_model_selector():
    """Create model selector with temperature control"""
    # Replace the section-header class (which has a border-bottom) with a custom style
    st.markdown("<div style='color:#60A5FA; padding-bottom:8px; margin:20px 0 12px 0; font-weight:600; font-size:1.1rem;'>⚙️ Model Settings</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="settings-card">
    """, unsafe_allow_html=True)
    
    text_models = {
        "Gemma 2 9B": "gemma2-9b-it",
        "Llama 3 70B": "llama3-70b-8192",
        "Claude 3 Haiku": "claude-3-haiku-20240307"
    }
    
    selected_model = st.selectbox(
        "Select Text Model:",
        list(text_models.keys())
    )
    
    temperature = st.slider("Temperature:", 0.0, 1.0, 0.7, 0.1)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return text_models[selected_model], temperature

def add_theme_toggle():
    """Create a toggle for switching between light and dark themes"""
    # Initialize theme in session state if not present
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"  # Default theme
        
    st.markdown("<div style='color:#60A5FA; padding-bottom:8px; margin:20px 0 12px 0; font-weight:600; font-size:1.1rem;'>🎨 Appearance</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌙 Dark", 
                    key="dark_theme", 
                    use_container_width=True, 
                    disabled=st.session_state.theme=="dark"):
            st.session_state.theme = "dark"
            st.experimental_rerun()
            
    with col2:
        if st.button("☀️ Light", 
                    key="light_theme", 
                    use_container_width=True,
                    disabled=st.session_state.theme=="light"):
            st.session_state.theme = "light"
            st.experimental_rerun()

def create_sidebar():
    """Create an informative sidebar with reordered elements"""
    with st.sidebar:
        st.markdown("<h2 style='color:#3B82F6;'>💡 AI Code Helper</h2>", unsafe_allow_html=True)
        
        # Logo or icon can be placed here
        if os.path.exists(os.path.join("assets", "logo.png")):
            st.image(os.path.join("assets", "logo.png"), width=120)
        
        # MODEL SETTINGS - Now added here, above the other sections
        selected_model, temperature = add_model_selector()
        
        st.markdown("<hr style='margin: 25px 0; border-color: #374151;'>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>How to use:</div>", unsafe_allow_html=True)
        st.markdown("""
        <ol class="sidebar-text">
            <li><strong>Text Tab:</strong> Type your code or question for AI analysis</li>
            <li><strong>Image Tab:</strong> Upload screenshot of code/error for visual recognition</li>
            <li><strong>Voice Tab:</strong> Speak your question for voice-to-text processing</li>
            <li><strong>Code Execution:</strong> Run and test Python code snippets</li>
            <li><strong>Translation:</strong> Convert code between languages</li>
        </ol>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 25px 0; border-color: #374151;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Model Information</div>", unsafe_allow_html=True)
        
        # Create a more visually appealing model display with 3 models
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="model-card" style="background:linear-gradient(135deg, #0D4C92 0%, #1A73E8 100%);">
                <p style="font-size:0.8rem !important;margin:0;color:#A5D8FF !important;font-weight:600;">TEXT MODEL</p>
                <p style="font-weight:bold;margin:0;font-size:0.9rem !important;color:#E0F2FE !important;">Gemma 2 9B</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="model-card" style="background:linear-gradient(135deg, #064E3B 0%, #059669 100%);">
                <p style="font-size:0.8rem !important;margin:0;color:#A7F3D0 !important;font-weight:600;">IMAGE MODEL</p>
                <p style="font-weight:bold;margin:0;font-size:0.9rem !important;color:#D1FAE5 !important;">Llama 4 Scout</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Add voice model information
        st.markdown("""
        <div class="model-card" style="background:linear-gradient(135deg, #581C87 0%, #9333EA 100%);">
            <p style="font-size:0.8rem !important;margin:0;color:#E9D5FF !important;font-weight:600;">VOICE MODEL</p>
            <p style="font-weight:bold;margin:0;font-size:0.9rem !important;color:#F3E8FF !important;">Google Speech API</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 25px 0; border-color: #374151;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>📊 Usage Stats</div>", unsafe_allow_html=True)
        
        # Initialize counters
        if "text_queries" not in st.session_state:
            st.session_state.text_queries = 0
        if "image_queries" not in st.session_state:
            st.session_state.image_queries = 0
        if "voice_queries" not in st.session_state:
            st.session_state.voice_queries = 0
        if "translation_queries" not in st.session_state:
            st.session_state.translation_queries = 0
        
        # Display stats with improved visibility using a card layout
        st.markdown("""
        <div class="stats-container">
        """, unsafe_allow_html=True)
        
        # Top row - Text and Image
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <p class="stat-label">📝 Text</p>
            <p class="stat-value">{st.session_state.text_queries}</p>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <p class="stat-label">🖼️ Image</p>
            <p class="stat-value">{st.session_state.image_queries}</p>
            """, unsafe_allow_html=True)
            
        # Middle row - Voice and Translation
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <p class="stat-label">🎤 Voice</p>
            <p class="stat-value">{st.session_state.voice_queries}</p>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <p class="stat-label">🔄 Translation</p>
            <p class="stat-value">{st.session_state.translation_queries}</p>
            """, unsafe_allow_html=True)
            
        # Bottom row - Total in its own row
        total = st.session_state.text_queries + st.session_state.image_queries + st.session_state.voice_queries + st.session_state.translation_queries
        st.markdown(f"""
        <div style="padding-top:10px; border-top:1px solid #374151; margin-top:10px;">
            <p class="stat-label" style="font-size:0.9rem !important;">Total Queries</p>
            <p class="stat-value" style="font-size:1.5rem !important; color:#60A5FA !important;">{total}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    return selected_model, temperature

def create_header():
    """Create a beautiful header for the app"""
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <h1 class='main-header'>🧑‍💻 AI-Powered Code Helper</h1>
        """, unsafe_allow_html=True)
    
    # Improved info card with better visibility
    st.markdown("""
    <div class='info-card'>
        <p style="font-size:1.15rem !important; color:#E0E7FF !important; line-height:1.7 !important;">
            This tool uses <strong>Groq's powerful AI models</strong> to help you with coding tasks through multiple input methods. 
            Choose the tab that works best for your needs - text, image, or voice!
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_text_tab():
    """Create the text input tab with styling"""
    st.markdown("<div class='section-header'>📝 Ask a coding question</div>", unsafe_allow_html=True)
    
    user_input = st.text_area(
        "Enter your question or paste your code below:",
        height=200,
        placeholder="Example: How do I use async/await in Python?"
    )
    
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        submit_button = st.button("🚀 Get Answer", use_container_width=True)
    
    return user_input, submit_button

def create_image_tab():
    """Create the image upload tab with styling"""
    st.markdown("<div class='section-header'>📸 Analyze Code Screenshot</div>", unsafe_allow_html=True)
    
    # File uploader with instructions
    st.markdown("""
    <p style="font-size:1.05rem !important; color:#E2E8F0 !important; background-color:#1E3A8A; padding:15px; border-radius:8px; border-left:4px solid #60A5FA;">
        Upload a screenshot of your code or error message. 
        For best results, make sure the text is clearly visible.
    </p>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG"
    )
    
    prompt_text = ""
    analyze_button = False
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Screenshot", use_column_width=True)
        
        # Add a visual separator
        st.markdown("<hr style='margin: 20px 0; border-color: #374151;'>", unsafe_allow_html=True)
        
        prompt_text = st.text_input(
            "What would you like to know about this code?",
            value="Explain this code and identify any issues",
            placeholder="Example: Fix the bugs in this code"
        )
        
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            analyze_button = st.button("🔍 Analyze Screenshot", use_container_width=True)
    
    return uploaded_file, prompt_text, analyze_button

def create_voice_tab():
    """Create the voice input tab with styling"""
    st.markdown("<div class='section-header'>🎤 Ask Using Voice</div>", unsafe_allow_html=True)
    
    # Instructions for voice usage with improved visibility
    st.markdown("""
    <p style="font-size:1.05rem !important; color:#E2E8F0 !important; background-color:#581C87; padding:15px; border-radius:8px; border-left:4px solid #C084FC;">
        Click the button below and speak your coding question clearly.
        Wait for the recording to complete before speaking.
    </p>
    """, unsafe_allow_html=True)
    
    # Add some visual elements for better UI
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:15px;">
            <span style="font-size:3rem; text-shadow: 0 0 10px rgba(192, 132, 252, 0.5);">🎙️</span>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        record_button = st.button("Start Recording", use_container_width=True)
    
    return record_button

def create_code_translation_tab():
    """Create the code translation tab with styling"""
    st.markdown("<div class='section-header'>🔄 Code Translation Engine</div>", unsafe_allow_html=True)
    
    # Instructions with color
    st.markdown("""
    <p style="font-size:1.05rem !important; color:#E2E8F0 !important; background-color:#0E7490; padding:15px; border-radius:8px; border-left:4px solid #22D3EE;">
        Translate code between different programming languages while preserving functionality.
    </p>
    """, unsafe_allow_html=True)
    
    # Language selection
    col1, col2 = st.columns(2)
    with col1:
        source_language = st.selectbox(
            "Source Language:",
            ["Python", "JavaScript", "Java", "C#", "C++", "Go", "Ruby", "PHP", "TypeScript", "Swift"]
        )
    with col2:
        target_language = st.selectbox(
            "Target Language:",
            ["JavaScript", "Python", "Java", "C#", "C++", "Go", "Ruby", "PHP", "TypeScript", "Swift"]
        )
    
    # Code input
    source_code = st.text_area(
        f"Enter your {source_language} code here:",
        height=200,
        placeholder=f"Paste your {source_language} code here..."
    )
    
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        translate_button = st.button("🔄 Translate Code", use_container_width=True)
    
    return source_language, target_language, source_code, translate_button

def display_response(response, response_type="text"):
    """Display AI response with nice formatting"""
    st.markdown("<div class='section-header'>✨ AI Response</div>", unsafe_allow_html=True)
    
    # Different styling based on response type
    if response_type == "code":
        st.code(response, language="python")
    else:
        st.markdown(f"""
        <div class="response-box">
            {response}
        </div>
        """, unsafe_allow_html=True)
    
    # Add helpful buttons with better styling
    st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.download_button(
            label="📥 Download Response",
            data=response,
            file_name="ai_response.txt",
            mime="text/plain"
        )
    with col3:
        if st.button("🔄 New Question"):
            st.experimental_rerun()

def display_loading_animation():
    """Display a custom loading animation"""
    with st.spinner("🧠 AI is thinking..."):
        # Add a progress bar for visual feedback
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            import time
            time.sleep(0.01)  # Adjust for desired animation speed
            progress_bar.progress(percent_complete + 1)
        st.success("Analysis complete!")

def display_api_progress():
    """Display a realistic API call progress indicator"""
    # Create placeholder for progress
    progress_placeholder = st.empty()
    
    # Indicate connection phase
    progress_placeholder.markdown("""
    <div style="padding:10px; border-radius:5px; background:#1E3A8A; margin-bottom:10px;">
        <p style="margin:0; color:#E0E7FF;">🔄 Connecting to API...</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Wait a bit to simulate connection
    import time
    time.sleep(0.7)
    
    # Indicate processing phase
    progress_placeholder.markdown("""
    <div style="padding:10px; border-radius:5px; background:#1E3A8A; margin-bottom:10px;">
        <p style="margin:0; color:#E0E7FF;">⚙️ Processing request...</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Return the placeholder to update when complete
    return progress_placeholder