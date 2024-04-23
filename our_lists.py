from typing import Generic, Optional, Iterator, TypeVar, Protocol

from our_array import Array

T = TypeVar("T")


class ListOutOfBoundsError(Exception):
    """List out of bounds error."""
    pass


class Link(Generic[T]):
    """Store a single element in a link "chain"."""

    def __init__(self, element: Optional[T] = None):
        self.element: Optional[T] = element
        self.next: Optional[Link[T]] = None


class List(Protocol[T]):
    """List API."""

    def append(self, element: T):
        """
        Appends (adds) an element to the end of the list.
        :param element: The new element.
        """
        pass

    def insert(self, position: int, element: T):
        """
        Inserts the element before the position in this list.
        :param position: The position to add the element, between 0 and list size (inclusive).
        :param element: The new element.
        """
        pass

    def remove(self, position: int) -> T:
        """
        Removes the element at the specified position in this list.
        :param position: The position to add the element, between 0 and list size (exclusive).
        :return: The removed element
        """
        pass

    def __getitem__(self, position: int) -> T:
        """
        Retrieve the element at the specified position in this list.
        :param position: The position to get the element, between 0 and list size (exclusive).
        :return: The element at position.
        """
        pass

    def __setitem__(self, position: int, element: T):
        """
        Replaces the element at the specified position in this list.
        :param position: The position to set the element, between 0 and list size (exclusive).
        :param element: The new element
        """
        pass

    def clear(self):
        """
        Removes all the elements from this list.
        """
        pass


class LinkedList(Generic[T]):
    """Link "chain" implementation of List API."""

    def __init__(self):
        self._head: Optional[Link[T]] = None
        self._last: Optional[Link[T]] = None

    def append(self, element: T):
        # Note: append work just like enqueue in LinkQueue
        if self._head is None:
            self._head = Link(element)
            self._last = self._head
        else:
            self._last.next = Link(element)
            self._last = self._last.next
        self._size += 1

    def _validate_pos(self, position: int):
        """Raise an error if the position is out of bounds"""
        if position < 0 or position >= self._size:
            raise ListOutOfBoundsError()

    def insert(self, position: int, element: T):
        
        # inserting beyond last is just appending
        if position == self._size:
            self.append(element)
            return

        self._validate_pos(position)

        # Note: inserting at position 0 is the same as push in the LinkStack
        if position == 0:
            tmp: Link[T] = Link(element)
            tmp.next = self._head
            self._head = tmp

        # TODO

        self._size += 1

    def remove(self, position: int) -> T:
        self._validate_pos(position)

        tmp: T

        # Note: removing at position is the same as pop in the LinkStack
        if position == 0:
            tmp = self._head.element
            self._head = self._head.next

        # TODO

        self._size -= 1
        return tmp

    def clear(self):
        # TODO
        self._size = 0

    def __getitem__(self, position: int) -> T:
        self._validate_pos(position)
        # TODO

    def __setitem__(self, position: int, element: int):
        self._validate_pos(position)
        # TODO

    def __iter__(self) -> Iterator[T]:
        # TODO
        return self

    def __next__(self) -> T:
        # TODO
        pass


class ArrayList(Generic[T]):
    """Array implementation of List API."""

    def __init__(self, initial_capacity: int = 20):
        self._elements: Array[T] = Array(initial_capacity)
        self._size: int = 0
        self._cursor: int = 0

    def _check_available_space(self):
        """Expand to a larger array of there is no space. Uses doubling."""
        if self._size == len(self._elements):
            tmp: Array[T] = Array(len(self._elements) * 2)
            for i in range(self._size):
                tmp[i] = self._elements[i]
            self._elements = tmp

    def append(self, element: T):
        self._check_available_space()
        self._elements[self._size] = element
        self._size += 1

    def _validate_pos(self, position: int):
        """Raise an error if the position is out of bounds"""
        if position < 0 or position >= self._size:
            raise ListOutOfBoundsError()

    def _shift(self, position: int):
        """Move all elements up one cell from position up to the length of the list."""
        for i in range(self._size, position, -1):
            self._elements[i] = self._elements[i - 1]

    def _unshift(self, position: int):
        """Move all elements down one cell from length of list down to position."""
        for i in range(position, self._size):
            self._elements[i] = self._elements[i + 1]
        self._elements[self._size] = None

    def insert(self, position: int, element: T):
        if position == self._size:
            self.append(element)
            return

        self._validate_pos(position)
        self._check_available_space()
        self._shift(position)
        self._elements[position] = element
        self._size += 1

    def remove(self, position: int) -> T:
        self._validate_pos(position)
        tmp: T = self._elements[position]
        self._unshift(position)
        self._size -= 1
        return tmp

    def clear(self):
        # Note: do we nullify?
        # Note: do we go back to a small array?
        self._size = 0

    def __getitem__(self, position: int) -> T:
        self._validate_pos(position)
        return self._elements[position]

    def __setitem__(self, position: int, element: int):
        self._validate_pos(position)
        self._elements[position] = element

    def __iter__(self) -> Iterator[T]:
        self._cursor = 0
        return self

    def __next__(self) -> T:
        if self._cursor >= self._size:
            raise StopIteration
        tmp: T = self._elements[self._cursor]
        self._cursor += 1
        return tmp
