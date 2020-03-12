import sys
from types import ModuleType, FunctionType
from gc import get_referents
from flee import flee
from flee import pflee

# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType


def getsize(obj):
    """sum size of object & members."""
    if isinstance(obj, BLACKLIST):
        raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
                print(size, type(obj), obj)
        objects = get_referents(*need_referents)
    return size

e = pflee.Ecosystem()

#print(getsize(flee.Person(flee.Location("A"))))
#print(getsize(flee.Location("A")))
print(getsize(pflee.Person(e.scores, pflee.Location(e, 0, "A"))))
print(sys.getsizeof(pflee.Person(e.scores, pflee.Location(e, 0, "A"))))
#print(getsize(pflee.Location(e, 0, "A")))
