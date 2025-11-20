"""
AI Sales Assistant - Streamlit Frontend
"""
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from streamlit_option_menu import option_menu

# Configuration
st.set_page_config(
    page_title="AI Sales Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .score-display {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .high-score { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; }
    .medium-score { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; }
    .low-score { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=100)
    st.title("AI Sales Assistant")
    
    selected = option_menu(
        menu_title="Navigation",
        options=["Dashboard", "Lead Scorer", "Email Generator", "Chat Assistant", "Analytics"],
        icons=["house", "calculator", "envelope", "chat-dots", "graph-up"],
        menu_icon="cast",
        default_index=0,
    )
    
    st.divider()
    
    # API Status
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Connected")
            health_data = response.json()
            st.caption(f"ML Model: {'✅' if health_data.get('ml_model_loaded') else '❌'}")
            st.caption(f"Groq API: {'✅' if health_data.get('groq_api_configured') else '❌'}")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")
        st.caption("Start backend with: python run_server.py")


# ============================================================
# PAGE: DASHBOARD
# ============================================================
if selected == "Dashboard":
    st.markdown('<p class="main-header">🏠 Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Sales & Lead Qualification Platform</p>', unsafe_allow_html=True)
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="📊 Total Leads", value="247", delta="+12")
    with col2:
        st.metric(label="🔥 High Quality", value="89", delta="+5")
    with col3:
        st.metric(label="✉️ Emails Generated", value="156", delta="+23")
    with col4:
        st.metric(label="📈 Avg Score", value="64.5%", delta="+2.3%")
    
    st.divider()
    
    # Recent Leads Table
    st.subheader("📋 Recent Leads")
    
    # Sample data
    recent_leads = pd.DataFrame({
        'Name': ['Ahmed Ben Ali', 'Sarah Mohamed', 'Youssef Trabelsi', 'Fatma Gharbi', 'Karim Mansour'],
        'Company': ['TechCorp', 'InnovateLab', 'StartupHub', 'FinanceGroup', 'DataSolutions'],
        'Job Title': ['CEO', 'CTO', 'Founder', 'CFO', 'VP Sales'],
        'Score': [85, 72, 91, 68, 77],
        'Quality': ['HIGH', 'MEDIUM', 'HIGH', 'MEDIUM', 'HIGH']
    })
    
    # Color coding
    def color_quality(val):
        if val == 'HIGH':
            return 'background-color: #d1fae5; color: #065f46'
        elif val == 'MEDIUM':
            return 'background-color: #fef3c7; color: #92400e'
        else:
            return 'background-color: #fee2e2; color: #991b1b'
    
    styled_df = recent_leads.style.applymap(color_quality, subset=['Quality'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Lead Distribution by Quality")
        quality_data = pd.DataFrame({
            'Quality': ['HIGH', 'MEDIUM', 'LOW'],
            'Count': [89, 112, 46]
        })
        fig = px.pie(quality_data, values='Count', names='Quality', 
                     color='Quality',
                     color_discrete_map={'HIGH': '#10b981', 'MEDIUM': '#f59e0b', 'LOW': '#ef4444'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Leads Over Time")
        time_data = pd.DataFrame({
            'Date': pd.date_range(start='2024-01-01', periods=7, freq='D'),
            'Leads': [23, 31, 28, 35, 42, 38, 50]
        })
        fig = px.line(time_data, x='Date', y='Leads', markers=True)
        fig.update_traces(line_color='#3b82f6')
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE: LEAD SCORER
# ============================================================
elif selected == "Lead Scorer":
    st.markdown('<p class="main-header">🧮 Lead Scorer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Score leads using AI-powered machine learning</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Lead Information")
        
        with st.form("lead_form"):
            # Personal Info
            col_a, col_b = st.columns(2)
            with col_a:
                first_name = st.text_input("First Name *", placeholder="Ahmed")
            with col_b:
                last_name = st.text_input("Last Name", placeholder="Ben Ali")
            
            email = st.text_input("Email *", placeholder="ahmed@company.com")
            company_name = st.text_input("Company Name", placeholder="TechCorp")
            
            # Company Info
            col_a, col_b = st.columns(2)
            with col_a:
                company_size = st.selectbox("Company Size", 
                    ["1-10", "11-50", "51-200", "201-1000", "1000+"])
            with col_b:
                industry = st.selectbox("Industry",
                    ["technology", "finance", "healthcare", "retail", "manufacturing", "other"])
            
            job_title = st.text_input("Job Title", placeholder="CEO")
            
            st.divider()
            st.subheader("📊 Engagement Metrics")
            
            col_a, col_b = st.columns(2)
            with col_a:
                website_visits = st.number_input("Website Visits", min_value=0, value=0)
                email_opens = st.number_input("Email Opens", min_value=0, value=0)
            with col_b:
                email_clicks = st.number_input("Email Clicks", min_value=0, value=0)
                form_submissions = st.number_input("Form Submissions", min_value=0, value=0)
            
            submitted = st.form_submit_button("🚀 Score Lead", use_container_width=True)
            
            if submitted:
                if not first_name or not email:
                    st.error("Please fill in required fields (Name & Email)")
                else:
                    # Prepare data
                    lead_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "company_name": company_name,
                        "company_size": company_size,
                        "industry": industry,
                        "job_title": job_title,
                        "website_visits": website_visits,
                        "email_opens": email_opens,
                        "email_clicks": email_clicks,
                        "form_submissions": form_submissions
                    }
                    
                    # Call API
                    with st.spinner("Scoring lead..."):
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/api/leads/score",
                                json=lead_data
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                st.session_state['score_result'] = result
                                st.success("✅ Lead scored successfully!")
                                st.rerun()
                            else:
                                st.error(f"Error: {response.text}")
                        except Exception as e:
                            st.error(f"Connection error: {e}")
    
    with col2:
        st.subheader("📊 Score Result")
        
        if 'score_result' in st.session_state:
            result = st.session_state['score_result']
            score = result['score_percentage']
            
            # Score display
            if score >= 70:
                score_class = "high-score"
                emoji = "🔥"
            elif score >= 40:
                score_class = "medium-score"
                emoji = "⚡"
            else:
                score_class = "low-score"
                emoji = "❄️"
            
            st.markdown(f'''
            <div class="score-display {score_class}">
                {emoji}<br>
                {score:.1f}%<br>
                <small>{result['quality_level']} QUALITY</small>
            </div>
            ''', unsafe_allow_html=True)
            
            # Recommendation
            st.info(f"**💡 Recommendation:** {result['recommendation']}")
            
            # Insights
            st.subheader("🔍 Lead Insights")
            st.json(result['insights'])
            
            # Clear button
            if st.button("🔄 Score Another Lead"):
                del st.session_state['score_result']
                st.rerun()
        else:
            st.info("👈 Fill out the form to score a lead")


# ============================================================
# PAGE: EMAIL GENERATOR
# ============================================================
elif selected == "Email Generator":
    st.markdown('<p class="main-header">✉️ Email Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Generate personalized emails with Groq AI</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Lead Information")
        
        with st.form("email_form"):
            first_name = st.text_input("First Name *")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email *")
            company_name = st.text_input("Company Name")
            job_title = st.text_input("Job Title")
            industry = st.selectbox("Industry", ["technology", "finance", "healthcare", "retail", "other"])
            
            email_type = st.selectbox("Email Type", ["introduction", "follow_up", "demo_request"])
            
            submitted = st.form_submit_button("✨ Generate Email", use_container_width=True)
            
            if submitted:
                if not first_name or not email:
                    st.error("Please fill in required fields")
                else:
                    lead_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "company_name": company_name,
                        "job_title": job_title,
                        "industry": industry
                    }
                    
                    request_data = {
                        "lead": lead_data,
                        "email_type": email_type
                    }
                    
                    with st.spinner("Generating email with Groq AI..."):
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/api/emails/generate",
                                json=request_data
                            )
                            
                            if response.status_code == 200:
                                email_result = response.json()
                                st.session_state['email_result'] = email_result
                                st.success("✅ Email generated!")
                                st.rerun()
                            else:
                                st.error(f"Error: {response.text}")
                        except Exception as e:
                            st.error(f"Error: {e}")
    
    with col2:
        st.subheader("📧 Generated Email")
        
        if 'email_result' in st.session_state:
            email_data = st.session_state['email_result']
            
            st.text_input("Subject", value=email_data['subject'], disabled=True)
            st.text_area("Body", value=email_data['body'], height=300, disabled=True)
            
            st.info(f"Lead Score: {email_data['lead_score']*100:.1f}%")
            st.caption(f"Generated at: {email_data['generated_at']}")
            
            if st.button("🔄 Generate Another"):
                del st.session_state['email_result']
                st.rerun()
        else:
            st.info("👈 Fill out the form to generate an email")


# ============================================================
# PAGE: CHAT ASSISTANT
# ============================================================
elif selected == "Chat Assistant":
    st.markdown('<p class="main-header">💬 Sales Chat Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Get real-time sales advice powered by Groq AI</p>', unsafe_allow_html=True)
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask for sales advice..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/api/chat/message",
                        json={
                            "session_id": "streamlit-session",
                            "message": prompt
                        }
                    )
                    
                    if response.status_code == 200:
                        assistant_response = response.json()['response']
                        st.markdown(assistant_response)
                        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    else:
                        st.error("Error communicating with assistant")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# PAGE: ANALYTICS
# ============================================================
elif selected == "Analytics":
    st.markdown('<p class="main-header">📊 Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">ML Model Performance & Insights</p>', unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/analytics/model-info")
        if response.status_code == 200:
            model_info = response.json()['model_info']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Model Type", model_info.get('model_type', 'N/A'))
            with col2:
                test_acc = model_info['metrics'].get('test_accuracy', 0) * 100
                st.metric("Test Accuracy", f"{test_acc:.1f}%")
            with col3:
                roc_auc = model_info['metrics'].get('roc_auc', 0)
                st.metric("ROC AUC", f"{roc_auc:.3f}")
            
            st.divider()
            
            # Feature Importance
            if model_info.get('feature_importance'):
                st.subheader("🎯 Feature Importance")
                feature_df = pd.DataFrame(model_info['feature_importance'])
                fig = px.bar(feature_df.head(10), x='importance', y='feature', 
                            orientation='h', title="Top 10 Most Important Features")
                st.plotly_chart(fig, use_container_width=True)
            
            # Model Details
            st.subheader("ℹ️ Model Details")
            st.json(model_info)
        else:
            st.error("Could not fetch model information")
    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.divider()
st.caption("🤖 AI Sales Assistant | Powered by FastAPI, Groq & Streamlit | Made with ❤️")
