#!/usr/bin/env python3
"""
Streamlit UI for interacting with an LLM.
"""

import os
import streamlit as st
from llm_test import call_llm, get_system_prompt

def get_available_prompts():
    """
    Get a list of all available system prompts in the prompts directory.
    
    Returns:
        list: List of prompt names without the .md extension
    """
    prompts_dir = "./prompts"
    if not os.path.exists(prompts_dir):
        return ["system_prompt"]
    
    prompt_files = [f[:-3] for f in os.listdir(prompts_dir) if f.endswith('.md')]
    if not prompt_files:
        return ["system_prompt"]
    
    return prompt_files

def main():
    """
    Main function to create the Streamlit UI.
    """
    st.title("LLM Chat Interface")
    
    # Initialize session state for chat history if it doesn't exist
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar for system prompt selection
    st.sidebar.header("Settings")
    available_prompts = get_available_prompts()
    selected_prompt = st.sidebar.selectbox(
        "Select System Prompt",
        available_prompts,
        index=available_prompts.index("system_prompt") if "system_prompt" in available_prompts else 0
    )
    
    # Display the content of the selected prompt
    with st.sidebar.expander("View Selected Prompt"):
        st.write(get_system_prompt(selected_prompt))
    
    # Button to restart chat
    if st.sidebar.button("Restart Chat"):
        st.session_state.messages = []
        st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write("You:")
            st.text_area("", message["content"], height=100, key=f"user_{len(st.session_state.messages)}", disabled=True)
        else:
            st.write("Assistant:")
            st.text_area("", message["content"], height=200, key=f"assistant_{len(st.session_state.messages)}", disabled=True)
    
    # User input
    user_input = st.text_area("Enter your message:", height=150)
    
    # Submit button
    if st.button("Send to LLM"):
        if user_input:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get LLM response
            with st.spinner("Thinking..."):
                response = call_llm(user_input, selected_prompt)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to update the UI
            st.rerun()

if __name__ == "__main__":
    main()
