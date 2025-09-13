#!/usr/bin/env python3
"""
CV-Job Description Matcher
Analyzes how well your CV matches a job description using Ollama
"""

import ollama
import json
import os
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import sys

class CVJobMatcher:
    def __init__(self, model: str = "tinyllama"):
        self.model = model
        self.analysis_results = {}
        
        # Test Ollama connection
        try:
            ollama.list()
            print(f"✅ Connected to Ollama using model: {model}")
        except Exception as e:
            print(f"❌ Cannot connect to Ollama: {e}")
            print("Make sure Ollama is running with 'ollama serve'")
            sys.exit(1)
    
    def read_file(self, file_path: str) -> str:
        """Read text from various file formats"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            if file_path.suffix.lower() == '.pdf':
                return self._read_pdf(file_path)
            elif file_path.suffix.lower() in ['.docx', '.doc']:
                return self._read_docx(file_path)
            else:
                # Assume text file
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")
            print("Trying to read as plain text...")
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            except Exception as e2:
                raise Exception(f"Could not read file: {e2}")
    
    def _read_pdf(self, file_path: Path) -> str:
        """Extract text from PDF"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            print("⚠️ PyPDF2 not installed. Install with: pip install PyPDF2")
            raise
    
    def _read_docx(self, file_path: Path) -> str:
        """Extract text from DOCX"""
        try:
            import docx
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            print("⚠️ python-docx not installed. Install with: pip install python-docx")
            raise
    
    def extract_key_sections(self, cv_text: str, job_text: str) -> Dict[str, str]:
        """Extract key sections from CV and job description"""
        prompt = f"""
        Analyze the following CV and Job Description. Extract the key information in JSON format.

        CV:
        {cv_text}

        JOB DESCRIPTION:
        {job_text}

        Please extract and return a JSON object with the following structure:
        {{
            "cv_skills": ["list of skills from CV"],
            "cv_experience": ["list of relevant experience from CV"],
            "cv_education": ["education/qualifications from CV"],
            "job_requirements": ["list of required skills/qualifications from job"],
            "job_responsibilities": ["main job responsibilities"],
            "job_company": "company name if mentioned"
        }}

        Only return the JSON object, nothing else.
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            result = response['response']
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                print("⚠️ Could not parse JSON from model response")
                return {}
        except Exception as e:
            print(f"❌ Error extracting sections: {e}")
            return {}
    
    def calculate_match_score(self, cv_text: str, job_text: str) -> Dict[str, any]:
        """Calculate overall match score and analysis"""
        prompt = f"""
        You are an expert recruiter. Analyze how well this CV matches the job description.

        CV:
        {cv_text[:2000]}  # Limit to avoid token limits

        JOB DESCRIPTION:
        {job_text[:2000]}

        Provide a detailed analysis with:
        1. Overall Match Score (0-100)
        2. Strengths (what matches well)
        3. Gaps (what's missing or weak)
        4. Recommendations (how to improve the match)
        5. Key Skills Assessment

        Format your response clearly with sections.
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            analysis = response['response']
            
            # Try to extract a numerical score
            score_match = re.search(r'(\d+)(?:/100|%|\s*out of 100)', analysis)
            score = int(score_match.group(1)) if score_match else 0
            
            return {
                "overall_score": score,
                "detailed_analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Error calculating match score: {e}")
            return {"overall_score": 0, "detailed_analysis": "Analysis failed", "timestamp": datetime.now().isoformat()}
    
    def generate_cover_letter_suggestions(self, cv_text: str, job_text: str) -> str:
        """Generate cover letter talking points"""
        prompt = f"""
        Based on this CV and job description, suggest 3-4 key talking points for a cover letter that highlight the strongest matches.

        CV:
        {cv_text[:1500]}

        JOB DESCRIPTION:
        {job_text[:1500]}

        Provide specific examples from the CV that directly relate to job requirements. Make the suggestions actionable and compelling.
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Error generating suggestions: {e}"
    
    def identify_skill_gaps(self, cv_text: str, job_text: str) -> str:
        """Identify missing skills and suggest improvements"""
        prompt = f"""
        Compare the skills and requirements in this job description with the CV. Identify:

        1. Missing technical skills
        2. Missing soft skills  
        3. Experience gaps
        4. Specific improvements needed
        5. Learning priorities

        CV:
        {cv_text[:1500]}

        JOB DESCRIPTION:
        {job_text[:1500]}

        Be specific and practical in your recommendations.
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Error identifying gaps: {e}"
    
    def analyze_match(self, cv_file: str, job_file: str) -> Dict[str, any]:
        """Main analysis function"""
        print("📄 Reading files...")
        
        try:
            cv_text = self.read_file(cv_file)
            job_text = self.read_file(job_file)
            
            print(f"✅ CV: {len(cv_text)} characters")
            print(f"✅ Job Description: {len(job_text)} characters")
        except Exception as e:
            print(f"❌ Error reading files: {e}")
            return {}
        
        print("\n🔍 Analyzing match...")
        results = {}
        
        # 1. Extract key sections
        print("  Extracting key information...")
        results['sections'] = self.extract_key_sections(cv_text, job_text)
        
        # 2. Calculate match score
        print("  Calculating match score...")
        results['match_analysis'] = self.calculate_match_score(cv_text, job_text)
        
        # 3. Generate cover letter suggestions
        print("  Generating cover letter suggestions...")
        results['cover_letter_suggestions'] = self.generate_cover_letter_suggestions(cv_text, job_text)
        
        # 4. Identify skill gaps
        print("  Identifying skill gaps...")
        results['skill_gaps'] = self.identify_skill_gaps(cv_text, job_text)
        
        # Store for later use
        self.analysis_results = results
        
        return results
    
    def generate_report(self, results: Dict[str, any], output_file: str = None) -> str:
        """Generate a formatted report"""
        if not results:
            return "No analysis results available."
        
        report = f"""
# CV-Job Match Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Match Score
**{results.get('match_analysis', {}).get('overall_score', 0)}/100**

## Detailed Analysis
{results.get('match_analysis', {}).get('detailed_analysis', 'No analysis available')}

## Key Skills Comparison
"""
        
        if 'sections' in results:
            sections = results['sections']
            report += f"""
### Your Skills (from CV)
{chr(10).join(['- ' + skill for skill in sections.get('cv_skills', [])])}

### Job Requirements
{chr(10).join(['- ' + req for req in sections.get('job_requirements', [])])}
"""
        
        report += f"""
## Cover Letter Suggestions
{results.get('cover_letter_suggestions', 'No suggestions available')}

## Skill Gaps & Improvement Areas
{results.get('skill_gaps', 'No gaps identified')}

---
*Report generated using Ollama model: {self.model}*
        """
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"📊 Report saved to: {output_file}")
        
        return report
    
    def save_results(self, filename: str = None):
        """Save analysis results as JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cv_job_analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
        
        print(f"💾 Results saved to: {filename}")


def main():
    parser = argparse.ArgumentParser(description="Analyze CV-Job Description match using Ollama")
    parser.add_argument("cv", help="Path to CV file (txt, pdf, docx)")
    parser.add_argument("job", help="Path to job description file (txt, pdf, docx)")
    parser.add_argument("--model", default="tinyllama", help="Ollama model to use")
    parser.add_argument("--output", "-o", help="Output file for report (markdown)")
    parser.add_argument("--save-json", help="Save results as JSON file")
    
    args = parser.parse_args()
    
    print("🤖 CV-Job Description Matcher")
    print("=" * 40)
    
    # Create matcher
    matcher = CVJobMatcher(model=args.model)
    
    # Run analysis
    results = matcher.analyze_match(args.cv, args.job)
    
    if results:
        print("\n" + "=" * 50)
        print("📊 ANALYSIS COMPLETE")
        print("=" * 50)
        
        # Generate and display report
        report = matcher.generate_report(results, args.output)
        
        if not args.output:
            print(report)
        
        # Save JSON if requested
        if args.save_json:
            matcher.save_results(args.save_json)
        
        # Summary
        score = results.get('match_analysis', {}).get('overall_score', 0)
        print(f"\n🎯 Overall Match Score: {score}/100")
        
        if score >= 80:
            print("🟢 Excellent match! You're well-qualified for this role.")
        elif score >= 60:
            print("🟡 Good match with some areas for improvement.")
        elif score >= 40:
            print("🟠 Moderate match. Consider addressing key gaps.")
        else:
            print("🔴 Limited match. Significant skill development needed.")
    
    else:
        print("❌ Analysis failed. Check your files and try again.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python cv_job_matcher.py <cv_file> <job_description_file>")
        print("\nExample:")
        print("  python cv_job_matcher.py my_cv.pdf job_posting.txt")
        print("  python cv_job_matcher.py cv.docx job.txt --output report.md")
        print("\nSupported file formats: .txt, .pdf, .docx")
        print("Optional dependencies for file reading:")
        print("  pip install PyPDF2 python-docx")
    else:
        main()