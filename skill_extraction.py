import re
from models import nlp
from config import skill_keywords, false_positives

def extract_skills_from_skills_section(text_data, confidence_threshold=0.8):
    """Extract skills ONLY from the skills section with improved confidence scoring"""
    # Get the sections
    sections = text_data['sections']
    original_text = text_data['original_text']

    # Initialize skills list
    skills = []

    # Find the skills section with comprehensive pattern matching
    skills_section_text = None
    skills_section_key = None

    # First, look for normalized 'SKILLS' section
    if 'SKILLS' in sections:
        skills_section_text = sections['SKILLS']
        skills_section_key = 'SKILLS'
    else:
        # Look for any section containing skill keywords
        skill_keywords_in_headers = ['SKILL', 'COMPETENC', 'EXPERTISE', 'TECHNOLOG', 'PROFICIENC', 'QUALIFICATION']
        skill_section_keys = [key for key in sections.keys()
                              if any(keyword in key.upper() for keyword in skill_keywords_in_headers)]

        if skill_section_keys:
            # Use the first matching skills section
            skills_section_key = skill_section_keys[0]
            skills_section_text = sections[skills_section_key]

    if not skills_section_text:
        print("WARNING: No dedicated skills section found. No skills will be extracted.")
        return []

    # Log the identified skills section for debugging
    print(f"Identified skills section: '{skills_section_key}'")
    print(f"Skills section content (first 100 chars): {skills_section_text[:100]}...")

    # Process skills section for known skills
    found_skills = {}  # Use dict to track highest confidence per skill

    # First pass: Look for exact skills in our database
    for skill in skill_keywords:
        # Case insensitive search with word boundaries
        pattern = re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
        if pattern.search(skills_section_text):
            # Find the actual case-preserved match in the original text
            for match in pattern.finditer(skills_section_text):
                matched_text = match.group(0)
                skill_lower = matched_text.lower()

                # Calculate confidence based on match location and context
                confidence = 0.95  # Base confidence for exact matches

                # Confidence boosts:
                # 1. If preceded by a bullet point
                context_before = skills_section_text[max(0, match.start()-5):match.start()]
                if '•' in context_before or '-' in context_before:
                    confidence += 0.03

                # 2. If it's a standalone skill (surrounded by punctuation/whitespace)
                context_after = skills_section_text[match.end():min(len(skills_section_text), match.end()+5)]
                if re.match(r'[,;.\s]', context_after) or context_after == '':
                    confidence += 0.02

                # Store with highest confidence seen
                if skill_lower not in found_skills or found_skills[skill_lower]['confidence'] < confidence:
                    found_skills[skill_lower] = {
                        'text': matched_text,
                        'confidence': min(confidence, 1.0),  # Cap at 1.0
                        'source': 'skills_section_exact_match'
                    }

    # Second pass: Use NLP for skill phrase extraction
    skills_doc = nlp(skills_section_text)

    # Extract skill phrases using noun chunks and entity recognition
    for chunk in skills_doc.noun_chunks:
        chunk_text = chunk.text.strip()
        chunk_lower = chunk_text.lower()

        # Check if any skill keyword is in this chunk
        matching_keywords = [kw for kw in skill_keywords if kw in chunk_lower]
        if matching_keywords:
            # Calculate confidence based on match quality
            # Higher confidence for exact matches, lower for partial
            if any(kw == chunk_lower for kw in matching_keywords):
                confidence = 0.9  # Exact match to a keyword
            else:
                # Confidence based on how much of the chunk is covered by keywords
                keyword_chars = sum(len(kw) for kw in matching_keywords if kw in chunk_lower)
                coverage = keyword_chars / len(chunk_lower)
                confidence = 0.7 + (coverage * 0.2)  # Between 0.7 and 0.9

            # Store with highest confidence seen
            if chunk_lower not in found_skills or found_skills[chunk_lower]['confidence'] < confidence:
                found_skills[chunk_lower] = {
                    'text': chunk_text,
                    'confidence': confidence,
                    'source': 'skills_section_nlp'
                }

    # Third pass: Extract skills from bullet points - these are often highly reliable
    bullet_pattern = r'•\s*([^•\n]+)'
    bullet_points = re.findall(bullet_pattern, skills_section_text)

    for point in bullet_points:
        point_text = point.strip()
        point_lower = point_text.lower()

        # Skip if it's too long to be a skill
        if len(point_text) > 50:
            continue

        # Check if any known skill keyword is in this point
        matching_keywords = [kw for kw in skill_keywords if kw in point_lower]
        if matching_keywords:
            # Calculate confidence - bullet points are high confidence
            confidence = 0.9  # Base high confidence for bullet points

            # Boost confidence if contains multiple skill keywords
            if len(matching_keywords) > 1:
                confidence = min(confidence + 0.05, 1.0)

            # Store with highest confidence seen
            if point_lower not in found_skills or found_skills[point_lower]['confidence'] < confidence:
                found_skills[point_lower] = {
                    'text': point_text,
                    'confidence': confidence,
                    'source': 'skills_bullet_point'
                }

    # Fourth pass: Extract comma-separated skills lists
    # This is common in skills sections: "Python, Java, SQL, React"
    comma_lists = re.findall(r'([^•\n:]+(?:,\s*[^,\n]+)+)', skills_section_text)
    for comma_list in comma_lists:
        items = [item.strip() for item in comma_list.split(',')]
        for item in items:
            item_lower = item.lower()

            # Skip if too long or too short to be a skill
            if len(item) > 40 or len(item) < 2:
                continue

            # Check if any skill keyword matches or is contained
            matching_keywords = [kw for kw in skill_keywords if kw == item_lower or kw in item_lower]
            if matching_keywords:
                # Calculate confidence - comma lists are usually skills
                if any(kw == item_lower for kw in matching_keywords):
                    confidence = 0.95  # Exact match
                else:
                    # Partial match - base on coverage
                    keyword_chars = sum(len(kw) for kw in matching_keywords if kw in item_lower)
                    coverage = keyword_chars / len(item_lower)
                    confidence = 0.8 + (coverage * 0.15)  # Between 0.8 and 0.95

                # Store with highest confidence seen
                if item_lower not in found_skills or found_skills[item_lower]['confidence'] < confidence:
                    found_skills[item_lower] = {
                        'text': item,
                        'confidence': confidence,
                        'source': 'skills_comma_list'
                    }

    # Convert found_skills dict to list
    skills = list(found_skills.values())

    # Filter out common false positives and skills below threshold
    filtered_skills = [
        s for s in skills
        if s['confidence'] >= confidence_threshold and
        not any(fp in s['text'].lower() for fp in false_positives)
    ]

    # Sort by confidence
    filtered_skills.sort(key=lambda x: x['confidence'], reverse=True)

    return filtered_skills

def normalize_skills(skills):
    """Normalize and clean the extracted skills"""
    normalized_skills = []

    for skill in skills:
        skill_text = skill['text'].strip()

        # Remove trailing punctuation
        skill_text = re.sub(r'[.,;:]+$', '', skill_text)

        # Remove common prefixes that might appear in skill lists
        skill_text = re.sub(r'^(- |• )', '', skill_text)

        # Remove excessive whitespace
        skill_text = re.sub(r'\s+', ' ', skill_text).strip()

        # Skip if empty after cleaning
        if not skill_text:
            continue

        # Add the normalized skill
        normalized_skills.append({
            'text': skill_text,
            'confidence': skill['confidence'],
            'source': skill['source']
        })

    return normalized_skills