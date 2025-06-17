import streamlit as st
import json
from sarvamai import SarvamAI
from typing import List, Dict
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Note: Custom styling is now handled via .streamlit/config.toml

# Configure Streamlit page
st.set_page_config(
    page_title="Sarvam AI Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to override default chat message styling
st.markdown("""
<style>
.st-emotion-cache-1bp69zu {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 1rem;
    border-radius: 0.6rem;
    background-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize Sarvam AI client
@st.cache_resource
def get_sarvam_client():
    """Initialize and cache the Sarvam AI client"""
    api_key = os.getenv("SARVAM_API_KEY") or st.secrets.get("SARVAM_API_KEY", "")
    if not api_key:
        st.error("❌ Sarvam AI API key not found! Please set SARVAM_API_KEY in your environment or Streamlit secrets.")
        st.stop()
    return SarvamAI(api_subscription_key=api_key)

def extract_thinking_and_response(text: str) -> tuple[str, str]:
    """Extract thinking process and clean response from AI output"""
    # Look for thinking tags
    thinking_pattern = r'<think>(.*?)</think>'
    thinking_matches = re.findall(thinking_pattern, text, re.DOTALL)
    
    # Extract thinking content
    thinking_content = ""
    if thinking_matches:
        thinking_content = thinking_matches[0].strip()
    
    # Remove thinking tags from response
    clean_response = re.sub(thinking_pattern, '', text, flags=re.DOTALL).strip()
    
    return thinking_content, clean_response

def get_ai_response(messages: List[Dict[str, str]], **kwargs) -> str:
    """Get response from Sarvam AI with advanced parameters"""
    try:
        client = get_sarvam_client()
        
        # Prepare API parameters
        api_params = {
            "messages": messages,
            **kwargs  # Include all additional parameters
        }
        
        response = client.chat.completions(**api_params)
        
        # Extract the content from the response object
        if response and hasattr(response, 'choices') and len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            return "Sorry, I couldn't generate a response. Please try again."
            
    except Exception as e:
        st.error(f"Error calling Sarvam AI: {str(e)}")
        return "Sorry, there was an error processing your request."

def main():
    # App title and description
    st.header("What can I help with?")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Reasoning effort
        reasoning_effort = st.selectbox(
            "🧠 Reasoning Effort",
            options=["low", "medium", "high"],
            index=1,
            help="Higher effort for complex reasoning tasks"
        )
        
        # Wiki grounding
        wiki_grounding = st.toggle(
            "📚 Wikipedia Grounding",
            value=False,
            help="Use Wikipedia knowledge for factual accuracy (Note: Wikipedia may not have the most recent events)"
        )
        
        if wiki_grounding:
            st.info("⚠️ Wiki grounding uses Wikipedia data, which may not include very recent events or breaking news.")
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Conversation", type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            # Use custom avatar for assistant messages
            if message["role"] == "assistant":
                with st.chat_message("assistant", avatar="image (7) (1).png"):
                    st.markdown(message["content"])
            else:
                with st.chat_message(message["role"],avatar="736198_480.png"):
                    st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user", avatar="736198_480.png"):
            st.markdown(prompt)
        
        # Prepare messages for API (include system message)
        api_messages = []
        
        # Use shorter system prompt when wiki grounding is enabled to save tokens
        if wiki_grounding:
            comprehensive_system_prompt = """You are a helpful AI assistant. Be concise, accurate, and acknowledge when Wikipedia data may not include recent events. Suggest checking current news sources for recent information."""
        else:
            comprehensive_system_prompt = """You are an exceptionally helpful, knowledgeable, and versatile AI assistant built by Sarvam AI. Your goal is to provide the most useful, accurate, and engaging responses possible.

            Key principles:
            - Be thorough yet concise - provide complete answers without being verbose
            - Show your reasoning when helpful - explain your thought process for complex topics
            - Be practical and actionable - give specific steps, examples, or solutions when possible
            - Adapt your communication style to the user's needs and context
            - Be honest about limitations - say when you're uncertain or need clarification
            - Stay curious and ask follow-up questions when it would help the user

            Always aim to:
            1. Understand the user's real need behind their question
            2. Provide comprehensive yet digestible information
            3. Offer multiple perspectives when relevant
            4. Give practical next steps or actionable advice
            5. Make complex topics accessible and engaging

            Be conversational, friendly, and genuinely helpful in every interaction."""

        api_messages.append({"role": "system", "content": comprehensive_system_prompt})
        
        # Add conversation history
        for msg in st.session_state.messages:
            api_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Prepare API parameters with good defaults
        # Use fewer max_tokens when wiki grounding is enabled to save space for Wikipedia content
        max_tokens = 512 if wiki_grounding else 1024
        
        api_params = {
            "temperature": 0.7,  # Balanced creativity
            "top_p": 0.9,  # Good diversity
            "max_tokens": max_tokens,
            "reasoning_effort": reasoning_effort,
            "frequency_penalty": 0.3,  # Slight repetition control
            "presence_penalty": 0.2,  # Slight topic diversity
            "wiki_grounding": wiki_grounding
        }
        
        # Get AI response with custom avatar
        with st.chat_message("assistant", avatar="image (7) (1).png"):
            with st.spinner("🧠 Thinking..."):
                full_response = get_ai_response(api_messages, **api_params)
                thinking_content, clean_response = extract_thinking_and_response(full_response)
                
                # Always show thinking process in an expandable section
                if thinking_content:
                    with st.expander("🤔 AI's Thinking Process", expanded=False):
                        st.markdown(f"*{thinking_content}*")
                        st.caption("This shows how the AI reasoned through your question")
                
                # Display the clean response
                if clean_response:
                    st.markdown(clean_response)
                else:
                    # If no clean response, show original (no thinking tags were found)
                    st.markdown(full_response)
            
            # Add assistant response to chat history (store clean response)
            response_to_store = clean_response if clean_response else full_response
            st.session_state.messages.append({"role": "assistant", "content": response_to_store})

if __name__ == "__main__":
    main() 