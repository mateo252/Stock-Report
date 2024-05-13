import streamlit as st
import platform
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


st.set_page_config(
    page_title = "Trading report",
    page_icon = "📈"
)


## Preparing AI model
@st.cache_resource
def load_llama_model():
    return Ollama(model="llama2")

# Load llama model
llm = load_llama_model()
ai_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a humble but very experienced mathematician and have knowledge in the field of finance."),
    ("user", "{input}")
])
chain = ai_prompt | llm | StrOutputParser()

# Sidebar for current model (only one)
with st.sidebar:
    st.text_input("Current model", "llama2", disabled=True)
    
    
# Main chat
## Header of chat
st.subheader("Talk with a AI support 🤓", divider="blue")

## Make messages history for AI
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", 
                                     "content": "Hey? How can I help you?",
                                     "avatar": "🧠"}]

## Display initial message from AI
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"], avatar=msg["avatar"]).write(msg["content"])
    

## Get user input
if user_prompt := st.chat_input(placeholder="Your question...", max_chars=255):
    st.chat_message("user", avatar="😎").write(user_prompt)
    st.session_state["messages"].append({"role": "user", 
                                         "content": user_prompt,
                                         "avatar": "😎"})
    
    ai_response = chain.stream({"input": user_prompt})
    with st.chat_message("assistant", avatar="🧠"):
        ai_response = st.write_stream(ai_response)

    st.session_state["messages"].append({"role": "assistant", 
                                         "content": ai_response,
                                         "avatar": "🧠"})
