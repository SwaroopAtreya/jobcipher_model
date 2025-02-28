import re
from config import skill_section_patterns

def preprocess_resume_text(text):
    """Enhanced preprocessing specifically for resumes with improved skills section detection"""
    # Save original capitalization for later skill matching
    original_text = text

    # Remove email addresses and URLs
    text = re.sub(r'\S+@\S+', 'EMAIL', text)
    text = re.sub(r'http\S+', 'URL', text)

    # Normalize sections - expanded list of potential section headers
    text = re.sub(r'(?i)EDUCATION|Education|education', 'EDUCATION', text)
    text = re.sub(r'(?i)EXPERIENCE|Experience|experience|WORK HISTORY|Work History|EMPLOYMENT|Employment', 'EXPERIENCE', text)
    text = re.sub(r'(?i)SKILLS|Skills|skills|TECHNICAL SKILLS|Technical Skills|CORE COMPETENCIES|Core Competencies', 'SKILLS', text)
    text = re.sub(r'(?i)CERTIFICATIONS|Certifications|certifications', 'CERTIFICATIONS', text)
    text = re.sub(r'(?i)PROJECTS|Projects|projects', 'PROJECTS', text)

    # Normalize bullet points and formatting
    text = re.sub(r'•|›|»|\*|⦿|⦁', '•', text)

    # Clean up whitespace while preserving structure
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r' • ', '\n• ', text)

    # Split into sections for contextual processing
    sections = {}
    lines = text.split('\n')
    current_section = "HEADER"
    section_text = ""

    for i, line in enumerate(lines):
        # Check if line contains a section header
        is_section_header = False

        # Check for main sections
        if any(re.search(r'(?i)\b' + section + r'\b', line) for section in
               ['EDUCATION', 'EXPERIENCE', 'PROJECTS', 'CERTIFICATIONS']):
            is_section_header = True
            sections[current_section] = section_text.strip()
            current_section = line.strip()
            section_text = ""

        # Check for skill section variations - more comprehensive pattern matching
        elif any(re.search(pattern, line) for pattern in skill_section_patterns):
            is_section_header = True
            sections[current_section] = section_text.strip()
            current_section = "SKILLS"  # Normalize all skill section variations
            section_text = ""

        # Check for formatting-based section headers (standalone short lines)
        elif (len(line.strip()) < 30 and i < len(lines)-1 and
              (lines[i+1].strip().startswith('•') or not lines[i+1].strip())):
            # This might be a section header
            possible_header = line.strip().upper()
            if any(re.search(pattern, possible_header) for pattern in skill_section_patterns):
                is_section_header = True
                sections[current_section] = section_text.strip()
                current_section = "SKILLS"
                section_text = ""

        if not is_section_header:
            section_text += line + "\n"

    # Add the last section
    sections[current_section] = section_text.strip()

    # Identify section boundaries for more precise skills extraction
    section_boundaries = {}
    position = 0

    for section in sections:
        section_text = sections[section]
        start_pos = text.find(section_text, position)
        if start_pos != -1:
            end_pos = start_pos + len(section_text)
            section_boundaries[section] = (start_pos, end_pos)
            position = end_pos

    return {
        'preprocessed_text': text,
        'original_text': original_text,
        'sections': sections,
        'section_boundaries': section_boundaries
    }