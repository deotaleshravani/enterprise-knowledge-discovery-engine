from chatbot.models import (
    ChatSession,
    ChatMessage
)


def create_session(title="New Chat"):

    session = ChatSession.objects.create(
        title=title
    )

    return session


def add_message(
        session,
        role,
        content
):

    ChatMessage.objects.create(
        session=session,
        role=role,
        content=content
    )


def get_history(
        session,
        max_messages=10
):

    messages = session.messages.order_by(
        "created_at"
    )[:max_messages]

    history = ""

    for msg in messages:

        history += (
            f"{msg.role.capitalize()}: "
            f"{msg.content}\n"
        )

    return history