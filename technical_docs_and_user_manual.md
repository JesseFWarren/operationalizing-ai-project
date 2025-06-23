# Health Live Chat

Health Live Chat is an AI-powered assistant for answering health-related questions using both text and optional image inputs (e.g., for skin issues). It provides friendly, context-aware responses while enforcing security, privacy, and responsible AI practices. The system is built using FastAPI for the backend and React for the frontend.

---

## Technical Documentation

### System Components

- **Frontend:** React single-page app (SPA)
- **Backend:** FastAPI server with OpenAI integration
- **Image Handling:** Temporary upload and captioning using a vision model
- **Moderation & PII Control:** Input filtering, PII redaction
- **Logging:** Secure audit and interaction logging (optional S3 support)
- **Model:** GPT-4 (via OpenAI)

### Endpoints

| Endpoint     | Method | Description                                |
| ------------ | ------ | ------------------------------------------ |
| `/ask`       | POST   | Handles text-only health queries           |
| `/ask_image` | POST   | Handles queries with optional image upload |

All endpoints require an API key via the `x-api-key` header.

### Backend Environment Variables

| Variable               | Purpose                            |
| -----------------------| ---------------------------------- |
| `API_KEY`              | Secures endpoints                  |
| `OPENAI_API_KEY`       | OpenAI API access                  |
| `USE_BEDROCK`          | Set to `false` to use OpenAI       |
| `S3_BUCKET`            | S3-based log storage               |
| `AWS_REGION`           | AWS region for S3                  |
| `AWS_SECRET_ACCESS_KEY`| AWS Secret Access Key              |
| `AWS_ACCESS_KEY_ID`    | AWS Access Key ID                  |


---

## User Manual  
Refer to the Deployment guide for deployment instructions.

### How to Use

1. Navigate to the Health Live Chat website.
2. Enter your symptom or question in the text box.
3. (Optional) Upload an image to accompany your query.
4. Click **Send** to receive a response from the AI assistant.

The assistant will:

- Respond with the top 3 likely conditions based on Mayo Clinic context
- Advise you to consult a healthcare professional
- Never diagnose, prescribe, or impersonate a doctor

### Example Use Cases

- "What are the symptoms of dehydration?"
- "I have a red rash on my leg, should I be concerned?" (with image)

---

## Architecture Diagram

```text
     [ User (Browser) ]
             |
             v
       [ React Frontend ]
             |
             v
      [ FastAPI Backend ]
         |    |     |   
         |    |     |   
       Moderation  PII
         |    |     |
         |  Image  Search
         | Captioning
         |    |     |
         +----v-----+----+
              |          
              v          
       [ OpenAI GPT-4 ]
              |
              v
          Response
```

## Test Coverage Report
| File                    | Stmts | Miss | Cover  | Missing Lines                        |
|-------------------------|-------|------|--------|--------------------------------------|
| `src/analytics.py`      | 53    | 25   | 53%    | 12–31, 53, 56–57, 62–65              |
| `src/bedrock_model.py`  | 9     | 9    | 0%     | 1–41                                 |
| `src/chatbot.py`        | 21    | 4    | 81%    | 10, 45–48                            |
| `src/dashboard.py`      | 36    | 36   | 0%     | 1–49                                 |
| `src/data_extraction.py`| 101   | 101  | 0%     | 1–156                                |
| `src/model_api.py`      | 7     | 2    | 71%    | 7–8                                  |
| `src/pipeline.py`       | 76    | 17   | 78%    | 46, 48–58, 95, 98, 105, 111, 118–122 |
| `src/retrieval.py`      | 24    | 4    | 83%    | 21, 28, 33–34                        |
| `src/vector_storage.py` | 63    | 63   | 0%     | 1–96                                 |
| `src/vision_model.py`   | 14    | 8    | 43%    | 10–17                                |
| Total                   | 404   | 269  | 33%    |                                      |

- Only the most important functionalities were tested. Files that were not used or used strictly for the rag system or the dashboard were not tested. This explains the low oeverall test coverage percentage.

## Additional Technical Assessment

### Complexity

This project builds a full-stack AI-powered health chatbot that supports both multimodal (Text and Image) inputs. It integrates:  

- A FastAPI backend with input validation and API key protection
- A React frontend for real-time user interaction
- A modular processing pipeline including moderation, RAG (retrieval-augmented generation), and vision components
- S3-based audit logging
- A Streamlit dashboard for usage analytics
- Unit test coverage with `pytest`

The Key Complexities include:  
- Multimodal input handling (text + image)
- Integration of multiple model types (OpenAI, FAISS, Vision)
- End-to-end logging and analytics
- Modular, testable architecture

---
### Big O of Key Aspects

| Component                | Operation                              | Time Complexity |
|--------------------------|----------------------------------------|-----------------|
| `moderate_input()`       | Regex matching on input string         | O(n)            |
| `strip_pii()`            | Regex substitution                     | O(n)            |
| `search()` (FAISS)       | Approx. k-NN over vector DB            | ~O(log n)       |
| `generate_response()`    | Transformer model inference            | O(n²) or higher |
| `run_pipeline()`         | Combined pipeline sequence             | O(n + m + log k)|

> **Notes**:
> - `n` = length of input string  
> - `m` = number of retrieved documents  
> - `k` = size of FAISS index

---

### CI/CD

The project is CI ready:

- All unit tests use `pytest`
- Test coverage is tracked with `pytest-cov`
- Modular code structure allows for easy CI integration

While deployment is currently manual via [Render](https://render.com), CI/CD can be integrated with:
- Test + linting steps on `git push`
- Coverage thresholds
- Optional auto-deploy using Render’s API or GitHub webhook

---

### Performance Profile

Performance was measured across the stack:

| Component         | Approximate Latency          |
|-------------------|------------------------------|
| Text-only queries | ~5-8 secs                    |
| Image + text      | ~10-12 secs                  |
| FAISS search      | < 0.2 sec                    |
| Dashboard load    | ~1.1 sec (includes S3 fetch) |

Performance highlights:  
- Lightweight and asynchronous audit logging
- In-memory caching added for repeated queries