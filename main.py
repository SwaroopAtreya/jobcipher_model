#!/usr/bin/env python
import argparse
from text_extraction import extract_text_with_layout
from text_preprocessing import preprocess_resume_text
from skill_extraction import extract_skills_from_skills_section, normalize_skills
from entity_extraction import extract_entities_with_confidence
from location_processing import standardize_locations
from utils import print_results

def parse_resume(file_path, confidence_threshold=0.75):
    """Parse a resume and extract skills ONLY from skills section and locations with confidence scores"""
    # Extract text with layout preservation
    text = extract_text_with_layout(file_path)

    # Preprocess the text
    text_data = preprocess_resume_text(text)

    # Extract skills ONLY from skills section with improved detection
    skills = extract_skills_from_skills_section(text_data, confidence_threshold)

    # Normalize skills
    skills = normalize_skills(skills)

    # Extract location entities
    location_entities = extract_entities_with_confidence(text_data, confidence_threshold)

    # Standardize locations
    validated_locations = standardize_locations(location_entities)

    # Filter locations by confidence threshold
    final_locations = [l for l in validated_locations if l['confidence'] >= confidence_threshold]

    # Sort by confidence
    skills.sort(key=lambda x: x['confidence'], reverse=True)
    final_locations.sort(key=lambda x: x['confidence'], reverse=True)

    return skills, final_locations

def main():
    """Main function to run the resume parser"""
    parser = argparse.ArgumentParser(description='Parse skills (STRICTLY from skills section only) and locations from resumes')
    parser.add_argument('file_path', help='Path to the resume file (PDF or DOCX)')
    parser.add_argument('--threshold', type=float, default=0.75,
                        help='Confidence threshold (0.0 to 1.0)')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose output for debugging')

    args = parser.parse_args()

    print(f"Parsing resume: {args.file_path}")
    print(f"Using confidence threshold: {args.threshold}")
    print(f"NOTE: Skills will be extracted STRICTLY from the skills section ONLY")

    try:
        skills, locations = parse_resume(args.file_path, args.threshold)
        print_results(skills, locations)
    except Exception as e:
        print(f"Error parsing resume: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # For command line usage
    main()