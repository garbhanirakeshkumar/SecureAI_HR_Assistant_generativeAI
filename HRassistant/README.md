# SecureAI HR Assistant 🔐

SecureAI HR Assistant is a secure, AI-powered HR chatbot and document intelligence system built with **Django, Python, Sentence Transformers, and Google Gemini**.

The system allows HR personnel to upload company HR documents and provides employees with an AI assistant that answers HR-related questions using only the documents uploaded by HR.

The project also demonstrates practical **AI security** concepts such as prompt injection detection, PII protection, AI response validation, and security audit logging.

---

## 🚀 Features

### 🤖 AI HR Assistant

* Employees can ask HR-related questions through the chatbot.
* Uses Google Gemini for natural-language responses.
* Uses Retrieval-Augmented Generation (RAG).
* Answers HR policy questions using HR-uploaded documents.
* Handles casual conversations separately.
* Does not use built-in project policy documents.

### 📄 HR Document Management

* HR users can upload company documents.
* Supported formats:

  * PDF
  * DOCX
  * TXT
  * Markdown
* Uploaded documents are automatically:

  * Processed
  * Text extracted
  * Split into chunks
  * Converted into embeddings
  * Stored for semantic search
* HR users can view uploaded documents.
* HR users can delete uploaded documents.
* Employees cannot upload or delete HR documents.

### 🔎 Semantic Search

* Uses `all-MiniLM-L6-v2` from Sentence Transformers.
* Converts user questions and document chunks into embeddings.
* Uses cosine similarity to find relevant information.
* Retrieves the most relevant HR document chunks for the chatbot.

### 🛡️ AI Security

#### Prompt Injection Detection

Detects suspicious instructions such as:

* Ignore previous instructions
* Reveal system prompts
* Bypass security
* Reveal passwords or API keys
* Role manipulation

#### PII Protection

Detects and masks sensitive information such as:

* Email addresses
* Phone numbers
* ID-like numbers

#### AI Response Validation

Checks generated responses for:

* Email addresses
* Phone numbers
* Potential ID numbers
* Passwords
* API keys
* Access tokens
* Other sensitive information

#### Security Audit Logs

Records security events with:

* Event type
* Message
* Risk level
* Timestamp

Security events can be viewed through:

* Total Events
* High Risk
* Medium Risk
* Low Risk

---

## 👥 User Roles

### HR

HR users can:

* Access the HR dashboard
* Manage employees
* Upload HR documents
* View uploaded documents
* Delete uploaded documents
* Use the HR chatbot
* View security logs
* Use the security scanner

### Employee

Employees can:

* Access the employee dashboard
* View their profile
* Use the HR chatbot
* Ask questions about available HR policies

Employees cannot upload or delete HR documents.

---

## 🧠 RAG Architecture

```text
                 HR USER
                    │
                    ▼
            Upload HR Document
                    │
                    ▼
          Document Text Extraction
                    │
                    ▼
             Text Chunking
                    │
                    ▼
        Sentence Transformer Model
             all-MiniLM-L6-v2
                    │
                    ▼
          Generate Embeddings
                    │
                    ▼
          HRDocumentChunk Database
                    │
                    │
                    ▼
EMPLOYEE ──► HR QUESTION
                    │
                    ▼
             Question Embedding
                    │
                    ▼
             Semantic Search
                    │
                    ▼
          Relevant HR Documents
                    │
                    ▼
               Google Gemini
                    │
                    ▼
           AI Response Validation
                    │
                    ▼
             Secure HR Answer
```

---

## 🔐 Security Architecture

```text
User Input
    │
    ▼
Prompt Injection Detection
    │
    ├── High Risk ──► Security Audit Log
    │
    ├── Medium Risk ► Security Audit Log
    │
    └── Low Risk
          │
          ▼
      PII Masking
          │
          ▼
       HR RAG
          │
          ▼
       Gemini AI
          │
          ▼
   Response Validation
          │
          ▼
      Final Response
```

---

## 🛠️ Technology Stack

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python                | Backend programming             |
| Django                | Web framework                   |
| SQLite                | Database                        |
| HTML                  | Frontend                        |
| CSS                   | User interface                  |
| Google Gemini         | Generative AI                   |
| Sentence Transformers | Text embeddings                 |
| Scikit-learn          | Cosine similarity               |
| PyPDF                 | PDF text extraction             |
| python-docx           | DOCX text extraction            |
| python-dotenv         | Environment variable management |
| Git & GitHub          | Version control                 |

---

## 📁 Project Structure

```text
SecureAI-HR-Assistant/
│
├── HRassistant/
│   │
│   ├── HRassistant/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── HRassistantApp/
│   │   │
│   │   ├── migrations/
│   │   │
│   │   ├── static/
│   │   │   └── css/
│   │   │
│   │   ├── templates/
│   │   │
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── document_ingestion.py
│   │   ├── document_processor.py
│   │   ├── gemini_rag.py
│   │   ├── models.py
│   │   ├── response_validator.py
│   │   ├── security_scanner.py
│   │   ├── semantic_search.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── hr_documents/
│   │
│   ├── manage.py
│   ├── requirements.txt
│   └── ...
│
├── .gitignore
└── README.md
```

> `hr_documents/` contains uploaded HR files and is excluded from Git using `.gitignore`.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/garbhanirakeshkumar/SecureAI-HR-Assistant.git
```

### 2. Open the project

```bash
cd SecureAI-HR-Assistant
```

### 3. Create a virtual environment

```bash
python -m venv myenv312
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\myenv312\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a `.env` file in the Django project directory.

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit `.env` to GitHub.

The project already excludes `.env` through `.gitignore`.

---

## 🗄️ Database Setup

Run:

```bash
python manage.py migrate
```

Create an administrator:

```bash
python manage.py createsuperuser
```

---

## ▶️ Run the Application

Start the Django development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 📄 HR Document Workflow

1. HR logs into SecureAI.
2. HR opens **HR Documents**.
3. HR uploads a supported document.
4. SecureAI extracts the document text.
5. The text is divided into chunks.
6. Sentence Transformers generates embeddings.
7. Embeddings are stored in the database.
8. Employees can ask questions through the chatbot.
9. SecureAI searches the uploaded HR documents.
10. Relevant information is provided to Gemini.
11. Gemini generates the answer.
12. The response is validated for sensitive information.
13. The final response is shown to the employee.

---

## 🛡️ Security Workflow

SecureAI is designed with multiple security layers:

```text
User Input
    ↓
Prompt Injection Detection
    ↓
PII Masking
    ↓
Secure RAG Retrieval
    ↓
Gemini Response
    ↓
Response Validation
    ↓
Security Audit Logging
    ↓
Final Answer
```

---

## 🧪 Testing

Before committing changes, run:

```bash
python manage.py check
```

Expected result:

```text
System check identified no issues (0 silenced).
```

You can also manually test:

* User login
* HR login
* Employee login
* HR document upload
* HR document deletion
* Document opening
* Semantic search
* HR chatbot
* Prompt injection detection
* PII masking
* Response validation
* Security audit logs
* High/Medium/Low risk events

---

## 🔒 Security Notes

* Never commit `.env`.
* Never expose the Gemini API key.
* Uploaded HR documents are excluded from Git.
* Production deployments should use proper authentication and authorization.
* Production deployments should use a production database and web server.
* Uploaded documents should be protected from unauthorized access.
* Security controls should be reviewed before deploying the application publicly.

---

## 🎯 Project Goals

SecureAI HR Assistant demonstrates how generative AI and RAG can be combined with practical security controls to build a safer enterprise HR assistant.

The project focuses on:

* Secure AI applications
* Retrieval-Augmented Generation
* Document intelligence
* Prompt injection detection
* PII protection
* AI response validation
* Security monitoring
* Role-based access control

---

## 👨‍💻 Author

**Garbhani Rakesh Kumar**

MCA Final Year Student
Aspiring Software Developer / AI Security Engineer

GitHub:
https://github.com/garbhanirakeshkumar

LinkedIn:
https://linkedin.com/in/rakesh-kumar-garbhani-636491314

---

## 📜 License

This project is intended for educational and demonstration purposes.
