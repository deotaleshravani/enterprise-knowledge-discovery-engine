import logging

logger = logging.getLogger(__name__)


HIGH_CONFIDENCE_PROMPT = """
You are Enterprise Knowledge Assistant.

Use ONLY the supplied company context.

Provide a concise answer.

Include document IDs whenever possible.

Never invent information.
"""


MEDIUM_CONFIDENCE_PROMPT = """
You are Enterprise Knowledge Assistant.

The retrieved context may be incomplete.

Answer ONLY if the information clearly exists.

If anything is uncertain,

state that additional documents may be required.

Never guess.
"""


LOW_CONFIDENCE_PROMPT = """
You are Enterprise Knowledge Assistant.

The retrieved context has very low confidence.

Do NOT answer using your own knowledge.

Instead explain that the company knowledge base
does not contain enough information.

Never invent facts.

Never fabricate citations.
"""


def create_prompt(
    question,
    context,
    confidence,
):
    """
    Builds the final prompt.

    Different confidence levels
    receive different instructions.
    """

    logger.info(
        "Creating prompt (confidence=%d).",
        confidence
    )

    if confidence >= 80:

        system_prompt = HIGH_CONFIDENCE_PROMPT

    elif confidence >= 50:

        system_prompt = MEDIUM_CONFIDENCE_PROMPT

    else:

        system_prompt = LOW_CONFIDENCE_PROMPT

    prompt = f"""
{system_prompt}

=========================
CONTEXT
=========================

{context}

=========================
QUESTION
=========================

{question}

=========================
ANSWER
=========================

"""

    return prompt