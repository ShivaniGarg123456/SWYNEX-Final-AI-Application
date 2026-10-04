from google import genai


client = genai.Client()

MODEL_NAME = "gemini-3.6-flash"


CLAUSES = [
    "Payment",
    "Termination",
    "Intellectual Property",
    "Confidentiality",
    "Liability",
    "Deliverables",
    "Deadlines",
    "Revision Terms",
    "Dispute Resolution",
    "Non-Compete / Non-Solicitation"
]


def audit_contract(contract_text):
    """Analyze a contract against important compliance categories."""

    clause_list = "\n".join(
        f"- {clause}" for clause in CLAUSES
    )

    prompt = f"""
You are an AI contract compliance assistant.

Analyze the contract below against these important categories:

{clause_list}

For each category, provide:

1. Status: Present, Missing, or Unclear
2. A short explanation based ONLY on the contract text.

Important rules:
- Do not invent information.
- Do not provide legal advice.
- Do not determine whether the contract is legally valid or enforceable.
- If the information is insufficient, use "Unclear".
- Keep explanations concise.

Return the result in this format:

Payment:
Status: Present/Missing/Unclear
Explanation: ...

Termination:
Status: Present/Missing/Unclear
Explanation: ...

Contract:
{contract_text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text