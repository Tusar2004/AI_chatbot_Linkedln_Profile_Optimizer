from flask import Flask, request, jsonify, render_template, send_file
import random
import time
from datetime import datetime
import pandas as pd
import io
from fpdf import FPDF

app = Flask(__name__)

# Enhanced knowledge base with more industries and keywords
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

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if data and 'message' in data:
        user_message = data['message'].lower()
        response = ""
        html = False

        # Simulate processing time
        time.sleep(random.uniform(0.5, 1.5))

        # Handle greetings
        if any(word in user_message for word in ["hello", "hi", "hey"]):
            response = "Hello! I'm Linky, your LinkedIn optimization assistant. How can I help you today?"
        
        # Handle API questions
        elif "api" in user_message:
            html = True
            response = generate_api_response()
        
        # Handle keyword requests
        elif "keyword" in user_message or "skills" in user_message:
            html = True
            response = generate_keyword_response(user_message)
        
        # Handle profile score requests
        elif "score" in user_message or "complete" in user_message or "strength" in user_message:
            html = True
            response = generate_profile_score_response()
        
        # Handle content ideas
        elif "content" in user_message or "post" in user_message or "article" in user_message:
            html = True
            response = generate_content_ideas(user_message)
        
        # Handle connection tips
        elif "connect" in user_message or "network" in user_message or "connection" in user_message:
            html = True
            response = generate_connection_tips()
        
        # Handle job search questions
        elif "job" in user_message or "hunt" in user_message or "recruiter" in user_message:
            response = generate_job_search_advice()
        
        # Handle profile optimization questions
        elif "optimize" in user_message or "improve" in user_message or "stand out" in user_message:
            response = generate_optimization_tips(user_message)
        
        # Handle help request
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
        
        # Default response for unrecognized queries
        else:
            response = handle_general_questions(user_message)

        return jsonify({"response": response, "html": html})
    else:
        return jsonify({"response": "Sorry, I couldn't understand that.", "html": False}), 400

# New endpoint for AI analysis
@app.route('/ai-analysis', methods=['POST'])
def ai_analysis():
    data = request.get_json()
    if data and 'profile_data' in data:
        # Simulate AI analysis
        analysis = {
            "strengths": ["Strong keyword optimization", "Complete experience section", "Good education background"],
            "weaknesses": ["Summary could be more compelling", "Need more recommendations", "Skills section needs updating"],
            "suggestions": [
                "Add 3-5 more technical skills",
                "Include metrics in your experience descriptions",
                "Write a more engaging summary with your unique value proposition"
            ],
            "score": 78,
            "comparison": "Your profile scores higher than 65% of profiles in your industry"
        }
        return jsonify(analysis)
    return jsonify({"error": "Invalid data"}), 400

# New endpoint for profile score visualization
@app.route('/profile-score-visualization')
def profile_score_visualization():
    # Create a DataFrame for visualization
    sections = list(knowledge_base["profile_sections"]["score_weights"].keys())
    weights = list(knowledge_base["profile_sections"]["score_weights"].values())
    
    df = pd.DataFrame({
        'Section': sections,
        'Weight': weights,
        'Completed': [True, True, False, True, True, False, False, False]  # Sample data
    })
    
    # Convert to Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Profile Score', index=False)
        
        # Add chart
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

# New endpoint for PDF export
@app.route('/export-profile-pdf')
def export_profile_pdf():
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add title
    pdf.cell(200, 10, txt="LinkedIn Profile Optimization Report", ln=1, align='C')
    pdf.ln(10)
    
    # Add sections
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Profile Analysis", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Your profile has been analyzed by our AI system. Here are the key findings and recommendations to improve your LinkedIn presence.")
    
    # Add analysis
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
    
    # Create a BytesIO buffer and save the PDF to it
    buffer = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_bytes)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='linkedin_optimization_report.pdf'
    )

# Helper functions
def generate_api_response():
    response = """
        <p class="font-medium text-indigo-700">LinkedIn API Integration Guide</p>
        <ol class="list-decimal pl-5 mt-2 space-y-1 text-sm">
            <li class="font-medium">Register your app at <a href="https://developer.linkedin.com/" class="text-indigo-600 hover:underline" target="_blank">LinkedIn Developer Portal</a></li>
            <li>Choose the appropriate product for your needs</li>
            <li>Get your API keys (Client ID and Client Secret)</li>
            <li>Implement OAuth 2.0 authentication</li>
            <li>Make API calls to relevant endpoints</li>
        </ol>
        <p class="mt-3 font-medium">Available API Resources:</p>
        <div class="mt-2 space-y-2">
    """
    for resource in knowledge_base["api_resources"]:
        response += f"""
            <div class="bg-blue-50 p-2 rounded-lg border border-blue-100">
                <p class="font-medium text-blue-800">{resource['name']}</p>
                <p class="text-xs text-blue-600">{resource['desc']}</p>
            </div>
        """
    response += "</div>"
    return response

def generate_keyword_response(user_message):
    industry = detect_industry_from_message(user_message)
    return f"""
        <p class="font-medium">Keyword Suggestions for <span class="text-indigo-700">{industry.title()}</span>:</p>
        <div class="mt-2 flex flex-wrap gap-2">
            {''.join([f'<span class="bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full text-xs">{keyword}</span>' for keyword in knowledge_base["keywords"][industry]["keywords"]])}
        </div>
        <p class="mt-3 text-sm text-gray-700">{knowledge_base["keywords"][industry]["tips"]}</p>
    """

def generate_profile_score_response():
    return """
        <p class="font-medium">LinkedIn Profile Completeness</p>
        <p class="text-sm mt-1">Your profile strength is calculated based on these sections:</p>
        <div class="mt-3 grid md:grid-cols-2 gap-3">
            <div>
                <p class="font-medium text-green-700">Essential Sections</p>
                <ul class="list-disc pl-5 mt-1 text-sm space-y-1">
    """ + ''.join([f"<li>{section} ({knowledge_base['profile_sections']['score_weights'].get(section, 0)}%)</li>" 
                   for section in knowledge_base["profile_sections"]["required"]]) + """
                </ul>
            </div>
            <div>
                <p class="font-medium text-blue-700">Recommended Sections</p>
                <ul class="list-disc pl-5 mt-1 text-sm space-y-1">
    """ + ''.join([f"<li>{section} ({knowledge_base['profile_sections']['score_weights'].get(section, 0)}%)</li>" 
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
        </div>
    """

def generate_content_ideas(user_message):
    industry = detect_industry_from_message(user_message)
    return f"""
        <p class="font-medium">Content Ideas for {industry.title()}</p>
        <ul class="list-disc pl-5 mt-2 space-y-2 text-sm">
            {''.join([f'<li>{idea}</li>' for idea in knowledge_base["content_ideas"][industry]])}
        </ul>
        <p class="mt-3 text-sm bg-purple-50 p-2 rounded-lg border border-purple-100">
            <span class="font-medium">Pro Tip:</span> Mix educational, inspirational, and personal content for best engagement.
        </p>
    """

def generate_connection_tips():
    return """
        <p class="font-medium">LinkedIn Connection Growth Tips</p>
        <ul class="list-disc pl-5 mt-2 space-y-2 text-sm">
            {0}
        </ul>
        <p class="mt-3 text-sm bg-green-50 p-2 rounded-lg border border-green-100">
            <span class="font-medium">Remember:</span> Quality connections are more valuable than quantity.
        </p>
    """.format(''.join([f'<li>{tip}</li>' for tip in knowledge_base["connection_tips"]]))

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
    # Check if question matches any general question categories
    for category, questions in knowledge_base["general_questions"].items():
        for q in questions:
            if q.lower() in user_message:
                return f"For '{q}', here's my advice: {generate_optimization_tips(q)}"
    
    # Default response if no match found
    return "I can help with LinkedIn profile optimization, keyword suggestions, API integration, profile analysis, content ideas, and networking strategies. Could you please be more specific about what you need help with?"

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

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
