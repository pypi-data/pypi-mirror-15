# -*- coding: utf-8 -*-
"""``cacheutils`` contains consistent implementations of fundamental
cache types. Currently there are two to choose from:

  * :class:`LRI` - Least-recently inserted
  * :class:`LRU` - Least-recently used

Both caches are :class:`dict` subtypes, designed to be as
interchangeable as possible, to facilitate experimentation. A key
practice with performance enhancement with caching is ensuring that
the caching strategy is working. If the cache is constantly missing,
it is just adding more overhead and code complexity. The standard
statistics are:

  * ``hit_count`` - the number of times the queried key has been in
    the cache
  * ``miss_count`` - the number of times a key has been absent and/or
    fetched by the cache
  * ``soft_miss_count`` - the number of times a key has been absent,
    but a default has been provided by the caller, as with
    :meth:`dict.get` and :meth:`dict.setdefault`. Soft misses are a
    subset of misses, so this number is always less than or equal to
    ``miss_count``.

Additionally, ``cacheutils`` provides :class:`ThresholdCounter`, a
cache-like bounded counter useful for online statistics collection.

Learn more about `caching algorithms on Wikipedia
<https://en.wikipedia.org/wiki/Cache_algorithms#Examples>`_.

"""

# TODO: TimedLRI
# TODO: support 0 max_size?

__all__ = ['LRI', 'LRU', 'cached', 'ThresholdCache']

import itertools
from collections import deque

try:
    from threading import RLock
except Exception:
    class RLock(object):
        'Dummy reentrant lock for builds without threads'
        def __enter__(self):
            pass

        def __exit__(self, exctype, excinst, exctb):
            pass

try:
    from typeutils import make_sentinel
    _MISSING = make_sentinel(var_name='_MISSING')
    _KWARG_MARK = make_sentinel(var_name='_KWARG_MARK')
except ImportError:
    _MISSING = object()
    _KWARG_MARK = object()

try:
    xrange
except NameError:
    xrange = range

PREV, NEXT, KEY, VALUE = range(4)   # names for the link fields
DEFAULT_MAX_SIZE = 128


class LRU(dict):
    """The ``LRU`` is :class:`dict` subtype implementation of the
    *Least-Recently Used* caching strategy.

    Args:
        max_size (int): Max number of items to cache. Defaults to ``128``.
        values (iterable): Initial values for the cache. Defaults to ``None``.
        on_miss (callable): a callable which accepts a single argument, the
            key not present in the cache, and returns the value to be cached.

    >>> cap_cache = LRU(max_size=2)
    >>> cap_cache['a'], cap_cache['b'] = 'A', 'B'
    >>> from pprint import pprint as pp
    >>> pp(dict(cap_cache))
    {'a': 'A', 'b': 'B'}
    >>> [cap_cache['b'] for i in range(3)][0]
    'B'
    >>> cap_cache['c'] = 'C'
    >>> print(cap_cache.get('a'))
    None

    This cache is also instrumented with statistics
    collection. ``hit_count``, ``miss_count``, and ``soft_miss_count``
    are all integer members that can be used to introspect the
    performance of the cache. ("Soft" misses are misses that did not
    raise :exc:`KeyError`, e.g., ``LRU.get()`` or ``on_miss`` was used to
    cache a default.

    >>> cap_cache.hit_count, cap_cache.miss_count, cap_cache.soft_miss_count
    (3, 1, 1)

    Other than the size-limiting caching behavior and statistics,
    ``LRU`` acts like its parent class, the built-in Python :class:`dict`.
    """
    def __init__(self, max_size=DEFAULT_MAX_SIZE, values=None,
                 on_miss=None):
        if max_size <= 0:
            raise ValueError('expected max_size > 0, not %r' % max_size)
        self.hit_count = self.miss_count = self.soft_miss_count = 0
        self.max_size = max_size
        self._lock = RLock()
        self._init_ll()

        if on_miss is not None and not callable(on_miss):
            raise TypeError('expected on_miss to be a callable'
                            ' (or None), not %r' % on_miss)
        self.on_miss = on_miss

        if values:
            self.update(values)

    # TODO: fromkeys()?

    # linked list manipulation methods.
    #
    # invariants:
    # 1) 'anchor' is the sentinel node in the doubly linked list.  there is
    #    always only one, and its KEY and VALUE are both _MISSING.
    # 2) the most recently accessed node comes immediately before 'anchor'.
    # 3) the least recently accessed node comes immediately after 'anchor'.
    def _init_ll(self):
        anchor = []
        anchor[:] = [anchor, anchor, _MISSING, _MISSING]
        # a link lookup table for finding linked list links in O(1)
        # time.
        self._link_lookup = {}
        self._anchor = anchor

    def _print_ll(self):
        link = self._anchor
        print('***')
        while True:
            print(link[KEY], link[VALUE])
            link = link[NEXT]
            if link is self._anchor:
                break
        print('***')
        return

    def _get_link_and_move_to_front_of_ll(self, key):
        # find what will become the newest link. this may raise a
        # KeyError, which is useful to __getitem__ and __setitem__
        newest = self._link_lookup[key]

        # splice out what will become the newest link.
        newest[PREV][NEXT] = newest[NEXT]
        newest[NEXT][PREV] = newest[PREV]

        # move what will become the newest link immediately before
        # anchor (invariant 2)
        anchor = self._anchor
        second_newest = anchor[PREV]
        second_newest[NEXT] = anchor[PREV] = newest
        newest[PREV] = second_newest
        newest[NEXT] = anchor
        return newest

    def _set_key_and_add_to_front_of_ll(self, key, value):
        # create a new link and place it immediately before anchor
        # (invariant 2).
        anchor = self._anchor
        second_newest = anchor[PREV]
        newest = [second_newest, anchor, key, value]
        second_newest[NEXT] = anchor[PREV] = newest
        self._link_lookup[key] = newest

    def _set_key_and_evict_last_in_ll(self, key, value):
        # the link after anchor is the oldest in the linked list
        # (invariant 3).  the current anchor becomes a link that holds
        # the newest key, and the oldest link becomes the new anchor
        # (invariant 1).  now the newest link comes before anchor
        # (invariant 2).  no links are moved; only their keys
        # and values are changed.
        oldanchor = self._anchor
        oldanchor[KEY] = key
        oldanchor[VALUE] = value

        self._anchor = anchor = oldanchor[NEXT]
        evicted = anchor[KEY]
        anchor[KEY] = anchor[VALUE] = _MISSING
        del self._link_lookup[evicted]
        self._link_lookup[key] = oldanchor
        return evicted

    def _remove_from_ll(self, key):
        # splice a link out of the list and drop it from our lookup
        # table.
        link = self._link_lookup.pop(key)
        link[PREV][NEXT] = link[NEXT]
        link[NEXT][PREV] = link[PREV]

    def __setitem__(self, key, value):
        with self._lock:
            try:
                link = self._get_link_and_move_to_front_of_ll(key)
            except KeyError:
                if len(self) < self.max_size:
                    self._set_key_and_add_to_front_of_ll(key, value)
                else:
                    evicted = self._set_key_and_evict_last_in_ll(key, value)
                    super(LRU, self).__delitem__(evicted)
                super(LRU, self).__setitem__(key, value)
            else:
                link[VALUE] = value

    def __getitem__(self, key):
        with self._lock:
            try:
                link = self._get_link_and_move_to_front_of_ll(key)
            except KeyError:
                self.miss_count += 1
                if not self.on_miss:
                    raise
                ret = self[key] = self.on_miss(key)
                return ret

            self.hit_count += 1
            return link[VALUE]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            self.soft_miss_count += 1
            return default

    def __delitem__(self, key):
        with self._lock:
            super(LRU, self).__delitem__(key)
            self._remove_from_ll(key)

    def pop(self, key, default=_MISSING):
        # NB: hit/miss counts are bypassed for pop()
        with self._lock:
            try:
                ret = super(LRU, self).pop(key)
            except KeyError:
                if default is _MISSING:
                    raise
                ret = default
            else:
                self._remove_from_ll(key)
            return ret

    def popitem(self):
        with self._lock:
            item = super(LRU, self).popitem()
            self._remove_from_ll(item[0])
            return item

    def clear(self):
        with self._lock:
            super(LRU, self).clear()
            self._init_ll()

    def copy(self):
        return self.__class__(max_size=self.max_size, values=self)

    def setdefault(self, key, default=None):
        with self._lock:
            try:
                return self[key]
            except KeyError:
                self.soft_miss_count += 1
                self[key] = default
                return default

    def update(self, E, **F):
        # E and F are throwback names to the dict() __doc__
        with self._lock:
            if E is self:
                return
            setitem = self.__setitem__
            if callable(getattr(E, 'keys', None)):
                for k in E.keys():
                    setitem(k, E[k])
            else:
                for k, v in E:
                    setitem(k, v)
            for k in F:
                setitem(k, F[k])
            return

    def __eq__(self, other):
        with self._lock:
            if self is other:
                return True
            if len(other) != len(self):
                return False
            if not isinstance(other, LRU):
                return other == self
            return super(LRU, self).__eq__(other)

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        cn = self.__class__.__name__
        val_map = super(LRU, self).__repr__()
        return ('%s(max_size=%r, on_miss=%r, values=%s)'
                % (cn, self.max_size, self.on_miss, val_map))


class LRI(dict):
    """The ``LRI`` implements the basic *Least Recently Inserted* strategy to
    caching. One could also think of this as a ``SizeLimitedDefaultDict``.

    *on_miss* is a callable that accepts the missing key (as opposed
    to :class:`collections.defaultdict`'s "default_factory", which
    accepts no arguments.) Also note that, like the :class:`LRU`,
    the ``LRI`` is instrumented with statistics tracking.

    >>> cap_cache = LRI(max_size=2)
    >>> cap_cache['a'], cap_cache['b'] = 'A', 'B'
    >>> from pprint import pprint as pp
    >>> pp(cap_cache)
    {'a': 'A', 'b': 'B'}
    >>> [cap_cache['b'] for i in range(3)][0]
    'B'
    >>> cap_cache['c'] = 'C'
    >>> print(cap_cache.get('a'))
    None
    >>> cap_cache.hit_count, cap_cache.miss_count, cap_cache.soft_miss_count
    (3, 1, 1)
    """
    # In order to support delitem andn .pop() setitem will need to
    # popleft until it finds a key still in the cache. or, only
    # support popitems and raise an error on pop.
    def __init__(self, max_size=DEFAULT_MAX_SIZE, values=None,
                 on_miss=None):
        super(LRI, self).__init__()
        self.hit_count = self.miss_count = self.soft_miss_count = 0
        self.max_size = max_size
        self.on_miss = on_miss
        self._queue = deque()

        if values:
            self.update(values)

    def __setitem__(self, key, value):
        # TODO: pop support (see above)
        if len(self) >= self.max_size:
            old = self._queue.popleft()
            del self[old]
        super(LRI, self).__setitem__(key, value)
        self._queue.append(key)

    def update(self, E, **F):
        # E and F are throwback names to the dict() __doc__
        if E is self:
            return
        setitem = self.__setitem__
        if callable(getattr(E, 'keys', None)):
            for k in E.keys():
                setitem(k, E[k])
        else:
            for k, v in E:
                setitem(k, v)
        for k in F:
            setitem(k, F[k])
        return

    def copy(self):
        return self.__class__(max_size=self.max_size, values=self)

    def clear(self):
        self._queue.clear()
        super(LRI, self).clear()

    def __getitem__(self, key):
        try:
            ret = super(LRI, self).__getitem__(key)
        except KeyError:
            self.miss_count += 1
            if not self.on_miss:
                raise
            ret = self[key] = self.on_miss(key)
            return ret
        self.hit_count += 1
        return ret

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            self.soft_miss_count += 1
            return default

    def setdefault(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            self.soft_miss_count += 1
            self[key] = default
            return default


### Cached decorator
# Key-making technique adapted from Python 3.4's functools

class _HashedKey(list):
    """The _HashedKey guarantees that hash() will be called no more than once
    per cached function invocation.
    """
    __slots__ = 'hash_value'

    def __init__(self, key):
        self[:] = key
        self.hash_value = hash(tuple(key))

    def __hash__(self):
        return self.hash_value


def _make_cache_key(args, kwargs, typed=False, kwarg_mark=_KWARG_MARK,
                    fasttypes=frozenset([int, str, frozenset, type(None)])):
    """Make a cache key from optionally typed positional and keyword
    arguments. If *typed* is ``True``, ``3`` and ``3.0`` will be
    treated as separate keys.

    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.

    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.
    """
    key = list(args)
    if kwargs:
        sorted_items = sorted(kwargs.items())
        key.append(kwarg_mark)
        key.extend(sorted_items)
    if typed:
        key.extend([type(v) for v in args])
        if kwargs:
            key.extend([type(v) for k, v in sorted_items])
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return _HashedKey(key)


class CachedFunction(object):
    def __init__(self, func, cache, typed=False):
        self.func = func
        self.cache = cache
        self.typed = typed

    def __call__(self, *args, **kwargs):
        key = _make_cache_key(args, kwargs, typed=self.typed)
        try:
            ret = self.cache[key]
        except KeyError:
            ret = self.cache[key] = self.func(*args, **kwargs)
        return ret

    def __repr__(self):
        cn = self.__class__.__name__
        if self.typed:
            return "%s(func=%r, typed=%r)" % (cn, self.func, self.typed)
        return "%s(func=%r)" % (cn, self.func)


def cached(cache, typed=False):
    """Cache any function with the cache instance of your choosing. Note
    that the function wrapped should take only `hashable`_ arguments.

    Args:
        cache (Mapping): Any :class:`dict`-like object suitable for
            use as a cache. Instances of the :class:`LRU` and
            :class:`LRI` are good choices.
        typed (bool): Whether to factor argument types into the cache
            check. Default ``False``, setting to ``True`` causes the
            cache keys for ``3`` and ``3.0`` to be considered unequal.

    >>> my_cache = LRU()
    >>> @cached(my_cache)
    ... def cached_lower(x):
    ...     return x.lower()
    ...
    >>> cached_lower("CaChInG's FuN AgAiN!")
    "caching's fun again!"
    >>> len(my_cache)
    1

    .. _hashable: https://docs.python.org/2/glossary.html#term-hashable
    """
    def cached_func_decorator(func):
        return CachedFunction(func, cache, typed=typed)
    return cached_func_decorator


class ThresholdCounter(object):
    """A **bounded** dict-like Mapping from keys to counts. The
    ThresholdCounter automatically compacts after every (1 /
    *threshold*) additions, maintaining exact counts for any keys
    whose count represents at least a *threshold* ratio of the total
    data. In other words, if a particular key is not present in the
    ThresholdCounter, its count represents less than *threshold* of
    the total data.

    >>> tc = ThresholdCounter(threshold=0.1)
    >>> tc.add(1)
    >>> tc.items()
    [(1, 1)]
    >>> tc.update([2] * 10)
    >>> tc.get(1)
    0
    >>> tc.add(5)
    >>> 5 in tc
    True
    >>> len(list(tc.elements()))
    11

    As you can see above, the API is kept similar to
    :class:`collections.Counter`. The most notable feature omissions
    being that counted items cannot be set directly, uncounted, or
    removed, as this would disrupt the math.

    Use the ThresholdCounter when you need best-effort long-lived
    counts for dynamically-keyed data. Without a bounded datastructure
    such as this one, the dynamic keys often represent a memory leak
    and can impact application reliability. The ThresholdCounter's
    item replacement strategy is fully deterministic and can be
    thought of as *Amortized Least Relevant*. The absolute upper bound
    of keys it will store is *(2/threshold)*, but realistically
    *(1/threshold)* is expected for uniformly random datastreams, and
    one or two orders of magnitude better for real-world data.

    This algorithm is an implementation of the Lossy Counting
    algorithm described in "Approximate Frequency Counts over Data
    Streams" by Manku & Motwani. Hat tip to Kurt Rose for discovery
    and initial implementation.

    """
    # TODO: hit_count/miss_count?
    def __init__(self, threshold=0.001):
        if not 0 < threshold < 1:
            raise ValueError('expected threshold between 0 and 1, not: %r'
                             % threshold)

        self.total = 0
        self._count_map = {}
        self._threshold = threshold
        self._thresh_count = int(1 / threshold)
        self._cur_bucket = 1

    @property
    def threshold(self):
        return self._threshold

    def add(self, key):
        """Increment the count of *key* by 1, automatically adding it if it
        does not exist.

        Cache compaction is triggered every *1/threshold* additions.
        """
        self.total += 1
        try:
            self._count_map[key][0] += 1
        except KeyError:
            self._count_map[key] = [1, self._cur_bucket - 1]

        if self.total % self._thresh_count == 0:
            self._count_map = dict([(k, v) for k, v in self._count_map.items()
                                    if sum(v) > self._cur_bucket])
            self._cur_bucket += 1
        return

    def elements(self):
        """Return an iterator of all the common elements tracked by the
        counter. Yields each key as many times as it has been seen.
        """
        repeaters = itertools.starmap(itertools.repeat, self.iteritems())
        return itertools.chain.from_iterable(repeaters)

    def most_common(self, n=None):
        """Get the top *n* keys and counts as tuples. If *n* is omitted,
        returns all the pairs.
        """
        if n <= 0:
            return []
        ret = sorted(self.iteritems(), key=lambda x: x[1][0], reverse=True)
        if n is None or n >= len(ret):
            return ret
        return ret[:n]

    def get_common_count(self):
        """Get the sum of counts for keys exceeding the configured data
        threshold.
        """
        return sum([count for count, _ in self._count_map.itervalues()])

    def get_uncommon_count(self):
        """Get the sum of counts for keys that were culled because the
        associated counts represented less than the configured
        threshold. The long-tail counts.
        """
        return self.total - self.get_common_count()

    def get_commonality(self):
        """Get a float representation of the effective count accuracy. The
        higher the number, the less uniform the keys being added, and
        the higher accuracy and efficiency of the ThresholdCounter.

        If a stronger measure of data cardinality is required,
        consider using hyperloglog.
        """
        return float(self.get_common_count()) / self.total

    def __getitem__(self, key):
        return self._count_map[key][0]

    def __len__(self):
        return len(self._count_map)

    def __contains__(self, key):
        return key in self._count_map

    def iterkeys(self):
        return iter(self._count_map)

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        count_map = self._count_map
        for k in count_map:
            yield count_map[k][0]

    def values(self):
        return list(self.itervalues())

    def iteritems(self):
        count_map = self._count_map
        for k in count_map:
            yield (k, count_map[k][0])

    def items(self):
        return list(self.iteritems())

    def get(self, key, default=0):
        "Get count for *key*, defaulting to 0."
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, iterable, **kwargs):
        """Like dict.update() but add counts instead of replacing them, used
        to add multiple items in one call.

        Source can be an iterable of keys to add, or a mapping of keys
        to integer counts.
        """
        if iterable is not None:
            if callable(getattr(iterable, 'iteritems', None)):
                for key, count in iterable.iteritems():
                    for i in xrange(count):
                        self.add(key)
            else:
                for key in iterable:
                    self.add(key)
        if kwargs:
            self.update(kwargs)

# end cacheutils.py
