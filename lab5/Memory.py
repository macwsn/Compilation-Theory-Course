class Memory:
    def __init__(self, name):
        self.name = name
        self.memory = {}
    
    def has_key(self, name):
        return name in self.memory
    
    def get(self, name):
        return self.memory.get(name)
    
    def put(self, name, value):
        self.memory[name] = value


class MemoryStack:
    def __init__(self, memory=None):
        self.stack = []
        if memory is not None:
            self.stack.append(memory)
    
    def get(self, name):
        # Search from top to bottom
        for mem in reversed(self.stack):
            if mem.has_key(name):
                return mem.get(name)
        return None
    
    def insert(self, name, value):
        # Insert into current (top) scope
        if self.stack:
            self.stack[-1].put(name, value)
    
    def set(self, name, value):
        # Set in the scope where variable exists, or top scope
        for mem in reversed(self.stack):
            if mem.has_key(name):
                mem.put(name, value)
                return
        # If not found, insert in current scope
        self.insert(name, value)
    
    def push(self, memory):
        self.stack.append(memory)
    
    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None