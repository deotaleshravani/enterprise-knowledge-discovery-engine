import networkx as nx

from documents.models import Document

graph = nx.Graph()


def add_node(name, node_type):

    if not name:
        return

    if not graph.has_node(name):

        graph.add_node(
            name,
            type=node_type,
        )


def add_relation(source, relation, target):

    if not source or not target:
        return

    add_node(source, "entity")
    add_node(target, "entity")

    graph.add_edge(
        source,
        target,
        relation=relation,
    )


def build_graph():

    graph.clear()

    documents = Document.objects.all()

    for document in documents:

        metadata = document.metadata

        # ----------------------------------
        # Jira
        # ----------------------------------

        if document.source == "jira":

            title = metadata.get("title")
            creator = metadata.get("created_by")
            project = metadata.get("project")
            team = metadata.get("team")
            technology = metadata.get("technology")
            category = metadata.get("category")

            add_relation(
                creator,
                "CREATED",
                title,
            )

            add_relation(
                title,
                "BELONGS_TO_PROJECT",
                project,
            )

            add_relation(
                title,
                "ASSIGNED_TO_TEAM",
                team,
            )

            add_relation(
                title,
                "USES_TECHNOLOGY",
                technology,
            )

            add_relation(
                title,
                "CATEGORY",
                category,
            )

        # ----------------------------------
        # Slack
        # ----------------------------------

        elif document.source == "slack":

            user = metadata.get("user")
            team = metadata.get("team")
            project = metadata.get("project")
            technology = metadata.get("technology")
            channel = metadata.get("channel")
            message = metadata.get("message")
            ticket = metadata.get("related_ticket")

            add_relation(
                user,
                "POSTED",
                message,
            )

            add_relation(
                message,
                "IN_CHANNEL",
                channel,
            )

            add_relation(
                message,
                "BELONGS_TO_PROJECT",
                project,
            )

            add_relation(
                message,
                "TEAM",
                team,
            )

            add_relation(
                message,
                "USES_TECHNOLOGY",
                technology,
            )

            add_relation(
                message,
                "RELATED_TO",
                ticket,
            )

        # ----------------------------------
        # Meeting
        # ----------------------------------

        elif document.source == "meeting":

            topic = metadata.get("topic")
            project = metadata.get("project")
            team = metadata.get("team")
            technology = metadata.get("technology")
            attendees = metadata.get(
                "attendees",
                [],
            )
            ticket = metadata.get(
                "related_ticket"
            )

            add_relation(
                topic,
                "BELONGS_TO_PROJECT",
                project,
            )

            add_relation(
                topic,
                "TEAM",
                team,
            )

            add_relation(
                topic,
                "USES_TECHNOLOGY",
                technology,
            )

            add_relation(
                topic,
                "RELATED_TO",
                ticket,
            )

            for attendee in attendees:

                add_relation(
                    attendee,
                    "ATTENDED",
                    topic,
                )

        # ----------------------------------
        # PDF
        # ----------------------------------

        elif document.source == "pdf":

            pdf_id = metadata.get("id")
            folder = metadata.get("source_folder")

            add_relation(
                pdf_id,
                "CATEGORY",
                folder,
            )

    return graph