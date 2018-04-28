# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import random


def test(a, b=2, *c, **ff):
    print a
    print b

    print c
    print ff
    test1(c)
    test1(*c)


def test1(*d):
    print(len(d))
    print d

test(1, 2, 3, 4, 5, d=3, e=4)


a = {
    1: 'a',
    2: 'b'
}


print(u'🍑')


print random.sample('abcdef', 4)

s = "asbcd"
print list(s)
