# ☀️ SolarMax Enterprise Advisor

SolarMax is a high-precision, conversational Generative AI web application built using **LangChain** and **Streamlit**. It acts as an intelligent Solar Energy Consultant, helping homeowners and businesses estimate their solar panel requirements, system sizing, and financial ROI with engineering-grade accuracy.

Unlike standard AI models that struggle with precise mathematics, SolarMax utilizes **LangChain Agents and Tool Calling** to run exact engineering formulas and regional grid tariffs (such as Tamil Nadu's TANGEDCO bi-monthly slab rates) via deterministic Python execution.

---

## 🚀 Features

- **High-Precision Calculations:** Automatically factors in a **20% system energy loss** (0.80 Derating Factor) and computes requirements using modern **540W Monocrystalline panels**.
- **Regional Grid Awareness:** Seamlessly handles localized utility rules, such as identifying if a user's usage crosses the critical 500-unit bi-monthly threshold in Tamil Nadu.
- **Conversational Memory:** Remembers past inputs throughout the chat session, allowing users to ask follow-up questions naturally (e.g., *"Can you change that to 440W panels instead?"*).
- **Professional Enterprise UI:** Built with a clean dashboard layout, responsive sidebar configuration tools, a quick-reset state button, and real-time connectivity status indicators.
- **Production-Grade Security:** Zero hardcoded credentials. All API keys are loaded safely from a local environment file.

---

## 🛠️ Tech Stack

- **Frontend UI:** Streamlit
- **LLM Orchestration:** LangChain (`langchain-openai`, `langchain-core`)
- **Foundation Model:** OpenAI `gpt-4o-mini`
- **Environment Management:** `python-dotenv`

---

## 📦 Installation & Setup

Follow these steps to set up and run SolarMax locally on your machine:

### 1. Clone or Create the Project Directory
Navigate to your project directory in your terminal:
```bash
cd "Basic Langchain demo"
