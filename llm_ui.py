#!/usr/bin/env python3
"""
Streamlit UI for interacting with an LLM.
"""

import os
import streamlit as st
from llm_test import call_llm, get_system_prompt
from PIL import Image
import pandas as pd
from bigquery_runner import init_client, run_query

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
    # Set page configuration
    st.set_page_config(
        page_title="Amboss LLM Chat",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize session state for BigQuery client if it doesn't exist
    if 'bq_client' not in st.session_state:
        st.session_state.bq_client = None
    
    # Display logo in the sidebar
    logo_path = "assets/amboss_logo.png"
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            st.sidebar.image(logo, width=200)
        except Exception as e:
            st.sidebar.warning(f"Error loading logo: {str(e)}")
            st.sidebar.info("Run create_logo.py to generate a placeholder logo")
    else:
        st.sidebar.warning("Logo file not found. Please run create_logo.py to generate a placeholder logo")
    
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
    
    # BigQuery section in sidebar
    st.sidebar.header("BigQuery")
    project_id = st.sidebar.text_input("Project ID", value="datawarehouse-385707")
    
    # Connect to BigQuery button
    if st.sidebar.button("Connect to BigQuery"):
        with st.sidebar.spinner("Connecting..."):
            try:
                st.session_state.bq_client = init_client(project_id)
                st.sidebar.success("Connected to BigQuery!")
            except Exception as e:
                st.sidebar.error(f"Failed to connect: {str(e)}")
    
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
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["Chat Input", "BigQuery"])
    
    with tab1:
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
    
    with tab2:
        # BigQuery input
        st.subheader("Run BigQuery SQL")
        sql_query = st.text_area("Enter SQL query:", height=150)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Run Query"):
                if not st.session_state.bq_client:
                    st.error("Please connect to BigQuery first!")
                elif sql_query:
                    with st.spinner("Running query..."):
                        try:
                            results = run_query(st.session_state.bq_client, sql_query)
                            st.session_state.query_results = results
                            st.success("Query executed successfully!")
                        except Exception as e:
                            st.error(f"Query error: {str(e)}")
        
        with col2:
            if st.button("Send Results to LLM"):
                if not hasattr(st.session_state, 'query_results') or st.session_state.query_results is None:
                    st.error("No query results to send!")
                else:
                    # Convert DataFrame to string representation
                    df_str = st.session_state.query_results.to_string()
                    prompt = f"Here are the results of my SQL query:\n\n{df_str}\n\nPlease analyze these results and provide insights."
                    
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    
                    # Get LLM response
                    with st.spinner("Thinking..."):
                        response = call_llm(prompt, selected_prompt)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Rerun to update the UI
                    st.rerun()
        
        # Display query results if available
        if hasattr(st.session_state, 'query_results') and st.session_state.query_results is not None:
            st.subheader("Query Results")
            st.dataframe(st.session_state.query_results)

    # Add footer with Amboss branding
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: gray;'>Powered by Amboss SE</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
