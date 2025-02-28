from models import geolocator

def standardize_locations(location_entities):
    """Standardize and validate locations"""
    validated_locations = []

    for location in location_entities:
        location_text = location['text']

        try:
            geo_location = geolocator.geocode(location_text, exactly_one=True, timeout=10)
            if geo_location:
                # Use standardized location with higher confidence
                validated_locations.append({
                    'text': geo_location.address,
                    'confidence': location['confidence'] + 0.1,  # Boost confidence for standardized
                    'original_text': location_text,
                    'coordinates': (geo_location.latitude, geo_location.longitude)
                })
            else:
                # Keep original with reduced confidence
                validated_locations.append({
                    'text': location_text,
                    'confidence': location['confidence'] * 0.8,  # Reduce confidence
                    'original_text': location_text
                })
        except Exception as e:
            print(f"Error standardizing location '{location_text}': {e}")
            # Keep original when standardization fails
            validated_locations.append({
                'text': location_text,
                'confidence': location['confidence'] * 0.7,  # Reduce confidence more
                'original_text': location_text
            })

    return validated_locations