import streamlit as st
# Set page config first, before any other st commands
st.set_page_config(
    page_title="AI Code Helper", 
    page_icon="🧑‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

import speech_recognition as sr
import base64
from groq import Groq
import os
from dotenv import load_dotenv
from ui_components import (
    set_page_style, create_sidebar, create_header,
    create_text_tab, create_image_tab, create_voice_tab, create_code_translation_tab,
    display_response, display_loading_animation
)
import io
import contextlib
import datetime
import networkx as nx
import matplotlib.pyplot as plt
import tempfile
import zipfile
import shutil
import subprocess
import json
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

def get_api_key():
    """Get API key from environment or Streamlit secrets"""
    # Try to get from environment first
    api_key = os.getenv("GROQ_API_KEY")
    
    # If not in environment, try to get from Streamlit secrets
    if not api_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    
    return api_key

# Initialize Groq client with more robust API key handling
groq_api_key = get_api_key()
if groq_api_key:
    groq_client = Groq(api_key=groq_api_key)
else:
    st.error("No Groq API key found. Please set it in the Streamlit secrets or .env file")
    groq_client = None

# Initialize usage counters
if "text_queries" not in st.session_state:
    st.session_state.text_queries = 0
if "image_queries" not in st.session_state:
    st.session_state.image_queries = 0
if "voice_queries" not in st.session_state:
    st.session_state.voice_queries = 0
if "translation_queries" not in st.session_state:
    st.session_state.translation_queries = 0

# === HELPER FUNCTIONS ===
def ask_groq(prompt):
    try:
        response = groq_client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return "Sorry, I encountered an error while processing your request. Please try again later."

def ask_groq_with_image(prompt, base64_image):
    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )
    return response.choices[0].message.content

def record_and_transcribe():
    """Record audio and transcribe it to text using Groq's Whisper API"""
    try:
        # Create a temporary directory for audio files if it doesn't exist
        temp_dir = os.path.join(os.getcwd(), "temp_audio")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate a unique filename
        audio_file_path = os.path.join(temp_dir, f"audio_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.m4a")
        
        # Record audio using SpeechRecognition
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Speak now")
            audio = recognizer.listen(source, timeout=5)
        
        # Save the recorded audio to a file
        with open(audio_file_path, "wb") as f:
            f.write(audio.get_wav_data())
        
        # Transcribe using Groq
        transcription = transcribe_with_groq(audio_file_path)
        
        # Clean up - remove the temporary audio file
        try:
            os.remove(audio_file_path)
        except:
            pass  # Ignore errors when removing temporary file
            
        return transcription
    
    except Exception as e:
        st.error(f"Error in voice recognition: {str(e)}")
        return "Sorry, voice input isn't available or encountered an error. Please use text input instead."

def transcribe_with_groq(audio_file_path):
    """Transcribe audio using Groq's Whisper API"""
    try:
        # Open audio file in binary mode
        with open(audio_file_path, "rb") as file:
            # Request transcription from Groq
            transcription = groq_client.audio.transcriptions.create(
                file=(audio_file_path, file.read()),
                model="whisper-large-v3",
                response_format="json"
            )
            
            # Return the transcribed text
            return transcription.text
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return f"Sorry, I encountered an error while transcribing your audio: {str(e)}"

def encode_image_to_base64(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")

def create_code_execution_area():
    st.markdown("<h3 class='section-header'>⚡ Code Playground</h3>", unsafe_allow_html=True)
    
    code = st.text_area("Enter Python code to execute:", height=200)
    if st.button("▶️ Run Code"):
        with st.spinner("Executing..."):
            try:
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    exec(code)
                st.success("Code executed successfully!")
                st.code(output.getvalue())
            except Exception as e:
                st.error(f"Error: {str(e)}")

def add_model_selector():
    st.sidebar.markdown("<h3 class='section-header'>⚙️ Model Settings</h3>", unsafe_allow_html=True)
    
    text_models = {
        "Gemma 2 9B": "gemma2-9b-it",
        "Llama 3 70B": "llama3-70b-8192",
        "Claude 3 Haiku": "claude-3-haiku-20240307"
    }
    
    selected_model = st.sidebar.selectbox(
        "Select Text Model:",
        list(text_models.keys())
    )
    
    temperature = st.sidebar.slider("Temperature:", 0.0, 1.0, 0.7, 0.1)
    
    return text_models[selected_model], temperature

def translate_code(source_code, source_language, target_language):
    """Translate code from one programming language to another using Groq"""
    
    prompt = f"""
    Translate the following {source_language} code to {target_language}.
    Maintain the same functionality, logic, and behavior.
    Add comments explaining any significant translation decisions or language differences.
    If any feature doesn't have a direct equivalent, explain the workaround used.
    
    Here's the {source_language} code to translate:
    ```{source_language}
    {source_code}
    ```
    """
    
    response = groq_client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_completion_tokens=2048
    )
    
    return response.choices[0].message.content

def analyze_project(upload_folder):
    """Analyze entire project structure and relationships"""
    # Extract file structure
    file_structure = extract_file_structure(upload_folder)
    
    # Parse files for imports, dependencies, and relationships
    dependency_graph = build_dependency_graph(upload_folder)
    
    # Identify architectural patterns currently in use
    current_patterns = identify_patterns(upload_folder)
    
    # Identify complexity hotspots
    complexity_analysis = analyze_complexity(upload_folder)
    
    return {
        "structure": file_structure,
        "dependencies": dependency_graph,
        "patterns": current_patterns,
        "complexity": complexity_analysis
    }

def visualize_dependencies(dependency_graph):
    """Create interactive visualization of project dependencies"""
    G = nx.DiGraph()
    
    # Add nodes and edges from dependency graph
    for source, targets in dependency_graph.items():
        G.add_node(source)
        for target in targets:
            G.add_edge(source, target)
    
    # Check if graph is empty and add placeholder if needed
    if len(G.nodes) == 0:
        G.add_node("No dependencies found")
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True, node_color="#3B82F6", 
                    edge_color="#60A5FA", node_size=300, font_size=8,
                    font_color="white", font_weight="bold")
    
    # Display in Streamlit
    st.pyplot(fig)

def get_architecture_recommendations(project_analysis):
    """Get AI recommendations for architectural improvements"""
    # Prepare detailed prompt with all analysis data
    prompt = f"""
    As an expert software architect, analyze this project and provide architectural recommendations.
    
    Project structure: {project_analysis['structure']}
    
    Dependency graph: {project_analysis['dependencies']}
    
    Current design patterns: {project_analysis['patterns']}
    
    Complexity analysis: {project_analysis['complexity']}
    
    Provide the following recommendations:
    1. Overall architectural assessment (current architecture pattern if identifiable)
    2. Suggested architectural improvements with reasoning
    3. Specific design patterns that would improve the codebase
    4. Component restructuring recommendations
    5. Dependency management suggestions
    6. Scalability considerations
    7. Code quality improvements
    
    Format recommendations as structured JSON with explanations.
    """
    
    # Get AI recommendations
    response = groq_client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_completion_tokens=4096  # Make sure this matches other API calls
    )
    
    # Parse and return recommendations
    recommendations = response.choices[0].message.content
    return recommendations

def generate_implementation_blueprint(project_analysis, recommendations_text):
    """Generate specific implementation examples for recommended changes"""
    # Initialize blueprint dictionary
    blueprint = {}
    
    try:
        # Try to parse recommendations as JSON
        try:
            recommendations = json.loads(recommendations_text)
        except json.JSONDecodeError:
            # If parsing fails, extract design patterns using AI
            prompt = f"""
            Based on the following architectural recommendations, identify the key design patterns 
            that were suggested and list them in a simple format.
            
            Recommendations:
            {recommendations_text}
            
            For each pattern, just provide the name, no description needed.
            """
            
            response = groq_client.chat.completions.create(
                model="gemma2-9b-it",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            
            pattern_text = response.choices[0].message.content
            
            # Extract pattern names using simple line processing
            patterns = []
            for line in pattern_text.split('\n'):
                if line.strip() and not line.startswith('#') and not line.startswith('-'):
                    patterns.append({"name": line.strip()})
            
            # Create a simple structure
            recommendations = {"design_patterns": patterns}
        
        # Process patterns if they exist
        if "design_patterns" in recommendations:
            for pattern in recommendations["design_patterns"]:
                if isinstance(pattern, dict) and "name" in pattern:
                    pattern_name = pattern["name"]
                elif isinstance(pattern, str):
                    pattern_name = pattern
                else:
                    continue
                    
                prompt = f"""
                Generate an implementation example for the {pattern_name} design pattern 
                in the context of this project. Use pseudocode or Python.
                
                Project context: {project_analysis['structure']}
                """
                
                response = groq_client.chat.completions.create(
                    model="gemma2-9b-it",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                
                blueprint[f"pattern_{pattern_name}"] = response.choices[0].message.content
        else:
            # No design patterns found, get general implementation advice
            prompt = f"""
            Based on the project structure below, provide implementation examples 
            for improving the architecture:
            
            Project structure: {project_analysis['structure']}
            """
            
            response = groq_client.chat.completions.create(
                model="gemma2-9b-it",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            blueprint["general_improvements"] = response.choices[0].message.content
    
    except Exception as e:
        blueprint["error"] = f"Error generating blueprint: {str(e)}"
        blueprint["fallback_advice"] = "Consider implementing common patterns like Repository, Factory, or Dependency Injection to improve your code structure."
    
    return blueprint

def extract_zip_project(uploaded_file):
    """Extract uploaded ZIP file to a temporary directory"""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save uploaded file to a temporary file
        temp_zip = os.path.join(temp_dir, "uploaded_project.zip")
        with open(temp_zip, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Extract the zip file
        extract_dir = os.path.join(temp_dir, "project")
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        return extract_dir
    
    except Exception as e:
        st.error(f"Error extracting ZIP file: {str(e)}")
        shutil.rmtree(temp_dir)
        return None

def clone_git_repo(repo_url):
    """Clone a Git repository to a temporary directory"""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Check if git is available
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            st.error("Git is not installed or not in PATH. Please install Git.")
            return None
        
        # Clone the repository - MODIFIED: Added timeout and better error handling
        try:
            result = subprocess.run(
                ["git", "clone", "--depth=1", repo_url, temp_dir],  # Added depth=1 for faster cloning
                check=True,
                capture_output=True,
                text=True,
                timeout=60  # Add timeout to prevent hanging
            )
            
            # Verify the repository was cloned (check for files)
            if not os.path.exists(os.path.join(temp_dir, ".git")):
                st.error("Repository appears empty or failed to clone properly.")
                return None
                
            st.success(f"Repository cloned successfully! Found {len(os.listdir(temp_dir))} files/directories.")
            return temp_dir
            
        except subprocess.TimeoutExpired:
            st.error("Git clone operation timed out. The repository might be too large or the connection is slow.")
            shutil.rmtree(temp_dir)
            return None
    
    except subprocess.CalledProcessError as e:
        st.error(f"Git error: {e.stderr}")
        shutil.rmtree(temp_dir)
        return None
    except Exception as e:
        st.error(f"Error cloning repository: {str(e)}")
        shutil.rmtree(temp_dir)
        return None

def get_project_structure_text(project_path):
    """Generate a text representation of the project structure"""
    result = []
    
    for root, dirs, files in os.walk(project_path):
        # Skip hidden directories and files
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        level = root.replace(project_path, '').count(os.sep)
        indent = ' ' * 4 * level
        folder_name = os.path.basename(root)
        
        if level > 0:  # Skip the root directory name
            result.append(f"{indent}{folder_name}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        for file in sorted([f for f in files if not f.startswith('.')]):
            result.append(f"{sub_indent}{file}")
    
    return '\n'.join(result)

def extract_file_structure(project_path):
    """Extract file structure from project folder with better error handling"""
    structure = {}
    
    try:
        if not os.path.exists(project_path):
            return {"error": "Project path does not exist"}
            
        # Get maximum depth to prevent recursion errors
        max_depth = 5
        current_depth = 0
        
        for root, dirs, files in os.walk(project_path, topdown=True):
            # Skip hidden directories and files
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
            
            # Skip deep directories to prevent overwhelming analysis
            depth = root.replace(project_path, '').count(os.sep)
            if depth > max_depth:
                continue
                
            # Skip large file counts for better performance
            if len(files) > 100:
                files = files[:100] + ["..."]
                
            rel_path = os.path.relpath(root, project_path)
            if rel_path == '.':
                rel_path = ''
                
            path_parts = rel_path.split(os.sep) if rel_path else []
            current_dict = structure
            
            # Build nested dictionary structure
            for part in path_parts:
                if part:
                    if part not in current_dict:
                        current_dict[part] = {}
                    current_dict = current_dict[part]
            
            # Add files
            current_dict['__files__'] = files
    
    except Exception as e:
        return {"error": f"Error analyzing file structure: {str(e)}"}
        
    return structure

def build_dependency_graph(project_path):
    """Build a dependency graph of project components"""
    # For demonstration purposes - in a real app, you'd parse actual imports
    dependency_graph = {}
    python_files = []
    
    # Find all Python files
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                rel_path = os.path.relpath(os.path.join(root, file), project_path)
                python_files.append(rel_path)
    
    # Build simple dependency graph (in a real app, you'd analyze imports)
    for file in python_files:
        module_name = os.path.splitext(file)[0].replace(os.sep, '.')
        dependency_graph[module_name] = []
        
        # Simple analysis: assume files in the same directory might be related
        for other_file in python_files:
            if file != other_file and os.path.dirname(file) == os.path.dirname(other_file):
                other_module = os.path.splitext(other_file)[0].replace(os.sep, '.')
                dependency_graph[module_name].append(other_module)
    
    return dependency_graph

def identify_patterns(project_path):
    """Identify common design patterns in the codebase"""
    # In a real app, this would be a complex analysis
    # For demonstration, we'll return placeholder data
    return {
        "singleton": ["Found potential Singleton pattern in app configuration"],
        "factory": ["Possible Factory pattern in model creation"],
        "observer": ["UI components may use Observer pattern"],
        "mvc": ["Application structure suggests MVC architecture"],
    }

def analyze_complexity(project_path):
    """Analyze code complexity metrics"""
    # In a real app, you would use tools like radon, pylint, etc.
    # For demonstration, we'll return placeholder data
    return {
        "cyclomatic_complexity": {
            "average": 4.2,
            "max": 15,
            "hotspots": ["app.py:create_architecture_recommendation_tab"]
        },
        "maintainability_index": {
            "average": 65.3,
            "issues": ["Long functions in data processing modules"]
        },
        "loc": {
            "total": 850,
            "per_module": {"app.py": 350, "ui_components.py": 500}
        }
    }

def display_architectural_recommendations(recommendations_text):
    """Display architectural recommendations in a readable format"""
    st.markdown("### Architectural Analysis Results")
    
    try:
        # First try to parse as JSON
        try:
            recommendations = json.loads(recommendations_text)
            
            # Display as formatted sections
            for section, content in recommendations.items():
                st.markdown(f"#### {section.replace('_', ' ').title()}")
                
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            for key, value in item.items():
                                st.markdown(f"**{key}**: {value}")
                        else:
                            st.markdown(f"- {item}")
                elif isinstance(content, dict):
                    for key, value in content.items():
                        st.markdown(f"**{key}**: {value}")
                else:
                    st.markdown(content)
                
                st.markdown("---")
            
            return True
                
        except json.JSONDecodeError:
            # If not valid JSON, parse as markdown
            st.markdown("*AI returned formatted text instead of JSON:*")
            st.markdown(recommendations_text)
            return True
            
    except Exception as e:
        st.error(f"Error displaying recommendations: {str(e)}")
        st.text_area("Raw recommendations", value=recommendations_text, height=300)
        return False

def display_implementation_blueprint(blueprint):
    """Display implementation examples in a readable format"""
    for pattern, implementation in blueprint.items():
        with st.expander(f"{pattern}"):
            st.code(implementation)

def create_architecture_recommendation_tab():
    """Create the architecture recommendation tab"""
    st.markdown("<div class='section-header'>🏛️ Architecture Advisor</div>", unsafe_allow_html=True)
    
    # Instructions
    st.markdown("""
    <p style="font-size:1.05rem !important; color:#E2E8F0 !important; background-color:#1E40AF; padding:15px; border-radius:8px; border-left:4px solid #60A5FA;">
        Upload a project folder to receive AI-powered architectural recommendations, 
        visualize component relationships, and get implementation guidance.
    </p>
    """, unsafe_allow_html=True)
    
    # Project upload method selection
    upload_method = st.radio(
        "Choose upload method:",
        ["Upload ZIP file", "Provide Git repository URL"]
    )
    
    project_path = None
    
    if upload_method == "Upload ZIP file":
        uploaded_file = st.file_uploader(
            "Upload project ZIP file",
            type=["zip"],
            help="Max size: 200MB"
        )
        
        if uploaded_file:
            # Save and extract zip file
            project_path = extract_zip_project(uploaded_file)
            
    else:  # Git repository
        repo_url = st.text_input(
            "Enter Git repository URL:",
            placeholder="https://github.com/username/repository"
        )
        
        # Add validation for repository URL
        if repo_url:
            # Basic validation
            if not (repo_url.startswith("http://") or repo_url.startswith("https://") or 
                    repo_url.startswith("git@")):
                st.warning("Please enter a valid Git repository URL (https:// or git@)")
            else:
                if st.button("Clone Repository"):
                    with st.spinner(f"Cloning repository from {repo_url}..."):
                        # Show more detailed progress
                        status = st.empty()
                        status.text("Initializing Git clone operation...")
                        
                        # Try to clone with detailed feedback
                        project_path = clone_git_repo(repo_url)
                        
                        if project_path:
                            status.text(f"Repository cloned to temporary directory: {project_path}")
                        else:
                            status.text("Failed to clone repository. See error message above.")
    
    if project_path:
        # Debug information
        st.write(f"Project path: {project_path}")
        st.write(f"Path exists: {os.path.exists(project_path)}")
        try:
            files = os.listdir(project_path)
            st.write(f"Number of files/directories: {len(files)}")
            st.write(f"First few files/dirs: {files[:5] if files else 'None'}")
        except Exception as e:
            st.write(f"Error listing directory: {str(e)}")
        
        # Add verification that the path exists and has content
        if not os.path.exists(project_path) or not os.listdir(project_path):
            st.error("Project path is empty or doesn't exist. Please try again.")
        else:
            # Show project structure
            try:
                project_structure = get_project_structure_text(project_path)
                with st.expander("Project Structure", expanded=True):
                    st.code(project_structure)
                
                # Analysis button
                if st.button("🔍 Analyze Architecture", use_container_width=True):
                    # Track usage first to avoid miss-counts on errors
                    if "architecture_analyses" not in st.session_state:
                        st.session_state.architecture_analyses = 0
                    st.session_state.architecture_analyses += 1
                    
                    analysis_progress = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("Step 1/4: Analyzing project structure...")
                    analysis_progress.progress(10)
                    
                    try:
                        # Perform initial analysis
                        analysis_results = analyze_project(project_path)
                        analysis_progress.progress(30)
                        
                        # Display dependency visualization
                        status_text.text("Step 2/4: Generating dependency visualization...")
                        st.subheader("Component Dependencies")
                        visualize_dependencies(analysis_results["dependencies"])
                        analysis_progress.progress(50)
                        
                        # Get AI recommendations
                        status_text.text("Step 3/4: Getting AI architectural recommendations...")
                        recommendations = get_architecture_recommendations(analysis_results)
                        
                        # Debugging output
                        status_text.text("Recommendations received from AI. Displaying results...")
                        st.write("Raw recommendations text (for debugging):")
                        st.code(recommendations[:500] + "...", language="json")  # Show first 500 chars
                        
                        analysis_progress.progress(75)
                        
                        # Display recommendation sections
                        st.subheader("Architectural Recommendations")
                        display_architectural_recommendations(recommendations)
                        
                        # Generate implementation blueprint
                        status_text.text("Step 4/4: Creating implementation blueprint...")
                        st.subheader("Implementation Blueprint")
                        blueprint = generate_implementation_blueprint(
                            analysis_results, recommendations
                        )
                        analysis_progress.progress(95)
                        
                        # Display implementation examples
                        display_implementation_blueprint(blueprint)
                        analysis_progress.progress(100)
                        status_text.text("Analysis complete!")
                            
                    except Exception as e:
                        st.error(f"Error during architecture analysis: {str(e)}")
                        st.warning("Try with a smaller project or check your API connection.")
            except Exception as e:
                st.error(f"Error reading project structure: {str(e)}")

def setup_for_streamlit_cloud():
    """Set up all needed configuration files for Streamlit Cloud deployment"""
    
    # Create minimal requirements.txt
    with open("requirements.txt", "w") as f:
        f.write("""
streamlit==1.31.0
groq==0.4.1
python-dotenv==1.0.0
matplotlib==3.8.2
networkx==3.2.1
Pillow==10.1.0
PyAudio-wheels==0.2.11
SpeechRecognition==3.10.0
""".strip())
    
    # Create runtime.txt
    with open("runtime.txt", "w") as f:
        f.write("python-3.10")
    
    # Create packages.txt
    with open("packages.txt", "w") as f:
        f.write("portaudio19-dev\npython3-dev\n")
    
    # Create .streamlit directory and config.toml
    os.makedirs(".streamlit", exist_ok=True)
    with open(".streamlit/config.toml", "w") as f:
        f.write("""
[theme]
primaryColor = "#3B82F6"
backgroundColor = "#111827"
secondaryBackgroundColor = "#1F2937"
textColor = "#F1F5F9"
        """)
    
    print("All configuration files created successfully!")

# Run the setup
setup_for_streamlit_cloud()

# === MAIN APP ===
def main():
    # Apply custom styling
    set_page_style()
    
    # Create sidebar with information
    selected_model, temperature = create_sidebar()
    
    # Create header
    create_header()
    
    # Create tabs for different input methods (removed favorites tab)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💬 Text Input", "🖼️ Image Analysis", 
        "🎤 Voice Input", "⚡ Code Execution",
        "🔄 Code Translation", "🏛️ Architecture Advisor"
    ])
    
    # === TEXT INPUT TAB ===
    with tab1:
        user_input, submit_text = create_text_tab()
        if submit_text:
            if user_input:
                display_loading_animation()
                response = ask_groq(user_input)
                
                # Track usage
                st.session_state.text_queries += 1
                
                # Display response
                display_response(response)
            else:
                st.warning("Please enter some text before submitting.")
    
    # === IMAGE INPUT TAB ===
    with tab2:
        uploaded_file, prompt_text, analyze_button = create_image_tab()
        
        if analyze_button and uploaded_file:
            display_loading_animation()
            
            # Process the image
            base64_image = encode_image_to_base64(uploaded_file)
            
            # Get AI response
            response = ask_groq_with_image(prompt_text, base64_image)
            
            # Track usage
            st.session_state.image_queries += 1
            
            # Display response
            display_response(response, response_type="code")
    
    # === VOICE INPUT TAB ===
    with tab3:
        # Check if we're running in Streamlit Cloud
        is_cloud = os.environ.get("STREAMLIT_DEPLOYMENT", "") != ""
        
        if is_cloud:
            # Use file upload version in cloud
            audio_file_path = create_fallback_voice_tab()
            
            if audio_file_path:
                with st.spinner("Transcribing audio..."):
                    # Transcribe using Groq
                    transcription = transcribe_with_groq(audio_file_path)
                    
                    # Clean up - remove the temporary file
                    try:
                        os.remove(audio_file_path)
                    except:
                        pass
                    
                    if transcription and "Sorry" not in transcription:
                        st.success(f"Transcription: {transcription}")
                        
                        display_loading_animation()
                        response = ask_groq(transcription)
                        
                        # Track usage
                        st.session_state.voice_queries += 1
                        
                        # Display response
                        display_response(response)
                    else:
                        st.error(transcription)
        else:
            # Use microphone version locally
            record_button = create_voice_tab()
            
            if record_button:
                with st.spinner("🎙️ Listening..."):
                    transcribed_text = record_and_transcribe()
                    
                    if "Sorry" not in transcribed_text:
                        st.success(f"You said: {transcribed_text}")
                        
                        display_loading_animation()
                        response = ask_groq(transcribed_text)
                        
                        # Track usage
                        st.session_state.voice_queries += 1
                        
                        # Display response
                        display_response(response)
                    else:
                        st.error(transcribed_text)
    
    # === CODE EXECUTION TAB ===
    with tab4:
        create_code_execution_area()
    
    # === CODE TRANSLATION TAB ===
    with tab5:
        source_language, target_language, source_code, translate_button = create_code_translation_tab()
        
        if translate_button:
            if source_code and source_language != target_language:
                with st.spinner(f"Translating {source_language} to {target_language}..."):
                    translated_code = translate_code(source_code, source_language, target_language)
                    
                    # Track usage
                    st.session_state.translation_queries += 1
                    
                    # Display side-by-side comparison
                    st.markdown("<h4>Translation Results:</h4>", unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"<p><strong>Original {source_language} Code:</strong></p>", unsafe_allow_html=True)
                        st.code(source_code, language=source_language.lower())
                    
                    with col2:
                        st.markdown(f"<p><strong>Translated {target_language} Code:</strong></p>", unsafe_allow_html=True)
                        st.code(translated_code, language=target_language.lower())
                    
                    # Option to download translated code
                    st.download_button(
                        "📥 Download Translated Code",
                        translated_code,
                        file_name=f"translated_code.{target_language.lower()}",
                        mime="text/plain"
                    )
            elif source_language == target_language:
                st.warning("Source and target languages must be different.")
            else:
                st.warning("Please enter some code to translate.")
    
    # === ARCHITECTURE RECOMMENDATION TAB ===
    with tab6:
        create_architecture_recommendation_tab()

if __name__ == "__main__":
    main()