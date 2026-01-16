import streamlit as st
import ticket_service
import auth_service
import time

# --- Page Config ---
st.set_page_config(
    page_title="AI Support Gen",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Initialization ---
@st.cache_resource
def init_app():
    ticket_service.initialize_system()
    auth_service.create_default_users()

init_app()

# --- Custom CSS (Dark & Simple) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #e2e8f0; /* Light text */
    }

    /* Main Background */
    .stApp {
        background-color: #0f1116;
    }
    
    .block-container {
        max-width: 800px;
        padding-top: 3rem;
    }

    /* Inputs & TextAreas */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 6px;
    }
    
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6;
        box-shadow: none;
    }

    /* Buttons */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        width: 100%;
        transition: background 0.2s;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #2563eb;
    }

    /* Headings */
    h1, h2, h3 {
        color: #f8fafc !important;
    }
    
    /* Result Box */
    .view-container {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .res-title {
        color: #60a5fa; /* Light Blue */
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    .res-content {
        color: #cbd5e1; /* Gray-300 */
        line-height: 1.6;
    }
    
    /* Tab Styling */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #94a3b8 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #3b82f6 !important;
        border-bottom-color: #3b82f6 !important;
    }

</style>
""", unsafe_allow_html=True)

# --- Authentication State ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

def auth_page():
    st.title("Welcome to AI Support")
    st.markdown("Your intelligent technical resolution partner.")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            st.subheader("Sign In")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Access Account")
            
            if submit:
                if username and password:
                    user = auth_service.login_user(username, password)
                    if user:
                        st.session_state['user'] = user
                        st.success(f"Welcome back, {user['username']}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                else:
                    st.warning("Please enter both username and password.")

    with tab2:
        with st.form("signup_form"):
            st.subheader("Create Account")
            new_user = st.text_input("Choose Username")
            new_pass = st.text_input("Choose Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            submit_signup = st.form_submit_button("Register")
            
            if submit_signup:
                if new_user and new_pass and confirm_pass:
                    if new_pass != confirm_pass:
                        st.error("Passwords do not match.")
                    else:
                        if auth_service.register_user(new_user, new_pass, role="user"):
                            st.success("Account created! Please switch to Login tab.")
                        else:
                            st.error("Username already exists.")
                else:
                    st.warning("All fields are required.")

# --- Main App Logic ---

if not st.session_state['user']:
    auth_page()
else:
    main_app_user = st.session_state['user']
    
    # Header w/ Logout
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("IT Operations")
        st.caption(f"Logged in as {main_app_user['username']}")
    with c2:
        if st.button("Logout", type="secondary", use_container_width=True):
            st.session_state['user'] = None
            st.rerun()

    tab_submit, tab_history = st.tabs(["🔥 New Incident", "📂 My History"])

    # --- TAB 1: SUBMIT TICKET ---
    with tab_submit:
        with st.container():
            st.markdown("### Describe your issue")
            st.markdown("Our AI engine will analyze your request and provide an instant resolution.")
            
            with st.form("ticket_form"):
                c_a, c_b = st.columns(2)
                with c_a:
                    cat = st.selectbox("Category", ["Hardware", "Software", "Network", "Account", "Security", "Other"])
                with c_b:
                    prio = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                
                title = st.text_input("Issue Title", placeholder="e.g. Cannot connect to VPN")
                desc = st.text_area("Detailed Description", placeholder="Please provide error messages, steps taken, and system details...", height=150)
                
                submitted = st.form_submit_button("Analyze & Resolve")
                
                if submitted:
                    if title and desc:
                        with st.spinner("Analyzing knowledge base & generating solution..."):
                            ticket_service.submit_ticket(title, desc, cat, prio, main_app_user['username'])
                            
                            # Fetch user's latest ticket
                            df = ticket_service.get_user_tickets(main_app_user['username'])
                            latest = df.iloc[0] if not df.empty else None
                            
                            if latest is not None:
                                st.success("Analysis Complete")
                                
                                # Display Result
                                cat_color = "#f87171" if latest['category'] in ['Technical', 'Hardware', 'Network'] else "#94a3b8"
                                prio_color = "#ef4444" if latest['priority'] in ['High', 'Critical'] else "#22c55e"
                                
                                html_content = f"""
                                <div class="view-container">
                                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                                        <div style="display:flex; flex-direction:column;">
                                            <span style="font-size:1.2rem; font-weight:700; color:#f8fafc;">{latest['title']}</span>
                                            <span style="font-size:0.8rem; color:#94a3b8;">ID: INC-{latest['id']:04d}</span>
                                        </div>
                                        <div style="display:flex; gap:0.5rem;">
                                            <span style="background:{cat_color}; color:black; padding:2px 10px; border-radius:4px; font-size:0.75rem; font-weight:600;">{latest['category']}</span>
                                            <span style="background:{prio_color}; color:white; padding:2px 10px; border-radius:4px; font-size:0.75rem; font-weight:600;">{latest['priority']}</span>
                                        </div>
                                    </div>
                                    <div class="res-title">
                                        <span>✨</span> AI Resolution
                                    </div>
                                    <div class="res-content">
                                        {latest['ai_resolution']}
                                    </div>
                                </div>
                                """
                                st.markdown(html_content, unsafe_allow_html=True)
                    else:
                        st.warning("Please provide details for accurate analysis.")

    # --- TAB 2: MY HISTORY ---
    with tab_history:
        st.markdown("### Your Past Incidents")
        df_hist = ticket_service.get_user_tickets(main_app_user['username'])
        
        if df_hist.empty:
            st.info("No tickets found in history.")
        else:
            for idx, row in df_hist.iterrows():
                with st.expander(f"{row['created_at'][:16]} | {row['title']} ({row['priority']})"):
                    st.markdown(f"**Category:** {row['category']} | **Priority:** {row['priority']}")
                    st.markdown(f"**Description:** {row['description']}")
                    st.markdown("---")
                    st.markdown(f"**AI Resolution:**\n{row['ai_resolution']}")


