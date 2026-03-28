from typing import List


class PromptBuilder:
    def __init__(self):
        self.system_instruction = (
            "You are a helpful assistant. Answer ONLY based on the provided context. "
            "If the answer is not in the context, say 'I don't know.' "
            "Do not make up information."
        )

    def build(self, query: str, context_docs: List[str]) -> str:
        """
        Build structured prompt for RAG.

        Args:
            query (str): User query
            context_docs (List[str]): Retrieved documents

        Returns:
            str: Final prompt
        """
        context = "\n\n".join(context_docs)

        prompt = f"""
Context:
{context}

Question:
{query}

Instructions:
- Answer only using the context above
- Be concise and accurate
- If not found, say "I don't know"
"""
        return prompt.strip()