# ⚖️ ContractIQ — AI Contract Compliance Auditor


ContractIQ is an AI-powered contract analysis application designed to help freelancers, independent contractors, consultants, and small businesses quickly review important terms in their contracts.

The application combines **Retrieval-Augmented Generation (RAG)**, **Gemini AI**, **FAISS similarity search**, and **Streamlit** to provide contract auditing and grounded question-answering with relevant contract evidence.

---

## 📌 Problem

Reviewing a contract manually can be time-consuming, especially when important clauses are spread across multiple pages.

Users may want to quickly identify:

* Payment terms
* Termination conditions
* Intellectual property ownership
* Confidentiality clauses
* Liability terms
* Deliverables
* Deadlines
* Revision terms
* Dispute resolution
* Non-compete / non-solicitation clauses

ContractIQ provides an AI-assisted way to review these areas and ask questions directly about uploaded contracts.

---

## 💡 Solution

ContractIQ allows users to upload one or more PDF contracts and interact with them through two main capabilities:

### 1. Contract Compliance Audit

The application analyzes the contract against important compliance categories and reports:

* **Present**
* **Missing**
* **Unclear**

Each result includes a short explanation based on the contract content.

### 2. Contract-Based AI Q&A

Users can ask questions such as:

* "What is the payment deadline?"
* "How much notice is required for termination?"
* "Who owns the final deliverables?"
* "What are the confidentiality requirements?"

The system retrieves the most relevant contract sections before generating an answer.

Relevant contract pages and evidence are displayed with the answer to improve transparency and reduce unsupported responses.

---

## 🚀 Key Features

* 📄 Upload PDF contracts
* 📚 Support for multiple contract documents
* 🔍 Contract clause compliance audit
* 🤖 AI-powered contract Q&A
* 🧠 Retrieval-Augmented Generation (RAG)
* 🔎 Semantic similarity search using FAISS
* 📑 Page-level source evidence
* ⚠️ Error handling for invalid or unreadable documents
* 💬 Chat-style question answering
* 📊 Contract overview and audit results
* 🔐 API key kept outside the source code
* ⚖️ Legal and ethical disclaimer

---

## 🧠 How It Works

```text
                PDF Contract
                     │
                     ▼
              PyMuPDF Extraction
                     │
                     ▼
                Text Chunks
                     │
                     ▼
           Gemini Embedding Model
                     │
                     ▼
                 FAISS Index
                     │
              ┌──────┴──────┐
              │             │
          User Question   Contract Audit
              │             │
              ▼             ▼
       Similarity Search   Gemini AI
              │
              ▼
       Relevant Contract Sections
              │
              ▼
        Gemini 3.6 Flash
              │
              ▼
       Answer + Evidence
```

---

## 🛠️ Tech Stack

| Technology         | Purpose                      |
| ------------------ | ---------------------------- |
| Python             | Application development      |
| Streamlit          | Web interface                |
| Google Gemini API  | AI generation and embeddings |
| Gemini 3.6 Flash   | Contract analysis and Q&A    |
| Gemini Embedding 2 | Text embeddings              |
| FAISS              | Similarity search            |
| PyMuPDF            | PDF text extraction          |
| NumPy              | Numerical processing         |

---

## 🔍 Contract Audit Categories

ContractIQ checks the following categories:

1. Payment
2. Termination
3. Intellectual Property
4. Confidentiality
5. Liability
6. Deliverables
7. Deadlines
8. Revision Terms
9. Dispute Resolution
10. Non-Compete / Non-Solicitation

Each category is classified as:

```text
Present
Missing
Unclear
```

The explanation is generated using the available contract content.

---

## 💬 Example Questions

### Payment

**Question:**

> What is the payment deadline?

**Example answer:**

> Payment will be made within 15 days after submission of the final deliverables.

**Evidence:**

The application displays the relevant contract section and page.

---

### Ownership

**Question:**

> Who owns the final project after completion?

The application retrieves the relevant intellectual-property section and provides an answer based on the contract rather than generating an unsupported response.

---

## 📑 Evidence-Based Answers

ContractIQ is designed to ground answers in the uploaded contract.

For each question:

1. The question is converted into an embedding.
2. FAISS searches for semantically relevant contract sections.
3. The most relevant sections are provided to Gemini.
4. Gemini generates an answer using those sections.
5. Relevant contract evidence and page numbers are shown to the user.

This approach helps reduce hallucination and makes the answer easier to verify.

---

## ⚠️ Error Handling

The application handles common failure cases, including:

* No contract uploaded
* Empty or unreadable PDF
* Unsupported document content
* Question unrelated to the uploaded contract
* API failures
* Missing or unavailable contract information

If relevant information cannot be found, the system is designed to avoid inventing an answer.

---

## 📊 Evaluation

The RAG functionality was tested using a small evaluation set containing contract-related questions.

Example evaluation questions included:

| Question                        | Expected Information            |
| ------------------------------- | ------------------------------- |
| What is the payment amount?     | Contract payment amount         |
| What is the payment deadline?   | Payment timeline                |
| What is the termination notice? | Required notice period          |
| Who owns the final work?        | Intellectual property ownership |
| Is liability clearly limited?   | Liability information           |

### Sample Evaluation Result

```text
Total Tests     : 4
Passed          : 4
Failed/Review   : 0
Pass Rate       : 100.00%
```

> **Note:** This represents the result on the sample evaluation set only. It should not be interpreted as a general model accuracy or real-world performance guarantee.

---

## 📂 Project Structure

```text
SWYNEX-Final-AI-Application/
│
├── app.py
├── document_processor.py
├── rag_engine.py
├── contract_auditor.py
├── requirements.txt
├── .gitignore
│
└── sample_contracts/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/ShivaniGarg123456/SWYNEX-Final-AI-Application.git
cd SWYNEX-Final-AI-Application
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Gemini API Key

Create an environment variable:

```text
GEMINI_API_KEY=your_api_key
```

**Never commit the API key to GitHub.**

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application will open in the browser.

---

## 🔐 Security

The Gemini API key is not included in the source code.

The project uses the `GEMINI_API_KEY` environment variable for API authentication.

The `.gitignore` file also prevents sensitive local files from being accidentally committed.

For cloud deployment, the API key should be stored using the deployment platform's secrets management system.

---

## ⚖️ Limitations

ContractIQ is an AI-assisted information and document analysis tool.

It has several limitations:

* AI-generated answers may contain errors.
* Contract wording can be ambiguous.
* Results may depend on PDF text extraction quality.
* Different jurisdictions may have different legal requirements.
* The system does not determine whether a contract is legally valid or enforceable.
* The system does not replace a qualified lawyer or legal professional.
* Evaluation results are based on a limited sample set.

---

## ⚖️ Ethical & Legal Disclaimer

ContractIQ is intended for **informational and educational purposes only**.

It does **not provide legal advice** and should not be used as a substitute for professional legal review.

Users should verify important contract decisions with a qualified legal professional.

Users should also avoid uploading confidential or sensitive contracts unless they understand and accept the privacy implications of using an AI-powered application.

---

## 🎯 Project Goal

The goal of ContractIQ is to demonstrate how modern AI techniques can be combined with document processing and retrieval systems to build a practical, beginner-friendly AI application for contract analysis.

The project demonstrates:

* AI API integration
* Prompt-based analysis
* Embeddings
* Vector similarity search
* Retrieval-Augmented Generation
* Document processing
* AI evaluation
* Error handling
* User interface development
* Responsible AI considerations

---

Project: **ContractIQ — AI Contract Compliance Auditor**

Developed as a final AI application demonstrating the integration of AI, RAG, document processing, and an interactive web interface.

---

## 📌 Repository

**GitHub:**
https://github.com/ShivaniGarg123456/SWYNEX-Final-AI-Application
