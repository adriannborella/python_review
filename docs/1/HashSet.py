class HashSet:
    def __init__(self, capacity=16, load_factor=0.75):
        self.capacity = capacity  # Number of buckets
        self.load_factor = load_factor  # Resize threshold
        self.size = 0  # Number of elements
        self.buckets = [[] for _ in range(capacity)]  # [[],[],[]]

    def _hash(self, key):
        """Compute bucket index for a key."""
        return hash(key) % self.capacity  # hash("apple") % 16

    def _resize(self):
        """Double the capacity and rehash all elements when load factor exceeded."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_buckets:
            for key in bucket:
                self.add(key)

    def add(self, key):
        """Insert key into HashSet if not already present."""
        index = self._hash(key)
        bucket = self.buckets[index]
        if key not in bucket:
            bucket.append(key)
            self.size += 1
            if self.size / self.capacity > self.load_factor:
                self._resize()

    def remove(self, key):
        """Remove key if present."""
        index = self._hash(key)
        bucket = self.buckets[index]
        if key in bucket:
            bucket.remove(key)
            self.size -= 1

    def contains(self, key):
        """Check if key exists in HashSet."""
        index = self._hash(key)
        return key in self.buckets[index]

    def __len__(self):
        return self.size

    def __iter__(self):
        """Iterator for all elements in HashSet."""
        for bucket in self.buckets:
            for key in bucket:
                yield key

    def __str__(self):
        """String representation for debugging."""
        elements = [str(key) for key in self]
        return "{" + ", ".join(elements) + "}"


# Create a new HashSet
hs = HashSet()

# Add elements
hs.add("apple")
hs.add("banana")
hs.add("cherry")

print(hs)  # {apple, banana, cherry}
print("apple" in hs)  # True (uses __iter__)

# Remove an element
hs.remove("banana")
print(hs.contains("banana"))  # False

# Add more elements to trigger resizing
for i in range(20):
    hs.add(i)

print(len(hs))  # Size of the set
print(hs)  # Shows all elements
