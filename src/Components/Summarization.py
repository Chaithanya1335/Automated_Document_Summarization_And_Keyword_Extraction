from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from src.logger import logging
from src.Exception import CustomException
from dotenv import load_dotenv
import sys

load_dotenv()

class Summarization:
    def __init__(self) :
        pass
    def Summarize(self,groq_api_key,docs):
        
        logging.info("Summarization started")

        try:
            logging.info("Accessing LLama3 Model from Chatgroq")
            ## Gemma Model Using Groq API
            llm_model =ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)

            logging.info("LLama3 model accessed from chatgroq")

            logging.info("Creating Summarize Chain")
            # Creating chain 
            chain=load_summarize_chain(
                    llm=llm_model,
                    chain_type="refine",
                    verbose=True
                )
            logging.info("Running The chain")
            output_summary=chain.run(docs)

            logging.info("Text Summarization completed")

            return output_summary
        
        except Exception as e:
            raise CustomException(e,sys)