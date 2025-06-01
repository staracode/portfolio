import streamlit as st
from llama_cpp import Llama
import os
import re

# Configure the page
st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🏥",
    layout="centered"
)

# Medical system prompt
MEDICAL_SYSTEM_PROMPT = """You are a medical AI assistant. Please:
1. Provide accurate, evidence-based medical information
2. Always include relevant medical context
3. Be clear about limitations and uncertainties
4. Include relevant medical terminology
5. Maintain professional medical communication standards
6. Always recommend consulting healthcare professionals for specific medical advice

Remember: This is for informational purposes only and not a substitute for professional medical advice."""

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
        # Basic medical context validation
        medical_keywords = ['symptom', 'diagnosis', 'treatment', 'disease', 'condition', 
                          'medicine', 'drug', 'patient', 'doctor', 'hospital', 'medical',
                          'health', 'illness', 'pain', 'therapy', 'clinical']
        
        has_medical_context = any(keyword in user_input.lower() for keyword in medical_keywords)
        
        if not has_medical_context:
            st.warning("Your question might not be medical-related. Please ensure you're asking about medical topics.")
        
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


