import sys, os

from dotenv import load_dotenv
load_dotenv(verbose=True)

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI # 채팅 모드 # please add an environment variable `OPENAI_API_KEY`
from langchain.llms import OpenAI # 질문을 주면 글을 이어서 써준다. --> complete mode
from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler

import tempfile

import streamlit as st
from streamlit_extras.buy_me_a_coffee import button
#################
# buy me a coffee
#################
# button(username="arcana", floating=True, width=221)

# title
st.title("ChatPDF")
st.write("---")

# 파일 업로드
uploaded_file = st.file_uploader("Choose a PDF file",
                                type = ["pdf"])
st.write("---")

########
# Loader
########
# loader = PyPDFLoader("taro.pdf")
# pages = loader.load_and_split()

def pdf2document(uploaded_file):
    temp_dir =tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getvalue())
    loader = PyPDFLoader(temp_filepath)
    pages = loader.load_and_split()
    return pages


# 업로드시 동작
if uploaded_file is not None:
    pages = pdf2document(uploaded_file)

    # split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 20,
        length_function = len,
        is_separator_regex = False,
    )
    texts = text_splitter.split_documents(pages)

    #Embedding
    embeddings_model = OpenAIEmbeddings()

    db = Chroma.from_documents(texts, embeddings_model) # persist_directory="/chroma"

    class StreamHandler(BaseCallbackHandler):
        def __init__(self, container, initial_text=""):
            self.container = container
            self.text = initial_text
        def on_llm_new_token(self, token:str, **kwargs) -> None:
            self.text += token
            self.container.markdown(self.text)

    # Question
    st.header("질문하세요")
    question = st.text_input("질문을 입력하세요")
    # question = "하이"

    if st.button("질문하기"):
        with st.spinner("Wait for it..."):
            chat_box = st.empty()
            stream_handler = StreamHandler(chat_box)

            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0,
                            streaming=True, callbacks=[stream_handler]) #StreamingStdOutCallbackHandler()
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
            result = qa_chain({"query": question})
            # print(result)
            # st.write(result["result"])