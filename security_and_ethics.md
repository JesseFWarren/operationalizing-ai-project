# Security and Responsible AI Practices

This document outlines the security measures, privacy controls, and responsible AI practices implemented in the **HealthLiveChat** system to ensure the ethical and secure deployment of AI in healthcare-related interactions.

---

## Security Measures

### 1. API Key Protection
- All endpoints (`/ask`, `/ask_image`) are secured using the `x-api-key` request header.
- Requests without a valid API key return a `401 Unauthorized` error.
- API keys are stored as environment variables on the backend.

### 2. Input Sanitization and Moderation
- User inputs are screened through a custom moderation layer.
- Inputs containing flagged or harmful keywords are blocked before processing.

### 3. PII Redaction
- Personally Identifiable Information (PII) such as email addresses, phone numbers, and credit card numbers is automatically detected and masked in user queries.

### 4. Secure Image Handling
- Uploaded images are temporarily saved to `/tmp` and automatically deleted after processing.
- Only valid image formats (`.jpg`, `.png`, etc.) are accepted.

### 5. HTTPS Communication
- All traffic between the frontend and backend is encrypted via HTTPS.
- No sensitive data is stored persistently on the server or client.

---

## Privacy Controls

- No user input (text or image) is stored long-term.
- Audit logs (for transparency and debugging) are anonymized and securely stored.
- Logs include timestamps, sanitized queries, and truncated model outputs only.
- The system does not use cookies or any method to track users across sessions.

---

## Responsible AI Practices

### 1. Bias and Fairness
- The system does not diagnose or make clinical decisions.
- All responses are generated for informational purposes and advise users to consult real healthcare professionals.

### 2. Transparency
- The chatbot avoids impersonating medical professionals or giving treatment recommendations.

### 3. Content Filtering
- Unsafe, offensive, or inappropriate prompts are blocked via keyword moderation.
- Profanity and violent language are filtered before processing.

### 4. Compliance and Ethics
- While not HIPAA-certified, the system is designed to avoid collecting or storing PHI (Protected Health Information).
- Implementation follows ethical guidelines for deploying LLMs in experimental, non-clinical settings.

---

## Disclaimer

This application is intended for informational and educational purposes only.  
It is not a substitute for professional medical advice, diagnosis, or treatment.  
Always seek the guidance of a qualified healthcare provider with any questions you may have regarding a medical condition.
