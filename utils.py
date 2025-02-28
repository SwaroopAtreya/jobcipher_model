def print_results(skills, locations):
    """Print extracted information in a well-formatted way"""
    print("\n" + "="*60)
    print("EXTRACTED SKILLS (STRICTLY FROM SKILLS SECTION ONLY)")
    print("="*60)

    if not skills:
        print("No skills found in skills section with sufficient confidence.")
    else:
        for i, skill in enumerate(skills, 1):
            confidence_pct = f"{skill['confidence']*100:.1f}%"
            print(f"{i}. {skill['text']} (Confidence: {confidence_pct})")
            if 'source' in skill:
                print(f"   Source: {skill['source']}")

    print("\n" + "="*60)
    print("EXTRACTED LOCATIONS")
    print("="*60)

    if not locations:
        print("No locations found with sufficient confidence.")
    else:
        for i, location in enumerate(locations, 1):
            confidence_pct = f"{location['confidence']*100:.1f}%"
            print(f"{i}. {location['text']} (Confidence: {confidence_pct})")
            if 'original_text' in location and location['original_text'] != location['text']:
                print(f"   Original text: {location['original_text']}")
            if 'coordinates' in location:
                print(f"   Coordinates: {location['coordinates']}")