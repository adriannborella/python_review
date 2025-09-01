class MinStack:
    """
    Stack que mantiene track del mínimo en O(1).
    Técnica: Stack auxiliar para mínimos.
    """

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)

        # Mantener el mínimo actual o el nuevo valor si es menor
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self):
        if not self.stack:
            return None

        val = self.stack.pop()

        # Si removemos el mínimo actual, también lo sacamos del min_stack
        if val == self.min_stack[-1]:
            self.min_stack.pop()

        return val

    def top(self):
        return self.stack[-1] if self.stack else None

    def get_min(self):
        return self.min_stack[-1] if self.min_stack else None


# Test
min_stack = MinStack()
min_stack.push(-2)
min_stack.push(0)
min_stack.push(-3)
print(f"Min: {min_stack.get_min()}")  # -3
min_stack.pop()
print(f"Top: {min_stack.top()}")  # 0
print(f"Min: {min_stack.get_min()}")  # -2
