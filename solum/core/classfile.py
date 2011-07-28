#!/usr/bin/env python
# -*- coding: utf8 -*-
__all__ = ['ClassFile', 'ClassError']

import struct


class ClassError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class ClassFile(object):
    def __init__(self, source=None):
        we_opened = False
        if source and isinstance(source, basestring):
            we_opened = True
            sin = open(source, 'rb')
        else:
            sin = source

        def read(fmt):
            return struct.unpack(fmt, sin.read(struct.calcsize(fmt)))

        magic_number, = read(">I")
        if magic_number != 0xCAFEBABE:
            raise ClassError('not a valid classfile')

        ver_min, ver_maj = read(">HH")
        self._version = (ver_maj, ver_min)

        if we_opened:
            sin.close()

    @staticmethod
    def is_classfile(source):
        """
        Returns `True` if `source` is a valid ClassFile, False otherwise.
        If the source does not exist, an exception will be raised.
        """
        we_opened = False
        if source and isinstance(source, basestring):
            we_opened = True
            sin = open(source, 'rb')
        else:
            sin = source

        magic, = struct.unpack('>I', sin.read(4))
        if we_opened:
            sin.close()

        if magic == 0xCAFEBABE:
            return True
        else:
            return False

    @property
    def version(self):
        """Returns a tuple of (major_version, minor_version)."""
        return self._version

    @property
    def version_string(self):
        """
        Returns a human-readable string representing the version of Java used
        to construct this ClassFile.
        """
        return {
            0x2D: "JDK 1.1",
            0x2E: "JDK 1.2",
            0x2F: "JDK 1.3",
            0x30: "JDK 1.4",
            0x31: "J2SE 5.0",
            0x32: "J2SE 6.0"
        }.get(self.version[0], "unknown")
