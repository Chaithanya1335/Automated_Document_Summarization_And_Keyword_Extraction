# Importing the Necessary packages
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from PyPDF2 import PdfReader
import os
from keybert import KeyBERT
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
from urllib.parse import quote_plus
load_dotenv()






# Set the page configuration at the beginning
st.set_page_config("Document Summarization")

st.header(" Document Summarization and Keyword extraction ")

'''
In this project we follow the following procedure:
1) Extract the text from Documents.
2) Splitting the text into Chunks to match the limit of the LLms input tokens Size.
3) Creating the chain that tell llms to summarize the documents.
4) Keywords extraction.
5) Storing in MongoDB. 
'''

# Configuring The MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client['app_db']
collection  = db['summarys']

# Getting Groq API Key
with st.sidebar:
    groq_api_key=st.text_input("Groq API Key",value="",type="password")

## Gemma Model Using Groq API
llm_model =ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)


# Getting pdfs 
pdf_docs = st.sidebar.file_uploader("Upload your PDF Files and Click on the Submit Button", accept_multiple_files=True)

if st.sidebar.button("Submit"):

    # Text extraction from pdf
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
        
    # converting entire text into chunks
    splitter =  RecursiveCharacterTextSplitter(chunk_size = 10000 , chunk_overlap = 1000 )
    docs = splitter.create_documents([text])
    
    # Creating chain 
    chain=load_summarize_chain(
        llm=llm_model,
        chain_type="refine",
        verbose=True
    )
    output_summary=chain.run(docs)

    # Extracting Keywords

    keyword_extraction_model = KeyBERT()
    keywords_with_scores = keyword_extraction_model.extract_keywords(text,keyphrase_ngram_range=(1,1),stop_words="english",use_maxsum = True,diversity=0.2,top_n=20)
    keywords_extracted = [keyword for keyword, score in keywords_with_scores]
    
    # Printing summarized text

    st.write("Summary:")
    st.success(output_summary)
    # Printing Keywords
    st.write("Keywords:")
    st.success(keywords_extracted)

    # Pushing the Summary & Keywords to MongoDB
    summarized_output = {"Summary":output_summary,"Keywords":keywords_extracted}
    collection.insert_one(summarized_output)
    st.write("Data Pushed To MongoDB")




# Closing the MongoDB connetion
client.close()
