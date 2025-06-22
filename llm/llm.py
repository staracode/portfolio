import streamlit as st
from llama_cpp import Llama
import os
import re
import requests
import json
from typing import List, Dict, Tuple

# Try to import pyhpo, install if not available
try:
    import pyhpo
    from pyhpo import Ontology, HPOTerm
    PYHPO_AVAILABLE = True
except ImportError:
    PYHPO_AVAILABLE = False
    st.warning("pyhpo not installed. Installing...")
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyhpo"])
        import pyhpo
        from pyhpo import Ontology, HPOTerm
        PYHPO_AVAILABLE = True
        st.success("pyhpo installed successfully!")
    except Exception as e:
        st.error(f"Failed to install pyhpo: {str(e)}")

# Configure the page
st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🏥",
    layout="centered"
)

# Medical keywords for validation (fallback)
MEDICAL_KEYWORDS = {
    'symptoms': [
        'pain', 'fever', 'headache', 'nausea', 'vomiting', 'diarrhea', 'constipation',
        'cough', 'sore throat', 'runny nose', 'fatigue', 'dizziness', 'shortness of breath',
        'chest pain', 'abdominal pain', 'back pain', 'joint pain', 'muscle pain',
        'rash', 'itching', 'swelling', 'bruising', 'bleeding', 'numbness', 'tingling'
    ],
    'conditions': [
        'diabetes', 'hypertension', 'asthma', 'arthritis', 'cancer', 'heart disease',
        'stroke', 'depression', 'anxiety', 'obesity', 'allergies', 'infection',
        'inflammation', 'tumor', 'cyst', 'ulcer', 'hernia', 'fracture', 'sprain'
    ],
    'body_parts': [
        'head', 'neck', 'chest', 'abdomen', 'back', 'arm', 'leg', 'hand', 'foot',
        'eye', 'ear', 'nose', 'mouth', 'throat', 'heart', 'lung', 'liver', 'kidney',
        'stomach', 'intestine', 'brain', 'spine', 'joint', 'muscle', 'bone'
    ],
    'treatments': [
        'medication', 'surgery', 'therapy', 'vaccination', 'antibiotics', 'painkillers',
        'anti-inflammatory', 'chemotherapy', 'radiation', 'physical therapy',
        'occupational therapy', 'psychotherapy', 'diet', 'exercise', 'rest'
    ]
}

# Medical system prompt
MEDICAL_SYSTEM_PROMPT = """You are a medical AI assistant. Please:
1. Provide accurate, evidence-based medical information
2. Always include relevant medical context
3. Be clear about limitations and uncertainties
4. Include relevant medical terminology
5. Maintain professional medical communication standards
6. Always recommend consulting healthcare professionals for specific medical advice

Remember: This is for informational purposes only and not a substitute for professional medical advice."""

@st.cache_resource
def load_hpo_ontology():
    """Load HPO ontology using pyhpo"""
    if not PYHPO_AVAILABLE:
        return None
    
    try:
        # Initialize the ontology
        Ontology()
        return True
    except Exception as e:
        st.error(f"Error loading HPO ontology: {str(e)}")
        return None

def search_hpo_terms(search_term: str) -> List[Dict]:
    """Search for HPO terms using pyhpo"""
    if not PYHPO_AVAILABLE:
        return []
    
    try:
        from pyhpo import Ontology
        
        search_results = []
        search_term_lower = search_term.lower()
        
        # Use pyhpo's built-in search methods
        # Method 1: Direct search
        try:
            search_results.extend(Ontology.search(search_term))
        except:
            pass
        
        # Method 2: Synonym search
        try:
            synonym_results = Ontology.synonym_search(search_term)
            search_results.extend(synonym_results)
        except:
            pass
        
        # Convert to standardized format
        formatted_results = []
        seen_ids = set()
        
        for term in search_results:
            if term.id not in seen_ids:
                formatted_results.append({
                    'id': term.id,
                    'name': term.name,
                    'definition': getattr(term, 'definition', '') or '',
                    'synonyms': [],  # pyhpo doesn't expose synonyms directly
                    'source': 'HPO',
                    'method': 'pyhpo'
                })
                seen_ids.add(term.id)
                
                # Limit results to avoid overwhelming
                if len(formatted_results) >= 10:
                    break
        
        return formatted_results
        
    except Exception as e:
        st.warning(f"Error searching HPO with pyhpo: {str(e)}")
        return []

def validate_medical_context(text: str) -> Tuple[bool, List[Dict]]:
    """Validate if the text contains medical concepts using HPO and fallback keywords"""
    found_terms = []
    
    # First try HPO search with pyhpo
    words = text.lower().split()
    for word in words:
        if len(word) > 3:  # Only search for meaningful terms
            hpo_terms = search_hpo_terms(word)
            found_terms.extend(hpo_terms)
    
    # If no HPO terms found, use fallback keyword matching
    if not found_terms:
        text_lower = text.lower()
        for category, keywords in MEDICAL_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_terms.append({
                        'id': f'keyword_{keyword}',
                        'name': keyword,
                        'category': category,
                        'confidence': 'high' if keyword in text_lower.split() else 'medium',
                        'source': 'keyword'
                    })
    
    return len(found_terms) > 0, found_terms

def display_medical_terms(terms: List[Dict]):
    """Display identified medical terms"""
    if not terms:
        return
    
    st.info("Identified medical concepts:")
    
    # Group by source
    hpo_terms = [t for t in terms if t.get('source') == 'HPO']
    keyword_terms = [t for t in terms if t.get('source') == 'keyword']
    
    if hpo_terms:
        st.subheader("🏥 HPO Ontology Terms")
        for term in hpo_terms:
            with st.expander(f"{term['name']} (HPO:{term['id']})"):
                st.write(f"**HPO ID:** {term['id']}")
                if term.get('definition'):
                    st.write(f"**Definition:** {term['definition']}")
                if term.get('synonyms'):
                    st.write(f"**Synonyms:** {', '.join(term['synonyms'][:5])}")
                st.write("**Source:** Human Phenotype Ontology (pyhpo)")
    
    if keyword_terms:
        st.subheader("🔍 Medical Keywords")
        for term in keyword_terms:
            with st.expander(f"{term['name'].title()} ({term['category']})"):
                st.write(f"**Category:** {term['category'].replace('_', ' ').title()}")
                st.write(f"**Confidence:** {term['confidence']}")
                
                # Add educational context
                if term['category'] == 'symptoms':
                    st.write("**Note:** This appears to be a symptom. Consider consulting a healthcare provider for proper diagnosis.")
                elif term['category'] == 'conditions':
                    st.write("**Note:** This appears to be a medical condition. Professional medical evaluation is recommended.")
                elif term['category'] == 'body_parts':
                    st.write("**Note:** This refers to a body part. Consider the specific symptoms or concerns related to this area.")
                elif term['category'] == 'treatments':
                    st.write("**Note:** This refers to a treatment option. Always consult healthcare professionals for appropriate treatment.")

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

# Load the model and HPO ontology
llm = load_model()
hpo_loaded = load_hpo_ontology()

# Main UI
st.title("🏥 Medical AI Assistant")
st.markdown("""
This AI assistant is designed to provide medical information and context using HPO (Human Phenotype Ontology) and medical keyword validation.
Please note that this is for informational purposes only and not a substitute for professional medical advice.
""")

# Show HPO status
if hpo_loaded:
    st.success("✅ HPO Ontology loaded successfully using pyhpo")
else:
    st.warning("⚠️ HPO Ontology not available, using keyword fallback only")

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
        # Validate medical context using HPO and keywords
        is_medical, medical_terms = validate_medical_context(user_input)
        
        if not is_medical:
            st.warning("Your question might not be medical-related. Please ensure you're asking about medical topics.")
        else:
            # Display relevant medical terms
            display_medical_terms(medical_terms)
        
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