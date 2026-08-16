class AgentState:
    def __init__(self, research_question):
        self.research_question = research_question

        # DECISION 1 - QUERY EXPANSION
        # Alternative search queries generated from the original research question
        self.expanded_queries = []

        # RETRIEVAL
        # Papers returned from arXiv, then deduplicated
        self.retrieved_papers = []
        self.unique_papers = []

        # DECISION 2 - RELEVANCE FILTERING
        # LLM KEEP/REMOVE decisions and the papers that survive the filter
        self.filter_decisions = []  # either REMOVE or KEEP
        self.relevant_papers = []

        # DECISION 3 -  SIGNAL ASSESSMENT / RANKING
        # Individual assessment scores used to calculate the final ranking
        self.ranking_assessments = [] # the gemini scores produced in score_papers()
        self.ranked_papers = []  # papers ordered by their final weighted score