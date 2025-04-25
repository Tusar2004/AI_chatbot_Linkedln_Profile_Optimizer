from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for, session, flash
import random
import time
from datetime import datetime
import pandas as pd
import io
from fpdf import FPDF
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-1234'  # Change this in production

# Mock database (replace with real database in production)
users_db = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'name': 'Admin User',
        'email': 'admin@linkedinoptimizer.com',
        'plan': 'premium'
    }
}

# Enhanced knowledge base
knowledge_base = {
    "keywords": {
        "software engineering": {
            "keywords": ["Python", "JavaScript", "Java", "C++", "Algorithms", "Data Structures",
                        "Machine Learning", "Web Development", "Backend", "Frontend", "Full Stack",
                        "Cloud Computing", "AWS", "Azure", "Docker", "Kubernetes", "CI/CD",
                        "Agile Methodologies", "Scrum", "Test-Driven Development", "DevOps",
                        "Microservices", "REST API", "GraphQL", "Node.js", "React", "Angular",
                        "Vue.js", "TypeScript", "SQL", "NoSQL", "MongoDB", "PostgreSQL"],
            "tips": "Use a mix of technical skills and methodologies. Include both specific technologies and broader concepts."
        },
        "digital marketing": {
            "keywords": ["SEO", "Content Marketing", "Social Media", "PPC", "Google Analytics",
                        "Email Marketing", "Conversion Optimization", "Brand Strategy",
                        "Influencer Marketing", "Marketing Automation", "Data Analysis",
                        "CRM", "Market Research", "Copywriting", "Growth Hacking",
                        "Google Ads", "Facebook Ads", "LinkedIn Ads", "Content Strategy",
                        "Video Marketing", "Marketing Analytics", "Customer Journey"],
            "tips": "Highlight both strategic and tactical skills. Include platform-specific skills when relevant."
        },
        "finance": {
            "keywords": ["Financial Analysis", "Investment Banking", "Portfolio Management",
                        "Risk Management", "Corporate Finance", "Financial Modeling",
                        "Valuation", "Mergers & Acquisitions", "Accounting", "CFA",
                        "Financial Reporting", "Excel", "Bloomberg Terminal", "Derivatives",
                        "Private Equity", "Venture Capital", "Financial Planning", "FP&A",
                        "Treasury", "Audit", "Compliance", "IFRS", "GAAP"],
            "tips": "Include certifications and specialized tools. Mix quantitative skills with strategic competencies."
        },
        "data science": {
            "keywords": ["Machine Learning", "Deep Learning", "Python", "R", "SQL",
                        "Data Visualization", "Statistical Analysis", "Predictive Modeling",
                        "Natural Language Processing", "Computer Vision", "Big Data",
                        "Hadoop", "Spark", "Tableau", "Power BI", "TensorFlow", "PyTorch",
                        "Data Mining", "Feature Engineering", "A/B Testing"],
            "tips": "Showcase both technical skills and business impact. Include specific tools and methodologies."
        },
        "product management": {
            "keywords": ["Product Strategy", "Roadmapping", "Agile", "Scrum", "User Stories",
                        "Market Research", "Competitive Analysis", "Customer Development",
                        "UX Design", "UI Design", "Prototyping", "A/B Testing", "Go-to-Market",
                        "Product Marketing", "KPIs", "OKRs", "JIRA", "Confluence", "Figma"],
            "tips": "Balance technical, business, and user experience skills. Show product impact with metrics."
        }
    },
    "profile_sections": {
        "required": ["Headline", "Summary", "Experience", "Education", "Skills"],
        "optional": ["Recommendations", "Accomplishments", "Volunteer Experience", "Licenses", "Projects"],
        "score_weights": {
            "Headline": 15,
            "Summary": 20,
            "Experience": 25,
            "Education": 15,
            "Skills": 10,
            "Recommendations": 5,
            "Media": 5,
            "Custom": 5
        }
    },
    "api_resources": [
        {"name": "Marketing Developer Platform", "desc": "For advertising and marketing solutions"},
        {"name": "Talent Solutions API", "desc": "For recruitment and talent management"},
        {"name": "Share on LinkedIn API", "desc": "To enable content sharing to LinkedIn"},
        {"name": "Sign In with LinkedIn", "desc": "For authentication using LinkedIn credentials"},
        {"name": "Profile API", "desc": "Access to member profile data"},
        {"name": "Posts API", "desc": "For creating and managing content"}
    ],
    "content_ideas": {
        "software engineering": [
            "Share a coding challenge you recently solved with your approach",
            "Explain a complex technical concept in simple terms",
            "Showcase a project you're working on with lessons learned",
            "Discuss emerging trends in your tech stack",
            "Share career advice for junior developers"
        ],
        "digital marketing": [
            "Analyze a recent successful marketing campaign",
            "Share tips for improving social media engagement",
            "Discuss changes in SEO best practices",
            "Showcase a creative marketing strategy",
            "Predict upcoming digital marketing trends"
        ],
        "finance": [
            "Analyze current market trends",
            "Explain a financial concept for non-experts",
            "Share tips for personal financial management",
            "Discuss regulatory changes in your sector",
            "Provide career advice for finance professionals"
        ],
        "data science": [
            "Walk through an interesting data analysis project",
            "Explain a machine learning concept in simple terms",
            "Share tips for effective data visualization",
            "Discuss ethical considerations in AI",
            "Compare different data science tools"
        ],
        "product management": [
            "Share your product development framework",
            "Discuss how you prioritize features",
            "Explain how you measure product success",
            "Share lessons from a product launch",
            "Discuss emerging product management trends"
        ]
    },
    "connection_tips": [
        "Personalize connection requests with a note about why you want to connect",
        "Engage with your network's content before requesting to connect",
        "Join and participate in LinkedIn groups in your industry",
        "Follow up new connections with a value-added message",
        "Maintain a regular posting schedule to stay visible"
    ],
    "general_questions": {
        "profile optimization": [
            "How can I make my profile stand out?",
            "What's the ideal profile picture for LinkedIn?",
            "Should I use the open to work banner?",
            "How often should I update my profile?",
            "What's the best way to showcase projects?"
        ],
        "job search": [
            "How can I optimize my profile for job hunting?",
            "Should I connect with recruiters?",
            "How to use LinkedIn's job search effectively?",
            "What to include in the 'About' section for jobs?",
            "How to handle employment gaps on LinkedIn?"
        ],
        "networking": [
            "How many connections should I aim for?",
            "Should I accept connection requests from strangers?",
            "How to rebuild an old LinkedIn network?",
            "Best practices for LinkedIn messaging?",
            "How to leverage LinkedIn groups?"
        ]
    }
}

def detect_industry_from_message(message):
    if "software" in message or "developer" in message or "engineer" in message:
        return "software engineering"
    elif "market" in message or "seo" in message or "social media" in message:
        return "digital marketing"
    elif "finance" in message or "bank" in message or "invest" in message:
        return "finance"
    elif "data" in message or "analyst" in message or "machine learning" in message:
        return "data science"
    elif "product" in message or "manager" in message or "roadmap" in message:
        return "product management"
    else:
        return random.choice(["software engineering", "digital marketing", "finance", "data science", "product management"])

def generate_api_response():
    response = """<p class="font-medium text-indigo-700">LinkedIn API Integration Guide</p>
    <ol class="list-decimal pl-5 mt-2 space-y-1 text-sm">
        <li class="font-medium">Register your app at <a href="https://developer.linkedin.com/" class="text-indigo-600 hover:underline" target="_blank">LinkedIn Developer Portal</a></li>
        <li>Choose the appropriate product for your needs</li>
        <li>Get your API keys (Client ID and Client Secret)</li>
        <li>Implement OAuth 2.0 authentication</li>
        <li>Make API calls to relevant endpoints</li>
    </ol>
    <p class="mt-3 font-medium">Available API Resources:</p>
    <div class="mt-2 space-y-2">"""
    
    for resource in knowledge_base["api_resources"]:
        response += f"""
        <div class="bg-blue-50 p-2 rounded-lg border border-blue-100">
            <p class="font-medium text-blue-800">{resource['name']}</p>
            <p class="text-xs text-blue-600">{resource['desc']}</p>
        </div>"""
    response += "</div>"
    return response

def generate_keyword_response(user_message):
    industry = detect_industry_from_message(user_message)
    return f"""
    <p class="font-medium">Keyword Suggestions for <span class="text-indigo-700">{industry.title()}</span>:</p>
    <div class="mt-2 flex flex-wrap gap-2">
        {''.join([f'<span class="bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full text-xs">{keyword}</span>' for keyword in knowledge_base["keywords"][industry]["keywords"]])}
    </div>
    <p class="mt-3 text-sm text-gray-700">{knowledge_base["keywords"][industry]["tips"]}</p>"""

def generate_profile_score_response():
    return """
    <p class="font-medium">LinkedIn Profile Completeness</p>
    <p class="text-sm mt-1">Your profile strength is calculated based on these sections:</p>
    <div class="mt-3 grid md:grid-cols-2 gap-3">
        <div>
            <p class="font-medium text-green-700">Essential Sections</p>
            <ul class="list-disc pl-5 mt-1 text-sm space-y-1">""" + ''.join([f"<li>{section} ({knowledge_base['profile_sections']['score_weights'].get(section, 0)}%)</li>" 
                   for section in knowledge_base["profile_sections"]["required"]]) + """
            </ul>
        </div>
        <div>
            <p class="font-medium text-blue-700">Recommended Sections</p>
            <ul class="list-disc pl-5 mt-1 text-sm space-y-1">""" + ''.join([f"<li>{section} ({knowledge_base['profile_sections']['score_weights'].get(section, 0)}%)</li>" 
                  for section in knowledge_base["profile_sections"]["optional"]]) + """
            </ul>
        </div>
    </div>
    <div class="mt-4 bg-blue-50 p-3 rounded-lg border border-blue-100">
        <p class="text-sm"><span class="font-medium">Tip:</span> Complete all essential sections and at least 3 recommended sections for maximum visibility.</p>
        <div class="mt-2 flex justify-between items-center">
            <button id="view-score-chart" class="text-xs bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-700 transition">View Score Visualization</button>
            <button id="export-pdf" class="text-xs bg-gray-600 text-white px-3 py-1 rounded hover:bg-gray-700 transition">Export as PDF</button>
        </div>
    </div>"""

def generate_content_ideas(user_message):
    industry = detect_industry_from_message(user_message)
    return f"""
    <p class="font-medium">Content Ideas for {industry.title()}</p>
    <ul class="list-disc pl-5 mt-2 space-y-2 text-sm">
        {''.join([f'<li>{idea}</li>' for idea in knowledge_base["content_ideas"][industry]])}
    </ul>
    <p class="mt-3 text-sm bg-purple-50 p-2 rounded-lg border border-purple-100">
        <span class="font-medium">Pro Tip:</span> Mix educational, inspirational, and personal content for best engagement.
    </p>"""

def generate_connection_tips():
    return """
    <p class="font-medium">LinkedIn Connection Growth Tips</p>
    <ul class="list-disc pl-5 mt-2 space-y-2 text-sm">
        {0}
    </ul>
    <p class="mt-3 text-sm bg-green-50 p-2 rounded-lg border border-green-100">
        <span class="font-medium">Remember:</span> Quality connections are more valuable than quantity.
    </p>""".format(''.join([f'<li>{tip}</li>' for tip in knowledge_base["connection_tips"]]))

def generate_job_search_advice():
    return random.choice([
        "For job hunting, optimize your profile with relevant keywords from job descriptions you're targeting.",
        "Make sure your 'About' section clearly states what you're looking for and what value you offer.",
        "Engage with content from companies you're interested in to increase your visibility.",
        "Consider adding 'Open to Work' to your profile if you're actively searching.",
        "Connect with recruiters in your industry and send personalized messages."
    ])

def generate_optimization_tips(user_message):
    if "picture" in user_message:
        return "Your profile picture should be professional, high-quality, with good lighting. Dress for the role you want and smile naturally."
    elif "headline" in user_message:
        return "Your headline should be more than just a job title. Include your specialty, value proposition, and keywords."
    else:
        return random.choice([
            "Use bullet points in your experience section to highlight achievements with metrics.",
            "Add media samples to your profile to showcase your work visually.",
            "Get recommendations from colleagues to add social proof to your profile.",
            "Customize your LinkedIn URL to make it cleaner and more professional.",
            "Join relevant LinkedIn groups and participate in discussions to increase visibility."
        ])

def handle_general_questions(user_message):
    for category, questions in knowledge_base["general_questions"].items():
        for q in questions:
            if q.lower() in user_message:
                return f"For '{q}', here's my advice: {generate_optimization_tips(q)}"
    
    return "I can help with LinkedIn profile optimization, keyword suggestions, API integration, profile analysis, content ideas, and networking strategies. Could you please be more specific about what you need help with?"

def generate_industry_specific_analysis(industry, profile_url):
    base_score = random.randint(60, 90)
    
    analysis = {
        "score": base_score,
        "comparison": f"Your profile scores higher than {random.randint(55, 85)}% of profiles in your industry"
    }
    
    if industry == "software engineering":
        analysis.update({
            "strengths": [
                "Strong technical skills section with relevant programming languages",
                "Well-structured experience section with project details",
                "Good use of technical keywords for search optimization"
            ],
            "weaknesses": [
                "Could showcase more measurable achievements in your experience",
                "Consider adding more media samples of your work",
                "Summary could better highlight your unique value proposition"
            ],
            "suggestions": [
                "Add 2-3 more technical skills from emerging technologies",
                "Include metrics in your experience (e.g., 'Improved performance by 30%')",
                "Create a portfolio section with links to GitHub or live projects"
            ],
            "industry": "Software Engineering",
            "profile_image": "https://img.icons8.com/color/96/source-code.png"
        })
    elif industry == "digital marketing":
        analysis.update({
            "strengths": [
                "Excellent showcase of marketing campaigns and results",
                "Good use of visual media to demonstrate work",
                "Strong network of marketing professionals"
            ],
            "weaknesses": [
                "Could include more data-driven results in experience descriptions",
                "Recommendations section needs more endorsements",
                "Skills section could be more specific to your niche"
            ],
            "suggestions": [
                "Add case studies with measurable ROI for your campaigns",
                "Include certifications from platforms like Google Ads or HubSpot",
                "Create more content to demonstrate thought leadership"
            ],
            "industry": "Digital Marketing",
            "profile_image": "https://img.icons8.com/color/96/online-marketing.png"
        })
    elif industry == "finance":
        analysis.update({
            "strengths": [
                "Professional headline with clear value proposition",
                "Strong education and certifications section",
                "Good use of industry-specific terminology"
            ],
            "weaknesses": [
                "Experience descriptions could show more quantitative impact",
                "Consider adding more recommendations from colleagues/clients",
                "Skills section could include more technical finance skills"
            ],
            "suggestions": [
                "Add specific deal sizes or financial impacts you've managed",
                "Include any published research or market analysis",
                "Highlight any regulatory expertise relevant to your field"
            ],
            "industry": "Finance",
            "profile_image": "https://img.icons8.com/color/96/money-bag.png"
        })
    elif industry == "data science":
        analysis.update({
            "strengths": [
                "Comprehensive technical skills section",
                "Good demonstration of projects and problem-solving",
                "Effective use of data visualization in profile"
            ],
            "weaknesses": [
                "Could better explain business impact of your analyses",
                "Consider adding more code samples or GitHub links",
                "Summary could tell more of a story about your journey"
            ],
            "suggestions": [
                "Add specific metrics from your data projects (e.g., accuracy improvements)",
                "Include links to published papers or conference talks",
                "Showcase tools you're expert in with specific examples"
            ],
            "industry": "Data Science",
            "profile_image": "https://img.icons8.com/color/96/data-configuration.png"
        })
    else:  # product management
        analysis.update({
            "strengths": [
                "Clear demonstration of product lifecycle experience",
                "Good mix of technical and business skills",
                "Effective storytelling in experience section"
            ],
            "weaknesses": [
                "Could include more product metrics and KPIs",
                "Consider adding more visual elements like roadmaps",
                "Skills section could better highlight methodologies"
            ],
            "suggestions": [
                "Add specific product growth metrics you've achieved",
                "Include certifications like CSPO or Pragmatic Marketing",
                "Showcase your product decision-making framework"
            ],
            "industry": "Product Management",
            "profile_image": "https://img.icons8.com/color/96/product.png"
        })
    
    if random.random() > 0.7:
        analysis['strengths'].append("Excellent profile picture - professional and approachable")
    if random.random() > 0.7:
        analysis['weaknesses'].append("Custom URL could be more professional")
    
    return analysis

# Authentication decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Auth routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users_db.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['name'] = user['name']
            session['email'] = user['email']
            session['plan'] = user.get('plan', 'free')
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        flash('Invalid username or password', 'danger')
    
    if 'username' in session:
        return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = request.form.get('name')
        email = request.form.get('email')
        
        if not all([username, password, name, email]):
            flash('All fields are required', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match', 'danger')
        elif username in users_db:
            flash('Username already exists', 'danger')
        else:
            users_db[username] = {
                'password': generate_password_hash(password),
                'name': name,
                'email': email,
                'plan': 'free'
            }
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Protected routes
@app.route('/')
@login_required
def home():
    return render_template('index.html', user={
        'name': session.get('name'),
        'email': session.get('email'),
        'plan': session.get('plan', 'free')
    })

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    if data and 'message' in data:
        user_message = data['message'].lower()
        response = ""
        html = False

        time.sleep(random.uniform(0.5, 1.5))

        if any(word in user_message for word in ["hello", "hi", "hey"]):
            response = f"Hello {session.get('name', 'there')}! I'm Linky, your LinkedIn optimization assistant. How can I help you today?"
        elif "api" in user_message:
            html = True
            response = generate_api_response()
        elif "keyword" in user_message or "skills" in user_message:
            html = True
            response = generate_keyword_response(user_message)
        elif "score" in user_message or "complete" in user_message or "strength" in user_message:
            html = True
            response = generate_profile_score_response()
        elif "content" in user_message or "post" in user_message or "article" in user_message:
            html = True
            response = generate_content_ideas(user_message)
        elif "connect" in user_message or "network" in user_message or "connection" in user_message:
            html = True
            response = generate_connection_tips()
        elif "job" in user_message or "hunt" in user_message or "recruiter" in user_message:
            response = generate_job_search_advice()
        elif "optimize" in user_message or "improve" in user_message or "stand out" in user_message:
            response = generate_optimization_tips(user_message)
        elif "help" in user_message:
            response = """I can help with:
- Profile optimization tips
- Keyword suggestions for your industry
- LinkedIn API integration
- Profile completeness score analysis
- Content ideas for posts
- Connection strategies
- Job search optimization
- Networking advice

What would you like help with specifically?"""
        else:
            response = handle_general_questions(user_message)

        return jsonify({"response": response, "html": html})
    else:
        return jsonify({"response": "Sorry, I couldn't understand that.", "html": False}), 400

@app.route('/ai-analysis', methods=['POST'])
@login_required
def ai_analysis():
    data = request.get_json()
    if data and 'profile_data' in data:
        profile_url = data.get('profile_data', '').lower()
        
        industry = detect_industry_from_message(profile_url)
        analysis = generate_industry_specific_analysis(industry, profile_url)
        
        return jsonify(analysis)
    return jsonify({"error": "Invalid data"}), 400

@app.route('/profile-score-visualization')
@login_required
def profile_score_visualization():
    sections = list(knowledge_base["profile_sections"]["score_weights"].keys())
    weights = list(knowledge_base["profile_sections"]["score_weights"].values())
    
    df = pd.DataFrame({
        'Section': sections,
        'Weight': weights,
        'Completed': [True, True, False, True, True, False, False, False]
    })
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Profile Score', index=False)
        
        workbook = writer.book
        worksheet = writer.sheets['Profile Score']
        chart = workbook.add_chart({'type': 'bar'})
        
        chart.add_series({
            'name': 'Profile Score',
            'categories': '=Profile Score!$A$2:$A$9',
            'values': '=Profile Score!$B$2:$B$9',
        })
        
        worksheet.insert_chart('D2', chart)
    
    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='linkedin_profile_score.xlsx'
    )

@app.route('/export-profile-pdf')
@login_required
def export_profile_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="LinkedIn Profile Optimization Report", ln=1, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Profile Analysis", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"Report generated for: {session.get('name', 'User')}\n\nYour profile has been analyzed by our AI system. Here are the key findings and recommendations to improve your LinkedIn presence.")
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Strengths:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="- Strong keyword optimization\n- Complete experience section\n- Good education background")
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Areas for Improvement:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="- Summary could be more compelling\n- Need more recommendations\n- Skills section needs updating")

    buffer = io.BytesIO()
    pdf_bytes = pdf.output(dest='S')
    buffer.write(pdf_bytes)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='linkedin_optimization_report.pdf'
    )

@app.route('/analyze-summary', methods=['POST'])
@login_required
def analyze_summary():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    text = data['text']
    suggestions = []
    
    if len(text) < 150:
        suggestions.append("Consider expanding your summary to at least 150 characters for better visibility")
    elif len(text) > 2000:
        suggestions.append("Your summary is quite long. Consider keeping it under 2000 characters for readability")
    
    if not any(char.isdigit() for char in text):
        suggestions.append("Try including quantifiable achievements (e.g., 'Increased sales by 30%')")
    
    if "I " not in text and "my " not in text:
        suggestions.append("Using first-person pronouns (I, my) can make your summary more personal")
    
    action_verbs = ["led", "managed", "created", "developed", "increased", "improved"]
    if not any(verb in text.lower() for verb in action_verbs):
        suggestions.append("Use more action verbs to describe your achievements (e.g., led, created, improved)")
    
    if not suggestions:
        suggestions.append("Your summary looks good! Consider adding a call-to-action (e.g., 'Let's connect!')")
    
    return jsonify({"suggestions": suggestions})

@app.route('/analyze-headline', methods=['POST'])
@login_required
def analyze_headline():
    data = request.get_json()
    if not data or 'headline' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    headline = data['headline']
    score = random.randint(50, 90)
    
    tips = []
    
    if len(headline) < 30:
        tips.append({
            "text": "Your headline is too short. Aim for 30-120 characters.",
            "important": True
        })
    elif len(headline) > 120:
        tips.append({
            "text": "Your headline is too long. Keep it under 120 characters.",
            "important": True
        })
    
    if " at " not in headline and " | " not in headline:
        tips.append({
            "text": "Consider using '|' or 'at' to separate job title from value proposition.",
            "important": False
        })
    
    if len(headline.split()) < 4:
        tips.append({
            "text": "Add more keywords to help your profile appear in searches.",
            "important": True
        })
    
    value_words = ["help", "create", "build", "transform", "specialize", "expert"]
    if not any(word in headline.lower() for word in value_words):
        tips.append({
            "text": "Include what value you provide (e.g., 'helping businesses grow').",
            "important": False
        })
    
    return jsonify({
        "score": score,
        "tips": tips
    })

@app.route('/get-keywords', methods=['POST'])
@login_required
def get_keywords():
    data = request.get_json()
    if not data or 'role' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    role = data['role'].lower()
    industry = None
    
    for ind, data in knowledge_base["keywords"].items():
        if any(word in role for word in ind.split()):
            industry = ind
            break
    
    if not industry:
        industry = random.choice(list(knowledge_base["keywords"].keys()))
    
    keywords = knowledge_base["keywords"][industry]["keywords"]
    
    role_keywords = []
    if "engineer" in role:
        role_keywords = ["Systems Design", "Code Review", "Technical Leadership"]
    elif "manager" in role:
        role_keywords = ["Team Leadership", "Stakeholder Management", "Strategic Planning"]
    elif "analyst" in role:
        role_keywords = ["Data Visualization", "Business Intelligence", "Reporting"]
    
    keywords = list(set(keywords + role_keywords))[:15]
    
    return jsonify({"keywords": keywords})

@app.route('/generate-headlines', methods=['POST'])
@login_required
def generate_headlines():
    data = request.get_json()
    if not data or 'jobTitle' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    job_title = data['jobTitle']
    
    headlines = [
        f"{job_title} | Specializing in innovative solutions | Helping businesses grow",
        f"Experienced {job_title} | Transforming ideas into reality | Passionate about excellence",
        f"{job_title} | Technical Expert | Problem Solver | Team Player",
        f"Senior {job_title} | Driving digital transformation | Focused on measurable results",
        f"{job_title} | Creating value through technology | Let's connect!"
    ]
    
    return jsonify({"headlines": headlines})

if __name__ == '__main__':
    app.run(debug=True)
