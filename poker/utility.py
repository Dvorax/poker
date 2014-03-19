import locale


class Collection(object):

    def __init__(self, *items):
        self.items = list(items)
    
    def _copy(self):
        return self.__class__(*self.items)

    def add(self, *items):
        collection = self._copy()
        for item in items:
            if item not in collection.items:
                collection.items.append(item)
            else:
                raise CollectionError(
                    'Duplicate item already exists in collection')
        return collection

    def remove(self, *items):
        collection = self._copy()
        for item in items:
            if item in collection.items:
                collection.items.remove(item)
            else:
                raise CollectionError(
                    'Item not available to be removed in collection')
        return collection

    def limit(self, amount):
        if 1 < amount <= len(self):
            result = self.__class__(*sorted(self)[-amount:])
        elif amount > 1 and len(self) < amount:
            result = self._copy()
        elif amount == 1 and len(self) > 0:
            result = max(self)
        else:
            result = None

        return result

    def filler(self, limit, *exclude):
        filler = self._copy()
        filler = filler.remove(*exclude)
        return filler.limit(limit)

    def intersect(self, other):
        return self.__class__(*(set(self.items) & set(other.items)))

    def __lt__(self, other):
        return sorted(self.items) < sorted(other.items)

    def __gt__(self, other):
        return sorted(self.items) > sorted(other.items)

    def __eq__(self, other):
        return type(other) is self.__class__ and \
            sorted(self.items) == sorted(other.items)

    def __le__(self, other):
        return sorted(self.items) <= sorted(other.items)

    def __ge__(self, other):
        return sorted(self.items) >= sorted(other.items)

    def __ne__(self, other):
        return type(other) is self.__class__ and \
            sorted(self.items) != sorted(other.items)

    def __getitem__(self, key):
        return self.items[key]

    def __add__(self, other):
        return self.__class__(*list(self.items + other.items))

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return '<' + self.__class__.__name__ + ': ' + str(self.items) + '>'


class Cache(object):
    pass


class CollectionError(Exception):
    pass


def currency(amount):
    # returns amount as a currency string without decimal
    locale.setlocale(locale.LC_ALL, '')
    return locale.currency(amount, grouping=True)[:-3]