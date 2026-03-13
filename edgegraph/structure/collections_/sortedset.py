"""
Sorted Set Implementation.
"""

from __future__ import annotations

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
            return self._set._list == value
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
            return self._set._list != value
        if isinstance(value, tuple):
            return tuple(self._set) != value
        return super().__ne__(value)


class SortedSet(set[T], Sequence[T]):
    """
    Basic implementation of a set that maintains insertion order.
    Contents are accessible by index and all set operations are
    implemented to maintain combined ordering.
    """

    __slots__ = ("_list",)

    @override
    def __init__(self, iterable: Iterable[T] | None = None):
        super().__init__()
        if isinstance(iterable, Iterable):
            self._list = list(iterable)
            super().update(self._list)
        elif iterable is None:
            self._list = []
        else:
            msg = f"Unable to initialize {self.__class__} from value"
            raise ValueError(msg)

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
        self._list.remove(element)
        super().remove(element)

    def _combined_generator(self, *s: Iterable[T]) -> Generator[T]:
        yield from self._list
        for i in s:
            yield from i

    def _ordered_combined_generator(
        self, set_: set[T], *s: Iterable[T]
    ) -> Generator[T]:
        comb_list = self._combined_generator(*s)
        for i in comb_list:
            if i in set_:
                set_.remove(i)
                yield i

    @override
    def difference(self, *s):
        new_set = super().difference(*s)
        return self.__class__(filter(lambda x: x in new_set, self._list))

    @override
    def difference_update(self, *s):
        super().difference_update(*s)
        self._list[:] = filter(lambda x: x in self, self._list)

    @override
    def intersection(self, *s):
        new_set = super().intersection(*s)
        return self.__class__(filter(lambda x: x in new_set, self._list))

    @override
    def intersection_update(self, *s):
        super().intersection_update(*s)
        self._list[:] = filter(lambda x: x in self, self._list)

    @override
    def symmetric_difference(self, s):
        new_set = super().symmetric_difference(s)
        comb_list = self._combined_generator(s)
        return self.__class__(filter(lambda x: x in new_set, comb_list))

    @override
    def symmetric_difference_update(self, s):
        super().symmetric_difference_update(s)
        comb_list = self._combined_generator(s)
        self._list[:] = filter(lambda x: x in self, comb_list)

    @override
    def union(self, *s):
        new_set = super().union(*s)
        return self.__class__(self._ordered_combined_generator(new_set, *s))

    @override
    def update(self, *s):
        super().update(*s)
        self._list[:] = self._ordered_combined_generator(super().copy(), *s)

    @override
    def pop(self, index: int = -1):
        i = self._list.pop(index)
        super().remove(i)
        return i

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
        Return a copy of the underlying list.
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
