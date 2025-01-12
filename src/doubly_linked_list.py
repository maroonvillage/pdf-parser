class Node:
    """Represents a node in the doubly-linked list."""
    def __init__(self, data):
        self.data = data  # Data stored in the node
        self.next = None  # Pointer to the next node
        self.prev = None  # Pointer to the previous node

class DoublyLinkedList:
    """Represents a doubly-linked list."""
    def __init__(self):
        self.head = None  # Head of the list
        self.tail = None  # Tail of the list

    def is_empty(self):
        """Check if the list is empty."""
        return self.head is None

    def append(self, data):
        """Append a new node with the given data to the end of the list."""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def prepend(self, data):
        """Insert a new node with the given data at the beginning of the list."""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def insert_after(self, target_data, data):
        """
        Insert a new node with the given data after the node containing `target_data`.
        """
        if self.is_empty():
            raise ValueError("List is empty")

        current = self.head
        while current:
            if current.data == target_data:
                new_node = Node(data)
                new_node.next = current.next
                new_node.prev = current
                if current.next:
                    current.next.prev = new_node
                else:
                    self.tail = new_node  # Update tail if inserting at the end
                current.next = new_node
                return
            current = current.next
        raise ValueError(f"Target data {target_data} not found in the list")

    def insert_before(self, target_data, data):
        """
        Insert a new node with the given data before the node containing `target_data`.
        """
        if self.is_empty():
            raise ValueError("List is empty")

        current = self.head
        while current:
            if current.data == target_data:
                new_node = Node(data)
                new_node.next = current
                new_node.prev = current.prev
                if current.prev:
                    current.prev.next = new_node
                else:
                    self.head = new_node  # Update head if inserting at the beginning
                current.prev = new_node
                return
            current = current.next
        raise ValueError(f"Target data {target_data} not found in the list")
    
    def search(self, data):
        """
        Search for a node with the given data.
        Returns True if the data is found, otherwise False.
        """
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def get_last_node(self):
        """Get the last node in the list."""
        current = self.head
        while current and current.next:
            current = current.next
        return current
    
    def print_list(self):
        """Print all elements in the list."""
        current = self.head
        while current:
            print(current.data, end=" <-> ")
            current = current.next
        print("None")

# Example usage
if __name__ == "__main__":
    # Create a new doubly-linked list
    dll = DoublyLinkedList()

    # Append elements
    dll.append(10)
    dll.append(20)
    dll.append(30)

    # Prepend an element
    dll.prepend(5)

    # Print the list
    print("Doubly Linked List:")
    dll.print_list()  # Output: 5 <-> 10 <-> 20 <-> 30 <-> None

    # Insert after a specific node
    dll.insert_after(10, 15)
    print("After inserting 15 after 10:")
    dll.print_list()  # Output: 5 <-> 10 <-> 15 <-> 20 <-> 30 <-> None

    # Insert before a specific node
    dll.insert_before(20, 18)
    print("After inserting 18 before 20:")
    dll.print_list()  # Output: 5 <-> 10 <-> 15 <-> 18 <-> 20 <-> 30 <-> None