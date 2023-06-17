class DS:
    # Custom Dictionary
    class DefaultDict:
        def __init__(self, default=int):
            self.default = default
            self.x = random.randrange(1, 1 << 31)
            self.dd = defaultdict(default)

        def __repr__(self):
            return "{"+", ".join(f"{k ^ self.x}: {v}" for k, v in self.dd.items())+"}"

        def __eq__(self, other):
            for k in set(self) | set(other):
                if self[k] != other[k]:
                    return False
            return True

        def __or__(self, other):
            res = DS().DefaultDict(self.default)
            for k, v in self.dd:
                res[k] = v
            for k, v in other.dd:
                res[k] = v
            return res

        def __len__(self):
            return len(self.dd)

        def __getitem__(self, item):
            return self.dd[item ^ self.x]

        def __setitem__(self, key, value):
            self.dd[key ^ self.x] = value

        def __delitem__(self, key):
            del self.dd[key ^ self.x]

        def __contains__(self, item):
            return item ^ self.x in self.dd

        def items(self):
            for k, v in self.dd.items():
                yield (k ^ self.x, v)

        def keys(self):
            for k in self.dd:
                yield k ^ self.x

        def values(self):
            for v in self.dd.values():
                yield v

        def __iter__(self):
            for k in self.dd:
                yield k ^ self.x
    # Int Counter
    class CounterInt(DefaultDict):
        def __init__(self, aa=[]):
            super().__init__(int)
            for a in aa:
                self.dd[a ^ self.x] += 1

        def __add__(self, other):
            res = DS().CounterInt()
            for k in set(self) | set(other):
                v = self[k]+other[k]
                if v > 0:
                    res[k] = v
            return res

        def __sub__(self, other):
            res = DS().CounterInt()
            for k in set(self) | set(other):
                v = self[k]-other[k]
                if v > 0:
                    res[k] = v
            return res

        def __and__(self, other):
            res = DS().CounterInt()
            for k in self:
                v = min(self[k], other[k])
                if v > 0:
                    res[k] = v
            return res

        def __or__(self, other):
            res = DS().CounterInt()
            for k in set(self) | set(other):
                v = max(self[k], other[k])
                if v > 0:
                    res[k] = v
            return res
            
    # Custom Set
    class Set:
        def __init__(self, aa=[]):
            self.x = random.randrange(1, 1 << 31)
            self.st = set()
            for a in aa:
                self.st.add(a ^ self.x)

        def __repr__(self):
            return "{"+", ".join(str(k ^ self.x) for k in self.st)+"}"

        def __len__(self):
            return len(self.st)

        def add(self, item):
            self.st.add(item ^ self.x)

        def discard(self, item):
            self.st.discard(item ^ self.x)

        def __contains__(self, item):
            return item ^ self.x in self.st

        def __iter__(self):
            for k in self.st:
                yield k ^ self.x

        def pop(self):
            return self.st.pop() ^ self.x

        def __or__(self, other):
            res = DS().Set(self)
            for a in other:
                res.add(a)
            return res

        def __and__(self, other):
            res = DS().Set()
            for a in self:
                if a in other:
                    res.add(a)
            for a in other:
                if a in self:
                    res.add(a)
            return res
