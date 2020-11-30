from typing import Iterator, Tuple, Any, Union


class NotSet:
    pass


class _KnowledgeBase(dict):

    def get(self, group: str, key: str = None, default: Any = NotSet) -> \
            Union[Iterator[Tuple[str, Any]], Any]:
        if key is not None:
            key = '/%s/%s' % (group, key)
            if key not in self:
                if default != NotSet:
                    return default
            return self[key]
        # spin up an iterator on the group
        return self.group(group)

    def group(self, group: str) -> Iterator[Tuple[str, Any]]:
        # this avoids issue with long iterations and multi-thread access
        keys = list(self.keys())
        # spin up an iterator on the group
        for key in keys:
            gkey = '/%s/' % group
            if key.startswith(gkey):
                yield key[len(gkey):], self[key]

    def set(self, group: str, key: str, value: Any):
        key = '/%s/%s' % (group, key)
        self[key] = value

    def has(self, group: str, key: str) -> bool:
        key = '/%s/%s' % (group, key)
        return key in self

    def remove(self, group: str, key: str):
        key = '/%s/%s' % (group, key)
        if key in self:
            del self[key]


KnowledgeBase = _KnowledgeBase()

__all__ = [
    'KnowledgeBase'
]
