from datetime import datetime, timezone

def calculate_recency_score(published):
    current_year = datetime.now(timezone.utc).year
    age = current_year - published.year

    if age <= 1:
        return 10
    elif age <= 2:
        return 8
    elif age <= 4:
        return 6
    elif age <= 6:
        return 4
    else:
        return 2


def rank_papers(papers, assessments):
    ranked = []

    for assessment in assessments:
        paper = papers[assessment["id"]]

        recency = calculate_recency_score(paper["published"])

        final_score = (
            0.50 * assessment["abstract_relevance"]
            + 0.25 * assessment["title_relevance"]
            + 0.15 * recency
            + 0.10 * assessment["coherence"]
        )

        # copying signals into ranked so we can output
        ranked.append({
            "paper": paper,
            "final_score": round(final_score, 2),
            "abstract_relevance": assessment["abstract_relevance"],
            "title_relevance": assessment["title_relevance"],
            "recency": recency,
            "coherence": assessment["coherence"],
            "reason": assessment["reason"]
        })

    return sorted(
        ranked,
        key=lambda item: item["final_score"],
        reverse=True
    )