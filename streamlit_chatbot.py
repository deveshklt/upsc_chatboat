import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

# Set page title and favicon
st.set_page_config(page_title="PDF Chatbot", page_icon=":robot_face:")

# Set app title and description
st.title("PDF Chatbot")
st.markdown("Upload a PDF file and ask a question to get answers!")

# Set background color and padding for the entire app
st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(to right, #11998e, #38ef7d);
        padding: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Ask question
question = st.text_input("Ask your question")

if uploaded_file is not None and question:
    # Save uploaded file to a temporary location
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load and split the PDF file
    loader = PyPDFLoader("temp.pdf")
    data = loader.load_and_split()

    # Create vector store
    vectorstore = Chroma.from_documents(documents=data, embedding=OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY')))

    # Retrieve relevant documents
    retriever = vectorstore.as_retriever(k=4)
    docs = retriever.invoke(question)

    # Chat initialization
    chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2, openai_api_key=os.environ.get('OPENAI_API_KEY'))

    # Set up system template
    SYSTEM_TEMPLATE = """
    Answer the user's questions based on the below context. 
    If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know":
    
    <context>
    {context}
    </context>
    """

    # Set up question answering prompt
    question_answering_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_TEMPLATE,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    # Create document chain
    document_chain = create_stuff_documents_chain(chat, question_answering_prompt)

    # Invoke document chain with user's question
    answer = document_chain.invoke({"context": docs, "messages": [HumanMessage(content=question)]})

    # Display the answer with colorful background
    st.success("Here's your answer:")
    st.markdown(
        f"""
        <div style='background-color:#84fab0; padding: 10px; border-radius: 10px;'>
            {answer}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Remove temporary file
    os.remove("temp.pdf")
