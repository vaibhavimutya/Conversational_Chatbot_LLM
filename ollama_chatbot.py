import streamlit as st
from langchain_ollama import ChatOllama  # Connection between LangChain and Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate


model = ChatOllama(model='llama3.2', base_url='http://localhost:11434')

# System Message
system_message = SystemMessagePromptTemplate.from_template("Your AI friend")

# Set page configuration
st.set_page_config(page_title="Conversational Chatbot", layout="wide")

st.title("🤖 Conversational Chatbot")

st.write("Using Ollama and LangChain")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'last_response' not in st.session_state:
    st.session_state['last_response'] = ""

# Layout with two columns
col1, col2 = st.columns([3, 1])  # Left: Input & Response, Right: Chat History

with col1:
    with st.form("chat-form"):
        input_text = st.text_area("Hello, what do you want to talk about today? 😊", height=100)
        
        submit_button = st.form_submit_button("Submit")

        def get_chat_history():
            chat_history = [system_message]
            for chat in st.session_state['chat_history']:
                prompt = HumanMessagePromptTemplate.from_template(chat['user'])
                chat_history.append(prompt)
                ai_message = AIMessagePromptTemplate.from_template(chat['AI friend'])
                chat_history.append(ai_message)
            return chat_history

        def generate_response(chat_history):
            chat_template = ChatPromptTemplate.from_messages(chat_history)
            chain = chat_template | model | StrOutputParser()
            response = chain.invoke({})
            return response

        if submit_button and input_text:
            with st.spinner("Thinking..."):
                user_prompt = HumanMessagePromptTemplate.from_template(input_text)
                chat_history = get_chat_history()
                chat_history.append(user_prompt)

                response = generate_response(chat_history)
                
                st.session_state['chat_history'].append({'user': input_text, 'AI friend': response})
                st.session_state['last_response'] = response

    # Display the latest response just below the submit button
    if st.session_state['last_response']:
        st.markdown(f"**🤖 AI Friend:** {st.session_state['last_response']}")

with col2:
    st.markdown("### Chat History", unsafe_allow_html=True)
    # st.write(st.session_state['chat_history'])
    for c in reversed(st.session_state['chat_history']):
        st.write(f"**User**: {c['user']}")
        st.write(f"**🤖 AI friend**: {c['AI friend']}")
        st.write("---")

# Custom CSS for Styling
st.markdown(
    """
    <style>
        body {
            background-color: #2c3e50;
            color: white;
            font-family: Arial, sans-serif;
        }

        .stTextArea textarea {
            font-size: 12px;
            color: white;
        }

        .stButton>button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #f1c40f;
            color: black;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }

        .stTextInput input, .stTextArea textarea {
            width: 100%; /* Increase form width */
            height: 500px; /* Increase form height */
            padding: 15px; /* Increase padding */
            font-size: 1em; /* Increase text size inside inputs */
            margin-bottom: 0px;
            border-radius: 8px; /* Rounded corners */
            background-color: #34495e; /* Darker input background */
            color: white;
        }

        .stButton>button:hover {
            background-color: #c0392b;
        }

        .stApp {
            padding: 20px;
        }

        h2 {
            color: #ecf0f1;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)
