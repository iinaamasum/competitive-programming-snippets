class ShortedDS:
    # Sorted List
    class SortedList:
        def __init__(self, iterable=[], _load=200):
            """Initialize sorted list instance."""
            values = sorted(iterable)
            self._len = _len = len(values)
            self._load = _load
            self._lists = _lists = [values[i:i + _load]
                                    for i in range(0, _len, _load)]
            self._list_lens = [len(_list) for _list in _lists]
            self._mins = [_list[0] for _list in _lists]
            self._fen_tree = []
            self._rebuild = True

        def _fen_build(self):
            """Build a fenwick tree instance."""
            self._fen_tree[:] = self._list_lens
            _fen_tree = self._fen_tree
            for i in range(len(_fen_tree)):
                if i | i + 1 < len(_fen_tree):
                    _fen_tree[i | i + 1] += _fen_tree[i]
            self._rebuild = False

        def _fen_update(self, index, value):
            """Update `fen_tree[index] += value`."""
            if not self._rebuild:
                _fen_tree = self._fen_tree
                while index < len(_fen_tree):
                    _fen_tree[index] += value
                    index |= index + 1

        def _fen_query(self, end):
            """Return `sum(_fen_tree[:end])`."""
            if self._rebuild:
                self._fen_build()

            _fen_tree = self._fen_tree
            x = 0
            while end:
                x += _fen_tree[end - 1]
                end &= end - 1
            return x

        def _fen_findkth(self, k):
            """Return a pair of (the largest `idx` such that `sum(_fen_tree[:idx]) <= k`, `k - sum(_fen_tree[:idx])`)."""
            _list_lens = self._list_lens
            if k < _list_lens[0]:
                return 0, k
            if k >= self._len - _list_lens[-1]:
                return len(_list_lens) - 1, k + _list_lens[-1] - self._len
            if self._rebuild:
                self._fen_build()

            _fen_tree = self._fen_tree
            idx = -1
            for d in reversed(range(len(_fen_tree).bit_length())):
                right_idx = idx + (1 << d)
                if right_idx < len(_fen_tree) and k >= _fen_tree[right_idx]:
                    idx = right_idx
                    k -= _fen_tree[idx]
            return idx + 1, k

        def _delete(self, pos, idx):
            """Delete value at the given `(pos, idx)`."""
            _lists = self._lists
            _mins = self._mins
            _list_lens = self._list_lens

            self._len -= 1
            self._fen_update(pos, -1)
            del _lists[pos][idx]
            _list_lens[pos] -= 1

            if _list_lens[pos]:
                _mins[pos] = _lists[pos][0]
            else:
                del _lists[pos]
                del _list_lens[pos]
                del _mins[pos]
                self._rebuild = True

        def _loc_left(self, value):
            """Return an index pair that corresponds to the first position of `value` in the sorted list."""
            if not self._len:
                return 0, 0

            _lists = self._lists
            _mins = self._mins

            lo, pos = -1, len(_lists) - 1
            while lo + 1 < pos:
                mi = (lo + pos) >> 1
                if value <= _mins[mi]:
                    pos = mi
                else:
                    lo = mi

            if pos and value <= _lists[pos - 1][-1]:
                pos -= 1

            _list = _lists[pos]
            lo, idx = -1, len(_list)
            while lo + 1 < idx:
                mi = (lo + idx) >> 1
                if value <= _list[mi]:
                    idx = mi
                else:
                    lo = mi

            return pos, idx

        def _loc_right(self, value):
            """Return an index pair that corresponds to the last position of `value` in the sorted list."""
            if not self._len:
                return 0, 0

            _lists = self._lists
            _mins = self._mins

            pos, hi = 0, len(_lists)
            while pos + 1 < hi:
                mi = (pos + hi) >> 1
                if value < _mins[mi]:
                    hi = mi
                else:
                    pos = mi

            _list = _lists[pos]
            lo, idx = -1, len(_list)
            while lo + 1 < idx:
                mi = (lo + idx) >> 1
                if value < _list[mi]:
                    idx = mi
                else:
                    lo = mi

            return pos, idx

        def add(self, value):
            """Add `value` to sorted list."""
            _load = self._load
            _lists = self._lists
            _mins = self._mins
            _list_lens = self._list_lens

            self._len += 1
            if _lists:
                pos, idx = self._loc_right(value)
                self._fen_update(pos, 1)
                _list = _lists[pos]
                _list.insert(idx, value)
                _list_lens[pos] += 1
                _mins[pos] = _list[0]
                if _load + _load < len(_list):
                    _lists.insert(pos + 1, _list[_load:])
                    _list_lens.insert(pos + 1, len(_list) - _load)
                    _mins.insert(pos + 1, _list[_load])
                    _list_lens[pos] = _load
                    del _list[_load:]
                    self._rebuild = True
            else:
                _lists.append([value])
                _mins.append(value)
                _list_lens.append(1)
                self._rebuild = True

        def discard(self, value):
            """Remove `value` from sorted list if it is a member."""
            _lists = self._lists
            if _lists:
                pos, idx = self._loc_right(value)
                if idx and _lists[pos][idx - 1] == value:
                    self._delete(pos, idx - 1)

        def remove(self, value):
            """Remove `value` from sorted list; `value` must be a member."""
            _len = self._len
            self.discard(value)
            if _len == self._len:
                raise ValueError('{0!r} not in list'.format(value))

        def pop(self, index=-1):
            """Remove and return value at `index` in sorted list."""
            pos, idx = self._fen_findkth(
                self._len + index if index < 0 else index)
            value = self._lists[pos][idx]
            self._delete(pos, idx)
            return value

        def bisect_left(self, value):
            """Return the first index to insert `value` in the sorted list."""
            pos, idx = self._loc_left(value)
            return self._fen_query(pos) + idx

        def bisect_right(self, value):
            """Return the last index to insert `value` in the sorted list."""
            pos, idx = self._loc_right(value)
            return self._fen_query(pos) + idx

        def count(self, value):
            """Return number of occurrences of `value` in the sorted list."""
            return self.bisect_right(value) - self.bisect_left(value)

        def __len__(self):
            """Return the size of the sorted list."""
            return self._len

        def __getitem__(self, index):
            """Lookup value at `index` in sorted list."""
            pos, idx = self._fen_findkth(
                self._len + index if index < 0 else index)
            return self._lists[pos][idx]

        def __delitem__(self, index):
            """Remove value at `index` from sorted list."""
            pos, idx = self._fen_findkth(
                self._len + index if index < 0 else index)
            self._delete(pos, idx)

        def __contains__(self, value):
            """Return true if `value` is an element of the sorted list."""
            _lists = self._lists
            if _lists:
                pos, idx = self._loc_left(value)
                return idx < len(_lists[pos]) and _lists[pos][idx] == value
            return False

        def __iter__(self):
            """Return an iterator over the sorted list."""
            return (value for _list in self._lists for value in _list)

        def __reversed__(self):
            """Return a reverse iterator over the sorted list."""
            return (value for _list in reversed(self._lists) for value in reversed(_list))

        def __repr__(self):
            """Return string representation of sorted list."""
            return 'DS().SortedList({0})'.format(list(self))

    # Sorted Set
    class SortedSet():
        from typing import Generic, Iterable, Iterator, List, Tuple, TypeVar, Optional
        T = TypeVar('T')
        BUCKET_RATIO = 50
        REBUILD_RATIO = 170

        def _build(self, a: Optional[List[T]] = None) -> None:
            "Evenly divide `a` into buckets."
            if a is None:
                a = list(self)
            size = self.size = len(a)
            bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
            self.a = [a[size * i // bucket_size: size *
                        (i + 1) // bucket_size] for i in range(bucket_size)]

        def __init__(self, a: Iterable[T] = []) -> None:
            "Make a new SortedSet from iterable. / O(N) if sorted and unique / O(N log N)"
            a = list(a)
            if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
                a = sorted(set(a))
            self._build(a)

        def __iter__(self) -> Iterator[T]:
            for i in self.a:
                for j in i:
                    yield j

        def __reversed__(self) -> Iterator[T]:
            for i in reversed(self.a):
                for j in reversed(i):
                    yield j

        def __eq__(self, other) -> bool:
            return list(self) == list(other)

        def __len__(self) -> int:
            return self.size

        def __repr__(self) -> str:
            return "SortedSet" + str(self.a)

        def __str__(self) -> str:
            s = str(list(self))
            return "{" + s[1: len(s) - 1] + "}"

        def _position(self, x: T) -> Tuple[List[T], int]:
            "Find the bucket and position which x should be inserted. self must not be empty."
            for a in self.a:
                if x <= a[-1]:
                    break
            return (a, bisect_left(a, x))

        def __contains__(self, x: T) -> bool:
            if self.size == 0:
                return False
            a, i = self._position(x)
            return i != len(a) and a[i] == x

        def add(self, x: T) -> bool:
            "Add an element and return True if added. / O(√N)"
            if self.size == 0:
                self.a = [[x]]
                self.size = 1
                return True
            a, i = self._position(x)
            if i != len(a) and a[i] == x:
                return False
            a.insert(i, x)
            self.size += 1
            if len(a) > len(self.a) * self.REBUILD_RATIO:
                self._build()
            return True

        def _pop(self, a: List[T], i: int) -> T:
            ans = a.pop(i)
            self.size -= 1
            if not a:
                self._build()
            return ans

        def discard(self, x: T) -> bool:
            "Remove an element and return True if removed. / O(√N)"
            if self.size == 0:
                return False
            a, i = self._position(x)
            if i == len(a) or a[i] != x:
                return False
            self._pop(a, i)
            return True

        def lt(self, x: T) -> Optional[T]:
            "Find the largest element < x, or None if it doesn't exist."
            for a in reversed(self.a):
                if a[0] < x:
                    return a[bisect_left(a, x) - 1]

        def le(self, x: T) -> Optional[T]:
            "Find the largest element <= x, or None if it doesn't exist."
            for a in reversed(self.a):
                if a[0] <= x:
                    return a[bisect_right(a, x) - 1]

        def gt(self, x: T) -> Optional[T]:
            "Find the smallest element > x, or None if it doesn't exist."
            for a in self.a:
                if a[-1] > x:
                    return a[bisect_right(a, x)]

        def ge(self, x: T) -> Optional[T]:
            "Find the smallest element >= x, or None if it doesn't exist."
            for a in self.a:
                if a[-1] >= x:
                    return a[bisect_left(a, x)]

        def __getitem__(self, i: int) -> T:
            "Return the i-th element."
            if i < 0:
                for a in reversed(self.a):
                    i += len(a)
                    if i >= 0:
                        return a[i]
            else:
                for a in self.a:
                    if i < len(a):
                        return a[i]
                    i -= len(a)
            raise IndexError

        def pop(self, i: int = -1) -> T:
            "Pop and return the i-th element."
            if i < 0:
                for a in reversed(self.a):
                    i += len(a)
                    if i >= 0:
                        return self._pop(a, i)
            else:
                for a in self.a:
                    if i < len(a):
                        return self._pop(a, i)
                    i -= len(a)
            raise IndexError

        def index(self, x: T) -> int:
            "Count the number of elements < x."
            ans = 0
            for a in self.a:
                if a[-1] >= x:
                    return ans + bisect_left(a, x)
                ans += len(a)
            return ans

        def index_right(self, x: T) -> int:
            "Count the number of elements <= x."
            ans = 0
            for a in self.a:
                if a[-1] > x:
                    return ans + bisect_right(a, x)
                ans += len(a)
            return ans

    # Sorted Multi Set
    class SortedMultiSet():
        from typing import Generic, Iterable, Iterator, List, Tuple, TypeVar, Optional
        T = TypeVar('T')
        BUCKET_RATIO = 50
        REBUILD_RATIO = 170

        def _build(self, a: Optional[List[T]] = None) -> None:
            "Evenly divide `a` into buckets."
            if a is None:
                a = list(self)
            size = self.size = len(a)
            bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
            self.a = [a[size * i // bucket_size: size *
                        (i + 1) // bucket_size] for i in range(bucket_size)]

        def __init__(self, a: Iterable[T] = []) -> None:
            "Make a new SortedMultiset from iterable. / O(N) if sorted / O(N log N)"
            a = list(a)
            if not all(a[i] <= a[i + 1] for i in range(len(a) - 1)):
                a = sorted(a)
            self._build(a)

        def __iter__(self) -> Iterator[T]:
            for i in self.a:
                for j in i:
                    yield j

        def __reversed__(self) -> Iterator[T]:
            for i in reversed(self.a):
                for j in reversed(i):
                    yield j

        def __eq__(self, other) -> bool:
            return list(self) == list(other)

        def __len__(self) -> int:
            return self.size

        def __repr__(self) -> str:
            return "SortedMultiSet" + str(self.a)

        def __str__(self) -> str:
            s = str(list(self))
            return "{" + s[1: len(s) - 1] + "}"

        def _position(self, x: T) -> Tuple[List[T], int]:
            "Find the bucket and position which x should be inserted. self must not be empty."
            for a in self.a:
                if x <= a[-1]:
                    break
            return (a, bisect_left(a, x))

        def __contains__(self, x: T) -> bool:
            if self.size == 0:
                return False
            a, i = self._position(x)
            return i != len(a) and a[i] == x

        def count(self, x: T) -> int:
            "Count the number of x."
            return self.index_right(x) - self.index(x)

        def add(self, x: T) -> None:
            "Add an element. / O(√N)"
            if self.size == 0:
                self.a = [[x]]
                self.size = 1
                return
            a, i = self._position(x)
            a.insert(i, x)
            self.size += 1
            if len(a) > len(self.a) * self.REBUILD_RATIO:
                self._build()

        def _pop(self, a: List[T], i: int) -> T:
            ans = a.pop(i)
            self.size -= 1
            if not a:
                self._build()
            return ans

        def discard(self, x: T) -> bool:
            "Remove an element and return True if removed. / O(√N)"
            if self.size == 0:
                return False
            a, i = self._position(x)
            if i == len(a) or a[i] != x:
                return False
            self._pop(a, i)
            return True

        def lt(self, x: T) -> Optional[T]:
            "Find the largest element < x, or None if it doesn't exist."
            for a in reversed(self.a):
                if a[0] < x:
                    return a[bisect_left(a, x) - 1]

        def le(self, x: T) -> Optional[T]:
            "Find the largest element <= x, or None if it doesn't exist."
            for a in reversed(self.a):
                if a[0] <= x:
                    return a[bisect_right(a, x) - 1]

        def gt(self, x: T) -> Optional[T]:
            "Find the smallest element > x, or None if it doesn't exist."
            for a in self.a:
                if a[-1] > x:
                    return a[bisect_right(a, x)]

        def ge(self, x: T) -> Optional[T]:
            "Find the smallest element >= x, or None if it doesn't exist."
            for a in self.a:
                if a[-1] >= x:
                    return a[bisect_left(a, x)]

        def __getitem__(self, i: int) -> T:
            "Return the i-th element."
            if i < 0:
                for a in reversed(self.a):
                    i += len(a)
                    if i >= 0:
                        return a[i]
            else:
                for a in self.a:
                    if i < len(a):
                        return a[i]
                    i -= len(a)
            raise IndexError

        def pop(self, i: int = -1) -> T:
            "Pop and return the i-th element."
            if i < 0:
                for a in reversed(self.a):
                    i += len(a)
                    if i >= 0:
                        return self._pop(a, i)
            else:
                for a in self.a:
                    if i < len(a):
                        return self._pop(a, i)
                    i -= len(a)
            raise IndexError

        def index(self, x: T) -> int:
            "Count the number of elements < x."
            ans = 0
            for a in self.a:
                if a[-1] >= x:
                    return ans + bisect_left(a, x)
                ans += len(a)
            return ans

        def index_right(self, x: T) -> int:
            "Count the number of elements <= x."
            ans = 0
            for a in self.a:
                if a[-1] > x:
                    return ans + bisect_right(a, x)
                ans += len(a)
            return ans
