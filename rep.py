import re

def analyze_cv(cv_text: str) -> dict:
    analysis = {
        'total_chars': len(cv_text),
        'total_words': len(cv_text.split()),
        'sections_found': [],
        'sections_content': {},       # NEW: full text per section
        'skills_indicators': [],
        'experience_indicators': [],
        'education_indicators': [],
        'contact_info': [],
        'potential_issues': []
    }

    # --- Define section headers and regex patterns ---
    section_patterns = {
        'Experience': r'(?i)(work\s+|professional\s+)?experience|employment|career',
        'Education': r'(?i)education|qualifications|study',
        'Skills': r'(?i)skills?|technologies|competencies',
    }

    # --- Extract full sections ---
    # Idea: split text by lines and group lines under section headers
    lines = cv_text.splitlines()
    current_section = None
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check if line matches a section header
        for section, pattern in section_patterns.items():
            if re.fullmatch(pattern, stripped, flags=re.IGNORECASE):
                current_section = section
                analysis['sections_found'].append(section)
                analysis['sections_content'][section] = []
                break
        else:
            # If we are inside a section, keep collecting lines
            if current_section:
                analysis['sections_content'][current_section].append(stripped)

    # Convert collected section lines into strings
    for section in analysis['sections_content']:
        analysis['sections_content'][section] = "\n".join(analysis['sections_content'][section])

    # --- Extract contact info ---
    emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', cv_text)
    phones = re.findall(r'\+?\d[\d\s-]{7,}', cv_text)
    analysis['contact_info'].extend(emails + phones)

    # --- Education indicators ---
    edu_patterns = [r'\bBSc\b', r'\bMSc\b', r'\bPhD\b', r'University', r'College']
    for pat in edu_patterns:
        matches = re.findall(pat, cv_text, flags=re.IGNORECASE)
        analysis['education_indicators'].extend(matches)

    # --- Experience indicators ---
    exp_patterns = [r'\bManager\b', r'\bEngineer\b', r'\bExperience\b', r'\bEmployment\b']
    for pat in exp_patterns:
        matches = re.findall(pat, cv_text, flags=re.IGNORECASE)
        analysis['experience_indicators'].extend(matches)

    # --- Skills indicators ---
    skills_list = ['Python', 'SQL', 'Kubernetes', 'Project Management', 'Data Analysis']
    for skill in skills_list:
        if re.search(rf'\b{skill}\b', cv_text, flags=re.IGNORECASE):
            analysis['skills_indicators'].append(skill)

    # --- Potential issues ---
    if 'Experience' not in analysis['sections_found']:
        analysis['potential_issues'].append('Missing experience section')
    if 'Education' not in analysis['sections_found']:
        analysis['potential_issues'].append('Missing education section')
    if not analysis['contact_info']:
        analysis['potential_issues'].append('No contact information found')

    return analysis

    for edu in analysis['education_indicators'][:5]:  # Show first 5
        print(f"  ✅ {edu}")
    if len(analysis['education_indicators']) > 5:
        print(f"  ... and {len(analysis['education_indicators']) - 5} more")
    else:
        print("  ❌ No clear education indicators found")