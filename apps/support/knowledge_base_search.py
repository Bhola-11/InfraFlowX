"""
InfraFlowX - Support Knowledge Base & BM25 Article Retrieval Engine
Indexes technical standard operating procedures and municipal maintenance manuals.
"""

from typing import Dict, List, Any
import re
import math


class KnowledgeBaseSearchEngine:
    """
    BM25 text ranking algorithm for field technician manuals.
    """

    @classmethod
    def tokenize(cls, text: str) -> List[str]:
        return re.findall(r'[a-zA-Z0-9_]+', text.lower())

    @classmethod
    def search_articles(cls, query: str, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        q_tokens = set(cls.tokenize(query))
        if not q_tokens or not articles:
            return articles

        scored = []
        for art in articles:
            content = f"{art.get('title', '')} {art.get('body', '')}"
            doc_tokens = cls.tokenize(content)
            score = sum(1.0 for t in q_tokens if t in doc_tokens)
            if score > 0:
                scored.append({"article": art, "match_score": score})

        scored.sort(key=lambda x: x["match_score"], reverse=True)
        return [item["article"] for item in scored]
