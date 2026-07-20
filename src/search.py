from ddgs import DDGS


def get_live_news_context(sport_name):
    """
    Search the web for recent sports information.
    Returns useful snippets for RAG generation.
    """

    query = (
        f"{sport_name} latest tournament results "
        "winner matches news 2026"
    )

    results_text = []

    try:
        with DDGS() as ddgs:
            results = ddgs.text(
                query,
                max_results=5
            )

            for index, result in enumerate(results, start=1):
                title = result.get("title", "")
                body = result.get("body", "")

                results_text.append(
                    f"Source {index}: {title}\n{body}"
                )

    except Exception as e:
        print("Web search error:", e)
        return ""

    return "\n\n".join(results_text)