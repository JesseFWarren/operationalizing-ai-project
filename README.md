# operationalizing-ai-project

**Health Live Chat** is an AI-powered conversational assistant that helps users ask general health-related questions and receive instant, informative answers. It uses large language models (LLMs) to provide context-aware, privacy-conscious, and user-friendly health information responses.
[HealthLiveChat](https://healthlivechat.onrender.com/)

## Project Goals
- Build and deploy a conversational health assistant
- Implement secure, ethical, and scalable LLM workflows
- Demonstrate week-by-week updates in line with production-ready AI standards
- Create a portfolio-ready project using AWS or open-source tools

## Weekly Breakdown

### Week 1: Foundational Conversational AI (OpenAI)
- Implemented initial version of the Health Live Chat assistant
- Used OpenAI GPT model to power health-related conversations
- Built core message loop and response logic
- Documented basic usage and architecture

### Week 2: Modular Pipeline & Bedrock Integration
- Refactored chatbot into a modular pipeline (`pipeline.py`)
  - Input → moderation → model → logging → output
- Implemented retry logic and logging to `chatlog.csv`
- Structured code to easily be switched to bedrock once I recieve access

### Week 3: Enterprise Deployment & Security
- Deploy the backend using AWS App Runner
- Add token-based authentication to secure endpoints
- Create `deployment_guide.md` with setup instructions
- Begin implementing basic audit logging for user activity

### Week 4: Usage Analytics & Dashboard
- Track key metrics:
  - Number of queries
  - Common keywords
  - Average response length
- Visualize logs with a basic dashboard (Streamlit + CSV analysis)
- Export log data for performance tracking

### Week 5: Safety Filters & Generative AI Ethics
- Implement basic content moderation for unsafe inputs
- Strip PII before sending queries to the model
- Add disclaimers and tune prompts to reduce hallucination
- Strengthen user safety and align with Responsible AI practices

### Week 6: Final Polish
- Finalize documentation:
  - `README.md`
  - `api_docs.md`
  - `security_and_ethics.md`
  - `deployment_guide.md`
- Record a 5-minute demo video walkthrough of the project
- Clean and organize code for final submission

### Final Project Summary
The final version of Health Live Chat includes:
- A fully functional health Q&A assistant powered by Amazon Bedrock
- Modular orchestration pipeline with retry and logging
- Secure deployment with authentication via App Runner
- Analytics dashboard for usage insights
- Safety and privacy filters for ethical AI usage
- Frontend interface and complete documentation