import logging

import requests

logger = logging.getLogger(__name__)


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llama3:8b"




def ask_llm(prompt):
    logger.info(
        "Prompt length: %d characters",
        len(prompt)
    )

    print("=" * 80)
    print("PROMPT LENGTH:", len(prompt))
    print("=" * 80)

    logger.info(
        "Sending prompt to Ollama."
    )    
    """
    Sends a prompt to Ollama and returns
    the generated response.

    Workflow
    --------
    Prompt
        ↓
    HTTP POST
        ↓
    Ollama
        ↓
    Llama 3
        ↓
    Generated Answer
    """

    logger.info(
        "Sending prompt to Ollama."
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        answer = response.json()["response"]

        logger.info(
            "Received response from Ollama."
        )

        return answer.strip()

    except requests.exceptions.RequestException as error:

        logger.exception(
            "Failed to communicate with Ollama."
        )

        raise RuntimeError(
            "Could not connect to Ollama."
        ) from error