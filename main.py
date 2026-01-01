import streamlit as st
import os

# Page config
st.set_page_config(page_title="IG Feed Generator", layout="wide")

# Paths - relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, 'prompts')
ANGLES_DIR = os.path.join(BASE_DIR, 'angles')
TONES_DIR = os.path.join(BASE_DIR, 'tones', 'english') # Defaulting to english folder

def load_file(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return f"[Error: File not found at {path}]"

def get_options(directory):
    if not os.path.exists(directory):
        return []
    return [f for f in os.listdir(directory) if f.endswith('.txt')]

st.title("🚀 Instagram Carousel Generator")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Settings")
    
    # Topic Input
    topic = st.text_area("Topic", height=100, placeholder="e.g. How to start coding in 2024")
    
    # Angle Selection
    angle_options = get_options(ANGLES_DIR)
    if angle_options:
        selected_angle = st.selectbox("Content Angle", angle_options)
    else:
        st.error(f"No files found in {ANGLES_DIR}")
        selected_angle = None
    
    # Tone Selection
    tone_options = get_options(TONES_DIR)
    if tone_options:
        selected_tone = st.selectbox("Tone of Voice", tone_options)
    else:
        st.error(f"No files found in {TONES_DIR}")
        selected_tone = None
    
    # Options
    include_caption = st.checkbox("Include Caption Instructions", value=True)
    include_meme = st.checkbox("Include Meme Analysis", value=False)

    generate_btn = st.button("Generate Prompt", type="primary")

with col2:
    st.header("Master Prompt")
    
    if generate_btn and topic and selected_angle and selected_tone:
        # Load contents
        viral_framework = load_file(os.path.join(PROMPTS_DIR, 'viral_framework.txt'))
        humanizer = load_file(os.path.join(PROMPTS_DIR, 'humanizer.txt'))
        angle_content = load_file(os.path.join(ANGLES_DIR, selected_angle))
        tone_content = load_file(os.path.join(TONES_DIR, selected_tone))
        
        prompt_parts = [
            "<ROLE>",
            "You are a world-class Instagram content strategist.",
            "</ROLE>\n",
            "<CONTEXT_AND_RULES>",
            "I need you to generate an Instagram Carousel post about the TOPIC below.",
            "You must strictly follow the frameworks and guidelines provided.\n",
            "1. VIRAL FRAMEWORK (Use these psychological triggers and structure):",
            viral_framework,
            "\n2. CONTENT ANGLE (Use this specific slide-by-slide structure):",
            angle_content,
            "\n3. TONE OF VOICE (Write exactly like this):",
            tone_content,
            "\n4. HUMANIZER INSTRUCTIONS (Apply these rules to the final output):",
            humanizer
        ]

        if include_caption:
            caption_content = load_file(os.path.join(PROMPTS_DIR, 'caption_writer.txt'))
            prompt_parts.append("\n5. CAPTION GUIDELINES:")
            prompt_parts.append(caption_content)

        if include_meme:
            meme_content = load_file(os.path.join(PROMPTS_DIR, 'meme_analyzer.txt'))
            prompt_parts.append("\n6. MEME MATCHING STRATEGY:")
            prompt_parts.append(meme_content)

        prompt_parts.append("</CONTEXT_AND_RULES>\n")
        prompt_parts.append("<TASK>")
        prompt_parts.append(f"Topic: {topic}")
        prompt_parts.append("\nGenerate the content following the structures above.")
        prompt_parts.append("</TASK>")

        full_prompt = "\n".join(prompt_parts)
        
        st.text_area("Copy this prompt:", value=full_prompt, height=600)
        st.success("Prompt generated! Copy and paste into your LLM.")
    
    elif generate_btn:
        st.warning("Please fill in the topic and ensure angle/tone files exist.")
    else:
        st.info("Configure the settings on the left and click Generate.")