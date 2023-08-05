// **********************************************************************
//
// Copyright (c) 2003-2016 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************
//
// Ice version 3.6.2
//
// <auto-generated>
//
// Generated from file `Endpoint.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

#ifndef __Ice_Endpoint_h__
#define __Ice_Endpoint_h__

#include <IceUtil/PushDisableWarnings.h>
#include <Ice/ProxyF.h>
#include <Ice/ObjectF.h>
#include <Ice/Exception.h>
#include <Ice/LocalObject.h>
#include <Ice/StreamHelpers.h>
#include <IceUtil/ScopedArray.h>
#include <IceUtil/Optional.h>
#include <Ice/Version.h>
#include <Ice/BuiltinSequences.h>
#include <Ice/EndpointF.h>
#include <IceUtil/UndefSysMacros.h>

#ifndef ICE_IGNORE_VERSION
#   if ICE_INT_VERSION / 100 != 306
#       error Ice version mismatch!
#   endif
#   if ICE_INT_VERSION % 100 > 50
#       error Beta header file detected
#   endif
#   if ICE_INT_VERSION % 100 < 2
#       error Ice patch level mismatch!
#   endif
#endif

#ifndef ICE_API
#   ifdef ICE_API_EXPORTS
#       define ICE_API ICE_DECLSPEC_EXPORT
#   elif defined(ICE_STATIC_LIBS)
#       define ICE_API /**/
#   else
#       define ICE_API ICE_DECLSPEC_IMPORT
#   endif
#endif

namespace Ice
{

class EndpointInfo;
ICE_API ::Ice::LocalObject* upCast(::Ice::EndpointInfo*);
typedef ::IceInternal::Handle< ::Ice::EndpointInfo> EndpointInfoPtr;

class Endpoint;
ICE_API ::Ice::LocalObject* upCast(::Ice::Endpoint*);
typedef ::IceInternal::Handle< ::Ice::Endpoint> EndpointPtr;

class IPEndpointInfo;
ICE_API ::Ice::LocalObject* upCast(::Ice::IPEndpointInfo*);
typedef ::IceInternal::Handle< ::Ice::IPEndpointInfo> IPEndpointInfoPtr;

class TCPEndpointInfo;
ICE_API ::Ice::LocalObject* upCast(::Ice::TCPEndpointInfo*);
typedef ::IceInternal::Handle< ::Ice::TCPEndpointInfo> TCPEndpointInfoPtr;

class UDPEndpointInfo;
ICE_API ::Ice::LocalObject* upCast(::Ice::UDPEndpointInfo*);
typedef ::IceInternal::Handle< ::Ice::UDPEndpointInfo> UDPEndpointInfoPtr;

class WSEndpointInfo;
ICE_API ::Ice::LocalObject* upCast(::Ice::WSEndpointInfo*);
typedef ::IceInternal::Handle< ::Ice::WSEndpointInfo> WSEndpointInfoPtr;

class OpaqueEndpointInfo;
ICE_API ::Ice::LocalObject* upCast(::Ice::OpaqueEndpointInfo*);
typedef ::IceInternal::Handle< ::Ice::OpaqueEndpointInfo> OpaqueEndpointInfoPtr;

}

namespace Ice
{

const ::Ice::Short TCPEndpointType = 1;

const ::Ice::Short SSLEndpointType = 2;

const ::Ice::Short UDPEndpointType = 3;

const ::Ice::Short WSEndpointType = 4;

const ::Ice::Short WSSEndpointType = 5;

}

namespace Ice
{

class ICE_API EndpointInfo : virtual public ::Ice::LocalObject
{
public:

    typedef EndpointInfoPtr PointerType;

    EndpointInfo()
    {
    }

    EndpointInfo(::Ice::Int __ice_timeout, bool __ice_compress) :
        timeout(__ice_timeout),
        compress(__ice_compress)
    {
    }


    virtual ::Ice::Short type() const = 0;

    virtual bool datagram() const = 0;

    virtual bool secure() const = 0;

public:

    ::Ice::Int timeout;

    bool compress;
};

inline bool operator==(const EndpointInfo& l, const EndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) == static_cast<const ::Ice::LocalObject&>(r);
}

inline bool operator<(const EndpointInfo& l, const EndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) < static_cast<const ::Ice::LocalObject&>(r);
}

class ICE_API Endpoint : virtual public ::Ice::LocalObject
{
public:

    typedef EndpointPtr PointerType;

    virtual ::std::string toString() const = 0;

    virtual ::Ice::EndpointInfoPtr getInfo() const = 0;
};

inline bool operator==(const Endpoint& l, const Endpoint& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) == static_cast<const ::Ice::LocalObject&>(r);
}

inline bool operator<(const Endpoint& l, const Endpoint& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) < static_cast<const ::Ice::LocalObject&>(r);
}

class ICE_API IPEndpointInfo : public ::Ice::EndpointInfo
{
public:

    typedef IPEndpointInfoPtr PointerType;

    IPEndpointInfo()
    {
    }

    IPEndpointInfo(::Ice::Int __ice_timeout, bool __ice_compress, const ::std::string& __ice_host, ::Ice::Int __ice_port, const ::std::string& __ice_sourceAddress) :
        ::Ice::EndpointInfo(__ice_timeout, __ice_compress),
        host(__ice_host),
        port(__ice_port),
        sourceAddress(__ice_sourceAddress)
    {
    }


public:

    ::std::string host;

    ::Ice::Int port;

    ::std::string sourceAddress;
};

inline bool operator==(const IPEndpointInfo& l, const IPEndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) == static_cast<const ::Ice::LocalObject&>(r);
}

inline bool operator<(const IPEndpointInfo& l, const IPEndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) < static_cast<const ::Ice::LocalObject&>(r);
}

class ICE_API TCPEndpointInfo : public ::Ice::IPEndpointInfo
{
public:

    typedef TCPEndpointInfoPtr PointerType;

    TCPEndpointInfo()
    {
    }

    TCPEndpointInfo(::Ice::Int __ice_timeout, bool __ice_compress, const ::std::string& __ice_host, ::Ice::Int __ice_port, const ::std::string& __ice_sourceAddress) :
        ::Ice::IPEndpointInfo(__ice_timeout, __ice_compress, __ice_host, __ice_port, __ice_sourceAddress)
    {
    }

};

inline bool operator==(const TCPEndpointInfo& l, const TCPEndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) == static_cast<const ::Ice::LocalObject&>(r);
}

inline bool operator<(const TCPEndpointInfo& l, const TCPEndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) < static_cast<const ::Ice::LocalObject&>(r);
}

class ICE_API UDPEndpointInfo : public ::Ice::IPEndpointInfo
{
public:

    typedef UDPEndpointInfoPtr PointerType;

    UDPEndpointInfo()
    {
    }

    UDPEndpointInfo(::Ice::Int __ice_timeout, bool __ice_compress, const ::std::string& __ice_host, ::Ice::Int __ice_port, const ::std::string& __ice_sourceAddress, const ::std::string& __ice_mcastInterface, ::Ice::Int __ice_mcastTtl) :
        ::Ice::IPEndpointInfo(__ice_timeout, __ice_compress, __ice_host, __ice_port, __ice_sourceAddress),
        mcastInterface(__ice_mcastInterface),
        mcastTtl(__ice_mcastTtl)
    {
    }


public:

    ::std::string mcastInterface;

    ::Ice::Int mcastTtl;
};

inline bool operator==(const UDPEndpointInfo& l, const UDPEndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) == static_cast<const ::Ice::LocalObject&>(r);
}

inline bool operator<(const UDPEndpointInfo& l, const UDPEndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) < static_cast<const ::Ice::LocalObject&>(r);
}

class ICE_API WSEndpointInfo : public ::Ice::TCPEndpointInfo
{
public:

    typedef WSEndpointInfoPtr PointerType;

    WSEndpointInfo()
    {
    }

    WSEndpointInfo(::Ice::Int __ice_timeout, bool __ice_compress, const ::std::string& __ice_host, ::Ice::Int __ice_port, const ::std::string& __ice_sourceAddress, const ::std::string& __ice_resource) :
        ::Ice::TCPEndpointInfo(__ice_timeout, __ice_compress, __ice_host, __ice_port, __ice_sourceAddress),
        resource(__ice_resource)
    {
    }


public:

    ::std::string resource;
};

inline bool operator==(const WSEndpointInfo& l, const WSEndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) == static_cast<const ::Ice::LocalObject&>(r);
}

inline bool operator<(const WSEndpointInfo& l, const WSEndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) < static_cast<const ::Ice::LocalObject&>(r);
}

class ICE_API OpaqueEndpointInfo : public ::Ice::EndpointInfo
{
public:

    typedef OpaqueEndpointInfoPtr PointerType;

    OpaqueEndpointInfo()
    {
    }

    OpaqueEndpointInfo(::Ice::Int __ice_timeout, bool __ice_compress, const ::Ice::EncodingVersion& __ice_rawEncoding, const ::Ice::ByteSeq& __ice_rawBytes) :
        ::Ice::EndpointInfo(__ice_timeout, __ice_compress),
        rawEncoding(__ice_rawEncoding),
        rawBytes(__ice_rawBytes)
    {
    }


public:

    ::Ice::EncodingVersion rawEncoding;

    ::Ice::ByteSeq rawBytes;
};

inline bool operator==(const OpaqueEndpointInfo& l, const OpaqueEndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) == static_cast<const ::Ice::LocalObject&>(r);
}

inline bool operator<(const OpaqueEndpointInfo& l, const OpaqueEndpointInfo& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) < static_cast<const ::Ice::LocalObject&>(r);
}

}

#include <IceUtil/PopDisableWarnings.h>
#endif
