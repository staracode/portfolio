import streamlit as st
from llama_cpp import Llama
import os
import re
import requests
import json

# Configure the page
st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🏥",
    layout="centered"
)

# SNOMED CT API configuration
SNOMED_API_BASE = "https://browser.ihtsdotools.org/snowstorm/snomed-ct"
SNOMED_API_KEY = st.secrets["SNOMED_API_KEY"]  # Store this securely in Streamlit secrets

# Medical system prompt
MEDICAL_SYSTEM_PROMPT = """You are a medical AI assistant. Please:
1. Provide accurate, evidence-based medical information
2. Always include relevant medical context
3. Be clear about limitations and uncertainties
4. Include relevant medical terminology
5. Maintain professional medical communication standards
6. Always recommend consulting healthcare professionals for specific medical advice

Remember: This is for informational purposes only and not a substitute for professional medical advice."""

def get_snomed_concepts(query):
    """Query SNOMED CT API for relevant medical concepts"""
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en",
        "Authorization": f"Bearer {SNOMED_API_KEY}"
    }
    
    params = {
        "term": query,
        "limit": 10,
        "offset": 0,
        "searchMode": "STANDARD"
    }
    
    try:
        response = requests.get(
            f"{SNOMED_API_BASE}/browser/MAIN/descriptions",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.warning(f"Error querying SNOMED CT: {str(e)}")
        return None

def validate_medical_context(text):
    """Validate if the text contains medical concepts using SNOMED CT"""
    concepts = get_snomed_concepts(text)
    if concepts and concepts.get("items"):
        return True, concepts["items"]
    return False, []

# Initialize the model
@st.cache_resource
def load_model():
    try:
        return Llama(
            model_path="capybarahermes-2.5-mistral-7b.Q4_K_M.gguf",
            temperature=0.3,  # Lower temperature for more precise responses
            max_tokens=512,   # Increased for more detailed medical explanations
            top_p=0.9,        # Slightly reduced for more focused responses
            n_ctx=2048,
            verbose=True,
        )
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# Load the model
llm = load_model()

# Main UI
st.title("🏥 Medical AI Assistant")
st.markdown("""
This AI assistant is designed to provide medical information and context. 
Please note that this is for informational purposes only and not a substitute for professional medical advice.
""")

# Input area
user_input = st.text_area(
    "Your medical question",
    placeholder="Type your medical question here...",
    height=100
)

# Add a clear button
if st.button("Clear"):
    st.session_state.clear()
    st.experimental_rerun()

# Process the input
if user_input:
    if not user_input.strip():
        st.warning("Please enter a medical question!")
    else:
        # Validate medical context using SNOMED CT
        is_medical, medical_concepts = validate_medical_context(user_input)
        
        if not is_medical:
            st.warning("Your question might not be medical-related. Please ensure you're asking about medical topics.")
        else:
            # Display relevant medical concepts
            st.info("Identified medical concepts:")
            for concept in medical_concepts:
                st.write(f"- {concept['term']} (SNOMED CT ID: {concept['conceptId']})")
        
        with st.spinner("Analyzing your medical question..."):
            try:
                # Create a prompt with medical context
                full_prompt = f"{MEDICAL_SYSTEM_PROMPT}\n\nQuestion: {user_input}\n\nAnswer:"
                
                response = llm.create_completion(
                    full_prompt,
                    max_tokens=512,
                    temperature=0.3,
                    top_p=0.9,
                )
                
                st.markdown("### Medical Response")
                response_text = response['choices'][0]['text']
                
                # Add a disclaimer
                st.markdown("""
                ---
                **Disclaimer**: This information is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
                """)
                
                st.write(response_text)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")