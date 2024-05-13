import streamlit as st


st.set_page_config(
    page_title = "Trading report",
    page_icon = "📈"
)

with st.sidebar:
    st.write("")

st.title("Trading report 📈")
st.subheader("How does it work? 🤔", divider="blue")

markdown_text = """
This project aimed to create a page that will prepare a brief summary in the form of charts of trading results.

On the site you can see three pages:
- **About** 📈 - this is the current page, which shows instructions on how to use the various elements of the page,
- **Report** 📄 - there are four key elements on the page:
    - Loading file widget - simply for loading a file in csv form
    - Table - contains main columns on which operations are performed. The user can enter custom column names from his file to correspond to those used by the system,
    - Date format - date format used in 'Close time' and 'Open time' columns
    - Balance - initial balance of the account,
- **AI-Support** 🧠 - a page where you can talk to the bot about subject you want. 

**No API key is needed for the bot chat service.**
"""

st.markdown(markdown_text)
