from chatbot.models import ChatSession


def get_all_sessions():

    return ChatSession.objects.order_by(
        "-updated_at"
    )


def get_session(session_id):

    return ChatSession.objects.get(
        id=session_id
    )


def rename_session(
    session,
    title,
):

    session.title = title
    session.save()

    return session


def delete_session(session):

    session.delete()