"""
Sorted Set Implementation.
"""

from __future__ import annotations

import itertools
from typing import (
    TYPE_CHECKING,
    Callable,
    Generator,
    Generic,
    Iterable,
    Sequence,
    TypeVar,
    override,
)

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison

T = TypeVar("T")


class SortedSetView(Generic[T], Sequence):
    """
    A view on the SortedSet.

    The view allows for observing the data in the underlying
    SortedSet, without the ability to modify what it contains.
    """

    __slots__ = ("_set",)

    @override
    def __init__(self, set_: SortedSet[T]):
        self._set = set_

    @override
    def __len__(self):
        return len(self._set)

    @override
    def __contains__(self, element):
        return element in self._set

    @override
    def __iter__(self):
        return self._set.__iter__()

    @override
    def __getitem__(self, index):
        return self._set.__getitem__(index)

    @override
    def __eq__(self, value):
        if isinstance(value, SortedSetView):
            return self._set == value._set
        if isinstance(value, set):
            return self._set == value
        if isinstance(value, list):
            return list(self._set) == value
        if isinstance(value, tuple):
            return tuple(self._set) == value
        return super().__eq__(value)

    @override
    def __ne__(self, value):
        if isinstance(value, SortedSetView):
            return self._set != value._set
        if isinstance(value, set):
            return self._set != value
        if isinstance(value, list):
            return list(self._set) != value
        if isinstance(value, tuple):
            return tuple(self._set) != value
        return super().__ne__(value)

    @override
    def __hash__(self):
        return object.__hash__(self)


class SortedSet(set[T], Sequence[T]):
    """
    Implementation of a set that maintains insertion order.
    Contents are accessible by index and all set operations are
    implemented to maintain combined ordering.
    """

    __slots__ = ("_list",)

    @override
    def __init__(self, iterable: Iterable[T] | None = None):
        super().__init__()
        self._list: list[T] = []

        if isinstance(iterable, Iterable):
            self.update(iterable)
        elif iterable is not None:
            msg = f"{type(iterable)} object is not iterable"
            raise TypeError(msg)

    @override
    def add(self, element):
        if element not in self:
            self._list.append(element)
            super().add(element)

    @override
    def clear(self):
        self._list.clear()
        super().clear()

    @override
    def discard(self, element):
        if element in self:
            self._list.remove(element)
        super().discard(element)

    @override
    def remove(self, element):
        super().remove(element)
        self._list.remove(element)

    def _combined_values(self, *s: Iterable[T]) -> Generator[T]:
        """
        Yield from the current values of the sorted set
        and the values of the passed iterables.
        """
        yield from self._list
        for i in s:
            yield from i

    def _filter_values(self, set_: set[T], s: Iterable[T]) -> Generator[T]:
        """
        Yield values from the passed iterable only once
        if they are in the passed set.
        """
        for i in s:
            if i in set_:
                set_.remove(i)
                yield i

    @override
    def difference(self, *s):
        i, j = itertools.tee(self._combined_values(*s), 2)
        new_set = super().difference(i)
        return self.__class__(filter(lambda x: x in new_set, j))

    @override
    def difference_update(self, *s):
        i, j = itertools.tee(self._combined_values(*s), 2)
        super().difference_update(i)
        self._list[:] = filter(lambda x: x in self, j)

    @override
    def intersection(self, *s):
        i, j = itertools.tee(self._combined_values(*s), 2)
        new_set = super().intersection(i)
        return self.__class__(filter(lambda x: x in new_set, j))

    @override
    def intersection_update(self, *s):
        i, j = itertools.tee(self._combined_values(*s), 2)
        super().intersection_update(i)
        self._list[:] = filter(lambda x: x in self, j)

    @override
    def symmetric_difference(self, s):
        i, j = itertools.tee(self._combined_values(s), 2)
        new_set = super().symmetric_difference(i)
        return self.__class__(self._filter_values(new_set, j))

    @override
    def symmetric_difference_update(self, s):
        i, j = itertools.tee(self._combined_values(s), 2)
        super().symmetric_difference_update(i)
        self._list[:] = self._filter_values(super().copy(), j)

    @override
    def union(self, *s):
        i, j = itertools.tee(self._combined_values(*s), 2)
        new_set = super().union(i)
        return self.__class__(self._filter_values(new_set, j))

    @override
    def update(self, *s):
        i, j = itertools.tee(self._combined_values(*s), 2)
        super().update(i)
        self._list[:] = self._filter_values(super().copy(), j)

    @override
    def pop(self, index: int = -1):
        i = self._list.pop(index)
        super().remove(i)
        return i

    pop.__doc__ = list.pop.__doc__

    @override
    def copy(self):
        return self.__class__(self._list)

    def get_view(self) -> SortedSetView[T]:
        """
        Return a view on the SortedSet.
        """
        return SortedSetView(self)

    def get_list(self) -> list[T]:
        """
        Return a shallow copy of the underlying list.
        """
        return self._list.copy()

    def sort(
        self,
        *,
        key: Callable[[T], SupportsRichComparison] | None = None,
        reverse: bool = False,
    ):
        """
        Call to the underlying list's sort method.
        """
        self._list.sort(key=key, reverse=reverse)

    sort.__doc__ += list.sort.__doc__  # type: ignore

    @override
    def __iter__(self):
        return self._list.__iter__()

    @override
    def __reversed__(self):
        return self._list.__reversed__()

    @override
    def __getitem__(self, index):
        return self._list.__getitem__(index)

    @override
    def __sub__(self, value):
        return self.difference(value)

    @override
    def __isub__(self, value):
        self.difference_update(value)
        return self

    @override
    def __and__(self, value):
        return self.intersection(value)

    @override
    def __iand__(self, value):
        self.intersection_update(value)
        return self

    @override
    def __or__(self, value):
        return self.union(value)

    @override
    def __ior__(self, value):
        self.update(value)
        return self

    @override
    def __xor__(self, value):
        return self.symmetric_difference(value)

    @override
    def __ixor__(self, value):
        self.symmetric_difference_update(value)
        return self

    @override
    def __repr__(self):
        vals = [f"{key}" for key in self._list]
        return f"{{{', '.join(vals)}}}"

    @override
    def __getstate__(self):
        return self._list.__getstate__()

    @override
    def __setstate__(self, state):
        self.update(state)

    @override
    def __eq__(self, value):
        if isinstance(value, SortedSet):
            return self._list == value._list
        return False

    @override
    def __ne__(self, value):
        if isinstance(value, SortedSet):
            return self._list != value._list
        return True

    @override
    def __hash__(self):
        return object.__hash__(self)
