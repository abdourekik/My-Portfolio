# 🎯 AI Sales & Lead Qualification Assistant

An intelligent sales automation platform powered by AI that helps businesses qualify leads, generate personalized emails, and provide real-time sales insights.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![Groq](https://img.shields.io/badge/Groq-API-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🎯 Intelligent Lead Scoring
- Automatic lead scoring based on multiple criteria
- Company size, budget, and industry analysis
- Real-time score calculation and ranking
- Priority-based lead organization

### ✉️ AI-Powered Email Generation
- Personalized outreach emails
- Industry-specific customization
- Multiple tone options (professional, friendly, casual)
- Ready-to-send email templates

### 💬 Lead Qualification Chat
- Interactive AI chatbot for lead qualification
- Natural conversation flow
- Extracts key information (budget, timeline, pain points)
- Conversational memory for context-aware responses

### 📊 Sales Insights & Analytics
- AI-generated lead insights
- Opportunity identification
- Challenge analysis
- Recommended sales approaches

### 🎓 Sales Coaching
- Real-time sales advice
- Situation-specific recommendations
- Best practices and talking points
- Action steps for sales reps


## 🛠️ Tech Stack

**Backend:**
- Python 3.10+
- Flask (Web framework)
- Groq API (LLM - Llama 3.1)
- Pandas (Data processing)

**Frontend:**
- HTML5/CSS3
- JavaScript (ES6+)
- Responsive Design

**AI/ML:**
- Groq Llama 3.1 8B Instant
- Natural Language Processing
- Lead Scoring Algorithm

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Groq API key ([Get one here](https://console.groq.com))
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-sales-assistant.git
cd ai-sales-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the application**
```bash
python app.py
```

6. **Open your browser**
```
http://localhost:5000
```

## 🚀 Usage

### Lead Scoring
1. Navigate to the "Leads Dashboard"
2. View automatically scored leads
3. Click on any lead for detailed insights

### Email Generation
1. Go to "Email Generator" tab
2. Select or enter lead details
3. Choose email tone
4. Click "Generate Email"
5. Copy and customize as needed

### Lead Qualification
1. Open "Qualification Chat"
2. Start conversation with the AI
3. AI asks qualifying questions
4. Receive qualification summary

### Sales Coaching
1. Navigate to "Sales Advisor"
2. Describe your sales situation
3. Get AI-powered advice and action steps

## 📁 Project Structure
```
ai-sales-assistant/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
├── .gitignore             # Git ignore file
├── README.md              # This file
│
├── templates/
│   └── index.html         # Main web interface
│
├── static/
│   ├── style.css          # Styling
│   └── js/
│       └── main.js        # Frontend JavaScript
│
├── leads_data/
│   └── sample_leads.csv   # Sample lead data
│
└── screenshots/           # Project screenshots
    ├── dashboard.png
    ├── email-gen.png
    └── chat.png
```

## 🔌 API Endpoints

### GET `/api/leads`
Get all leads with calculated scores
```json
{
  "success": true,
  "leads": [
    {
      "id": 1,
      "name": "Tech Corp",
      "score": 85,
      ...
    }
  ]
}
```

### GET `/api/lead/<id>`
Get detailed lead information
```json
{
  "success": true,
  "lead": {
    "id": 1,
    "score": 85,
    "insights": "AI-generated insights..."
  }
}
```

### POST `/api/generate-email`
Generate personalized sales email
```json
{
  "lead_name": "John Doe",
  "company": "Tech Corp",
  "industry": "Technology",
  "tone": "professional"
}
```

### POST `/api/qualify-lead`
Lead qualification conversation
```json
{
  "message": "We're looking for a CRM solution",
  "conversation": []
}
```

### POST `/api/sales-advice`
Get sales coaching advice
```json
{
  "situation": "Client objecting to price"
}
```

### POST `/api/add-lead`
Add new lead to system
```json
{
  "name": "Company Name",
  "email": "email@example.com",
  "company_size": "100",
  "industry": "Technology",
  "budget": "$50k-100k"
}
```

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)
*Lead scoring and prioritization dashboard*

### Email Generator
![Email Generator](screenshots/email-gen.png)
*AI-powered personalized email generation*

### Qualification Chat
![Chat](screenshots/chat.png)
*Interactive lead qualification conversation*

## 🔮 Future Enhancements

- [ ] CRM integration (Salesforce, HubSpot)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Email tracking and analytics
- [ ] Lead enrichment from external APIs
- [ ] Automated follow-up sequences
- [ ] Team collaboration features
- [ ] Mobile app version
- [ ] Voice call analysis
- [ ] Meeting scheduler integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@abdourekik](https://github.com/abdourekik)
- LinkedIn: [abderrahmen rekik](linkedin.com/in/abderrahmen-rekik)
- Email: rekikabderrahmen52@gmail.com

## 🙏 Acknowledgments

- Groq for providing the LLM API
- Flask community for the excellent web framework
- All contributors and testers

---

⭐ If you found this project helpful, please give it a star!

**Built with ❤️ for the sales automation community**
