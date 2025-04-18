from flask import Flask, request, jsonify, render_template
import random
import time
from datetime import datetime

app = Flask(__name__)

# Enhanced knowledge base for LinkedIn optimization
knowledge_base = {
    "keywords": {
        "software engineering": {
            "keywords": ["Python", "JavaScript", "Java", "C++", "Algorithms", "Data Structures",
                         "Machine Learning", "Web Development", "Backend", "Frontend", "Full Stack",
                         "Cloud Computing", "AWS", "Azure", "Docker", "Kubernetes", "CI/CD",
                         "Agile Methodologies", "Scrum", "Test-Driven Development", "DevOps"],
            "tips": "Use a mix of technical skills and methodologies. Include both specific technologies and broader concepts."
        },
        "digital marketing": {
            "keywords": ["SEO", "Content Marketing", "Social Media", "PPC", "Google Analytics",
                         "Email Marketing", "Conversion Optimization", "Brand Strategy",
                         "Influencer Marketing", "Marketing Automation", "Data Analysis",
                         "CRM", "Market Research", "Copywriting", "Growth Hacking"],
            "tips": "Highlight both strategic and tactical skills. Include platform-specific skills when relevant."
        },
        "finance": {
            "keywords": ["Financial Analysis", "Investment Banking", "Portfolio Management",
                         "Risk Management", "Corporate Finance", "Financial Modeling",
                         "Valuation", "Mergers & Acquisitions", "Accounting", "CFA",
                         "Financial Reporting", "Excel", "Bloomberg Terminal", "Derivatives"],
            "tips": "Include certifications and specialized tools. Mix quantitative skills with strategic competencies."
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
        ]
    },
    "connection_tips": [
        "Personalize connection requests with a note about why you want to connect",
        "Engage with your network's content before requesting to connect",
        "Join and participate in LinkedIn groups in your industry",
        "Follow up new connections with a value-added message",
        "Maintain a regular posting schedule to stay visible"
    ]
}

@app.route('/chat', methods=['POST'])
def chat():
    print("Received a POST request to /chat")  # Added print statement
    data = request.get_json()
    if data and 'message' in data:
        user_message = data['message'].lower()
        print(f"User message received: {user_message}")  # Added print statement
        response = ""
        html = False

        # Simulate processing time
        time.sleep(random.uniform(0.5, 1.5))

        # Handle different user queries
        if any(word in user_message for word in ["hello", "hi", "hey"]):
            response = "Hello! I'm Linky, your LinkedIn optimization assistant. How can I help you today?"
        elif "api" in user_message:
            html = True
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
        elif "keyword" in user_message:
            industry = "software engineering"  # default
            if "marketing" in user_message:
                industry = "digital marketing"
            elif "finance" in user_message:
                industry = "finance"

            response = f"""
                <p class="font-medium">Keyword Suggestions for <span class="text-indigo-700">{industry.title()}</span>:</p>
                <div class="mt-2 flex flex-wrap gap-2">
                    {''.join([f'<span class="bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full text-xs">{keyword}</span>' for keyword in knowledge_base["keywords"][industry]["keywords"]])}
                </div>
                <p class="mt-3 text-sm text-gray-700">{knowledge_base["keywords"][industry]["tips"]}</p>
            """
            html = True
        elif "score" in user_message or "complete" in user_message:
            html = True
            response = """
                <p class="font-medium">LinkedIn Profile Completeness</p>
                <p class="text-sm mt-1">Your profile strength is calculated based on these sections:</p>
                <div class="mt-3 grid md:grid-cols-2 gap-3">
                    <div>
                        <p class="font-medium text-green-700">Essential Sections</p>
                        <ul class="list-disc pl-5 mt-1 text-sm space-y-1">
            """
            for section in knowledge_base["profile_sections"]["required"]:
                response += f"<li>{section} ({knowledge_base['profile_sections']['score_weights'].get(section, 0)}%)</li>"

            response += """
                        </ul>
                    </div>
                    <div>
                        <p class="font-medium text-blue-700">Recommended Sections</p>
                        <ul class="list-disc pl-5 mt-1 text-sm space-y-1">
            """
            for section in knowledge_base["profile_sections"]["optional"]:
                response += f"<li>{section} ({knowledge_base['profile_sections']['score_weights'].get(section, 0)}%)</li>"

            response += """
                        </ul>
                    </div>
                </div>
                <p class="mt-3 text-sm bg-blue-50 p-2 rounded-lg border border-blue-100">
                    <span class="font-medium">Tip:</span> Complete all essential sections and at least 3 recommended sections for maximum visibility.
                </p>
            """
        elif "content" in user_message or "post" in user_message:
            industry = detect_industry_from_message(user_message)
            html = True
            response = f"""
                <p class="font-medium">Content Ideas for {industry.title()}</p>
                <ul class="list-disc pl-5 mt-2 space-y-2 text-sm">
                    {''.join([f'<li>{idea}</li>' for idea in knowledge_base["content_ideas"][industry]])}
                </ul>
                <p class="mt-3 text-sm bg-purple-50 p-2 rounded-lg border border-purple-100">
                    <span class="font-medium">Pro Tip:</span> Mix educational, inspirational, and personal content for best engagement.
                </p>
            """
        elif "connect" in user_message or "network" in user_message:
            html = True
            response = """
                <p class="font-medium">LinkedIn Connection Growth Tips</p>
                <ul class="list-disc pl-5 mt-2 space-y-2 text-sm">
                    {}
                </ul>
                <p class="mt-3 text-sm bg-green-50 p-2 rounded-lg border border-green-100">
                    <span class="font-medium">Remember:</span> Quality connections are more valuable than quantity.
                </p>
            """.format(''.join([f'<li>{tip}</li>' for tip in knowledge_base["connection_tips"]]))
        elif "help" in user_message:
            response = """I can help with:
- Profile optimization tips
- Keyword suggestions
- LinkedIn API integration
- Profile completeness score
- Content ideas
- Connection strategies

What would you like help with?"""
        else:
            response = "I can help with LinkedIn profile optimization, keyword suggestions, API integration, profile analysis, content ideas, and networking strategies. Could you please be more specific about what you need help with?"

        print(f"Sending response: {response}, HTML: {html}") # Added print statement
        return jsonify({"response": response, "html": html})
    else:
        print("Error: Invalid JSON data received") # Added print statement
        return jsonify({"response": "Sorry, I couldn't understand that.", "html": False}), 400

def detect_industry_from_message(message):
    if "software" in message or "developer" in message or "engineer" in message:
        return "software engineering"
    elif "market" in message:
        return "digital marketing"
    elif "finance" in message or "bank" in message or "invest" in message:
        return "finance"
    else:
        return random.choice(["software engineering", "digital marketing", "finance"])

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)