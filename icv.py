#!/usr/bin/env python3
"""
Simple Interactive CV Matcher
Uses the same reliable approach as cv_job_matcher.py
"""

import os
import sys
from pathlib import Path
import tempfile

# Import the working CV matcher
try:
    from cv_job_matcher import CVJobMatcher
except ImportError:
    print("❌ Make sure cv_job_matcher.py is in the same directory")
    sys.exit(1)

def get_file_path(prompt_text):
    """Get a valid file path from user"""
    while True:
        file_path = input(f"\n{prompt_text}: ").strip().strip('"\'')
        
        if not file_path:
            print("Please enter a file path.")
            continue
            
        if os.path.exists(file_path):
            return file_path
        else:
            print(f"❌ File not found: {file_path}")
            
            # Show current directory files as help
            current_dir = Path.cwd()
            print(f"\n📁 Files in current directory:")
            files = [f for f in current_dir.iterdir() if f.is_file()]
            for file in files[:10]:  # Show first 10 files
                print(f"  - {file.name}")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more files")

def get_model_choice():
    """Let user choose a model"""
    # Try to get available models
    try:
        import ollama
        models_response = ollama.list()
        available = [model['name'] for model in models_response['models']]
        
        print(f"\n🤖 Available Models:")
        for i, model in enumerate(available, 1):
            print(f"  {i}. {model}")
        
        while True:
            choice = input(f"\nChoose model (1-{len(available)}) or press Enter for 'phi': ").strip()
            
            if not choice:
                return "phi" if "phi:latest" in available else available[0] if available else "phi"
            
            try:
                model_index = int(choice) - 1
                if 0 <= model_index < len(available):
                    return available[model_index]
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")
                
    except Exception as e:
        print(f"⚠️ Could not list models: {e}")
        return "phi"  # Default fallback

def get_job_description():
    """Get job description - either from file or text input"""
    print(f"\n💼 Job Description Options:")
    print("1. Upload a file")
    print("2. Paste job description text")
    
    while True:
        choice = input("Choose option (1 or 2): ").strip()
        
        if choice == "1":
            return get_file_path("📄 Enter job description file path"), "file"
        elif choice == "2":
            print("\n📝 Paste your job description (press Ctrl+D when done on Linux/Mac, Ctrl+Z on Windows):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            
            job_text = '\n'.join(lines).strip()
            if job_text:
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
                temp_file.write(job_text)
                temp_file.close()
                return temp_file.name, "temp"
            else:
                print("No job description entered. Please try again.")
        else:
            print("Please enter 1 or 2.")

def display_results_nicely(results):
    """Display results in a user-friendly format"""
    if not results:
        print("❌ No results to display")
        return
    
    match_analysis = results.get('match_analysis', {})
    score = match_analysis.get('overall_score', 0)
    
    print("\n" + "="*70)
    print("🎯 CV-JOB ANALYSIS RESULTS")
    print("="*70)
    
    # Score display
    print(f"\n📊 Overall Match Score: {score}/100")
    
    # Visual score bar
    filled_bars = int(score / 5)  # 20 bars total
    empty_bars = 20 - filled_bars
    score_bar = "█" * filled_bars + "░" * empty_bars
    print(f"     [{score_bar}] {score}%")
    
    # Score interpretation
    if score >= 80:
        print("🟢 Excellent match! You're well-qualified for this role.")
    elif score >= 60:
        print("🟡 Good match with some areas for improvement.")
    elif score >= 40:
        print("🟠 Moderate match. Consider addressing key gaps.")
    else:
        print("🔴 Limited match. Significant skill development needed.")
    
    # Detailed sections
    sections = results.get('sections', {})
    if sections.get('cv_skills'):
        print(f"\n🔧 Your Key Skills:")
        for skill in sections['cv_skills'][:8]:  # Top 8
            print(f"  ✓ {skill}")
    
    if sections.get('job_requirements'):
        print(f"\n📋 Job Requirements:")
        for req in sections['job_requirements'][:8]:  # Top 8
            print(f"  • {req}")
    
    # Analysis
    detailed_analysis = match_analysis.get('detailed_analysis', '')
    if detailed_analysis:
        print(f"\n📝 Detailed Analysis:")
        print("-" * 50)
        print(detailed_analysis)
    
    # Cover letter suggestions
    cover_suggestions = results.get('cover_letter_suggestions', '')
    if cover_suggestions:
        print(f"\n💡 Cover Letter Talking Points:")
        print("-" * 50)
        print(cover_suggestions)
    
    # Skill gaps
    skill_gaps = results.get('skill_gaps', '')
    if skill_gaps:
        print(f"\n⚠️ Areas for Improvement:")
        print("-" * 50)
        print(skill_gaps)
    
    print("\n" + "="*70)

def save_results_option(matcher, results):
    """Offer to save results"""
    save = input(f"\n💾 Would you like to save these results? (y/n): ").strip().lower()
    
    if save in ['y', 'yes']:
        print("\nSave options:")
        print("1. Detailed report (Markdown)")
        print("2. Raw data (JSON)")
        print("3. Both")
        
        choice = input("Choose option (1-3): ").strip()
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if choice in ['1', '3']:
            report_file = f"cv_analysis_report_{timestamp}.md"
            matcher.generate_report(results, report_file)
        
        if choice in ['2', '3']:
            json_file = f"cv_analysis_data_{timestamp}.json"
            matcher.analysis_results = results
            matcher.save_results(json_file)

def main():
    print("🤖 Interactive CV-Job Matcher")
    print("=" * 50)
    print("This tool analyzes how well your CV matches a job description using AI.")
    
    try:
        # Get model choice
        model = get_model_choice()
        print(f"\n🔧 Using model: {model}")
        
        # Create matcher
        matcher = CVJobMatcher(model=model)
        
        while True:
            print("\n" + "=" * 50)
            
            # Get CV file
            cv_file = get_file_path("📄 Enter path to your CV file")
            
            # Get job description
            job_source, job_type = get_job_description()
            temp_files = []
            if job_type == "temp":
                temp_files.append(job_source)
            
            try:
                print(f"\n🔍 Analyzing CV against job description...")
                print("This may take 30-60 seconds...")
                
                # Run analysis
                results = matcher.analyze_match(cv_file, job_source)
                
                if results:
                    # Display results
                    display_results_nicely(results)
                    
                    # Offer to save
                    save_results_option(matcher, results)
                else:
                    print("❌ Analysis failed. Please check your files and try again.")
                
            finally:
                # Clean up temp files
                for temp_file in temp_files:
                    try:
                        os.unlink(temp_file)
                    except:
                        pass
            
            # Ask about another analysis
            another = input(f"\n🔄 Would you like to analyze another job? (y/n): ").strip().lower()
            if another not in ['y', 'yes']:
                break
        
        print("\n👋 Thanks for using CV-Job Matcher!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure Ollama is running and cv_job_matcher.py is in the same directory.")

if __name__ == "__main__":
    main()