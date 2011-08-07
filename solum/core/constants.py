#!/usr/bin/env python
# -*- coding: utf8 -*-
__all__ = ['ConstantError']

import struct
from functools import partial


class ConstantError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class Constant(object):
    @staticmethod
    def read(r):
        """Reads the packed representation of a Cosntant."""
        raise NotImplementedError()

    @staticmethod
    def write(w):
        """Saves the packed representation of a Constant."""
        raise NotImplementedError()

    def __str__(self):
        """Retuns a human-readable representation of this Constant."""
        raise NotImplementedError()

    def resolve_index(self, pool):
        """Used to resolve indexes when reading from a file."""
        raise NotImplementedError()

    @property
    def tag(self):
        raise NotImplementedError()


class ConstantClass(Constant):
    def __init__(self, name_index=None):
        self.name_index = name_index
        self.name = None 

    @staticmethod
    def read(r):
        t = ConstantClass(*r('>H'))
        return t

    def __str__(self):
        return 'ConstantClass(name=%s)' % self.name

    def resolve_index(self, pool):
        self.name = pool[self.name_index]

    @property
    def tag(self):
        return 7


class ConstantField(Constant):
    def __init__(self, class_index=None, name_type_index=None):
        self.class_index = class_index
        self.name_and_type_index = name_type_index
        self.class_ = None
        self.name_and_type = None

    @staticmethod
    def read(r):
        t = ConstantField(*r('>HH'))
        return t

    def __str__(self):
        return 'ConstantField(class_=%s, name_and_type=%s)' % (
            self.class_, self.name_and_type)

    def resolve_index(self, pool):
        self.class_ = pool[self.class_index]
        self.name_and_type = pool[self.name_and_type_index]

    @property
    def tag(self):
        return 9


class ConstantMethod(Constant):
    def __init__(self, class_index=None, name_type_index=None):
        self.class_index = class_index
        self.name_and_type_index = name_type_index
        self.class_ = None
        self.name_and_type = None

    @staticmethod
    def read(r):
        t = ConstantMethod(*r('>HH'))
        return t

    def __str__(self):
        return 'ConstantMethod(class_=%s, name_and_type=%s)' % (
            self.class_, self.name_and_type)

    def resolve_index(self, pool):
        self.class_ = pool[self.class_index]
        self.name_and_type = pool[self.name_and_type_index]

    @property
    def tag(self):
        return 10


class ConstantIMethod(Constant):
    def __init__(self, class_index=None, name_type_index=None):
        self.class_index = class_index
        self.name_and_type_index = name_type_index
        self.class_ = None
        self.name_and_type = None

    @staticmethod
    def read(r):
        t = ConstantIMethod(*r('>HH'))
        return t

    def __str__(self):
        return 'ConstantIMethod(class_=%s, name_and_type=%s)' % (
            self.class_, self.name_and_type)

    def resolve_index(self, pool):
        self.class_ = pool[self.class_index]
        self.name_and_type = pool[self.name_and_type_index]

    @property
    def tag(self):
        return 11


class ConstantString(Constant):
    def __init__(self, string_index=None):
        self.string_index = string_index
        self.string = None

    @staticmethod
    def read(r):
        t = ConstantString(*r('>H'))
        return t

    def __str__(self):
        return 'ConstantString(string=%s)' % self.string

    def resolve_index(self, pool):
        self.string = pool[self.string_index]

    @property
    def tag(self):
        return 8


class ConstantInteger(Constant):
    def __init__(self, value=None):
        self.value = value

    @staticmethod
    def read(r):
        t = ConstantInteger(*r('>i'))
        return t

    def __str__(self):
        return 'ConstantInteger(value=%r)' % self.value

    def resolve_index(self, pool):
        pass

    @property
    def tag(self):
        return 3


class ConstantFloat(Constant):
    def __init__(self, value=None):
        self.value = value

    @staticmethod
    def read(r):
        t = ConstantFloat(*r('>f'))
        return t

    def __str__(self):
        return 'ConstantFloat(value=%r)' % self.value

    def resolve_index(self, pool):
        pass

    @property
    def tag(self):
        return 4


class ConstantLong(Constant):
    def __init__(self, value=None):
        self.value = value

    @staticmethod
    def read(r):
        t = ConstantLong(*r('>q'))
        return t

    def __str__(self):
        return 'ConstantLong(value=%r)' % self.value

    def resolve_index(self, pool):
        pass

    @property
    def tag(self):
        return 5


class ConstantDouble(Constant):
    def __init__(self, value=None):
        self.value = value

    @staticmethod
    def read(r):
        t = ConstantDouble(*r('>d'))
        return t

    def __str__(self):
        return 'ConstantDouble(value=%r)' % self.value

    def resolve_index(self, pool):
        pass

    @property
    def tag(self):
        return 6


class ConstantNameAndType(Constant):
    def __init__(self, name_index=None, descriptor_index=None):
        self.name_index = name_index
        self.descriptor_index = descriptor_index
        self.name = None
        self.descriptor = None

    @staticmethod
    def read(r):
        t = ConstantNameAndType(*r('>HH'))
        return t

    def __str__(self):
        return 'ConstantNameAndType(name=%s, descriptor=%s)' % (
            self.name, self.descriptor)

    def resolve_index(self, pool):
        self.name = pool[self.name_index]
        self.descriptor = pool[self.descriptor_index]

    @property
    def tag(self):
        return 12


class ConstantUTF8(Constant):
    def __init__(self, value=None):
        self.value = value

    @staticmethod
    def read(r):
        size, = r('>H')
        t = ConstantUTF8(*r('>%ss' % size))
        return t

    def __str__(self):
        return 'ConstantUTF8(value=%r)' % self.value

    def resolve_index(self, pool):
        pass

    @property
    def tag(self):
        return 1


class ConstantPool(object):
    def __init__(self):
        self._storage = []
        self._index_map = {}

    def add_constant(self, constant, index=None):
        self._storage.append(constant)
        if index is not None:
            self._index_map[index] = constant

    def __getitem__(self, index):
        return self._index_map[index]

    def find(self, tag=None, f=None):
        if not tag and not f:
            return self._storage

        tmp = []
        for const in self._storage:
            if tag is not None and const.tag != tag:
                continue

            if f is not None and not f(const):
                continue

            tmp.append(const)

        return tmp

    def find_one(self, tag=None, f=None):
        if not self._storage:
            return None
        elif not tag and not f:
            return self._storage[0]
        
        for const in self._storage:
            if tag and const.tag != tag:
                continue
            elif f and not f(const):
                continue
            else:
                return const

    @staticmethod
    def _read(fmt, stream):
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, stream.read(size))

    @staticmethod
    def read(stream):
        pool = ConstantPool()
        r = partial(ConstantPool._read, stream=stream)

        # Size is 1-based, and counts LONG and DOUBLE
        # constants as two entries (for legacy reasons).
        size, = r('>H')
        x = 1

        while x < size:
            tag, = r('>B')

            pool.add_constant({
                7: ConstantClass,
                9: ConstantField,
                10: ConstantMethod,
                11: ConstantIMethod,
                8: ConstantString,
                3: ConstantInteger,
                4: ConstantFloat,
                5: ConstantLong,
                6: ConstantDouble,
                12: ConstantNameAndType,
                1: ConstantUTF8
            }[tag].read(r), x)

            x += 2 if tag in (5, 6) else 1

        for const in pool.find():
            const.resolve_index(pool)

        return pool
