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
// Generated from file `LocatorF.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

#ifndef __Ice_LocatorF_h__
#define __Ice_LocatorF_h__

#include <IceUtil/PushDisableWarnings.h>
#include <Ice/ProxyF.h>
#include <Ice/ObjectF.h>
#include <Ice/Exception.h>
#include <Ice/LocalObject.h>
#include <Ice/StreamHelpers.h>
#include <Ice/Proxy.h>
#include <IceUtil/ScopedArray.h>
#include <IceUtil/Optional.h>
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

namespace Ice
{

class Locator;
ICE_API void __read(::IceInternal::BasicStream*, ::IceInternal::ProxyHandle< ::IceProxy::Ice::Locator>&);
ICE_API ::IceProxy::Ice::Object* upCast(::IceProxy::Ice::Locator*);

class LocatorRegistry;
ICE_API void __read(::IceInternal::BasicStream*, ::IceInternal::ProxyHandle< ::IceProxy::Ice::LocatorRegistry>&);
ICE_API ::IceProxy::Ice::Object* upCast(::IceProxy::Ice::LocatorRegistry*);

}

}

namespace Ice
{

class Locator;
ICE_API ::Ice::Object* upCast(::Ice::Locator*);
typedef ::IceInternal::Handle< ::Ice::Locator> LocatorPtr;
typedef ::IceInternal::ProxyHandle< ::IceProxy::Ice::Locator> LocatorPrx;
ICE_API void __patch(LocatorPtr&, const ::Ice::ObjectPtr&);

class LocatorRegistry;
ICE_API ::Ice::Object* upCast(::Ice::LocatorRegistry*);
typedef ::IceInternal::Handle< ::Ice::LocatorRegistry> LocatorRegistryPtr;
typedef ::IceInternal::ProxyHandle< ::IceProxy::Ice::LocatorRegistry> LocatorRegistryPrx;
ICE_API void __patch(LocatorRegistryPtr&, const ::Ice::ObjectPtr&);

}

#include <IceUtil/PopDisableWarnings.h>
#endif
