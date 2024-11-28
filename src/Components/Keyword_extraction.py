from keybert import KeyBERT
from src.Exception import CustomException
from src.logger import logging
import sys

class KeywordExtraction:
    def __init__(self) -> None:
        pass
    def extract_keywords(self,text):
        logging.info("Keyword extraction started")

        try:
            # Extracting Keywords

            keyword_extraction_model = KeyBERT()
            keywords_with_scores = keyword_extraction_model.extract_keywords(text,keyphrase_ngram_range=(1,1),stop_words="english",use_maxsum = True,diversity=0.2,top_n=20)
            keywords_extracted = [keyword for keyword, score in keywords_with_scores]

            logging.info("Keywords Extracted")

            return keywords_extracted
        
        except Exception as e:
            raise CustomException(e,sys)