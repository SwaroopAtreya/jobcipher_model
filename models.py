import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from geopy.geocoders import Nominatim
from config import MODEL_NAME

# Load a better NER model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)

# Load spaCy model for additional NER and text processing
try:
    nlp = spacy.load("en_core_web_lg")
except:
    # If model not found, download it
    import os
    os.system("python -m spacy download en_core_web_lg")
    nlp = spacy.load("en_core_web_lg")

# Initialize geolocator with a better user agent
geolocator = Nominatim(user_agent="resume_parser_v2")