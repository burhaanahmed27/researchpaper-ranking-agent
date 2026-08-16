from agent import expand_query, filter_papers, score_papers
from arxiv_client import search_arxiv, remove_duplicates
from ranking import rank_papers
from state import AgentState

question = input("Research question: ")
state = AgentState(question)

# Decision 1 - expand the user's question
state.expanded_queries = expand_query(state.research_question)

print("\n--- QUERY EXPANSION ---")

for query in state.expanded_queries:
    print(f"- {query}")

# Retrieve papers for every expanded query
for query in state.expanded_queries:
    print(f"\nSearching arXiv for: {query}")

    papers = search_arxiv(query, max_results=5) # maximum 5 results for each of the 3 queries
    state.retrieved_papers.extend(papers)

print(f"\nRetrieved {len(state.retrieved_papers)} papers.")

# Removing duplicates from the 15 results
state.unique_papers = remove_duplicates(state.retrieved_papers)

print(
    f"After deduplication: "
    f"{len(state.unique_papers)} unique papers."
)

# Decision 2 - Relevance Filtering
print("\n--- RELEVANCE FILTERING ---")

state.filter_decisions = filter_papers(
    state.research_question,
    state.unique_papers
)

for decision in state.filter_decisions:
    paper = state.unique_papers[decision["id"]]

    if decision["relevant"]:
        state.relevant_papers.append(paper)
        symbol = "KEEP"
    else:
        symbol = "REMOVE"

    print(f"\n[{symbol}] {paper['title']}")
    print(f"Reason: {decision['reason']}")

print(
    f"\n{len(state.relevant_papers)} of "
    f"{len(state.unique_papers)} unique papers passed relevance filtering."
)

# Decision 3 - Final Ranking
print("\n--- FINAL RANKING ---")

state.ranking_assessments = score_papers(
    state.research_question,
    state.relevant_papers
)

state.ranked_papers = rank_papers(
    state.relevant_papers,
    state.ranking_assessments
)

for position, result in enumerate(state.ranked_papers[:5], start=1):
    paper = result["paper"]

    print(f"\n#{position} {paper['title']}")
    print(f"Final score: {result['final_score']}/10")

    print(
        f"Signals: "
        f"abstract={result['abstract_relevance']}/10, "
        f"title={result['title_relevance']}/10, "
        f"recency={result['recency']}/10, "
        f"coherence={result['coherence']}/10"
    )

    print(f"Reason: {result['reason']}")
    print(f"URL: {paper['url']}")