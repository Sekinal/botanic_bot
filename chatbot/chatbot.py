from openai import OpenAI
from rich import print
import streamlit as st

@st.cache_data
def create_thread():
    return client.beta.threads.create()

@st.cache_data
def retrieve_assistant():
    return client.beta.assistants.retrieve("asst_xnzJ83ZR7AFV47SxctzU1e4U")

client = OpenAI(
    api_key = st.secrets["OPENAI_API_KEY"]
)

assistant = retrieve_assistant()

thread = create_thread()

st.title("BOTanic - Your botanic chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to ask?"):
    with st.chat_message("User"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )

    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )
    
    for thread_message in messages.data:
        if thread_message.role == "user":
            break
        else:
            with st.chat_message("Assistant"):
                assistant_response = messages.data[0].content[0].text.value
                print(assistant_response)
                st.markdown(assistant_response)
                
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
