from __future__ import absolute_import, print_function

import errno
import logging
import os
import threading
import traceback

import pykka

class _TellCallableProxy(object):
    """Internal helper class for proxying callables."""

    def __init__(self, ref, attr_path):
        self.actor_ref = ref
        self._attr_path = attr_path

    def __call__(self, *args, **kwargs):
        message = {
            'command': 'pykka_call',
            'attr_path': self._attr_path,
            'args': args,
            'kwargs': kwargs,
        }
        self.actor_ref.tell(message)


class TellActorProxy(pykka.ActorProxy):
    """ActorProxy in which all calls are implemented as using tell().

    The standard pykka.ActorProxy always uses ask() and returns a Future.  If
    the target method raises an exception, it is placed in the Future object
    and re-raised when get() is called on the Future.  Unfortunately, most
    messaging in Node Manager is asynchronous and the caller does not store the
    Future object returned by the call to ActorProxy.  As a result, exceptions
    resulting from these calls end up in limbo, neither reported in the logs
    nor handled by on_failure().

    The TellActorProxy uses tell() instead of ask() and does not return a
    Future object.  As a result, if the target method raises an exception, it
    will be logged and on_failure() will be called as intended.

    """

    def __repr__(self):
        return '<ActorProxy for %s, attr_path=%s>' % (
            self.actor_ref, self._attr_path)

    def __getattr__(self, name):
        """Get a callable from the actor."""
        attr_path = self._attr_path + (name,)
        if attr_path not in self._known_attrs:
            self._known_attrs = self._get_attributes()
        attr_info = self._known_attrs.get(attr_path)
        if attr_info is None:
            raise AttributeError('%s has no attribute "%s"' % (self, name))
        if attr_info['callable']:
            if attr_path not in self._callable_proxies:
                self._callable_proxies[attr_path] = _TellCallableProxy(
                    self.actor_ref, attr_path)
            return self._callable_proxies[attr_path]
        else:
            raise AttributeError('attribute "%s" is not a callable on %s' % (name, self))

class TellableActorRef(pykka.ActorRef):
    """ActorRef adding the tell_proxy() method to get TellActorProxy."""

    def tell_proxy(self):
        return TellActorProxy(self)

class BaseNodeManagerActor(pykka.ThreadingActor):
    """Base class for actors in node manager, redefining actor_ref as a
    TellableActorRef and providing a default on_failure handler.
    """

    def __init__(self, *args, **kwargs):
         super(pykka.ThreadingActor, self).__init__(*args, **kwargs)
         self.actor_ref = TellableActorRef(self)

    def on_failure(self, exception_type, exception_value, tb):
        lg = getattr(self, "_logger", logging)
        if (exception_type in (threading.ThreadError, MemoryError) or
            exception_type is OSError and exception_value.errno == errno.ENOMEM):
            lg.critical("Unhandled exception is a fatal error, killing Node Manager")
            os.killpg(os.getpgid(0), 9)
