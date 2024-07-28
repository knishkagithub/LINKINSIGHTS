import streamlit as st
import pickle
import time
from langchain.llms import openai
from openai import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
import google.generativeai as genai 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os
# os.environ['OPEN_API_KEY'] = "newskey"

from dotenv import load_dotenv
load_dotenv()

st.title("NEWS RESEARCH TOOL📰🗞️")

st.sidebar.title("news research urls")

urls=[]
for i in range(3):
    url=st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)


process_url_clicked = st.sidebar.button("Process URLs")
file_path= "faiss_store_openai.pkl"

main_placefolder=st.empty()
llm=OpenAI(  )
if process_url_clicked:
    loader=UnstructuredURLLoader(urls=urls)
    main_placefolder.text("DATA LOADING....STARTED....✅✅✅✅")
    data=loader.load()
    text_splitter= RecursiveCharacterTextSplitter(
        separators=['\n\n' ,'\n', ',' , '.'],
        chunk_size=1000
    )
    main_placefolder.text("kTEXT SPLITTER....STARTED....✅✅✅✅")
    docs= text_splitter.split_documents(data)
    ##create embeddings are save it to FASS 
    embeddings=OpenAIEmbeddings()
    vectorstore_openai=FAISS.from_documents(docs,embeddings)
    main_placefolder.text("Embedding vector started building....✅✅✅✅")
    time.sleep()
    
    #save faiss as a pickle file
    with open(file_path, "wb") as f: 
        pickle.dump(vectorstore_openai,f)   

query=main_placefolder.text_input("Question:")
if query:
    if os.path.exists(file_path):
        with open(file_path,"rb") as f:
            vector_store=pickle.load(f)
            chain=RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vector_store.as_retriever)
            result=chain({"question": query}, return_only_outputs= True)
            st.header("answer")
            st.subheader(result["answer"])
            sources=result.get("sources","")
            if sources:
                st.subheader("Sources:")
                sources_list=sources.split("\n")
                for source in sources_list:
                    st.write(source)
