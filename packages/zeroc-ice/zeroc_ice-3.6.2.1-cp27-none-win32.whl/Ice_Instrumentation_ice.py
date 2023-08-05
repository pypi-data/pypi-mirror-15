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
# Generated from file `Instrumentation.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

import Ice, IcePy
import Ice_EndpointF_ice
import Ice_ConnectionF_ice
import Ice_Current_ice

# Included module Ice
_M_Ice = Ice.openModule('Ice')

# Start of module Ice
__name__ = 'Ice'

# Start of module Ice.Instrumentation
_M_Ice.Instrumentation = Ice.openModule('Ice.Instrumentation')
__name__ = 'Ice.Instrumentation'
_M_Ice.Instrumentation.__doc__ = """The Instrumentation local interfaces enable observing a number of
Ice core internal components (threads, connections, etc)."""

if 'Observer' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.Observer = Ice.createTempClass()
    class Observer(object):
        """The object observer interface used by instrumented objects to
        notify the observer of their existence."""
        def __init__(self):
            if Ice.getType(self) == _M_Ice.Instrumentation.Observer:
                raise RuntimeError('Ice.Instrumentation.Observer is an abstract class')

        def attach(self):
            """This method is called when the instrumented object is created
            or when the observer is attached to an existing object."""
            pass

        def detach(self):
            """This method is called when the instrumented object is destroyed
            and as a result the observer detached from the object."""
            pass

        def failed(self, exceptionName):
            """Notification of a failure.
            Arguments:
            exceptionName -- The name of the exception."""
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Ice.Instrumentation._t_Observer)

        __repr__ = __str__

    _M_Ice.Instrumentation._t_Observer = IcePy.defineClass('::Ice::Instrumentation::Observer', Observer, -1, (), True, False, None, (), ())
    Observer._ice_type = _M_Ice.Instrumentation._t_Observer

    _M_Ice.Instrumentation.Observer = Observer
    del Observer

if 'ThreadState' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.ThreadState = Ice.createTempClass()
    class ThreadState(Ice.EnumBase):
        """The thread state enumeration keeps track of the different possible
        states of Ice threads.
        Enumerators:
        ThreadStateIdle -- The thread is idle.
        ThreadStateInUseForIO -- The thread is in use performing reads or writes for Ice
        connections. This state is only for threads from an Ice thread
        pool.
        ThreadStateInUseForUser -- The thread is calling user code (servant implementation, AMI
        callbacks). This state is only for threads from an Ice thread
        pool.
        ThreadStateInUseForOther -- The thread is performing other internal activities (DNS
        lookups, timer callbacks, etc)."""

        def __init__(self, _n, _v):
            Ice.EnumBase.__init__(self, _n, _v)

        def valueOf(self, _n):
            if _n in self._enumerators:
                return self._enumerators[_n]
            return None
        valueOf = classmethod(valueOf)

    ThreadState.ThreadStateIdle = ThreadState("ThreadStateIdle", 0)
    ThreadState.ThreadStateInUseForIO = ThreadState("ThreadStateInUseForIO", 1)
    ThreadState.ThreadStateInUseForUser = ThreadState("ThreadStateInUseForUser", 2)
    ThreadState.ThreadStateInUseForOther = ThreadState("ThreadStateInUseForOther", 3)
    ThreadState._enumerators = { 0:ThreadState.ThreadStateIdle, 1:ThreadState.ThreadStateInUseForIO, 2:ThreadState.ThreadStateInUseForUser, 3:ThreadState.ThreadStateInUseForOther }

    _M_Ice.Instrumentation._t_ThreadState = IcePy.defineEnum('::Ice::Instrumentation::ThreadState', ThreadState, (), ThreadState._enumerators)

    _M_Ice.Instrumentation.ThreadState = ThreadState
    del ThreadState

if 'ThreadObserver' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.ThreadObserver = Ice.createTempClass()
    class ThreadObserver(_M_Ice.Instrumentation.Observer):
        """The thread observer interface to instrument Ice threads. This can
        be threads from the Ice thread pool or utility threads used by the
        Ice core."""
        def __init__(self):
            if Ice.getType(self) == _M_Ice.Instrumentation.ThreadObserver:
                raise RuntimeError('Ice.Instrumentation.ThreadObserver is an abstract class')

        def stateChanged(self, oldState, newState):
            """Notification of thread state change.
            Arguments:
            oldState -- The previous thread state.
            newState -- The new thread state."""
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Ice.Instrumentation._t_ThreadObserver)

        __repr__ = __str__

    _M_Ice.Instrumentation._t_ThreadObserver = IcePy.defineClass('::Ice::Instrumentation::ThreadObserver', ThreadObserver, -1, (), True, False, None, (_M_Ice.Instrumentation._t_Observer,), ())
    ThreadObserver._ice_type = _M_Ice.Instrumentation._t_ThreadObserver

    _M_Ice.Instrumentation.ThreadObserver = ThreadObserver
    del ThreadObserver

if 'ConnectionState' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.ConnectionState = Ice.createTempClass()
    class ConnectionState(Ice.EnumBase):
        """The state of an Ice connection.
        Enumerators:
        ConnectionStateValidating -- The connection is being validated.
        ConnectionStateHolding -- The connection is holding the reception of new messages.
        ConnectionStateActive -- The connection is active and can send and receive messages.
        ConnectionStateClosing -- The connection is being gracefully shutdown and waits for the
        peer to close its end of the connection.
        ConnectionStateClosed -- The connection is closed and waits for potential dispatch to be
        finished before being destroyed and detached from the observer."""

        def __init__(self, _n, _v):
            Ice.EnumBase.__init__(self, _n, _v)

        def valueOf(self, _n):
            if _n in self._enumerators:
                return self._enumerators[_n]
            return None
        valueOf = classmethod(valueOf)

    ConnectionState.ConnectionStateValidating = ConnectionState("ConnectionStateValidating", 0)
    ConnectionState.ConnectionStateHolding = ConnectionState("ConnectionStateHolding", 1)
    ConnectionState.ConnectionStateActive = ConnectionState("ConnectionStateActive", 2)
    ConnectionState.ConnectionStateClosing = ConnectionState("ConnectionStateClosing", 3)
    ConnectionState.ConnectionStateClosed = ConnectionState("ConnectionStateClosed", 4)
    ConnectionState._enumerators = { 0:ConnectionState.ConnectionStateValidating, 1:ConnectionState.ConnectionStateHolding, 2:ConnectionState.ConnectionStateActive, 3:ConnectionState.ConnectionStateClosing, 4:ConnectionState.ConnectionStateClosed }

    _M_Ice.Instrumentation._t_ConnectionState = IcePy.defineEnum('::Ice::Instrumentation::ConnectionState', ConnectionState, (), ConnectionState._enumerators)

    _M_Ice.Instrumentation.ConnectionState = ConnectionState
    del ConnectionState

if 'ConnectionObserver' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.ConnectionObserver = Ice.createTempClass()
    class ConnectionObserver(_M_Ice.Instrumentation.Observer):
        """The connection observer interface to instrument Ice connections."""
        def __init__(self):
            if Ice.getType(self) == _M_Ice.Instrumentation.ConnectionObserver:
                raise RuntimeError('Ice.Instrumentation.ConnectionObserver is an abstract class')

        def sentBytes(self, num):
            """Notification of sent bytes over the connection.
            Arguments:
            num -- The number of bytes sent."""
            pass

        def receivedBytes(self, num):
            """Notification of received bytes over the connection.
            Arguments:
            num -- The number of bytes received."""
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Ice.Instrumentation._t_ConnectionObserver)

        __repr__ = __str__

    _M_Ice.Instrumentation._t_ConnectionObserver = IcePy.defineClass('::Ice::Instrumentation::ConnectionObserver', ConnectionObserver, -1, (), True, False, None, (_M_Ice.Instrumentation._t_Observer,), ())
    ConnectionObserver._ice_type = _M_Ice.Instrumentation._t_ConnectionObserver

    _M_Ice.Instrumentation.ConnectionObserver = ConnectionObserver
    del ConnectionObserver

if 'DispatchObserver' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.DispatchObserver = Ice.createTempClass()
    class DispatchObserver(_M_Ice.Instrumentation.Observer):
        """The dispatch observer to instrument servant dispatch."""
        def __init__(self):
            if Ice.getType(self) == _M_Ice.Instrumentation.DispatchObserver:
                raise RuntimeError('Ice.Instrumentation.DispatchObserver is an abstract class')

        def userException(self):
            """Notification of a user exception."""
            pass

        def reply(self, size):
            """Reply notification.
            Arguments:
            size -- The size of the reply."""
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Ice.Instrumentation._t_DispatchObserver)

        __repr__ = __str__

    _M_Ice.Instrumentation._t_DispatchObserver = IcePy.defineClass('::Ice::Instrumentation::DispatchObserver', DispatchObserver, -1, (), True, False, None, (_M_Ice.Instrumentation._t_Observer,), ())
    DispatchObserver._ice_type = _M_Ice.Instrumentation._t_DispatchObserver

    _M_Ice.Instrumentation.DispatchObserver = DispatchObserver
    del DispatchObserver

if 'ChildInvocationObserver' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.ChildInvocationObserver = Ice.createTempClass()
    class ChildInvocationObserver(_M_Ice.Instrumentation.Observer):
        """The child invocation observer to instrument remote or collocated
        invocations."""
        def __init__(self):
            if Ice.getType(self) == _M_Ice.Instrumentation.ChildInvocationObserver:
                raise RuntimeError('Ice.Instrumentation.ChildInvocationObserver is an abstract class')

        def reply(self, size):
            """Reply notification.
            Arguments:
            size -- The size of the reply."""
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Ice.Instrumentation._t_ChildInvocationObserver)

        __repr__ = __str__

    _M_Ice.Instrumentation._t_ChildInvocationObserver = IcePy.defineClass('::Ice::Instrumentation::ChildInvocationObserver', ChildInvocationObserver, -1, (), True, False, None, (_M_Ice.Instrumentation._t_Observer,), ())
    ChildInvocationObserver._ice_type = _M_Ice.Instrumentation._t_ChildInvocationObserver

    _M_Ice.Instrumentation.ChildInvocationObserver = ChildInvocationObserver
    del ChildInvocationObserver

if 'RemoteObserver' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.RemoteObserver = Ice.createTempClass()
    class RemoteObserver(_M_Ice.Instrumentation.ChildInvocationObserver):
        """The remote observer to instrument invocations that are sent over
        the wire."""
        def __init__(self):
            if Ice.getType(self) == _M_Ice.Instrumentation.RemoteObserver:
                raise RuntimeError('Ice.Instrumentation.RemoteObserver is an abstract class')

        def __str__(self):
            return IcePy.stringify(self, _M_Ice.Instrumentation._t_RemoteObserver)

        __repr__ = __str__

    _M_Ice.Instrumentation._t_RemoteObserver = IcePy.defineClass('::Ice::Instrumentation::RemoteObserver', RemoteObserver, -1, (), True, False, None, (_M_Ice.Instrumentation._t_ChildInvocationObserver,), ())
    RemoteObserver._ice_type = _M_Ice.Instrumentation._t_RemoteObserver

    _M_Ice.Instrumentation.RemoteObserver = RemoteObserver
    del RemoteObserver

if 'CollocatedObserver' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.CollocatedObserver = Ice.createTempClass()
    class CollocatedObserver(_M_Ice.Instrumentation.ChildInvocationObserver):
        """The collocated observer to instrument invocations that are
        collocated."""
        def __init__(self):
            if Ice.getType(self) == _M_Ice.Instrumentation.CollocatedObserver:
                raise RuntimeError('Ice.Instrumentation.CollocatedObserver is an abstract class')

        def __str__(self):
            return IcePy.stringify(self, _M_Ice.Instrumentation._t_CollocatedObserver)

        __repr__ = __str__

    _M_Ice.Instrumentation._t_CollocatedObserver = IcePy.defineClass('::Ice::Instrumentation::CollocatedObserver', CollocatedObserver, -1, (), True, False, None, (_M_Ice.Instrumentation._t_ChildInvocationObserver,), ())
    CollocatedObserver._ice_type = _M_Ice.Instrumentation._t_CollocatedObserver

    _M_Ice.Instrumentation.CollocatedObserver = CollocatedObserver
    del CollocatedObserver

if 'InvocationObserver' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.InvocationObserver = Ice.createTempClass()
    class InvocationObserver(_M_Ice.Instrumentation.Observer):
        """The invocation observer to instrument invocations on proxies. A
        proxy invocation can either result in a collocated or remote
        invocation. If it results in a remote invocation, a sub-observer is
        requested for the remote invocation."""
        def __init__(self):
            if Ice.getType(self) == _M_Ice.Instrumentation.InvocationObserver:
                raise RuntimeError('Ice.Instrumentation.InvocationObserver is an abstract class')

        def retried(self):
            """Notification of the invocation being retried."""
            pass

        def userException(self):
            """Notification of a user exception."""
            pass

        def getRemoteObserver(self, con, endpt, requestId, size):
            """Get a remote observer for this invocation.
            Arguments:
            con -- The connection information.
            endpt -- The connection endpoint.
            requestId -- The ID of the invocation.
            size -- The size of the invocation.
            Returns: The observer to instrument the remote invocation."""
            pass

        def getCollocatedObserver(self, adapter, requestId, size):
            """Get a collocated observer for this invocation.
            Arguments:
            adapter -- The object adapter hosting the collocated Ice object.
            requestId -- The ID of the invocation.
            size -- The size of the invocation.
            Returns: The observer to instrument the collocated invocation."""
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Ice.Instrumentation._t_InvocationObserver)

        __repr__ = __str__

    _M_Ice.Instrumentation._t_InvocationObserver = IcePy.defineClass('::Ice::Instrumentation::InvocationObserver', InvocationObserver, -1, (), True, False, None, (_M_Ice.Instrumentation._t_Observer,), ())
    InvocationObserver._ice_type = _M_Ice.Instrumentation._t_InvocationObserver

    _M_Ice.Instrumentation.InvocationObserver = InvocationObserver
    del InvocationObserver

if 'ObserverUpdater' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.ObserverUpdater = Ice.createTempClass()
    class ObserverUpdater(object):
        """The observer updater interface. This interface is implemented by
        the Ice run-time and an instance of this interface is provided by
        the Ice communicator on initialization to the 
        CommunicatorObserver object set with the communicator
        initialization data. The Ice communicator calls 
        CommunicatorObserver#setObserverUpdater to provide the observer
        updater.
        This interface can be used by add-ins implementing the 
        CommunicatorObserver interface to update the observers of
        connections and threads."""
        def __init__(self):
            if Ice.getType(self) == _M_Ice.Instrumentation.ObserverUpdater:
                raise RuntimeError('Ice.Instrumentation.ObserverUpdater is an abstract class')

        def updateConnectionObservers(self):
            """Update connection observers associated with each of the Ice
            connection from the communicator and its object adapters.
            When called, this method goes through all the connections and
            for each connection CommunicatorObserver#getConnectionObserver
            is called. The implementation of getConnectionObserver has the
            possibility to return an updated observer if necessary."""
            pass

        def updateThreadObservers(self):
            """Update thread observers associated with each of the Ice thread
            from the communicator and its object adapters.
            When called, this method goes through all the threads and for
            each thread CommunicatorObserver#getThreadObserver is
            called. The implementation of getThreadObserver has the
            possibility to return an updated observer if necessary."""
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Ice.Instrumentation._t_ObserverUpdater)

        __repr__ = __str__

    _M_Ice.Instrumentation._t_ObserverUpdater = IcePy.defineClass('::Ice::Instrumentation::ObserverUpdater', ObserverUpdater, -1, (), True, False, None, (), ())
    ObserverUpdater._ice_type = _M_Ice.Instrumentation._t_ObserverUpdater

    _M_Ice.Instrumentation.ObserverUpdater = ObserverUpdater
    del ObserverUpdater

if 'CommunicatorObserver' not in _M_Ice.Instrumentation.__dict__:
    _M_Ice.Instrumentation.CommunicatorObserver = Ice.createTempClass()
    class CommunicatorObserver(object):
        """The communicator observer interface used by the Ice run-time to
        obtain and update observers for its observable objects. This
        interface should be implemented by add-ins that wish to observe Ice
        objects in order to collect statistics. An instance of this
        interface can be provided to the Ice run-time through the Ice
        communicator initialization data."""
        def __init__(self):
            if Ice.getType(self) == _M_Ice.Instrumentation.CommunicatorObserver:
                raise RuntimeError('Ice.Instrumentation.CommunicatorObserver is an abstract class')

        def getConnectionEstablishmentObserver(self, endpt, connector):
            """This method should return an observer for the given endpoint
            information and connector. The Ice run-time calls this method
            for each connection establishment attempt.
            Arguments:
            endpt -- The endpoint.
            connector -- The description of the connector. For IP transports, this is typically the IP address to connect to.
            Returns: The observer to instrument the connection establishment."""
            pass

        def getEndpointLookupObserver(self, endpt):
            """This method should return an observer for the given endpoint
            information. The Ice run-time calls this method to resolve an
            endpoint and obtain the list of connectors. 
            For IP endpoints, this typically involves doing a DNS lookup to
            obtain the IP addresses associated with the DNS name.
            Arguments:
            endpt -- The endpoint.
            Returns: The observer to instrument the endpoint lookup."""
            pass

        def getConnectionObserver(self, c, e, s, o):
            """This method should return a connection observer for the given
            connection. The Ice run-time calls this method for each new
            connection and for all the Ice communicator connections when
            ObserverUpdater#updateConnections is called.
            Arguments:
            c -- The connection information.
            e -- The connection endpoint.
            s -- The state of the connection.
            o -- The old connection observer if one is already set or a null reference otherwise.
            Returns: The connection observer to instrument the connection."""
            pass

        def getThreadObserver(self, parent, id, s, o):
            """This method should return a thread observer for the given
            thread. The Ice run-time calls this method for each new thread
            and for all the Ice communicator threads when
            ObserverUpdater#updateThreads is called.
            Arguments:
            parent -- The parent of the thread.
            id -- The ID of the thread to observe.
            s -- The state of the thread.
            o -- The old thread observer if one is already set or a null reference otherwise.
            Returns: The thread observer to instrument the thread."""
            pass

        def getInvocationObserver(self, prx, operation, ctx):
            """This method should return an invocation observer for the given
            invocation. The Ice run-time calls this method for each new
            invocation on a proxy.
            Arguments:
            prx -- The proxy used for the invocation.
            operation -- The name of the invocation.
            ctx -- The context specified by the user.
            Returns: The invocation observer to instrument the invocation."""
            pass

        def getDispatchObserver(self, c, size):
            """This method should return a dispatch observer for the given
            dispatch. The Ice run-time calls this method each time it
            receives an incoming invocation to be dispatched for an Ice
            object.
            Arguments:
            c -- The current object as provided to the Ice servant dispatching the invocation.
            size -- The size of the dispatch.
            Returns: The dispatch observer to instrument the dispatch."""
            pass

        def setObserverUpdater(self, updater):
            """The Ice run-time calls this method when the communicator is
            initialized. The add-in implementing this interface can use
            this object to get the Ice run-time to re-obtain observers for
            observed objects.
            Arguments:
            updater -- The observer updater object."""
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Ice.Instrumentation._t_CommunicatorObserver)

        __repr__ = __str__

    _M_Ice.Instrumentation._t_CommunicatorObserver = IcePy.defineClass('::Ice::Instrumentation::CommunicatorObserver', CommunicatorObserver, -1, (), True, False, None, (), ())
    CommunicatorObserver._ice_type = _M_Ice.Instrumentation._t_CommunicatorObserver

    _M_Ice.Instrumentation.CommunicatorObserver = CommunicatorObserver
    del CommunicatorObserver

# End of module Ice.Instrumentation

__name__ = 'Ice'

# End of module Ice
