#!/usr/bin/env python
# -*- coding: utf8 -*-
__all__ = ['JarFile', 'JarError']

import zipfile

from .manifest import ManifestFile


class JarError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class JarFile(object):
    def __init__(self, source=None):
        self._files = {}

        if source and zipfile.is_zipfile(source):
            source_ = zipfile.ZipFile(source, 'r')
            # TODO: Can we creatively patch ZipFile to allow us to
            # safely pass ZipInfo on Python < 2.6?
            for zi in source_.infolist():
                self._files[zi.filename] = source_.read(zi.filename)
            source_.close()
        elif source:
            raise JarError('source is not a valid zip file')

        self._manifest = ManifestFile(
            self._files.pop('META-INF/MANIFEST.MF', None)
        )

    def save(self, output):
        if not self._files:
            # Trying to write empty ZIPs with ZipFile will produce
            # invalid archives (missing central directory).
            raise JarError('cannot save an empty JAR')

        out = zipfile.ZipFile(output, 'w')

        # Make sure the manifest (if it exists) is the first record
        # in the JAR for legacy reasons.
        out.writestr('META-INF/MANIFEST.MF', self.manifest.build())
        for filename, filedata in self._files.iteritems():
            out.writestr(filename, filedata)
        out.close()

    @property
    def manifest(self):
        return self._manifest
