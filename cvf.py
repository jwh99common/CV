#!/usr/bin/env python3
"""
CV Format Checker - Test how well your CV can be read and parsed
"""

import sys
import re
from pathlib import Path

def read_file(file_path):
    """Read file with multiple encoding attempts"""
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read(), encoding
        except UnicodeDecodeError:
            continue
    
    raise Exception("Could not read file with any encoding")

def analyze_cv_structure(cv_text):
    """Analyze CV structure and content"""
    analysis = {
        'total_chars': len(cv_text),
        'total_words': len(cv_text.split()),
        'sections_found': [],
        'skills_indicators': [],
        'experience_indicators': [],
        'education_indicators': [],
        'contact_info': [],
        'potential_issues': []
    }
    
    lines = cv_text.split('\n')
    analysis['total_lines'] = len(lines)
    
    # Look for common section headers
    section_patterns = {
        'Skills': r'(?i)(technical\s+)?skills?|competenc(ies|y)|technologies?',
        'Experience': r'(?i)(work\s+|professional\s+)?experience|employment|career',
        'Education': r'(?i)education|qualifications?|academic',
        'Contact': r'(?i)contact|personal\s+info',
        'Summary': r'(?i)summary|profile|objective',
        'Projects': r'(?i)projects?|portfolio'
    }
    
    for section, pattern in section_patterns.items():
        matches = re.findall(pattern, cv_text)
        if matches:
            analysis['sections_found'].append(section)
    
    # Look for skills indicators
    skill_patterns = [
        r'python|javascript|java|sql|html|css|react|angular|vue',
        r'aws|azure|docker|kubernetes|git|linux',
        r'machine learning|ai|data science|analytics',
        r'project management|leadership|agile|scrum'
    ]
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, cv_text, re.IGNORECASE)
        if matches:
            analysis['skills_indicators'].extend(matches)
    
    # Remove duplicates
    analysis['skills_indicators'] = list(set(analysis['skills_indicators']))
    
    # Look for experience indicators
    exp_patterns = [
        r'\d+\+?\s+years?(?:\s+(?:of\s+)?experience)?',
        r'(?:senior|junior|lead|principal|manager|director)',
        r'\d{4}\s*[-–]\s*(?:\d{4}|present|current)',
        r'(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}'
    ]
    
    for pattern in exp_patterns:
        matches = re.findall(pattern, cv_text, re.IGNORECASE)
        analysis['experience_indicators'].extend(matches)
    
    # Look for education indicators
    edu_patterns = [
        r'(?:bachelor|master|phd|doctorate|degree)',
        r'(?:university|college|institute|school)',
        r'(?:bsc|msc|ba|ma|phd|mba)',
        r'certified?|certification'
    ]
    
    for pattern in edu_patterns:
        matches = re.findall(pattern, cv_text, re.IGNORECASE)
        analysis['education_indicators'].extend(matches)
    
    # Look for contact info
    contact_patterns = [
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Email
        r'\+?\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',  # Phone
        r'linkedin\.com/in/[\w-]+',  # LinkedIn
        r'github\.com/[\w-]+'  # GitHub
    ]
    
    for pattern in contact_patterns:
        matches = re.findall(pattern, cv_text, re.IGNORECASE)
        analysis['contact_info'].extend(matches)
    
    # Check for potential issues
    if analysis['total_chars'] < 500:
        analysis['potential_issues'].append("CV seems very short (less than 500 characters)")
    
    if analysis['total_chars'] > 10000:
        analysis['potential_issues'].append("CV is quite long (over 10,000 characters) - consider summarizing")
    
    if not analysis['skills_indicators']:
        analysis['potential_issues'].append("No clear technical skills found - make sure to list your skills clearly")
    
    if not analysis['experience_indicators']:
        analysis['potential_issues'].append("No clear work experience found - include job titles and dates")
    
    if 'Experience' not in analysis['sections_found'] and 'Skills' not in analysis['sections_found']:
        analysis['potential_issues'].append("No clear section headers found - consider adding section headers like 'SKILLS' and 'EXPERIENCE'")
    
    return analysis

def display_analysis(analysis, filename):
    """Display the analysis results"""
    print(f"📄 CV Analysis Report for: {filename}")
    print("=" * 60)
    
    print(f"\n📊 Basic Statistics:")
    print(f"  • Characters: {analysis['total_chars']:,}")
    print(f"  • Words: {analysis['total_words']:,}")
    print(f"  • Lines: {analysis['total_lines']:,}")
    
    print(f"\n📋 Sections Detected:")
    if analysis['sections_found']:
        for section in analysis['sections_found']:
            print(f"  ✅ {section}")
    else:
        print("  ❌ No clear section headers found")
    
    print(f"\n🔧 Skills Found:")
    if analysis['skills_indicators']:
        for skill in analysis['skills_indicators'][:10]:  # Show first 10
            print(f"  ✅ {skill}")
        if len(analysis['skills_indicators']) > 10:
            print(f"  ... and {len(analysis['skills_indicators']) - 10} more")
    else:
        print("  ❌ No clear skills found")
    
    print(f"\n💼 Experience Indicators:")
    if analysis['experience_indicators']:
        for exp in analysis['experience_indicators'][:5]:  # Show first 5
            print(f"  ✅ {exp}")
        if len(analysis['experience_indicators']) > 5:
            print(f"  ... and {len(analysis['experience_indicators']) - 5} more")
    else:
        print("  ❌ No clear experience indicators found")
    
    print(f"\n📚 Education Indicators:")
    if analysis['education_indicators']:
        for edu in analysis['education_indicators'][:5]:
            print(f"  ✅ {edu}")
    else:
        print("  ❌ No education information found")
    
    print(f"\n📞 Contact Information:")
    if analysis['contact_info']:
        for contact in analysis['contact_info']:
            print(f"  ✅ {contact}")
    else:
        print("  ❌ No contact information found")
    
    if analysis['potential_issues']:
        print(f"\n⚠️  Potential Issues:")
        for issue in analysis['potential_issues']:
            print(f"  • {issue}")
    else:
        print(f"\n✅ No major issues found!")
    
    print(f"\n💡 Recommendations:")
    
    if 'Skills' not in analysis['sections_found']:
        print("  • Add a clear 'SKILLS' or 'TECHNICAL SKILLS' section")
    
    if not analysis['skills_indicators']:
        print("  • List specific technologies, programming languages, and tools")
    
    if not analysis['experience_indicators']:
        print("  • Include job titles, company names, and employment dates")
    
    if not analysis['contact_info']:
        print("  • Add email address and phone number")
    
    print("  • Use keywords from job descriptions you're applying to")
    print("  • Quantify achievements with numbers when possible")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 cv_format_checker.py <cv_file>")
        print("Example: python3 cv_format_checker.py my_cv.pdf")
        return
    
    cv_file = sys.argv[1]
    
    if not Path(cv_file).exists():
        print(f"❌ File not found: {cv_file}")
        return
    
    try:
        cv_text, encoding = read_file(cv_file)
        print(f"✅ File read successfully using {encoding} encoding")
        
        analysis = analyze_cv_structure(cv_text)
        display_analysis(analysis, cv_file)
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")

if __name__ == "__main__":
    main()