class AgentMemory:
    def __init__(self):
        self.data = {
            "age": None,
            "income": None,
            "state": None,
            "category": None,
            "gender": None,
            "occupation": None
        }

        # Track contradictions if user changes answers
        self.contradictions = []

    def set(self, key, value):
        """
        Set value without conflict checking (used after confirmation)
        """
        self.data[key] = value

    def update(self, key, value):
        """
        Update value with contradiction tracking
        """
        if value is None:
            return

        if self.data.get(key) is not None and self.data[key] != value:
            self.contradictions.append(
                f"{key}: {self.data[key]} -> {value}"
            )

        self.data[key] = value

    def update_bulk(self, extracted: dict):
        """
        Update multiple fields at once (future LLM use)
        """
        for k, v in extracted.items():
            self.update(k, v)
