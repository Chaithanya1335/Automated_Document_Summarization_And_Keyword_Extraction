# Importing Necessary packages
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from pymongo import MongoClient
from src.Components.DataIngestion import DataIngestion
from src.Components.Summarization import Summarization
from src.Components.Keyword_extraction import KeywordExtraction

# Set page configuration
st.set_page_config("Document Summarization")

st.header("Document Summarization and Keyword Extraction")

'''
### Procedure:
1. Extract text from documents.
2. Split text into chunks to match the token limit of LLMs.
3. Summarize the documents.
4. Extract keywords.
5. Store results in MongoDB.
'''

# Configuring MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URI)
db = client["app_db"]
collection = db["summaries"]

# Sidebar inputs
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")
    pdf_docs = st.file_uploader("Upload PDF Files", accept_multiple_files=True)

# Ensure PDFs are uploaded
if not pdf_docs:
    st.warning("Please upload your PDF files.")
    st.stop()

# Process text from PDFs
try:
    text = DataIngestion().initiate_data_Ingestion(pdf_docs)
    if not text:
        st.error("Failed to extract text from PDFs.")
        st.stop()
except Exception as e:
    st.error(f"Data ingestion failed: {e}")
    st.stop()

# Handle Submit
if st.sidebar.button("Submit"):
    try:
        # Split text into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        docs = splitter.create_documents([text])

        print(type(docs))
        
        # Summarization
        with st.spinner("Summarizing the document..."):
            output_summary = Summarization().Summarize(groq_api_key, docs)

        # Keyword extraction
        with st.spinner("Extracting keywords..."):
            keywords_extracted = KeywordExtraction().extract_keywords(text)

        # Display results
        st.subheader("Summary:")
        st.success(output_summary)

        st.subheader("Keywords:")
        st.success(keywords_extracted)

        # Save results to MongoDB
        collection.insert_one({"Summary": output_summary, "Keywords": keywords_extracted})
        st.success("Results saved to MongoDB.")

    except Exception as e:
        st.error(f"Processing failed: {e}")

# Close MongoDB connection
client.close()
