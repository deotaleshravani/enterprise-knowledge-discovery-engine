from search.context.context_builder import build_context

from chatbot.prompts.prompt_template import create_prompt

from chatbot.llm.ollama_client import ask_llm


def ask_ekde(query, history=""):
    """
    Enterprise Knowledge Discovery Engine (EKDE)
    Retrieval-Augmented Generation Pipeline.

    Workflow:
        1. Retrieve relevant document chunks.
        2. Build context.
        3. Create LLM prompt.
        4. Generate answer.
        5. Return answer with citations and confidence.
    """

    # -----------------------------------------
    # Step 1 : Retrieve relevant context
    # -----------------------------------------
    data = build_context(query)

    context = data["context"]
    print("=" * 80)
    print("CONTEXT LENGTH:", len(context))
    print("=" * 80)
    citations = data["citations"]
    confidence = data["confidence"]

    # -----------------------------------------
    # Step 2 : Create prompt
    # -----------------------------------------

    prompt = create_prompt(
        query=query,
        context=context,
        history=history
    )
    print("=" * 80)
    print("PROMPT LENGTH:", len(prompt))
    print("=" * 80)

    # -----------------------------------------
    # Step 3 : Generate answer
    # -----------------------------------------

    answer = ask_llm(prompt)

    # -----------------------------------------
    # Step 4 : Return response
    # -----------------------------------------

    return {
        "answer": answer,
        "citations": citations,
        "confidence": confidence,
        "context": context,
    }