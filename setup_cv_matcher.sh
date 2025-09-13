#!/bin/bash

echo "🚀 Setting up CV-Job Matcher"
echo "=" * 30

# Install optional dependencies
echo "📦 Installing optional dependencies..."
pip install PyPDF2 python-docx

# Create example files directory
mkdir -p examples
cd examples

# Create example CV
cat > example_cv.txt << 'EOF'
John Smith
Software Developer
Email: john.smith@email.com
Phone: +44 123 456 7890

PROFESSIONAL SUMMARY
Experienced software developer with 5 years of experience in full-stack development. 
Proficient in Python, JavaScript, and cloud technologies. Strong background in agile 
development and team collaboration.

TECHNICAL SKILLS
- Programming Languages: Python, JavaScript, Java, SQL
- Frameworks: Django, React, Node.js, Flask
- Databases: PostgreSQL, MongoDB, Redis
- Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
- Tools: Git, Jenkins, JIRA, VS Code

PROFESSIONAL EXPERIENCE

Senior Software Developer | TechCorp Ltd | 2021-Present
- Led development of microservices architecture serving 100k+ users
- Implemented CI/CD pipelines reducing deployment time by 60%
- Mentored junior developers and conducted code reviews
- Technologies: Python, Django, PostgreSQL, AWS, Docker

Software Developer | StartupXYZ | 2019-2021
- Built responsive web applications using React and Node.js
- Integrated third-party APIs and payment systems
- Participated in agile development cycles
- Technologies: JavaScript, React, MongoDB, Express.js

Junior Developer | DevAgency | 2018-2019
- Developed and maintained client websites
- Fixed bugs and implemented new features
- Learned best practices in software development
- Technologies: HTML, CSS, JavaScript, PHP

EDUCATION
BSc Computer Science | University of Technology | 2014-2018
- First Class Honours
- Relevant coursework: Algorithms, Data Structures, Software Engineering

CERTIFICATIONS
- AWS Certified Solutions Architect (2022)
- Certified Scrum Master (2021)

PROJECTS
E-commerce Platform: Built a full-stack e-commerce solution with payment integration
Task Management App: React-based project management tool with real-time updates
API Gateway Service: Microservice for handling authentication and routing
EOF

# Create example job description
cat > example_job.txt << 'EOF'
Senior Full-Stack Developer
InnovateTech Solutions

ABOUT THE ROLE
We are seeking a Senior Full-Stack Developer to join our growing engineering team. 
You will be responsible for designing and implementing scalable web applications 
and working closely with our product and design teams.

REQUIRED SKILLS & EXPERIENCE
- 4+ years of professional software development experience
- Strong proficiency in Python and JavaScript
- Experience with modern web frameworks (Django, React, Vue.js)
- Solid understanding of database design and SQL
- Experience with cloud platforms (AWS, Azure, or GCP)
- Knowledge of containerization (Docker, Kubernetes)
- Familiarity with CI/CD pipelines and DevOps practices
- Experience with version control systems (Git)
- Strong problem-solving and analytical skills
- Excellent communication and teamwork abilities

PREFERRED QUALIFICATIONS
- Experience with microservices architecture
- Knowledge of NoSQL databases (MongoDB, Redis)
- Previous experience in fintech or e-commerce
- Leadership or mentoring experience
- Relevant certifications (AWS, Google Cloud, etc.)
- Experience with agile development methodologies

RESPONSIBILITIES
- Design and develop robust, scalable web applications
- Collaborate with cross-functional teams to define and implement features
- Write clean, maintainable, and well-tested code
- Participate in code reviews and architectural discussions  
- Mentor junior developers and share knowledge
- Stay updated with latest technology trends and best practices
- Contribute to technical documentation and process improvements

WHAT WE OFFER
- Competitive salary £60,000-£80,000
- Flexible working arrangements
- Professional development opportunities
- Health and wellness benefits
- Equity participation

Apply now to join our innovative team!
EOF

echo "✅ Example files created:"
echo "  - examples/example_cv.txt"
echo "  - examples/example_job.txt"

cd ..

echo ""
echo "🎯 Quick Test:"
echo "python cv_job_matcher.py examples/example_cv.txt examples/example_job.txt"
echo ""
echo "📚 Usage examples:"
echo "python cv_job_matcher.py my_cv.pdf job_posting.txt --output report.md"
echo "python cv_job_matcher.py cv.docx job.txt --model phi --save-json results.json"