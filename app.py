import streamlit as st
import hashlib
import time

from document_processor import extract_text_from_pdf, create_chunks
from rag_engine import create_embeddings, create_faiss_index, search_contract
from contract_auditor import audit_contract
from google import genai


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="ContractIQ | AI Contract Auditor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

    .main {
        padding-top: 1rem;
    }

    .hero {
        padding: 25px 10px 10px 10px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #7a7f87;
        margin-bottom: 25px;
    }

    .metric-card {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.18);
        background: rgba(128,128,128,0.05);
        text-align: center;
    }

    .metric-number {
        font-size: 30px;
        font-weight: 800;
    }

    .metric-label {
        color: #7a7f87;
        font-size: 14px;
    }

    .source-card {
        padding: 12px 16px;
        border-left: 4px solid #4f8cff;
        border-radius: 8px;
        background: rgba(79,140,255,0.08);
        margin-top: 10px;
    }

    .status-present {
        color: #16a34a;
        font-weight: 700;
    }

    .status-missing {
        color: #dc2626;
        font-weight: 700;
    }

    .status-unclear {
        color: #d97706;
        font-weight: 700;
    }

    .disclaimer {
        padding: 14px;
        border-radius: 12px;
        background: rgba(234,179,8,0.08);
        border: 1px solid rgba(234,179,8,0.25);
        font-size: 13px;
        color: #6b5b00;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# GEMINI CLIENT
# ---------------------------------------------------------

client = genai.Client()

MODEL_NAME = "gemini-3.6-flash"


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "documents" not in st.session_state:
    st.session_state.documents = {}

if "selected_document" not in st.session_state:
    st.session_state.selected_document = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "audit_results" not in st.session_state:
    st.session_state.audit_results = {}


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def get_file_hash(file_bytes):
    return hashlib.md5(file_bytes).hexdigest()


def get_status_class(status):
    status = status.lower()

    if "present" in status:
        return "status-present"

    if "missing" in status:
        return "status-missing"

    return "status-unclear"


def answer_question(question, document_data):
    """
    Generate an answer using retrieved contract sections.
    """

    results = search_contract(
        question,
        document_data["chunks"],
        document_data["index"],
        top_k=3
    )

    if not results:
        return (
            "Information not found in the provided contract.",
            []
        )

    # Ignore results that are too far from the question.
    relevant_results = [
        result for result in results
        if result["distance"] <= 0.8
    ]

    if not relevant_results:
        return (
            "Information not found in the provided contract.",
            []
        )

    context = "\n\n".join(
        f"Page {result['page']}:\n{result['text']}"
        for result in relevant_results
    )

    prompt = f"""
You are an AI contract information assistant.

Answer the user's question using ONLY the contract sections provided below.

Rules:
- Do not make up information.
- Do not use outside knowledge.
- If the answer is not present, say:
  "Information not found in the provided contract."
- Do not provide legal advice.
- Do not determine whether the contract is legally valid or enforceable.
- Keep the answer clear and concise.

Contract sections:

{context}

User question:
{question}

Give a direct answer.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text, relevant_results


def process_document(file):
    """
    Read PDF, create chunks, embeddings and FAISS index.
    """

    pdf_bytes = file.getvalue()

    pages = extract_text_from_pdf(pdf_bytes)

    if not pages:
        return None

    chunks = create_chunks(pages)

    if not chunks:
        return None

    embeddings = create_embeddings(chunks)

    index = create_faiss_index(embeddings)

    return {
        "name": file.name,
        "pages": pages,
        "chunks": chunks,
        "embeddings": embeddings,
        "index": index,
        "hash": get_file_hash(pdf_bytes)
    }


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## ⚖️ ContractIQ")

    st.caption("AI Contract Intelligence")

    st.divider()

    st.markdown("### 📚 Document Library")

    if st.session_state.documents:

        for doc_id, document in st.session_state.documents.items():

            is_selected = (
                st.session_state.selected_document == doc_id
            )

            if st.button(
                f"📄 {document['name']}",
                key=f"doc_{doc_id}",
                use_container_width=True
            ):
                st.session_state.selected_document = doc_id
                st.rerun()

    else:
        st.caption("No contracts uploaded yet.")

    st.divider()

    st.markdown("### 📌 Quick Guide")

    st.markdown("""
**1. Upload** your contract PDF

**2. Analyze** important clauses

**3. Ask AI** questions about your contract

**4. Review** the source section
    """)

    st.divider()

    st.markdown(
        '<div class="disclaimer">'
        '⚠️ <b>Important:</b> This application provides '
        'informational contract analysis only. It does not provide '
        'legal advice or determine legal enforceability.'
        '</div>',
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown("""
<div class="hero">

<div class="hero-title">
⚖️ ContractIQ
</div>

<div class="hero-subtitle">
AI-powered contract analysis, compliance auditing and intelligent Q&A.
</div>

</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# UPLOAD AREA
# ---------------------------------------------------------

uploaded_files = st.file_uploader(
    "📄 Upload contract PDF(s)",
    type=["pdf"],
    accept_multiple_files=True,
    help="You can upload one or multiple contract PDFs."
)


if uploaded_files:

    new_files = []

    for file in uploaded_files:

        file_bytes = file.getvalue()
        file_hash = get_file_hash(file_bytes)

        if file_hash not in st.session_state.documents:

            new_files.append(file)

    if new_files:

        progress = st.progress(0)

        status = st.empty()

        for i, file in enumerate(new_files):

            status.info(
                f"📖 Reading and analyzing {file.name}..."
            )

            try:

                document_data = process_document(file)

                if document_data:

                    doc_id = document_data["hash"]

                    st.session_state.documents[doc_id] = document_data

                    st.session_state.chat_history[doc_id] = []

                    progress.progress(
                        int(((i + 1) / len(new_files)) * 100)
                    )

                else:

                    st.error(
                        f"❌ Could not read readable text from {file.name}."
                    )

            except Exception as e:

                st.error(
                    f"⚠️ Could not process {file.name}. "
                    "Please try another PDF."
                )

        status.success("✅ Contract processing completed.")

        time.sleep(0.5)

        if st.session_state.selected_document is None:

            first_doc = next(
                iter(st.session_state.documents.keys())
            )

            st.session_state.selected_document = first_doc

        st.rerun()


# ---------------------------------------------------------
# EMPTY STATE
# ---------------------------------------------------------

if not st.session_state.documents:

    st.info(
        "👆 Upload one or more contract PDFs above to start analyzing them."
    )

    st.markdown("### What you can do")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        **🔎 Audit Contracts**

        Check important clauses such as payment,
        termination, IP and confidentiality.
        """)

    with col2:

        st.markdown("""
        **🤖 Ask AI**

        Ask natural-language questions and get
        answers grounded in your contract.
        """)

    with col3:

        st.markdown("""
        **📚 Multiple Documents**

        Upload multiple contracts and switch
        between them from the document library.
        """)

    st.stop()


# ---------------------------------------------------------
# SELECT DOCUMENT
# ---------------------------------------------------------

if st.session_state.selected_document not in st.session_state.documents:

    st.session_state.selected_document = next(
        iter(st.session_state.documents.keys())
    )


selected_id = st.session_state.selected_document

document = st.session_state.documents[selected_id]


# ---------------------------------------------------------
# DOCUMENT HEADER
# ---------------------------------------------------------

st.markdown("---")

col1, col2 = st.columns([4, 1])

with col1:

    st.markdown(
        f"## 📄 {document['name']}"
    )

    st.caption(
        f"{len(document['pages'])} pages • "
        f"{len(document['chunks'])} searchable sections"
    )

with col2:

    if st.button(
        "🗑️ Clear All",
        use_container_width=True
    ):

        st.session_state.documents = {}
        st.session_state.selected_document = None
        st.session_state.chat_history = {}
        st.session_state.audit_results = {}

        st.rerun()


# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Compliance Audit",
        "🤖 Ask AI",
        "📚 Documents"
    ]
)


# =========================================================
# TAB 1 — AUDIT
# =========================================================

with tab1:

    st.markdown("### Contract Compliance Overview")

    st.caption(
        "AI checks whether important contract categories are present, missing or unclear."
    )

    audit_key = selected_id

    if audit_key not in st.session_state.audit_results:

        if st.button(
            "🔍 Analyze Contract",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "AI is auditing your contract..."
            ):

                try:

                    full_text = "\n\n".join(
                        chunk["text"]
                        for chunk in document["chunks"]
                    )

                    result = audit_contract(full_text)

                    st.session_state.audit_results[audit_key] = result

                    st.rerun()

                except Exception:

                    st.error(
                        "⚠️ The AI service is temporarily unavailable. "
                        "Please try again later."
                    )

    else:

        audit_text = st.session_state.audit_results[audit_key]

        st.success("✅ Contract audit completed")

        st.markdown(audit_text)

        st.divider()

        st.caption(
            "Audit results are informational and should be reviewed by a qualified professional."
        )


# =========================================================
# TAB 2 — ASK AI
# =========================================================

with tab2:

    st.markdown("### 🤖 Ask AI")

    st.caption(
        "Ask questions about the uploaded contract. "
        "Answers are generated from the contract content."
    )

    history = st.session_state.chat_history[selected_id]

    # Display previous messages
    for message in history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message.get("sources"):

                for source in message["sources"]:

                    st.markdown(
                        f"""
                        <div class="source-card">
                        📄 <b>Source:</b> Page {source['page']}<br>
                        <small>{source['text'][:350]}...</small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    question = st.chat_input(
        "Ask anything about your contract..."
    )

    if question:

        history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("🔎 Finding the relevant contract section..."):

                try:

                    answer, sources = answer_question(
                        question,
                        document
                    )

                    st.markdown(answer)

                    if sources:

                        st.markdown("#### 📌 Evidence")

                        for source in sources:

                            st.markdown(
                                f"""
                                <div class="source-card">
                                📄 <b>Page {source['page']}</b><br>
                                {source['text'][:500]}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    history.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception:

                    error_message = (
                        "⚠️ I couldn't process that question right now. "
                        "Please try again."
                    )

                    st.error(error_message)

                    history.append({
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    })


# =========================================================
# TAB 3 — DOCUMENTS
# =========================================================

with tab3:

    st.markdown("### 📚 Your Contract Library")

    st.caption(
        f"{len(st.session_state.documents)} contract(s) available"
    )

    for doc_id, doc in st.session_state.documents.items():

        col1, col2, col3 = st.columns([5, 2, 1])

        with col1:

            st.markdown(
                f"**📄 {doc['name']}**"
            )

            st.caption(
                f"{len(doc['pages'])} pages • "
                f"{len(doc['chunks'])} sections"
            )

        with col2:

            if doc_id == selected_id:

                st.success("Currently selected")

            else:

                if st.button(
                    "Open",
                    key=f"open_{doc_id}"
                ):

                    st.session_state.selected_document = doc_id
                    st.rerun()

        with col3:

            if st.button(
                "✕",
                key=f"delete_{doc_id}"
            ):

                del st.session_state.documents[doc_id]

                st.session_state.chat_history.pop(
                    doc_id,
                    None
                )

                st.session_state.audit_results.pop(
                    doc_id,
                    None
                )

                if st.session_state.documents:

                    st.session_state.selected_document = next(
                        iter(st.session_state.documents.keys())
                    )

                else:

                    st.session_state.selected_document = None

                st.rerun()

        st.divider()