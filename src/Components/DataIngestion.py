from PyPDF2 import PdfReader
from src.Exception import CustomException
from src.logger import logging
import os
import sys


class DataIngestion:
    def __init__(self) -> None:
       pass
    def initiate_data_Ingestion(self,pdf_docs):
        logging.info("DataIngestion Started")
        try:
                logging.info("Extracting Text from Pdf Files")
            
            # Text extraction from pdf
                text=""
                for pdf in pdf_docs:
                    pdf_reader= PdfReader(pdf)
                    for page in pdf_reader.pages:
                        text+= page.extract_text()
                logging.info("Text Extracted")

                logging.info("Data Ingestion completed")

                return text
        
        except Exception as e:
             raise CustomException(e,sys)
            