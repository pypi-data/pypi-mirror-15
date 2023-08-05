###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECT<ION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from __future__ import absolute_import

import six

__all__ = (
    'ComponentConfig',
    'HelloReturn',
    'Accept',
    'Deny',
    'Challenge',
    'HelloDetails',
    'SessionDetails',
    'CloseDetails',
    'SubscribeOptions',
    'EventDetails',
    'PublishOptions',
    'RegisterOptions',
    'CallDetails',
    'CallOptions',
    'CallResult',
)


class ComponentConfig(object):
    """
    WAMP application component configuration. An instance of this class is
    provided to the constructor of :class:`autobahn.wamp.protocol.ApplicationSession`.
    """

    __slots__ = (
        'realm',
        'extra',
        'keyring',
        'controller'
    )

    def __init__(self, realm=None, extra=None, keyring=None, controller=None):
        """

        :param realm: The realm the session should join.
        :type realm: unicode
        :param extra: Optional user-supplied object with extra configuration.
            This can be any object you like, and is accessible in your
            `ApplicationSession` subclass via `self.config.extra`. `dict` is
            a good default choice. Important: if the component is to be hosted
            by Crossbar.io, the supplied value must be JSON serializable.
        :type extra: arbitrary
        :param keyring: A mapper from WAMP URIs to "from"/"to" Ed25519 keys. When using
            WAMP end-to-end encryption, application payload is encrypted using a
            symmetric message key, which in turn is encrypted using the "to" URI (topic being
            published to or procedure being called) public key and the "from" URI
            private key. In both cases, the key for the longest matching URI is used.
        :type keyring: obj implementing IKeyRing or None
        :param controller: A WAMP ApplicationSession instance that holds a session to
            a controlling entity.
        :type controller: instance of ApplicationSession or None
        """
        assert(realm is None or type(realm) == six.text_type)
        # assert(keyring is None or ...) # FIXME

        self.realm = realm
        self.extra = extra
        self.keyring = keyring
        self.controller = controller

    def __str__(self):
        return "ComponentConfig(realm=<{0}>, extra={1}, keyring={2}, controller={3})".format(self.realm, self.extra, self.keyring, self.controller)


class HelloReturn(object):
    """
    Base class for ``HELLO`` return information.
    """


class Accept(HelloReturn):
    """
    Information to accept a ``HELLO``.
    """

    __slots__ = (
        'realm',
        'authid',
        'authrole',
        'authmethod',
        'authprovider',
        'authextra',
    )

    def __init__(self, realm=None, authid=None, authrole=None, authmethod=None, authprovider=None, authextra=None):
        """

        :param realm: The realm the client is joined to.
        :type realm: unicode
        :param authid: The authentication ID the client is assigned, e.g. ``"joe"`` or ``"joe@example.com"``.
        :type authid: unicode
        :param authrole: The authentication role the client is assigned, e.g. ``"anonymous"``, ``"user"`` or ``"com.myapp.user"``.
        :type authrole: unicode
        :param authmethod: The authentication method that was used to authenticate the client, e.g. ``"cookie"`` or ``"wampcra"``.
        :type authmethod: unicode
        :param authprovider: The authentication provider that was used to authenticate the client, e.g. ``"mozilla-persona"``.
        :type authprovider: unicode
        :param authextra: Application-specific authextra to be forwarded to the client in `WELCOME.details.authextra`.
        :type authextra: dict
        """
        assert(realm is None or type(realm) == six.text_type)
        assert(authid is None or type(authid) == six.text_type)
        assert(authrole is None or type(authrole) == six.text_type)
        assert(authmethod is None or type(authmethod) == six.text_type)
        assert(authprovider is None or type(authprovider) == six.text_type)
        assert(authextra is None or type(authextra) == dict)

        self.realm = realm
        self.authid = authid
        self.authrole = authrole
        self.authmethod = authmethod
        self.authprovider = authprovider
        self.authextra = authextra

    def __str__(self):
        return "Accept(realm=<{0}>, authid=<{1}>, authrole=<{2}>, authmethod={3}, authprovider={4}, authextra={5})".format(self.realm, self.authid, self.authrole, self.authmethod, self.authprovider, self.authextra)


class Deny(HelloReturn):
    """
    Information to deny a ``HELLO``.
    """

    __slots__ = (
        'reason',
        'message',
    )

    def __init__(self, reason=u"wamp.error.not_authorized", message=None):
        """

        :param reason: The reason of denying the authentication (an URI, e.g. ``wamp.error.not_authorized``)
        :type reason: unicode
        :param message: A human readable message (for logging purposes).
        :type message: unicode
        """
        assert(type(reason) == six.text_type)
        assert(message is None or type(message) == six.text_type)

        self.reason = reason
        self.message = message

    def __str__(self):
        return "Deny(reason=<{0}>, message='{1}')".format(self.reason, self.message)


class Challenge(HelloReturn):
    """
    Information to challenge the client upon ``HELLO``.
    """

    __slots__ = (
        'method',
        'extra',
    )

    def __init__(self, method, extra=None):
        """

        :param method: The authentication method for the challenge (e.g. ``"wampcra"``).
        :type method: unicode

        :param extra: Any extra information for the authentication challenge. This is
           specific to the authentication method.
        :type extra: dict
        """
        assert(type(method) == six.text_type)
        assert(extra is None or type(extra) == dict)

        self.method = method
        self.extra = extra or {}

    def __str__(self):
        return "Challenge(method={0}, extra={1})".format(self.method, self.extra)


class HelloDetails(object):
    """
    Provides details of a WAMP session while still attaching.
    """

    __slots__ = (
        'realm',
        'authmethods',
        'authid',
        'authrole',
        'authextra',
        'session_roles',
        'pending_session',
    )

    def __init__(self, realm=None, authmethods=None, authid=None, authrole=None, authextra=None, session_roles=None, pending_session=None):
        """

        :param realm: The realm the client wants to join.
        :type realm: unicode or None
        :param authmethods: The authentication methods the client is willing to perform.
        :type authmethods: list of unicode or None
        :param authid: The authid the client wants to authenticate as.
        :type authid: unicode or None
        :param authrole: The authrole the client wants to authenticate as.
        :type authrole: unicode or None
        :param authextra: Any extra information the specific authentication method requires the client to send.
        :type authextra: arbitrary or None
        :param session_roles: The WAMP session roles and features by the connecting client.
        :type session_roles: dict or None
        :param pending_session: The session ID the session will get once successfully attached.
        :type pending_session: int or None
        """
        assert(realm is None or type(realm) == six.text_type)
        assert(authmethods is None or (type(authmethods) == list and all(type(x) == six.text_type for x in authmethods)))
        assert(authid is None or type(authid) == six.text_type)
        assert(authrole is None or type(authrole) == six.text_type)
        assert(authextra is None or type(authextra) == dict)
        # assert(session_roles is None or ...)  # FIXME
        assert(pending_session is None or type(pending_session) in six.integer_types)

        self.realm = realm
        self.authmethods = authmethods
        self.authid = authid
        self.authrole = authrole
        self.authextra = authextra
        self.session_roles = session_roles
        self.pending_session = pending_session

    def __str__(self):
        return "HelloDetails(realm=<{}>, authmethods={}, authid=<{}>, authrole=<{}>, authextra={}, session_roles={}, pending_session={})".format(self.realm, self.authmethods, self.authid, self.authrole, self.authextra, self.session_roles, self.pending_session)


class SessionDetails(object):
    """
    Provides details for a WAMP session upon open.

    .. seealso:: :func:`autobahn.wamp.interfaces.ISession.onJoin`
    """

    __slots__ = (
        'realm',
        'session',
        'authid',
        'authrole',
        'authmethod',
        'authprovider',
        'authextra',
    )

    def __init__(self, realm, session, authid=None, authrole=None, authmethod=None, authprovider=None, authextra=None):
        """

        :param realm: The realm this WAMP session is attached to.
        :type realm: unicode
        :param session: WAMP session ID of this session.
        :type session: int
        """
        assert(type(realm) == six.text_type)
        assert(type(session) in six.integer_types)
        assert(authid is None or type(authid) == six.text_type)
        assert(authrole is None or type(authrole) == six.text_type)
        assert(authmethod is None or type(authmethod) == six.text_type)
        assert(authprovider is None or type(authprovider) == six.text_type)
        assert(authextra is None or type(authextra) == dict)

        self.realm = realm
        self.session = session
        self.authid = authid
        self.authrole = authrole
        self.authmethod = authmethod
        self.authprovider = authprovider
        self.authextra = authextra

    def __str__(self):
        return "SessionDetails(realm=<{0}>, session={1}, authid=<{2}>, authrole=<{3}>, authmethod={4}, authprovider={5}, authextra={6})".format(self.realm, self.session, self.authid, self.authrole, self.authmethod, self.authprovider, self.authextra)


class CloseDetails(object):
    """
    Provides details for a WAMP session upon close.

    .. seealso:: :func:`autobahn.wamp.interfaces.ISession.onLeave`
    """
    REASON_DEFAULT = u"wamp.close.normal"
    REASON_TRANSPORT_LOST = u"wamp.close.transport_lost"

    __slots__ = (
        'reason',
        'message',
    )

    def __init__(self, reason=None, message=None):
        """

        :param reason: The close reason (an URI, e.g. ``wamp.close.normal``)
        :type reason: unicode
        :param message: Closing log message.
        :type message: unicode
        """
        assert(reason is None or type(reason) == six.text_type)
        assert(message is None or type(message) == six.text_type)

        self.reason = reason
        self.message = message

    def __str__(self):
        return "CloseDetails(reason=<{0}>, message='{1}')".format(self.reason, self.message)


class SubscribeOptions(object):
    """
    Used to provide options for subscribing in
    :func:`autobahn.wamp.interfaces.ISubscriber.subscribe`.
    """

    __slots__ = (
        'match',
        'details_arg',
    )

    def __init__(self, match=None, details_arg=None):
        """

        :param match: The topic matching method to be used for the subscription.
        :type match: unicode
        :param details_arg: When invoking the handler, provide event details
          in this keyword argument to the callable.
        :type details_arg: str
        """
        assert(match is None or (type(match) == six.text_type and match in [u'exact', u'prefix', u'wildcard']))
        assert(details_arg is None or type(details_arg) == str)

        self.match = match
        self.details_arg = details_arg

    def message_attr(self):
        """
        Returns options dict as sent within WAMP messages.
        """
        options = {}

        if self.match is not None:
            options[u'match'] = self.match

        return options

    def __str__(self):
        return "SubscribeOptions(match={0}, details_arg={1})".format(self.match, self.details_arg)


class EventDetails(object):
    """
    Provides details on an event when calling an event handler
    previously registered.
    """

    __slots__ = (
        'publication',
        'publisher',
        'publisher_authid',
        'publisher_authrole',
        'topic',
        'enc_algo',
    )

    def __init__(self, publication, publisher=None, publisher_authid=None, publisher_authrole=None, topic=None, enc_algo=None):
        """

        :param publication: The publication ID of the event (always present).
        :type publication: int
        :param publisher: The WAMP session ID of the original publisher of this event.
            Only filled when publisher is disclosed.
        :type publisher: None or int
        :param publisher_authid: The WAMP authid of the original publisher of this event.
            Only filled when publisher is disclosed.
        :type publisher_authid: None or unicode
        :param publisher_authrole: The WAMP authrole of the original publisher of this event.
            Only filled when publisher is disclosed.
        :type publisher_authrole: None or unicode
        :param topic: For pattern-based subscriptions, the actual topic URI being published to.
            Only filled for pattern-based subscriptions.
        :type topic: None or unicode
        :param enc_algo: Payload encryption algorithm that
            was in use (currently, either `None` or `"cryptobox"`).
        :type enc_algo: None or unicode
        """
        assert(type(publication) in six.integer_types)
        assert(publisher is None or type(publisher) in six.integer_types)
        assert(publisher_authid is None or type(publisher_authid) == six.text_type)
        assert(publisher_authrole is None or type(publisher_authrole) == six.text_type)
        assert(topic is None or type(topic) == six.text_type)
        assert(enc_algo is None or (type(enc_algo) == six.text_type and enc_algo in [u'cryptobox']))

        self.publication = publication
        self.publisher = publisher
        self.publisher_authid = publisher_authid
        self.publisher_authrole = publisher_authrole
        self.topic = topic
        self.enc_algo = enc_algo

    def __str__(self):
        return "EventDetails(publication={0}, publisher={1}, publisher_authid={2}, publisher_authrole={3}, topic=<{4}>, enc_algo={5})".format(self.publication, self.publisher, self.publisher_authid, self.publisher_authrole, self.topic, self.enc_algo)


class PublishOptions(object):
    """
    Used to provide options for subscribing in
    :func:`autobahn.wamp.interfaces.IPublisher.publish`.
    """

    __slots__ = (
        'acknowledge',
        'exclude_me',
        'exclude',
        'exclude_authid',
        'exclude_authrole',
        'eligible',
        'eligible_authid',
        'eligible_authrole',
    )

    def __init__(self,
                 acknowledge=None,
                 exclude_me=None,
                 exclude=None,
                 exclude_authid=None,
                 exclude_authrole=None,
                 eligible=None,
                 eligible_authid=None,
                 eligible_authrole=None):
        """

        :param acknowledge: If ``True``, acknowledge the publication with a success or
           error response.
        :type acknowledge: bool
        :param exclude_me: If ``True``, exclude the publisher from receiving the event, even
           if he is subscribed (and eligible).
        :type exclude_me: bool or None
        :param exclude: A single WAMP session ID or a list thereof to exclude from receiving this event.
        :type exclude: int or list of int or None
        :param exclude_authid: A single WAMP authid or a list thereof to exclude from receiving this event.
        :type exclude_authid: unicode or list of unicode or None
        :param exclude_authrole: A single WAMP authrole or a list thereof to exclude from receiving this event.
        :type exclude_authrole: list of unicode or None
        :param eligible: A single WAMP session ID or a list thereof eligible to receive this event.
        :type eligible: int or list of int or None
        :param eligible_authid: A single WAMP authid or a list thereof eligible to receive this event.
        :type eligible_authid: unicode or list of unicode or None
        :param eligible_authrole: A single WAMP authrole or a list thereof eligible to receive this event.
        :type eligible_authrole: unicode or list of unicode or None
        """
        assert(acknowledge is None or type(acknowledge) == bool)
        assert(exclude_me is None or type(exclude_me) == bool)
        assert(exclude is None or type(exclude) in six.integer_types or (type(exclude) == list and all(type(x) in six.integer_types for x in exclude)))
        assert(exclude_authid is None or type(exclude_authid) == six.text_type or (type(exclude_authid) == list and all(type(x) == six.text_type for x in exclude_authid)))
        assert(exclude_authrole is None or type(exclude_authrole) == six.text_type or (type(exclude_authrole) == list and all(type(x) == six.text_type for x in exclude_authrole)))
        assert(eligible is None or type(eligible) in six.integer_types or (type(eligible) == list and all(type(x) in six.integer_types for x in eligible)))
        assert(eligible_authid is None or type(eligible_authid) == six.text_type or (type(eligible_authid) == list and all(type(x) == six.text_type for x in eligible_authid)))
        assert(eligible_authrole is None or type(eligible_authrole) == six.text_type or (type(eligible_authrole) == list and all(type(x) == six.text_type for x in eligible_authrole)))

        self.acknowledge = acknowledge
        self.exclude_me = exclude_me
        self.exclude = exclude
        self.exclude_authid = exclude_authid
        self.exclude_authrole = exclude_authrole
        self.eligible = eligible
        self.eligible_authid = eligible_authid
        self.eligible_authrole = eligible_authrole

    def message_attr(self):
        """
        Returns options dict as sent within WAMP messages.
        """
        options = {}

        if self.acknowledge is not None:
            options[u'acknowledge'] = self.acknowledge

        if self.exclude_me is not None:
            options[u'exclude_me'] = self.exclude_me

        if self.exclude is not None:
            options[u'exclude'] = self.exclude if type(self.exclude) == list else [self.exclude]

        if self.exclude_authid is not None:
            options[u'exclude_authid'] = self.exclude_authid if type(self.exclude_authid) == list else self.exclude_authid

        if self.exclude_authrole is not None:
            options[u'exclude_authrole'] = self.exclude_authrole if type(self.exclude_authrole) == list else self.exclude_authrole

        if self.eligible is not None:
            options[u'eligible'] = self.eligible if type(self.eligible) == list else self.eligible

        if self.eligible_authid is not None:
            options[u'eligible_authid'] = self.eligible_authid if type(self.eligible_authid) == list else self.eligible_authid

        if self.eligible_authrole is not None:
            options[u'eligible_authrole'] = self.eligible_authrole if type(self.eligible_authrole) == list else self.eligible_authrole

        return options

    def __str__(self):
        return "PublishOptions(acknowledge={0}, exclude_me={1}, exclude={2}, exclude_authid={3}, exclude_authrole={4}, eligible={5}, eligible_authid={6}, eligible_authrole={7})".format(self.acknowledge, self.exclude_me, self.exclude, self.exclude_authid, self.exclude_authrole, self.eligible, self.eligible_authid, self.eligible_authrole)


class RegisterOptions(object):
    """
    Used to provide options for registering in
    :func:`autobahn.wamp.interfaces.ICallee.register`.
    """

    __slots__ = (
        'match',
        'invoke',
        'details_arg',
    )

    def __init__(self, match=None, invoke=None, details_arg=None):
        """

        :param details_arg: When invoking the endpoint, provide call details
           in this keyword argument to the callable.
        :type details_arg: str
        """
        assert(match is None or (type(match) == six.text_type and match in [u'exact', u'prefix', u'wildcard']))
        assert(invoke is None or (type(invoke) == six.text_type and invoke in [u'single', u'first', u'last', u'roundrobin', u'random']))
        assert(details_arg is None or type(details_arg) == str)

        self.match = match
        self.invoke = invoke
        self.details_arg = details_arg

    def message_attr(self):
        """
        Returns options dict as sent within WAMP messages.
        """
        options = {}

        if self.match is not None:
            options[u'match'] = self.match

        if self.invoke is not None:
            options[u'invoke'] = self.invoke

        return options

    def __str__(self):
        return "RegisterOptions(match={0}, invoke={1}, details_arg={2})".format(self.match, self.invoke, self.details_arg)


class CallDetails(object):
    """
    Provides details on a call when an endpoint previously
    registered is being called and opted to receive call details.
    """

    __slots__ = (
        'progress',
        'caller',
        'caller_authid',
        'caller_authrole',
        'procedure',
        'enc_algo',
    )

    def __init__(self, progress=None, caller=None, caller_authid=None, caller_authrole=None, procedure=None, enc_algo=None):
        """

        :param progress: A callable that will receive progressive call results.
        :type progress: callable
        :param caller: The WAMP session ID of the caller, if the latter is disclosed.
            Only filled when caller is disclosed.
        :type caller: int
        :param caller_authid: The WAMP authid of the original caller of this event.
            Only filled when caller is disclosed.
        :type caller_authid: None or unicode
        :param caller_authrole: The WAMP authrole of the original caller of this event.
            Only filled when caller is disclosed.
        :type caller_authrole: None or unicode
        :param procedure: For pattern-based registrations, the actual procedure URI being called.
        :type procedure: None or unicode
        :param enc_algo: Payload encryption algorithm that
            was in use (currently, either `None` or `"cryptobox"`).
        :type enc_algo: None or string
        """
        assert(progress is None or callable(progress))
        assert(caller is None or type(caller) in six.integer_types)
        assert(caller_authid is None or type(caller_authid) == six.text_type)
        assert(caller_authrole is None or type(caller_authrole) == six.text_type)
        assert(procedure is None or type(procedure) == six.text_type)
        assert(enc_algo is None or (type(enc_algo) == six.text_type and enc_algo in [u'cryptobox']))

        self.progress = progress
        self.caller = caller
        self.caller_authid = caller_authid
        self.caller_authrole = caller_authrole
        self.procedure = procedure
        self.enc_algo = enc_algo

    def __str__(self):
        return "CallDetails(progress={0}, caller={1}, caller_authid={2}, caller_authrole={3}, procedure=<{4}>, enc_algo={5})".format(self.progress, self.caller, self.caller_authid, self.caller_authrole, self.procedure, self.enc_algo)


class CallOptions(object):
    """
    Used to provide options for calling with :func:`autobahn.wamp.interfaces.ICaller.call`.
    """

    __slots__ = (
        'on_progress',
        'timeout',
    )

    def __init__(self,
                 on_progress=None,
                 timeout=None):
        """

        :param on_progress: A callback that will be called when the remote endpoint
           called yields interim call progress results.
        :type on_progress: callable
        :param timeout: Time in seconds after which the call should be automatically canceled.
        :type timeout: float
        """
        assert(on_progress is None or callable(on_progress))
        assert(timeout is None or (type(timeout) in list(six.integer_types) + [float] and timeout > 0))

        self.on_progress = on_progress
        self.timeout = timeout

    def message_attr(self):
        """
        Returns options dict as sent within WAMP messages.
        """
        options = {}

        if self.timeout is not None:
            options[u'timeout'] = self.timeout

        if self.on_progress is not None:
            options[u'receive_progress'] = True

        return options

    def __str__(self):
        return "CallOptions(on_progress={0}, timeout={1})".format(self.on_progress, self.timeout)


class CallResult(object):
    """
    Wrapper for remote procedure call results that contain multiple positional
    return values or keyword return values.
    """

    __slots__ = (
        'results',
        'kwresults',
        'enc_algo',
    )

    def __init__(self, *results, **kwresults):
        """

        :param results: The positional result values.
        :type results: list
        :param kwresults: The keyword result values.
        :type kwresults: dict
        """
        enc_algo = kwresults.pop('enc_algo', None)
        assert(enc_algo is None or (type(enc_algo) == six.text_type and enc_algo in [u'cryptobox']))

        self.enc_algo = enc_algo
        self.results = results
        self.kwresults = kwresults

    def __str__(self):
        return "CallResult(results={0}, kwresults={1}, enc_algo={2})".format(self.results, self.kwresults, self.enc_algo)


class IPublication(object):
    """
    Represents a publication of an event. This is used with acknowledged publications.
    """

    def id(self):
        """
        The WAMP publication ID for this publication.
        """


class ISubscription(object):
    """
    Represents a subscription to a topic.
    """

    def id(self):
        """
        The WAMP subscription ID for this subscription.
        """

    def active(self):
        """
        Flag indicating if subscription is active.
        """

    def unsubscribe(self):
        """
        Unsubscribe this subscription that was previously created from
        :func:`autobahn.wamp.interfaces.ISubscriber.subscribe`.

        After a subscription has been unsubscribed successfully, no events
        will be routed to the event handler anymore.

        Returns an instance of :tx:`twisted.internet.defer.Deferred` (when
        running on **Twisted**) or an instance of :py:class:`asyncio.Future`
        (when running on **asyncio**).

        - If the unsubscription succeeds, the returned Deferred/Future will
          *resolve* (with no return value).

        - If the unsubscription fails, the returned Deferred/Future will *reject*
          with an instance of :class:`autobahn.wamp.exception.ApplicationError`.

        :returns: A Deferred/Future for the unsubscription
        :rtype: instance(s) of :tx:`twisted.internet.defer.Deferred` / :py:class:`asyncio.Future`
        """


class IRegistration(object):
    """
    Represents a registration of an endpoint.
    """

    def id(self):
        """
        The WAMP registration ID for this registration.
        """

    def active(self):
        """
        Flag indicating if registration is active.
        """

    def unregister(self):
        """
        Unregister this registration that was previously created from
        :func:`autobahn.wamp.interfaces.ICallee.register`.

        After a registration has been unregistered successfully, no calls
        will be routed to the endpoint anymore.

        Returns an instance of :tx:`twisted.internet.defer.Deferred` (when
        running on **Twisted**) or an instance of :py:class:`asyncio.Future`
        (when running on **asyncio**).

        - If the unregistration succeeds, the returned Deferred/Future will
          *resolve* (with no return value).

        - If the unregistration fails, the returned Deferred/Future will be rejected
          with an instance of :class:`autobahn.wamp.exception.ApplicationError`.

        :returns: A Deferred/Future for the unregistration
        :rtype: instance(s) of :tx:`twisted.internet.defer.Deferred` / :py:class:`asyncio.Future`
        """
