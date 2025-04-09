# AI Code Helper 🧑‍💻
![image](https://github.com/user-attachments/assets/a8b6e5ef-1f41-4857-bb0b-33174cc2d3fe)


![AI Code Helper Banner](https://via.placeholder.com/800x200?text=AI+Code+Helper)

## Overview

AI Code Helper is a powerful Streamlit application that leverages Groq's AI models to assist developers with various coding tasks through multiple input methods. This tool helps programmers solve coding problems, analyze code, translate between programming languages, and receive architectural recommendations for their projects.

## Features

- **Multi-Modal Input**:
  - 💬 **Text Input**: Ask coding questions or paste code for analysis
  - 🖼️ **Image Analysis**: Upload screenshots of code or error messages for visual recognition
  - 🎤 **Voice Input**: Ask questions using voice commands

- **Code Tools**:
  - ⚡ **Code Execution**: Run and test Python code snippets directly within the app
  - 🔄 **Code Translation**: Convert code between different programming languages
  - 🏛️ **Architecture Advisor**: Get AI-powered recommendations for project architecture

## Installation

### Prerequisites
- Python 3.7+
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-code-helper.git
   cd ai-code-helper
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage Guide

### Text Input
1. Navigate to the "Text Input" tab
2. Type your coding question or paste your code
3. Click "Get Answer" to receive AI assistance

### Image Analysis
1. Navigate to the "Image Analysis" tab
2. Upload a screenshot of your code or error message
3. Specify what you'd like to know about the image
4. Click "Analyze Screenshot" to get insights

### Voice Input
1. Navigate to the "Voice Input" tab
2. Click "Start Recording"
3. Speak your coding question clearly
4. Wait for the AI to process and respond

### Code Execution
1. Navigate to the "Code Execution" tab
2. Enter Python code in the text area
3. Click "Run Code" to execute and see the results

### Code Translation
1. Navigate to the "Code Translation" tab
2. Select source and target programming languages
3. Enter the code you want to translate
4. Click "Translate Code" to convert between languages

### Architecture Advisor
1. Navigate to the "Architecture Advisor" tab
2. Upload a ZIP file of your project or provide a Git repository URL
3. Click "Analyze Architecture" to receive recommendations
4. View dependency visualizations and implementation guidance

## AI Models

The application uses several AI models from Groq:
- **Text Processing**: Gemma 2 9B, Llama 3 70B, Claude 3 Haiku
- **Image Analysis**: Llama 4 Scout 17B
- **Voice Recognition**: Google Speech API

## Project Structure

```
├── app.py                 # Main application file
├── ui_components.py       # UI styling and component functions
├── requirements.txt       # Python dependencies
├── assets/                # Application assets like images
└── .env                   # Environment variables (API keys)
```

## Requirements

Core dependencies:
- streamlit==1.31.0
- groq==0.4.0
- Pillow==10.2.0
- SpeechRecognition==3.10.0
- PyAudio==0.2.13
- python-dotenv==1.0.0
- requests==2.31.0
- matplotlib
- networkx

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Groq](https://groq.com/) for providing the AI models
- [Streamlit](https://streamlit.io/) for the web app framework
- All contributors and users of this tool

---

Created with ❤️ by Lakshya Tripathi
