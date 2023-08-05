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
// Generated from file `ObjectAdapter.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

#ifndef __Ice_ObjectAdapter_h__
#define __Ice_ObjectAdapter_h__

#include <IceUtil/PushDisableWarnings.h>
#include <Ice/ProxyF.h>
#include <Ice/ObjectF.h>
#include <Ice/Exception.h>
#include <Ice/LocalObject.h>
#include <Ice/StreamHelpers.h>
#include <Ice/Proxy.h>
#include <IceUtil/ScopedArray.h>
#include <IceUtil/Optional.h>
#include <Ice/CommunicatorF.h>
#include <Ice/ServantLocatorF.h>
#include <Ice/LocatorF.h>
#include <Ice/Identity.h>
#include <Ice/FacetMap.h>
#include <Ice/Endpoint.h>
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

namespace IceProxy
{

}

namespace Ice
{

class ObjectAdapter;
ICE_API ::Ice::LocalObject* upCast(::Ice::ObjectAdapter*);
typedef ::IceInternal::Handle< ::Ice::ObjectAdapter> ObjectAdapterPtr;

}

namespace Ice
{

class ICE_API ObjectAdapter : virtual public ::Ice::LocalObject
{
public:

    typedef ObjectAdapterPtr PointerType;

    virtual ::std::string getName() const = 0;

    virtual ::Ice::CommunicatorPtr getCommunicator() const = 0;

    virtual void activate() = 0;

    virtual void hold() = 0;

    virtual void waitForHold() = 0;

    virtual void deactivate() = 0;

    virtual void waitForDeactivate() = 0;

    virtual bool isDeactivated() const = 0;

    virtual void destroy() = 0;

    virtual ::Ice::ObjectPrx add(const ::Ice::ObjectPtr&, const ::Ice::Identity&) = 0;

    virtual ::Ice::ObjectPrx addFacet(const ::Ice::ObjectPtr&, const ::Ice::Identity&, const ::std::string&) = 0;

    virtual ::Ice::ObjectPrx addWithUUID(const ::Ice::ObjectPtr&) = 0;

    virtual ::Ice::ObjectPrx addFacetWithUUID(const ::Ice::ObjectPtr&, const ::std::string&) = 0;

    virtual void addDefaultServant(const ::Ice::ObjectPtr&, const ::std::string&) = 0;

    virtual ::Ice::ObjectPtr remove(const ::Ice::Identity&) = 0;

    virtual ::Ice::ObjectPtr removeFacet(const ::Ice::Identity&, const ::std::string&) = 0;

    virtual ::Ice::FacetMap removeAllFacets(const ::Ice::Identity&) = 0;

    virtual ::Ice::ObjectPtr removeDefaultServant(const ::std::string&) = 0;

    virtual ::Ice::ObjectPtr find(const ::Ice::Identity&) const = 0;

    virtual ::Ice::ObjectPtr findFacet(const ::Ice::Identity&, const ::std::string&) const = 0;

    virtual ::Ice::FacetMap findAllFacets(const ::Ice::Identity&) const = 0;

    virtual ::Ice::ObjectPtr findByProxy(const ::Ice::ObjectPrx&) const = 0;

    virtual void addServantLocator(const ::Ice::ServantLocatorPtr&, const ::std::string&) = 0;

    virtual ::Ice::ServantLocatorPtr removeServantLocator(const ::std::string&) = 0;

    virtual ::Ice::ServantLocatorPtr findServantLocator(const ::std::string&) const = 0;

    virtual ::Ice::ObjectPtr findDefaultServant(const ::std::string&) const = 0;

    virtual ::Ice::ObjectPrx createProxy(const ::Ice::Identity&) const = 0;

    virtual ::Ice::ObjectPrx createDirectProxy(const ::Ice::Identity&) const = 0;

    virtual ::Ice::ObjectPrx createIndirectProxy(const ::Ice::Identity&) const = 0;

    virtual void setLocator(const ::Ice::LocatorPrx&) = 0;

    virtual ::Ice::LocatorPrx getLocator() const = 0;

    virtual void refreshPublishedEndpoints() = 0;

    virtual ::Ice::EndpointSeq getEndpoints() const = 0;

    virtual ::Ice::EndpointSeq getPublishedEndpoints() const = 0;
};

inline bool operator==(const ObjectAdapter& l, const ObjectAdapter& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) == static_cast<const ::Ice::LocalObject&>(r);
}

inline bool operator<(const ObjectAdapter& l, const ObjectAdapter& r)
{
    return static_cast<const ::Ice::LocalObject&>(l) < static_cast<const ::Ice::LocalObject&>(r);
}

}

#include <IceUtil/PopDisableWarnings.h>
#endif
