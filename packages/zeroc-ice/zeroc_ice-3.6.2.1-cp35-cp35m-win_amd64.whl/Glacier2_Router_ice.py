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
# Generated from file `Router.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

import Ice, IcePy
import Ice_Router_ice
import Glacier2_Session_ice
import Glacier2_PermissionsVerifier_ice

# Included module Ice
_M_Ice = Ice.openModule('Ice')

# Included module Glacier2
_M_Glacier2 = Ice.openModule('Glacier2')

# Start of module Glacier2
__name__ = 'Glacier2'
_M_Glacier2.__doc__ = """Glacier2 is a firewall solution for Ice. Glacier2 authenticates
and filters client requests and allows callbacks to the client in a
secure fashion. In combination with IceSSL, Glacier2 provides a
security solution that is both non-intrusive and easy to configure."""

if 'SessionNotExistException' not in _M_Glacier2.__dict__:
    _M_Glacier2.SessionNotExistException = Ice.createTempClass()
    class SessionNotExistException(Ice.UserException):
        """This exception is raised if a client tries to destroy a session
        with a router, but no session exists for the client."""
        def __init__(self):
            pass

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

        _ice_name = 'Glacier2::SessionNotExistException'

    _M_Glacier2._t_SessionNotExistException = IcePy.defineException('::Glacier2::SessionNotExistException', SessionNotExistException, (), False, None, ())
    SessionNotExistException._ice_type = _M_Glacier2._t_SessionNotExistException

    _M_Glacier2.SessionNotExistException = SessionNotExistException
    del SessionNotExistException

if 'Router' not in _M_Glacier2.__dict__:
    _M_Glacier2.Router = Ice.createTempClass()
    class Router(_M_Ice.Router):
        """The Glacier2 specialization of the Ice.Router
        interface."""
        def __init__(self):
            if Ice.getType(self) == _M_Glacier2.Router:
                raise RuntimeError('Glacier2.Router is an abstract class')

        def ice_ids(self, current=None):
            return ('::Glacier2::Router', '::Ice::Object', '::Ice::Router')

        def ice_id(self, current=None):
            return '::Glacier2::Router'

        def ice_staticId():
            return '::Glacier2::Router'
        ice_staticId = staticmethod(ice_staticId)

        def getCategoryForClient(self, current=None):
            """This category must be used in the identities of all of the client's
            callback objects. This is necessary in order for the router to
            forward callback requests to the intended client. If the Glacier2
            server endpoints are not set, the returned category is an empty
            string.
            Arguments:
            current -- The Current object for the invocation.
            Returns: The category."""
            pass

        def createSession_async(self, _cb, userId, password, current=None):
            """Create a per-client session with the router. If a
            SessionManager has been installed, a proxy to a Session
            object is returned to the client. Otherwise, null is returned
            and only an internal session (i.e., not visible to the client)
            is created.
            If a session proxy is returned, it must be configured to route
            through the router that created it. This will happen automatically
            if the router is configured as the client's default router at the
            time the session proxy is created in the client process, otherwise
            the client must configure the session proxy explicitly.
            Arguments:
            _cb -- The asynchronous callback object.
            userId -- The user id for which to check the password.
            password -- The password for the given user id.
            current -- The Current object for the invocation.
            Throws:
            CannotCreateSessionException -- Raised if the session cannot be created.
            PermissionDeniedException -- Raised if the password for the given user id is not correct, or if the user is not allowed access."""
            pass

        def createSessionFromSecureConnection_async(self, _cb, current=None):
            """Create a per-client session with the router. The user is
            authenticated through the SSL certificates that have been
            associated with the connection. If a SessionManager has been
            installed, a proxy to a Session object is returned to the
            client. Otherwise, null is returned and only an internal
            session (i.e., not visible to the client) is created.
            If a session proxy is returned, it must be configured to route
            through the router that created it. This will happen automatically
            if the router is configured as the client's default router at the
            time the session proxy is created in the client process, otherwise
            the client must configure the session proxy explicitly.
            Arguments:
            _cb -- The asynchronous callback object.
            current -- The Current object for the invocation.
            Throws:
            CannotCreateSessionException -- Raised if the session cannot be created.
            PermissionDeniedException -- Raised if the user cannot be authenticated or if the user is not allowed access."""
            pass

        def refreshSession_async(self, _cb, current=None):
            """Keep the calling client's session with this router alive.
            Arguments:
            _cb -- The asynchronous callback object.
            current -- The Current object for the invocation.
            Throws:
            SessionNotExistException -- Raised if no session exists for the calling client."""
            pass

        def destroySession(self, current=None):
            """Destroy the calling client's session with this router.
            Arguments:
            current -- The Current object for the invocation.
            Throws:
            SessionNotExistException -- Raised if no session exists for the calling client."""
            pass

        def getSessionTimeout(self, current=None):
            """Get the value of the session timeout. Sessions are destroyed
            if they see no activity for this period of time.
            Arguments:
            current -- The Current object for the invocation.
            Returns: The timeout (in seconds)."""
            pass

        def getACMTimeout(self, current=None):
            """Get the value of the ACM timeout. Clients supporting connection
            heartbeats can enable them instead of explicitly sending keep
            alives requests.
            NOTE: This method is only available since Ice 3.6.
            Arguments:
            current -- The Current object for the invocation.
            Returns: The timeout (in seconds)."""
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Glacier2._t_Router)

        __repr__ = __str__

    _M_Glacier2.RouterPrx = Ice.createTempClass()
    class RouterPrx(_M_Ice.RouterPrx):

        """This category must be used in the identities of all of the client's
        callback objects. This is necessary in order for the router to
        forward callback requests to the intended client. If the Glacier2
        server endpoints are not set, the returned category is an empty
        string.
        Arguments:
        _ctx -- The request context for the invocation.
        Returns: The category."""
        def getCategoryForClient(self, _ctx=None):
            return _M_Glacier2.Router._op_getCategoryForClient.invoke(self, ((), _ctx))

        """This category must be used in the identities of all of the client's
        callback objects. This is necessary in order for the router to
        forward callback requests to the intended client. If the Glacier2
        server endpoints are not set, the returned category is an empty
        string.
        Arguments:
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation."""
        def begin_getCategoryForClient(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_Glacier2.Router._op_getCategoryForClient.begin(self, ((), _response, _ex, _sent, _ctx))

        """This category must be used in the identities of all of the client's
        callback objects. This is necessary in order for the router to
        forward callback requests to the intended client. If the Glacier2
        server endpoints are not set, the returned category is an empty
        string.
        Arguments:
        Returns: The category."""
        def end_getCategoryForClient(self, _r):
            return _M_Glacier2.Router._op_getCategoryForClient.end(self, _r)

        """Create a per-client session with the router. If a
        SessionManager has been installed, a proxy to a Session
        object is returned to the client. Otherwise, null is returned
        and only an internal session (i.e., not visible to the client)
        is created.
        If a session proxy is returned, it must be configured to route
        through the router that created it. This will happen automatically
        if the router is configured as the client's default router at the
        time the session proxy is created in the client process, otherwise
        the client must configure the session proxy explicitly.
        Arguments:
        userId -- The user id for which to check the password.
        password -- The password for the given user id.
        _ctx -- The request context for the invocation.
        Returns: A proxy for the newly created session, or null if no SessionManager has been installed.
        Throws:
        CannotCreateSessionException -- Raised if the session cannot be created.
        PermissionDeniedException -- Raised if the password for the given user id is not correct, or if the user is not allowed access."""
        def createSession(self, userId, password, _ctx=None):
            return _M_Glacier2.Router._op_createSession.invoke(self, ((userId, password), _ctx))

        """Create a per-client session with the router. If a
        SessionManager has been installed, a proxy to a Session
        object is returned to the client. Otherwise, null is returned
        and only an internal session (i.e., not visible to the client)
        is created.
        If a session proxy is returned, it must be configured to route
        through the router that created it. This will happen automatically
        if the router is configured as the client's default router at the
        time the session proxy is created in the client process, otherwise
        the client must configure the session proxy explicitly.
        Arguments:
        userId -- The user id for which to check the password.
        password -- The password for the given user id.
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation."""
        def begin_createSession(self, userId, password, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_Glacier2.Router._op_createSession.begin(self, ((userId, password), _response, _ex, _sent, _ctx))

        """Create a per-client session with the router. If a
        SessionManager has been installed, a proxy to a Session
        object is returned to the client. Otherwise, null is returned
        and only an internal session (i.e., not visible to the client)
        is created.
        If a session proxy is returned, it must be configured to route
        through the router that created it. This will happen automatically
        if the router is configured as the client's default router at the
        time the session proxy is created in the client process, otherwise
        the client must configure the session proxy explicitly.
        Arguments:
        userId -- The user id for which to check the password.
        password -- The password for the given user id.
        Returns: A proxy for the newly created session, or null if no SessionManager has been installed.
        Throws:
        CannotCreateSessionException -- Raised if the session cannot be created.
        PermissionDeniedException -- Raised if the password for the given user id is not correct, or if the user is not allowed access."""
        def end_createSession(self, _r):
            return _M_Glacier2.Router._op_createSession.end(self, _r)

        """Create a per-client session with the router. The user is
        authenticated through the SSL certificates that have been
        associated with the connection. If a SessionManager has been
        installed, a proxy to a Session object is returned to the
        client. Otherwise, null is returned and only an internal
        session (i.e., not visible to the client) is created.
        If a session proxy is returned, it must be configured to route
        through the router that created it. This will happen automatically
        if the router is configured as the client's default router at the
        time the session proxy is created in the client process, otherwise
        the client must configure the session proxy explicitly.
        Arguments:
        _ctx -- The request context for the invocation.
        Returns: A proxy for the newly created session, or null if no SessionManager has been installed.
        Throws:
        CannotCreateSessionException -- Raised if the session cannot be created.
        PermissionDeniedException -- Raised if the user cannot be authenticated or if the user is not allowed access."""
        def createSessionFromSecureConnection(self, _ctx=None):
            return _M_Glacier2.Router._op_createSessionFromSecureConnection.invoke(self, ((), _ctx))

        """Create a per-client session with the router. The user is
        authenticated through the SSL certificates that have been
        associated with the connection. If a SessionManager has been
        installed, a proxy to a Session object is returned to the
        client. Otherwise, null is returned and only an internal
        session (i.e., not visible to the client) is created.
        If a session proxy is returned, it must be configured to route
        through the router that created it. This will happen automatically
        if the router is configured as the client's default router at the
        time the session proxy is created in the client process, otherwise
        the client must configure the session proxy explicitly.
        Arguments:
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation."""
        def begin_createSessionFromSecureConnection(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_Glacier2.Router._op_createSessionFromSecureConnection.begin(self, ((), _response, _ex, _sent, _ctx))

        """Create a per-client session with the router. The user is
        authenticated through the SSL certificates that have been
        associated with the connection. If a SessionManager has been
        installed, a proxy to a Session object is returned to the
        client. Otherwise, null is returned and only an internal
        session (i.e., not visible to the client) is created.
        If a session proxy is returned, it must be configured to route
        through the router that created it. This will happen automatically
        if the router is configured as the client's default router at the
        time the session proxy is created in the client process, otherwise
        the client must configure the session proxy explicitly.
        Arguments:
        Returns: A proxy for the newly created session, or null if no SessionManager has been installed.
        Throws:
        CannotCreateSessionException -- Raised if the session cannot be created.
        PermissionDeniedException -- Raised if the user cannot be authenticated or if the user is not allowed access."""
        def end_createSessionFromSecureConnection(self, _r):
            return _M_Glacier2.Router._op_createSessionFromSecureConnection.end(self, _r)

        """Keep the calling client's session with this router alive.
        Arguments:
        _ctx -- The request context for the invocation.
        Throws:
        SessionNotExistException -- Raised if no session exists for the calling client."""
        def refreshSession(self, _ctx=None):
            return _M_Glacier2.Router._op_refreshSession.invoke(self, ((), _ctx))

        """Keep the calling client's session with this router alive.
        Arguments:
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation."""
        def begin_refreshSession(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_Glacier2.Router._op_refreshSession.begin(self, ((), _response, _ex, _sent, _ctx))

        """Keep the calling client's session with this router alive.
        Arguments:
        Throws:
        SessionNotExistException -- Raised if no session exists for the calling client."""
        def end_refreshSession(self, _r):
            return _M_Glacier2.Router._op_refreshSession.end(self, _r)

        """Destroy the calling client's session with this router.
        Arguments:
        _ctx -- The request context for the invocation.
        Throws:
        SessionNotExistException -- Raised if no session exists for the calling client."""
        def destroySession(self, _ctx=None):
            return _M_Glacier2.Router._op_destroySession.invoke(self, ((), _ctx))

        """Destroy the calling client's session with this router.
        Arguments:
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation."""
        def begin_destroySession(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_Glacier2.Router._op_destroySession.begin(self, ((), _response, _ex, _sent, _ctx))

        """Destroy the calling client's session with this router.
        Arguments:
        Throws:
        SessionNotExistException -- Raised if no session exists for the calling client."""
        def end_destroySession(self, _r):
            return _M_Glacier2.Router._op_destroySession.end(self, _r)

        """Get the value of the session timeout. Sessions are destroyed
        if they see no activity for this period of time.
        Arguments:
        _ctx -- The request context for the invocation.
        Returns: The timeout (in seconds)."""
        def getSessionTimeout(self, _ctx=None):
            return _M_Glacier2.Router._op_getSessionTimeout.invoke(self, ((), _ctx))

        """Get the value of the session timeout. Sessions are destroyed
        if they see no activity for this period of time.
        Arguments:
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation."""
        def begin_getSessionTimeout(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_Glacier2.Router._op_getSessionTimeout.begin(self, ((), _response, _ex, _sent, _ctx))

        """Get the value of the session timeout. Sessions are destroyed
        if they see no activity for this period of time.
        Arguments:
        Returns: The timeout (in seconds)."""
        def end_getSessionTimeout(self, _r):
            return _M_Glacier2.Router._op_getSessionTimeout.end(self, _r)

        """Get the value of the ACM timeout. Clients supporting connection
        heartbeats can enable them instead of explicitly sending keep
        alives requests.
        NOTE: This method is only available since Ice 3.6.
        Arguments:
        _ctx -- The request context for the invocation.
        Returns: The timeout (in seconds)."""
        def getACMTimeout(self, _ctx=None):
            return _M_Glacier2.Router._op_getACMTimeout.invoke(self, ((), _ctx))

        """Get the value of the ACM timeout. Clients supporting connection
        heartbeats can enable them instead of explicitly sending keep
        alives requests.
        NOTE: This method is only available since Ice 3.6.
        Arguments:
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation."""
        def begin_getACMTimeout(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_Glacier2.Router._op_getACMTimeout.begin(self, ((), _response, _ex, _sent, _ctx))

        """Get the value of the ACM timeout. Clients supporting connection
        heartbeats can enable them instead of explicitly sending keep
        alives requests.
        NOTE: This method is only available since Ice 3.6.
        Arguments:
        Returns: The timeout (in seconds)."""
        def end_getACMTimeout(self, _r):
            return _M_Glacier2.Router._op_getACMTimeout.end(self, _r)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Glacier2.RouterPrx.ice_checkedCast(proxy, '::Glacier2::Router', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_Glacier2.RouterPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

        def ice_staticId():
            return '::Glacier2::Router'
        ice_staticId = staticmethod(ice_staticId)

    _M_Glacier2._t_RouterPrx = IcePy.defineProxy('::Glacier2::Router', RouterPrx)

    _M_Glacier2._t_Router = IcePy.defineClass('::Glacier2::Router', Router, -1, (), True, False, None, (_M_Ice._t_Router,), ())
    Router._ice_type = _M_Glacier2._t_Router

    Router._op_getCategoryForClient = IcePy.Operation('getCategoryForClient', Ice.OperationMode.Idempotent, Ice.OperationMode.Nonmutating, False, None, (), (), (), ((), IcePy._t_string, False, 0), ())
    Router._op_createSession = IcePy.Operation('createSession', Ice.OperationMode.Normal, Ice.OperationMode.Normal, True, Ice.FormatType.SlicedFormat, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0)), (), ((), _M_Glacier2._t_SessionPrx, False, 0), (_M_Glacier2._t_PermissionDeniedException, _M_Glacier2._t_CannotCreateSessionException))
    Router._op_createSessionFromSecureConnection = IcePy.Operation('createSessionFromSecureConnection', Ice.OperationMode.Normal, Ice.OperationMode.Normal, True, Ice.FormatType.SlicedFormat, (), (), (), ((), _M_Glacier2._t_SessionPrx, False, 0), (_M_Glacier2._t_PermissionDeniedException, _M_Glacier2._t_CannotCreateSessionException))
    Router._op_refreshSession = IcePy.Operation('refreshSession', Ice.OperationMode.Normal, Ice.OperationMode.Normal, True, None, (), (), (), None, (_M_Glacier2._t_SessionNotExistException,))
    Router._op_destroySession = IcePy.Operation('destroySession', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), None, (_M_Glacier2._t_SessionNotExistException,))
    Router._op_getSessionTimeout = IcePy.Operation('getSessionTimeout', Ice.OperationMode.Idempotent, Ice.OperationMode.Nonmutating, False, None, (), (), (), ((), IcePy._t_long, False, 0), ())
    Router._op_getACMTimeout = IcePy.Operation('getACMTimeout', Ice.OperationMode.Idempotent, Ice.OperationMode.Nonmutating, False, None, (), (), (), ((), IcePy._t_int, False, 0), ())

    _M_Glacier2.Router = Router
    del Router

    _M_Glacier2.RouterPrx = RouterPrx
    del RouterPrx

# End of module Glacier2

Ice.sliceChecksums["::Glacier2::Router"] = "dfe8817f11292a5582437c19a65b63"
Ice.sliceChecksums["::Glacier2::SessionNotExistException"] = "9b3392dc48a63f86d96c13662972328"
