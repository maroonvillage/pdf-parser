from typing import Any, List, Optional

class Stack:
    """
    Represents a stack data structure.

    Attributes:
        _items (List[Any]): The underlying list to store stack elements.
    """

    def __init__(self):
        """Initializes an empty stack."""
        self._items: List[Any] = []

    def is_empty(self) -> bool:
        """Checks if the stack is empty."""
        return not self._items

    def push(self, item: Any) -> None:
        """Adds an item to the top of the stack."""
        self._items.append(item)

    def pop(self) -> Optional[Any]:
        """
        Removes and returns the item at the top of the stack.

        Returns:
           Optional[Any]: The element that was popped or None if the stack is empty.
        """
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self) -> Optional[Any]:
        """
        Returns the item at the top of the stack without removing it.

        Returns:
            Optional[Any]: The element at the top of the stack or None if the stack is empty.
        """
        if self.is_empty():
            return None
        return self._items[-1]

    def size(self) -> int:
        """Returns the number of items in the stack."""
        return len(self._items)

    def to_list(self) -> List[Any]:
       """
         Returns:
           List[Any]: The list of all of the items in the stack.
       """
       return self._items