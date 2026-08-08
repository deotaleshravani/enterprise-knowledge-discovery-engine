class ConversationMemory:
    """
    Stores conversation history for a chat session.

    The memory is intentionally lightweight.
    It does not perform retrieval or reasoning—
    it only stores and exposes conversation history.
    """

    def __init__(self, max_history=5):

        self.max_history = max_history
        self.messages = []

    # -----------------------------------
    # Add Messages
    # -----------------------------------

    def add_user_message(self, message):

        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )

        self._trim_history()

    def add_assistant_message(self, message):

        self.messages.append(
            {
                "role": "assistant",
                "content": message
            }
        )

        self._trim_history()

    # -----------------------------------
    # Context
    # -----------------------------------

    def get_context(self):

        history = ""

        for msg in self.messages:

            history += (
                f"{msg['role'].capitalize()}: "
                f"{msg['content']}\n"
            )

        return history.strip()

    # -----------------------------------
    # Helper Methods
    # -----------------------------------

    def get_last_user_message(self):

        for msg in reversed(self.messages):

            if msg["role"] == "user":
                return msg["content"]

        return ""

    def get_last_assistant_message(self):

        for msg in reversed(self.messages):

            if msg["role"] == "assistant":
                return msg["content"]

        return ""

    def get_recent_messages(self, count=4):

        return self.messages[-count:]

    def has_history(self):

        return len(self.messages) > 0

    def clear(self):

        self.messages = []

    # -----------------------------------
    # Internal
    # -----------------------------------

    def _trim_history(self):

        max_messages = self.max_history * 2

        if len(self.messages) > max_messages:

            self.messages = self.messages[-max_messages:]