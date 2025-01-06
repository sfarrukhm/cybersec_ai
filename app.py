import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()
gemini_api=os.getenv("gemini_api")
openai_api=os.getenv("openai_api")
os.environ['GOOGLE_API_KEY']=gemini_api
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_openai.chat_models import ChatOpenAI
# llm = ChatOpenAI(model="gpt-4o-mini",api_key=openai_api, temperature=0)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp",   api_key=gemini_api)

from langgraph.graph import StateGraph, END,START
from langgraph.prebuilt import ToolNode,tool_node, create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool

from pydantic import BaseModel, Field
from typing import TypedDict, List, Dict, Union





def main():
    st.set_page_config(page_title="IP Investigator",page_icon=":dark_sunglasses:")
    with st.sidebar:
        
        vt_api_key=st.text_input(label="Enter your VirusTotal API key")
        st.subheader("Query")
        query=st.chat_input(key="user_input",)

        @tool
        def get_ip_all_details(input_ip:str):
            """Get details related to provided IP address"""

            headers = {
            "accept": "application/json",
            "x-apikey": vt_api_key}
            url = "https://www.virustotal.com/api/v3/ip_addresses/"

            ip_to_search=input_ip
            response = requests.get(url+ip_to_search, headers=headers)
            if response.status_code==200:
                return response.text
            else:
                return "Provided input is not a correct IP address"
        tools=[get_ip_all_details]

        system_prompt = f"""
            You are a skilled cybersecurity analyst tasked with evaluating IP addresses. 
            Your role is to use the VirusTotal tool to gather relevant information about the IP address provided. 
            Analyze the VirusTotal results thoroughly and provide:
            1. A concise summary of key findings, including reputation, associated tags, and analysis results.
            2. Clear and actionable recommendations based on the analysis.
            Ensure your analysis is precise and actionable. Write your response in Markdown format.

            """

        memory=MemorySaver()
        graph=create_react_agent(model=llm, tools=tools,checkpointer=memory, state_modifier=system_prompt )
        
        thread={"configurable":{"thread_id":"1"}}

        result = None
        if vt_api_key and query:
            response=graph.invoke({"messages":query},config=thread)
            result=response['messages'][-1].content

    if result:
        st.markdown(result)



if __name__=="__main__":
    main()
    # st.session_state

    
