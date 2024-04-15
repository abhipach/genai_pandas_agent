from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
import streamlit as st
import pandas as pd
import os
import textwrap


def clear_submit():
    """
    Clear the Submit Button State
    Returns:

    """
    st.session_state["submit"] = False


#@st.cache_data(ttl="2h")


st.set_page_config(page_title="Mangalyaan Chatbot", page_icon="🤖")
st.title("Customer Support ChatBot🤖")

#df1 = pd.read_csv("F:\\Virtusa_Gen_AI_Hackathon\\Pandas_Agent\\bankingpaymentsFAQqueries.csv")
df2 = pd.read_csv("F:\\Virtusa_Gen_AI_Hackathon\\Pandas_Agent\\bankingpaymentsFAQ.csv")
df =df2
#if df1 is not None and df2 is not None:
    #df = df1.to_string(index=False) + '\n' + df2.to_string(index=False)
 #   df = pd.concat([df1, df2], ignore_index=True)
           









print(df)
#openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

openai_api_key = "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"
customer_name="Abhishek"

if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
    st.session_state["messages"] = [{"role": "assistant", "content":  f"Hi {customer_name}! Welcome to our Customer Support ChatBot for payments and banking! 🏦💳\n\nHow can we assist you today? Whether you have questions about transactions, account balances, or any other banking inquiries, feel free to ask. We're here to help you with any payment-related or banking-related concerns you may have.\n\nSimply type your query in the chatbox below, and we'll provide you with the assistance you need.\n\nLet's get started! 🚀"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
       st.info("Please add your OpenAI API key to continue.")
       st.stop()

    llm = ChatOpenAI(
       temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=openai_api_key, streaming=True)
    

    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=True,
    )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)