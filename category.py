class Category:
    def __init__(self, name, category_type, is_default=False):
        self.name = name
        self.category_type = category_type
        self.is_default = is_default

    def __repr__(self):
        return (
            f"{self.name} "
            f"({self.category_type}) "
            f"- Default: {self.is_default}"
        )