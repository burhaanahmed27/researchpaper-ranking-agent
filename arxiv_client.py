import arxiv

def remove_duplicates(papers): # papers is a list of dictionaries
    unique_papers = {}

    for paper in papers:
        unique_papers[paper["url"]] = paper

    return list(unique_papers.values())

# function that takes a search query and retrieves papers from arXiv
def search_arxiv(query, max_results=10):
    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

    # looping through every paper returned by the search
    for result in client.results(search):
        paper = {
            "title": result.title,
            "abstract": result.summary,
            "authors": [author.name for author in result.authors],
            "published": result.published,
            "url": result.entry_id
        }

        papers.append(paper)

    return papers