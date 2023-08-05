# -*- coding: utf-8 -*-
"""Ordered attribute mapping type

Similar to :class:`argparse.Namespace`, but is ordered, and behaves like
dictionary except there are no public methods on OrderedMapping. All operations
are operators or Python builtins so that the attribute names from clients of
a OrderedMapping don't collide.

:copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function

# Avoid pykern imports so avoid dependency issues for pkconfig

def map_items(value, op=None):
    """Iterate over mapping, calling op with key, value

    Args:
        value (object): Any object that implements iteration on keys
        op (function): called with each key, value, in order
            (default: return (key, value))

    Returns:
        list: list of results of op
    """
    if not op:
        return [(k, value[k]) for k in value]
    return [op(k, value[k]) for k in value]


def map_keys(value, op=None):
    """Iterate over mapping, calling op with key

    Args:
        value (object): Any object that implements iteration on keys
        op (function): called with each key, in order (default: return key)

    Returns:
        list: list of results of op
    """
    if not op:
        return [k for k in value]
    return [op(k) for k in value]


def mapping_merge(base, to_merge):
    """Add or replace values from to_merge into base

    Args:
        base (object): Implements setitem
        to_merge (object): implements iter and getitem
    """
    for k in to_merge:
        base[k] = to_merge[k]


def map_values(value, op=None):
    """Iterate over mapping, calling op with value

    Args:
        value (object): Any object that implements iteration on values
        op (function): called with each key, in order (default: return value)

    Returns:
        list: list of results of op
    """
    if not op:
        return [value[k] for k in value]
    return [op(value[k]) for k in value]


class OrderedMapping(object):
    """Ordered mapping can be initialized by kwargs or single argument.

    Args:
        first (object): copy map in order of iterator, OR
        kwargs (dict): initial values (does not preserver order)

    All operations are munged names to avoid collisions with the clients
    of OrderedMapping so there are no "methods" on self except operator overloads.
    """
    def __init__(self, *args, **kwargs):
        self.__order = []
        # Remove __order's mangled name from __order
        self.__order.pop(0)
        if args:
            assert not kwargs, \
                'May not pass kwargs if passing args'
            if len(args) == 1:
                if isinstance(args[0], list):
                    args = args[0]
                else:
                    kwargs = args[0]
                    args = None
            if args:
                if len(args) % 2 != 0:
                    raise TypeError(
                        'Only one argument must be a mapping type')
                i = iter(args)
                for k, v in zip(i, i):
                    setattr(self, k, v)
                return
            # If args[0] is not mapping type, then this method
            # will not fail as it should. The problem is that you
            # can't test for a mapping type. Sequences implement all
            # the same functions, just that they don't return the keys
            # for iterators but the values, which is why ['a'] will
            # fail as an initializer.
        for k in kwargs:
            setattr(self, k, kwargs[k])

    __hash__ = None

    def __contains__(self, key):
        return key in self.__order

    def __delattr__(self, name):
        super(OrderedMapping, self).__delattr__(name)
        self.__order.remove(name)

    def __delitem__(self, key):
        try:
            delattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def __eq__(self, other):
        """Type of object, and order of keys and values must be the same"""
        if not type(self) == type(other):
            return False
        # Types must be the same. "__order" is included in vars()
        # so verifies order, too.
        return vars(self) == vars(other)

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def __iter__(self):
        return iter(self.__order)

    def __len__(self):
        return len(self.__order)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        res = type(self).__name__ + '('
        if not len(self):
            return res + ')'
        for name in self:
            res += '{!s}={!r}, '.format(name, getattr(self, name))
        return res[:-2] + ')'

    def __setattr__(self, name, value):
        super(OrderedMapping, self).__setattr__(name, value)
        if name not in self.__order:
            self.__order.append(name)

    def __setitem__(self, key, value):
        setattr(self, key, value)
