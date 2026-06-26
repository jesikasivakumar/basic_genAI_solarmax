import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# --- 1. Load Environment Variables ---
# This automatically searches for a .env file and loads variables into the environment
load_dotenv()

# --- 2. Page Configuration & Professional UI Theme ---
st.set_page_config(
    page_title="SolarMax Enterprise Advisor", 
    page_icon="☀️", 
    layout="wide"  # Using wide layout for a cleaner dashboard look
)

# --- 3. Professional Sidebar Layout ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/solar-panel.png", width=80)
    st.title("SolarMax Control Panel")
    st.markdown("---")
    st.markdown("### System Configuration")
    
    # Let users change the creativity/precision parameter seamlessly
    temperature = st.slider("Model Precision (Temperature)", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    
    st.markdown("---")
    # Quick action button to wipe the conversation history clean
    if st.button("Clear Conversation History", type="primary", use_container_width=True):
        if "chat_history" in st.session_state:
            st.session_state.chat_history.clear()
            st.rerun()
            
    st.markdown("---")
    st.caption("🔒 **Security Note:** Your data and API connection are fully secured using environment variables.")

# --- 4. Main Application Interface ---
# Create columns to align the title and status badge cleanly
col1, col2 = st.columns([4, 1])
with col1:
    st.title("☀️ Solar Sizing & Consultation Assistant")
with col2:
    st.write("") # Padding adjustment
    st.success("● Engine Connected", icon="✅")

st.markdown("Use this intelligent calculator to estimate your property's solar potential, required panels, and projected capacity based on your consumption.")
st.markdown("---")

# --- 5. Initialize LangChain Components ---
@st.cache_resource
def init_langchain(temp):
    # The API key is safely pulled implicitly from the environment loaded by dotenv
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=temp)
    
    solar_system_prompt = (
    "You are an expert Solar Energy Consultant specializing in the Tamil Nadu (TANGEDCO) electrical grid environment.\n\n"
    "When a user provides their electricity bill details, use these precise engineering rules for calculation:\n"
    "1. Convert monthly metrics to standard TANGEDCO bi-monthly metrics (multiply units by 2).\n"
    "2. Account for a 20% system energy loss by applying a standard Derating Factor of 0.80 to the final system calculation.\n"
    "3. Assume average peak sunlight hours in Tamil Nadu is 5 hours/day.\n"
    "4. Use modern high-efficiency 540W panel sizes for calculating panel count rather than outdated low-wattage alternatives.\n"
    "5. Highlight the financial strategy: Emphasize how a solar setup helps them stay below TANGEDCO's high-tier 500-unit bi-monthly slab threshold.\n\n"
    "Format your final output with distinct, bold sections: '📊 TANGEDCO Slab Analysis', '📐 Technical System Sizing', and '💰 Financial Impact'."
)
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", solar_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    
    return prompt_template | llm | StrOutputParser()

# Pass the sidebar dynamic temperature slider value into our architecture
base_chain = init_langchain(temperature)

# --- 6. Manage Memory State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = InMemoryChatMessageHistory()

def get_session_history(session_id: str):
    return st.session_state.chat_history

conversational_chain = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

# --- 7. Render Streamlined Chat Experience ---
# Container constraint to prevent layout shifts
chat_container = st.container()

with chat_container:
    for msg in st.session_state.chat_history.messages:
        role = "user" if msg.type == "human" else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)

# --- 8. Handle Execution Input ---
if user_input := st.chat_input("Enter your consumption (e.g., 'My monthly bill is 700 kWh in Texas')..."):
    
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("assistant"):
            config = {"configurable": {"session_id": "solar_session_pro"}}
            response = st.write_stream(
                conversational_chain.stream({"input": user_input}, config=config)
            )