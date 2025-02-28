import re
from models import nlp, ner_pipeline
from config import location_patterns

def extract_entities_with_confidence(text_data, confidence_threshold=0.7):
    """Extract entities focusing on locations"""
    # Get the preprocessed text
    preprocessed_text = text_data['preprocessed_text']

    # Use the transformer NER pipeline
    transformer_entities = ner_pipeline(preprocessed_text)

    # Use spaCy for additional entity extraction
    doc = nlp(preprocessed_text)
    spacy_entities = [(ent.text, ent.label_, ent.start_char, ent.end_char) for ent in doc.ents]

    # Initialize locations list
    locations = []

    # Extract from transformer model
    for entity in transformer_entities:
        if entity['score'] > confidence_threshold:
            if entity['entity_group'] in ['LOC', 'GPE']:
                locations.append({
                    'text': entity['word'],
                    'confidence': entity['score'],
                    'source': 'transformer'
                })

    # Extract from spaCy for locations
    for entity in spacy_entities:
        text, label, _, _ = entity
        if label in ['GPE', 'LOC', 'FAC']:
            locations.append({
                'text': text,
                'confidence': 0.8,  # Higher confidence for locations from spaCy
                'source': 'spacy'
            })

    # Extract locations with contextual patterns
    for pattern in location_patterns:
        matches = re.findall(pattern, preprocessed_text)
        for match in matches:
            locations.append({
                'text': match.strip(),
                'confidence': 0.85,  # High confidence for pattern-matched locations
                'source': 'pattern'
            })

    # Deduplicate locations
    unique_locations = {}
    for location in locations:
        loc_text = location['text'].lower()
        if loc_text not in unique_locations or unique_locations[loc_text]['confidence'] < location['confidence']:
            unique_locations[loc_text] = location

    return list(unique_locations.values())