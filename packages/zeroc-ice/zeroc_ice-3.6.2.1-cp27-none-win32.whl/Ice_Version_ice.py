# -*- coding: utf-8 -*-
# **********************************************************************
#
# Copyright (c) 2003-2016 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************
#
# Ice version 3.6.2
#
# <auto-generated>
#
# Generated from file `Version.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

import Ice, IcePy

# Start of module Ice
_M_Ice = Ice.openModule('Ice')
__name__ = 'Ice'

if 'ProtocolVersion' not in _M_Ice.__dict__:
    _M_Ice.ProtocolVersion = Ice.createTempClass()
    class ProtocolVersion(object):
        """A version structure for the protocol version."""
        def __init__(self, major=0, minor=0):
            self.major = major
            self.minor = minor

        def __hash__(self):
            _h = 0
            _h = 5 * _h + Ice.getHash(self.major)
            _h = 5 * _h + Ice.getHash(self.minor)
            return _h % 0x7fffffff

        def __compare(self, other):
            if other is None:
                return 1
            elif not isinstance(other, _M_Ice.ProtocolVersion):
                return NotImplemented
            else:
                if self.major is None or other.major is None:
                    if self.major != other.major:
                        return (-1 if self.major is None else 1)
                else:
                    if self.major < other.major:
                        return -1
                    elif self.major > other.major:
                        return 1
                if self.minor is None or other.minor is None:
                    if self.minor != other.minor:
                        return (-1 if self.minor is None else 1)
                else:
                    if self.minor < other.minor:
                        return -1
                    elif self.minor > other.minor:
                        return 1
                return 0

        def __lt__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r < 0

        def __le__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r <= 0

        def __gt__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r > 0

        def __ge__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r >= 0

        def __eq__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r == 0

        def __ne__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r != 0

        def __str__(self):
            return IcePy.stringify(self, _M_Ice._t_ProtocolVersion)

        __repr__ = __str__

    _M_Ice._t_ProtocolVersion = IcePy.defineStruct('::Ice::ProtocolVersion', ProtocolVersion, (), (
        ('major', (), IcePy._t_byte),
        ('minor', (), IcePy._t_byte)
    ))

    _M_Ice.ProtocolVersion = ProtocolVersion
    del ProtocolVersion

if 'EncodingVersion' not in _M_Ice.__dict__:
    _M_Ice.EncodingVersion = Ice.createTempClass()
    class EncodingVersion(object):
        """A version structure for the encoding version."""
        def __init__(self, major=0, minor=0):
            self.major = major
            self.minor = minor

        def __hash__(self):
            _h = 0
            _h = 5 * _h + Ice.getHash(self.major)
            _h = 5 * _h + Ice.getHash(self.minor)
            return _h % 0x7fffffff

        def __compare(self, other):
            if other is None:
                return 1
            elif not isinstance(other, _M_Ice.EncodingVersion):
                return NotImplemented
            else:
                if self.major is None or other.major is None:
                    if self.major != other.major:
                        return (-1 if self.major is None else 1)
                else:
                    if self.major < other.major:
                        return -1
                    elif self.major > other.major:
                        return 1
                if self.minor is None or other.minor is None:
                    if self.minor != other.minor:
                        return (-1 if self.minor is None else 1)
                else:
                    if self.minor < other.minor:
                        return -1
                    elif self.minor > other.minor:
                        return 1
                return 0

        def __lt__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r < 0

        def __le__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r <= 0

        def __gt__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r > 0

        def __ge__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r >= 0

        def __eq__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r == 0

        def __ne__(self, other):
            r = self.__compare(other)
            if r is NotImplemented:
                return r
            else:
                return r != 0

        def __str__(self):
            return IcePy.stringify(self, _M_Ice._t_EncodingVersion)

        __repr__ = __str__

    _M_Ice._t_EncodingVersion = IcePy.defineStruct('::Ice::EncodingVersion', EncodingVersion, (), (
        ('major', (), IcePy._t_byte),
        ('minor', (), IcePy._t_byte)
    ))

    _M_Ice.EncodingVersion = EncodingVersion
    del EncodingVersion

# End of module Ice
