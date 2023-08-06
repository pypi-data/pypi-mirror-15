#!/usr/bin/env python
# encoding: utf-8

#
# The MIT License (MIT)
#
# Copyright (c) 2014-2016 CNRS

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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# AUTHORS
# Hervé BREDIN (http://herve.niderb.fr/)
# Johann POIGNANT
# Claude BARRAS


import tortilla
import requests
import os
import threading
import json
from base64 import b64encode, b64decode
from getpass import getpass
from sseclient import SSEClient
import warnings
import time


class CamomileBadRequest(Exception):
    pass


class CamomileUnauthorized(Exception):
    pass


class CamomileForbidden(Exception):
    pass


class CamomileNotFound(Exception):
    pass


class CamomileInternalError(Exception):
    pass


class CamomileBadJSON(Exception):
    pass


class CamomileErrorHandling(object):
    """Decorator for handling Camomile errors as exceptions

    Handles HTTP status code and "keep alive" behavior.

    Parameters
    ----------
    resuscitate : boolean, optional
        If `resuscitate` is True and user set `keep_alive` to True at login,
        automatically try to relogging on connection or authentication errors.
        Note that `rescucitate` must be set to False for login/logout methods
        as setting it to rue would result in an infinite login loop...

    """

    def __init__(self, resuscitate=True):
        super(CamomileErrorHandling, self).__init__()
        self.resuscitate = resuscitate

    def __call__(self, func, *args, **kwargs):
        def decorated_method(client, *args, **kwargs):
            try:
                return func(client, *args, **kwargs)

            # (optionnally) resuscitate in case of connection error
            except requests.exceptions.ConnectionError as e:
                if self.resuscitate and client._keep_alive:
                    client._resuscitate(max_trials=-1)
                    return func(client, *args, **kwargs)

                raise e

            # handle Camomile errors
            except requests.exceptions.HTTPError as e:

                if not hasattr(e, 'response'):
                    raise e

                try:
                    content = e.response.json()
                except AttributeError as e:
                    raise CamomileBadJSON(e.response.content)
                else:
                    pass

                message = content.get('error', None)
                if message is None:
                    raise e

                status_code = e.response.status_code

                if status_code == 400:
                    raise CamomileBadRequest(message)

                if status_code == 401:
                    if self.resuscitate and client._keep_alive:
                        client._resuscitate(max_trials=-1)
                        return func(client, *args, **kwargs)
                    else:
                        raise CamomileUnauthorized(message)

                if status_code == 403:
                    raise CamomileForbidden(message)

                if status_code == 404:
                    raise CamomileNotFound(message)

                if status_code == 500:
                    raise CamomileInternalError(message)

                raise e


        # keep name and docstring of the initial function
        decorated_method.__name__ = func.__name__
        decorated_method.__doc__ = func.__doc__
        return decorated_method


class Camomile(object):
    """Client for Camomile REST API

    Parameters
    ----------
    url : str
        Base URL of Camomile API.
    username, password : str, optional
        If provided, an attempt is made to log in.
    delay : float, optional
        If provided, make sure at least `delay` seconds pass between
        each request to the Camomile API.  Defaults to no delay.

    Example
    -------
    >>> url = 'http://camomile.fr'
    >>> client = Camomile(url)
    >>> client.login(username='root', password='password')
    >>> corpora = client.getCorpora(returns_id=True)
    >>> corpus = corpora[0]
    >>> layers = client.getLayers(corpus=corpus)
    >>> media = client.getMedia(corpus=corpus)
    >>> client.logout()
    """

    ADMIN = 3
    WRITE = 2
    READ = 1

    def __init__(self, url, username=None, password=None, keep_alive=False,
                 delay=0., debug=False):
        super(Camomile, self).__init__()

        # internally rely on tortilla generic API wrapper
        # see http://github.com/redodo/tortilla
        self._api = tortilla.wrap(url, format='json', delay=delay, debug=debug)
        self._url = url;
        self._listenerCallbacks = {}
        self._thread = None

        self._keep_alive = None

        if username:
            self.login(username, password, keep_alive=keep_alive)

    def __enter__(self):
        """
        Example
        -------
        >>> url = 'http://camomile.fr'
        >>> with Camomile(url, username='root', password='password') as client:
        >>>     corpora = client.corpus()
        """
        return self

    def __exit__(self, type, value, traceback):
        self.logout()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # HELPER FUNCTIONS
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _user(self, id_user=None):
        user = self._api.user
        if id_user:
            user = user(id_user)
        return user

    def _group(self, id_group=None):
        group = self._api.group
        if id_group:
            group = group(id_group)
        return group

    def _corpus(self, id_corpus=None):
        corpus = self._api.corpus
        if id_corpus:
            corpus = corpus(id_corpus)
        return corpus

    def _medium(self, id_medium=None):
        medium = self._api.medium
        if id_medium:
            medium = medium(id_medium)
        return medium

    def _layer(self, id_layer=None):
        layer = self._api.layer
        if id_layer:
            layer = layer(id_layer)
        return layer

    def _annotation(self, id_annotation=None):
        annotation = self._api.annotation
        if id_annotation:
            annotation = annotation(id_annotation)
        return annotation

    def _queue(self, id_queue=None):
        queue = self._api.queue
        if id_queue:
            queue = queue(id_queue)
        return queue

    def _id(self, result):
        if isinstance(result, list):
            return [r._id for r in result]
        return result._id

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # AUTHENTICATION
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @CamomileErrorHandling(resuscitate=False)
    def login(self, username, password=None, keep_alive=False):
        """Login

        Parameters
        ----------
        username: str
        password : str, optional
        keep_alive : boolean, optional
        """

        if password is None:
            password = getpass()

        credentials = {'username': username,
                       'password': password}

        result = self._api.login.post(data=credentials)

        if keep_alive:
            self._keep_alive = credentials

        return result

    def _resuscitate(self, max_trials=-1):
        """Try rescuscitating a dead "keep_alive" client

        Parameters
        ----------
        max_trials : int, optional
            Default to unlimited number of trials.
        """

        username = self._keep_alive['username']
        password = self._keep_alive['password']

        trials = 0

        success = None
        while trials != max_trials:
            try:
                success = self.login(username, password=password,
                                     keep_alive=True)
                if success:
                    break
            except requests.exceptions.ConnectionError as e:
                trials += 1
                wait = 2 ** trials
                warning = 'Lost connection. Waiting {wait:d} seconds before trying again...'
                warnings.warn(warning.format(wait=wait))
                time.sleep(wait)


    @CamomileErrorHandling(resuscitate=False)
    def logout(self):
        """Logout"""

        if self._thread:
           self._thread.isRun = False
           self._thread = None

        self._keep_alive = None

        return self._api.logout.post()

    @CamomileErrorHandling()
    def me(self, returns_id=False):
        """Get information about logged in user"""
        result = self._api.me.get()
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def getMyGroups(self):
        """Get groups the logged in user belongs to"""
        return self._api.me.group.get()

    @CamomileErrorHandling()
    def update_password(self, new_password=None):
        """Update password"""

        if new_password is None:
            new_password = getpass('New password: ')

        return self._api.me.put(data={'password': new_password})

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # USERS
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @CamomileErrorHandling()
    def getUser(self, user):
        """Get user by ID

        Parameters
        ----------
        user : str
            User ID.

        Returns
        -------
        user : dict

        """
        return self._user(user).get()

    @CamomileErrorHandling()
    def getUsers(self, username=None, returns_id=False):
        """Get user(s)

        Parameters
        ----------
        username : str, optional
            Filter by username.
        returns_id : boolean, optional.
            Returns IDs rather than user dictionaries.

        Returns
        -------
        users : list
            List of users
        """
        params = {'username': username} if username else None
        result = self._user().get(params=params)
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def createUser(self,
                   username, password,
                   description=None, role='user',
                   returns_id=False):
        """Create new user

        Parameters
        ----------
        username, password : str, optional
        description : object, optional
            Must be JSON serializable.
        role : {'user', 'admin'}, optional
            Defaults to 'user'.
        returns_id : boolean, optional.
            Returns IDs rather than user dictionaries.

        Returns
        -------
        user : dict
            Newly created user.
        """

        data = {'username': username,
                'password': password,
                'description': description if description else {},
                'role': role}

        result = self._user().post(data=data)
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def updateUser(self, user, password=None, description=None, role=None):
        """Update existing user

        Parameters
        ----------
        user : str
            User ID.
        password : str, optional
            Set new password.
        description : object, optional
            Set new description. Must be JSON serializable.
        role : {'user', 'admin'}, optional
            Set new role.

        Returns
        -------
        user : dict
            Updated user.
        """
        data = {}

        if password is not None:
            data['password'] = password

        if description is not None:
            data['description'] = description

        if role is not None:
            data['role'] = role

        return self._user(user).put(data=data)

    @CamomileErrorHandling()
    def deleteUser(self, user):
        """Delete existing user

        Parameters
        ----------
        user : str
            User ID.
        """
        return self._user(user).delete()

    @CamomileErrorHandling()
    def getUserGroups(self, user):
        """Get groups of existing user

        Parameters
        ----------
        user : str

        Returns
        -------
        groups : list
            List of user's groups
        """
        return self._user(user).group.get()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # GROUPS
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @CamomileErrorHandling()
    def getGroup(self, group):
        """Get group by ID

        Parameters
        ----------
        group : str
            Group ID.

        Returns
        -------
        group : dict

        """
        return self._group(group).get()

    @CamomileErrorHandling()
    def getGroups(self, name=None, returns_id=False):
        """Get group(s)

        Parameters
        ----------
        name : str, optional
            Filter groups by name.
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.

        Returns
        -------
        groups : list
            List of groups
        """
        params = {'name': name} if name else None
        result = self._group().get(params=params)
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def createGroup(self, name, description=None, returns_id=False):
        """Create new group

        Parameters
        ----------
        name : str
            Group name.
        description : object, optional
            Group description. Must be JSON serializable.
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.

        Returns
        -------
        group : dict
            Newly created group.

        Example
        -------
        >>> description = {'country': 'France',
        ...                'town': 'Orsay'}
        >>> client.create_group('LIMSI', description=description)

        """
        data = {'name': name,
                'description': description if description else {}}

        result = self._group().post(data=data)
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def updateGroup(self, group, description=None):
        """Update existing group

        Parameters
        ----------
        group : str
            Group ID.
        description : object, optional

        Returns
        -------
        group : dict
            Updated group.
        """
        data = {'description': description}
        return self._group(group).put(data=data)

    @CamomileErrorHandling()
    def deleteGroup(self, group):
        """Delete existing group

        Parameters
        ----------
        group : str
            Group ID.
        """
        return self._group(group).delete()

    @CamomileErrorHandling()
    def addUserToGroup(self, user, group):
        return self._group(group).user(user).put()

    @CamomileErrorHandling()
    def removeUserFromGroup(self, user, group):
        return self._group(group).user(user).delete()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CORPORA
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @CamomileErrorHandling()
    def getCorpus(self, corpus, history=False):
        """Get corpus by ID

        Parameters
        ----------
        corpus : str
            Corpus ID.
        history : boolean, optional
            Whether to return history.  Defaults to False.

        Returns
        -------
        corpus : dict

        """
        params = {'history': 'on'} if history else {}
        return self._corpus(corpus).get(params=params)

    @CamomileErrorHandling()
    def getCorpora(self, name=None, history=False, returns_id=False):
        """Get corpora

        Parameters
        ----------
        name : str, optional
            Get corpus by name.
        history : boolean, optional
            Whether to return history.  Defaults to False.
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.

        Returns
        -------
        corpora : list
            List of corpora.

        """
        params = {'history': 'on'} if history else {}
        if name:
            params['name'] = name

        result = self._corpus().get(params=params)
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def createCorpus(self, name, description=None, returns_id=False):
        """Create new corpus

        Parameters
        ----------
        name : str
            Corpus name.
        description : object, optional
            Corpus description. Must be JSON-serializable.
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.

        Returns
        -------
        corpus : dict
            Newly created corpus.
        """
        data = {'name': name,
                'description': description if description else {}}
        result = self._corpus().post(data=data)
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def updateCorpus(self, corpus, name=None, description=None):
        """Update corpus

        Parameters
        ----------
        corpus : str
            Corpus ID

        Returns
        -------
        corpus : dict
            Updated corpus.

        """
        data = {}

        if name:
            data['name'] = name

        if description:
            data['description'] = description

        return self._corpus(corpus).put(data=data)

    @CamomileErrorHandling()
    def deleteCorpus(self, corpus):
        """Delete corpus

        Parameters
        ----------
        corpus : str
            Corpus ID
        """
        return self._corpus(corpus).delete()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MEDIA
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @CamomileErrorHandling()
    def getMedium(self, medium, history=False):
        """Get medium by ID

        Parameters
        ----------
        medium : str
            Medium ID.
        history : boolean, optional
            Whether to return history.  Defaults to False.

        Returns
        -------
        medium : dict

        """
        params = {'history': 'on'} if history else {}
        return self._medium(medium).get(params=params)

    @CamomileErrorHandling()
    def getMedia(self, corpus=None, name=None, history=False,
                 returns_id=False, returns_count=False):
        """Get media

        Parameters
        ----------
        corpus : str, optional
            Corpus ID. Get media for this corpus.
        name : str, optional
            Filter medium by name.
        history : boolean, optional
            Whether to return history.  Defaults to False.
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.
        returns_count : boolean, optional.
            Returns count of media instead of media.

        Returns
        -------
        media : list
            List of media
        """

        params = {'history': 'on'} if history else {}
        if name:
            params['name'] = name

        if corpus:
            # /corpus/:id_corpus/medium
            route = self._corpus(corpus).medium
            if returns_count:
                # /corpus/:id_corpus/medium/count
                route = route.count
            result = route.get(params=params)
        else:
            # /medium/count does not exist
            if returns_count:
                raise ValueError('returns_count needs a corpus.')
            result = self._medium().get(params=params)

        return (self._id(result)
                if (returns_id and not returns_count)
                else result)

    @CamomileErrorHandling()
    def createMedium(self, corpus, name, url=None, description=None,
                     returns_id=False):
        """Add new medium to corpus

        Parameters
        ----------
        corpus : str
            Corpus ID.
        name : str
            Medium name.
        url : str, optional
            Relative path to medium files.
        description : object, optional
            Medium description.  Must be JSON-serializable.
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.

        Returns
        -------
        medium : dict
            Newly created medium.
        """
        medium = {'name': name,
                  'url': url if url else '',
                  'description': description if description else {}}

        result = self._corpus(corpus).medium.post(data=medium)
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def createMedia(self, corpus, media, returns_id=False):
        """Add several media to corpus

        Parameters
        ----------
        corpus : str
            Corpus ID.
        media : list
            List of media.
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.

        Returns
        -------
        media : list
            List of new media.
        """
        result = self._corpus(corpus).medium.post(data=media)
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def updateMedium(self, medium, name=None, url=None, description=None):
        """Update existing medium

        Parameters
        ----------
        medium : str
            Medium ID
        name : str, optional
        url : str, optional
        description : object, optional
            Must be JSON-serializable.

        Returns
        -------
        medium : dict
            Updated medium.
        """
        data = {}

        if name is not None:
            data['name'] = name

        if url is not None:
            data['url'] = url

        if description is not None:
            data['description'] = description

        return self._medium(medium).put(data=data)

    @CamomileErrorHandling()
    def deleteMedium(self, medium):
        """Delete existing medium

        Parameters
        ----------
        medium : str
            Medium ID
        """
        return self._medium(medium).delete()

    @CamomileErrorHandling()
    def streamMedium(self, medium, format=None):
        """Stream medium

        Parameters
        ----------
        medium : str
            Medium ID
        format : {'webm', 'mp4', 'ogv', 'mp3', 'wav'}, optional
            Streaming format.
        """

        if format is None:
            format = 'video'

        return self._medium(medium).get(format)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # LAYERS
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @CamomileErrorHandling()
    def getLayer(self, layer, history=False):
        """Get layer by ID

        Parameters
        ----------
        layer : str
            Layer ID.
        history : boolean, optional
            Whether to return history.  Defaults to False.

        Returns
        -------
        layer : dict

        """
        params = {'history': 'on'} if history else {}
        return self._layer(layer).get(params=params)

    @CamomileErrorHandling()
    def getLayers(self, corpus=None, name=None,
                  fragment_type=None, data_type=None,
                  history=False, returns_id=False):
        """Get layers

        Parameters
        ----------
        corpus : str, optional
            Corpus ID. Get layers for this corpus.
        name : str, optional
            Filter layer by name.
        fragment_type : str, optional
            Filter layer by fragment type.
        data_type : str, optional
            Filter layer by data type.
        history : boolean, optional
            Whether to return history.  Defaults to False.
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.

        Returns
        -------
        layers : list
            List of layers in corpus.
        """

        params = {'history': 'on'} if history else {}

        if name:
            params['name'] = name

        if fragment_type:
            params['fragment_type'] = fragment_type

        if data_type:
            params['data_type'] = data_type

        if corpus:
            result = self._corpus(corpus).layer.get(params=params)
        else:
            result = self._layer().get(params=params)

        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def createLayer(self, corpus,
                    name, description=None,
                    fragment_type=None, data_type=None,
                    annotations=None, returns_id=False):
        """Add new layer to corpus

        Parameters
        ----------
        corpus : str
            Corpus ID.
        name : str
            Layer name.
        description : object, optional
            Layer description.  Must be JSON-serializable.
        fragment_type : object, optional
            Layer fragment type.  Must be JSON-serializable.
        data_type : object, optional
            Layer data type.  Must be JSON-serializable.
        annotations : list, optional
            List of annotations.
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.

        Returns
        -------
        layer : dict
            Newly created layer.
        """
        layer = {'name': name,
                 'fragment_type': fragment_type if fragment_type else {},
                 'data_type': data_type if data_type else {},
                 'description': description if description else {},
                 'annotations': annotations if annotations else []}

        result = self._corpus(corpus).layer.post(data=layer)

        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def updateLayer(self, layer,
                    name=None, description=None,
                    fragment_type=None, data_type=None):
        """Update existing layer

        Parameters
        ----------
        layer : str
            Layer ID
        name : str, optional
        description : object, optional
            Must be JSON-serializable.
        fragment_type : str, optional
        data_type : str, optional

        Returns
        -------
        layer : dict
            Updated layer.
        """
        data = {}

        if name is not None:
            data['name'] = name

        if description is not None:
            data['description'] = description

        if fragment_type is not None:
            data['fragment_type'] = fragment_type

        if data_type is not None:
            data['data_type'] = data_type

        return self._layer(layer).put(data=data)

    @CamomileErrorHandling()
    def deleteLayer(self, layer):
        """Delete layer

        Parameters
        ----------
        layer : str
            Layer ID
        """
        return self._layer(layer).delete()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ANNOTATIONS
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @CamomileErrorHandling()
    def getAnnotation(self, annotation, history=False):
        """Get annotation by ID

        Parameters
        ----------
        annotation : str
            Annotation ID.
        history : boolean, optional
            Whether to return history.  Defaults to False.

        Returns
        -------
        annotation : dict

        """
        params = {'history': 'on'} if history else {}
        return self._annotation(annotation).get(params=params)

    @CamomileErrorHandling()
    def getAnnotations(self, layer=None, medium=None,
                       fragment=None, data=None,
                       history=False, returns_id=False,
                       returns_count=False):
        """Get annotations

        Parameters
        ----------
        layer : str, optional
            Filter annotations by layer.
        medium : str, optional
            Filter annotations by medium.
        fragment : optional
            Filter annotations by fragment.
        data : optional
            Filter annotations by data.
        history : boolean, optional
            Whether to return history.  Defaults to False.
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.
        returns_count : boolean, optional.
            Returns number of annotations instead of annotations

        Returns
        -------
        annotations : list
            List of annotations.

        """

        params = {'history': 'on'} if history else {}
        if medium:
            params['id_medium'] = medium
        if fragment:
            params['fragment'] = fragment
        if data:
            params['data'] = data

        if layer:
            # /layer/:id_layer/annotation
            route = self._layer(layer).annotation
            if returns_count:
                # /layer/:id_layer/annotation/count
                route = route.count
            result = route.get(params=params)

        else:
            # admin user only
            if returns_count:
                # /annotatoin/count does not exist
                raise ValueError('returns_count needs a layer')
            result = self._annotation().get(params=params)

        return (self._id(result)
                if (returns_id and not returns_count)
                else result)

    @CamomileErrorHandling()
    def createAnnotation(self, layer, medium=None, fragment=None, data=None,
                         returns_id=False):
        """Create new annotation

        Parameters
        ----------
        layer : str
        medium : str, optional
        fragment :
        data :
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.
        """
        annotation = {'id_medium': medium,
                      'fragment': fragment if fragment else {},
                      'data': data if data else {}}

        result = self._layer(layer).annotation.post(data=annotation)

        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def createAnnotations(self, layer, annotations, returns_id=False):
        """
                returns_id : boolean, optional.
            Returns IDs rather than dictionaries.
        """
        result = self._layer(layer).annotation.post(data=annotations)
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def updateAnnotation(self, annotation, fragment=None, data=None):
        """Update existing annotation

        Parameters
        ----------
        annotation : str
            Annotation ID
        fragment, data : object, optional

        Returns
        -------
        annotation : dict
            Updated annotation.
        """
        _data = {}

        if fragment is not None:
            _data['fragment'] = fragment

        if data is not None:
            _data['data'] = data

        return self._annotation(annotation).put(data=_data)

    @CamomileErrorHandling()
    def deleteAnnotation(self, annotation):
        """Delete existing annotation

        Parameters
        ----------
        annotation : str
            Annotation ID
        """
        return self._annotation(annotation).delete()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # QUEUES
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @CamomileErrorHandling()
    def getQueue(self, queue):
        """Get queue by ID

        Parameters
        ----------
        queue : str
            Queue ID.

        Returns
        -------
        queue : dict

        """
        return self._queue(queue).get()

    @CamomileErrorHandling()
    def getQueues(self, name=None, returns_id=False):
        """Get queues

        Parameters
        ----------
        name : str, optional
            Filter queues by name.
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.

        Returns
        -------
        queues : list or dict
        """

        params = {'name': name} if name else {}

        result = self._queue().get(params=params)
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def createQueue(self, name, description=None, returns_id=False):
        """Create queue

        Parameters
        ----------
        id_queue : str
            Queue ID
        returns_id : boolean, optional.
            Returns IDs rather than dictionaries.

        Returns
        -------
        queue : dict
            Newly created queue.
        """
        data = {'name': name, 'description': description}
        result = self._queue().post(data=data)
        return self._id(result) if returns_id else result

    @CamomileErrorHandling()
    def updateQueue(self, queue, name=None, description=None, elements=None):
        """Update queue

        Parameters
        ----------
        queue : str
            Queue ID

        Returns
        -------
        queue : dict
            Updated queue.
        """
        data = {}

        if name is not None:
            data['name'] = name

        if description is not None:
            data['description'] = description

        if elements is not None:
            data['list'] = elements

        return self._queue(queue).put(data=data)

    @CamomileErrorHandling()
    def enqueue(self, queue, elements):
        """Enqueue elements

        Parameters
        ----------
        queue : str
            Queue ID
        elements : list
            List of elements.

        Returns
        -------
        queue : dict
            Updated queue.
        """

        if not isinstance(elements, list):
            elements = [elements]

        return self._queue(queue).next.put(data=elements)

    @CamomileErrorHandling()
    def dequeue(self, queue):
        """Dequeue element

        Parameters
        ----------
        queue : str
            Queue ID

        Returns
        -------
        element : object
            Popped element from queue.
        """
        return self._queue(queue).next.get()

    @CamomileErrorHandling()
    def pick(self, queue):
        """(Non-destructively) pick first element of queue"""
        return self._queue(queue).first.get()

    @CamomileErrorHandling()
    def pickAll(self, queue):
        """(Non-destructively) pick all elements of queue"""
        return self._queue(queue).all.get()

    @CamomileErrorHandling()
    def pickLength(self, queue):
        """(Non-destructively) get number of elements in queue"""
        return self._queue(queue).length.get()

    @CamomileErrorHandling()
    def deleteQueue(self, queue):
        """Delete existing queue

        Parameters
        ----------
        queue : str
            Queue ID
        """
        return self._queue(queue).delete()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # RIGHTS
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # on a corpus

    @CamomileErrorHandling()
    def getCorpusPermissions(self, corpus):
        """Get permissions on existing corpus

        Parameters
        ----------
        corpus : str
            Corpus ID

        Returns
        -------
        permissions : dict
            Permissions on corpus.
        """
        return self._corpus(corpus).permissions.get()

    @CamomileErrorHandling()
    def setCorpusPermissions(self, corpus, permission, user=None, group=None):
        """Update permissions on a corpus

        Parameters
        ----------
        corpus : str
            Corpus ID
        user : str, optional
            User ID
        group : str, optional
            Group ID
        permission : 1 (READ), 2 (WRITE) or 3 (ADMIN)
            Read, Write or Admin privileges.

        Returns
        -------
        permissions : dict
            Updated permissions on the corpus.

        """
        if user is None and group is None:
            raise ValueError('')

        data = {'right': permission}

        if user:
            self._corpus(corpus).user(user).put(data=data)

        if group:
            self._corpus(corpus).group(group).put(data=data)

        return self.getCorpusPermissions(corpus)

    @CamomileErrorHandling()
    def removeCorpusPermissions(self, corpus, user=None, group=None):
        """Remove permissions on a corpus

        Parameters
        ----------
        corpus : str
            Corpus ID
        user : str, optional
            User ID
        group : str, optional
            Group ID

        Returns
        -------
        permissions : dict
            Updated permissions on the corpus.
        """

        if user is None and group is None:
            raise ValueError('')

        if user:
            self._corpus(corpus).user(user).delete()

        if group:
            self._corpus(corpus).group(group).delete()

        return self.getCorpusPermissions(corpus)

    # on a layer

    @CamomileErrorHandling()
    def getLayerPermissions(self, layer):
        """Get permissions on existing layer

        Parameters
        ----------
        layer : str
            Layer ID

        Returns
        -------
        permissions : dict
            Permissions on layer.
        """
        return self._layer(layer).permissions.get()

    @CamomileErrorHandling()
    def setLayerPermissions(self, layer, permission, user=None, group=None):
        """Update rights on a layer

        Parameters
        ----------
        layer : str
            Layer ID
        user : str, optional
            User ID
        group : str, optional
            Group ID
        permission : 1 (READ), 2 (WRITE) or 3 (ADMIN)
            Read, Write or Admin privileges.

        Returns
        -------
        permissions : dict
            Updated permissions on the layer.

        """
        if user is None and group is None:
            raise ValueError('')

        data = {'right': permission}

        if user:
            self._layer(layer).user(user).put(data=data)

        if group:
            self._layer(layer).group(group).put(data=data)

        return self.getLayerPermissions(layer)

    @CamomileErrorHandling()
    def removeLayerPermissions(self, layer, user=None, group=None):
        """Remove permissions on a layer

        Parameters
        ----------
        layer : str
            Layer ID
        user : str, optional
            User ID
        group : str, optional
            Group ID

        Returns
        -------
        permissions : dict
            Updated permissions on the layer.
        """

        if user is None and group is None:
            raise ValueError('')

        if user:
            self._layer(layer).user(user).delete()

        if group:
            self._layer(layer).group(group).delete()

        return self.getLayerPermissions(layer)

    # on a queue

    @CamomileErrorHandling()
    def getQueuePermissions(self, queue):
        """Get permissions on existing queue

        Parameters
        ----------
        queue : str
            Queue ID

        Returns
        -------
        permissions : dict
            Permissions on queue.
        """
        return self._queue(queue).permissions.get()

    @CamomileErrorHandling()
    def setQueuePermissions(self, queue, permission, user=None, group=None):
        """Update permissions on a queue

        Parameters
        ----------
        queue : str
            Queue ID
        user : str, optional
            User ID
        group : str, optional
            Group ID
        permission : 1 (READ), 2 (WRITE) or 3 (ADMIN)
            Read, Write or Admin privileges.

        Returns
        -------
        permissions : dict
            Updated permissions on the queue.

        """
        if user is None and group is None:
            raise ValueError('')

        data = {'right': permission}

        if user:
            self._queue(queue).user(user).put(data=data)

        if group:
            self._queue(queue).group(group).put(data=data)

        return self.getQueuePermissions(queue)

    @CamomileErrorHandling()
    def removeQueuePermissions(self, queue, user=None, group=None):
        """Remove permissions on a queue

        Parameters
        ----------
        queue : str
            Queue ID
        user : str, optional
            User ID
        group : str, optional
            Group ID

        Returns
        -------
        permissions : dict
            Updated permissions on the queue.
        """

        if user is None and group is None:
            raise ValueError('')

        if user:
            self._queue(queue).user(user).delete()

        if group:
            self._queue(queue).group(group).delete()

        return self.getQueuePermissions(queue)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # METADATA (Corpus, Layer, Medium)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #
    # CORPUS

    @CamomileErrorHandling()
    def getCorpusMetadata(self, corpus, path=None, file=False):
        """Get corpus metadata

        Parameters
        ----------
        corpus : str
            Corpus ID
        path : str, optional
            Metadata path. Defaults to root.
        file : boolean, optional
            If True and metadata is actually a file, returns the file content.
            Defaults to False.

        Returns
        -------
        metadata : object
            Metadata at 'path'.
        """
        return self.__getMetadata(self._corpus(corpus), path=path, file=file)

    @CamomileErrorHandling()
    def getCorpusMetadataKeys(self, corpus, path=None):
        """Get corpus metadata keys at 'path'

        Parameters
        ----------
        corpus : str
            Corpus ID
        path : str, optional
            Metadata path. Default to root.

        Returns
        -------
        keys : list
            List of metadata keys at 'path'.
        """
        return self.__getMetadataKeys(self._corpus(corpus), path=path)

    @CamomileErrorHandling()
    def setCorpusMetadata(self, corpus, metadata, path=None):
        """Set Corpus metadatas

        Parameters
        ----------
        corpus : str
            corpus ID
        metadata : dict
            metadatas
        """
        return self.__setMetadata(self._corpus(corpus), metadata, path=path)

    @CamomileErrorHandling()
    def sendCorpusMetadataFile(self, corpus, path, filepath):
        """Send corpus metadata file

        Parameters
        ----------
        corpus : str
            corpus ID
        path : str
            metadata path
        filepath : str
            metadata filepath
        """
        return self.__sendMetadataFile(self._corpus(corpus), path, filepath)

    @CamomileErrorHandling()
    def deleteCorpusMetadata(self, corpus, path):
        """Delete Corpus metadatas

        Parameters
        ----------
        corpus : str
            corpus ID
        path : str
            delete path
        """
        return self.__deleteMetadata(self._corpus(corpus), path)

    #
    # LAYER
    @CamomileErrorHandling()
    def getLayerMetadata(self, layer, path=None, file=False):
        """Get layer metadata

        Parameters
        ----------
        layer : str
            Layer ID
        path : str, optional
            Metadata path. Defaults to root.
        file : boolean, optional
            If True and metadata is actually a file, returns the file content.
            Defaults to False.

        Returns
        -------
        metadata : object
            Metadata at 'path'.
        """
        return self.__getMetadata(self._layer(layer), path=path, file=file)

    @CamomileErrorHandling()
    def getLayerMetadataKeys(self, layer, path=None):
        """Get layer metadata keys at 'path'

        Parameters
        ----------
        layer : str
            Layer ID
        path : str, optional
            Metadata path. Default to root.

        Returns
        -------
        keys : list
            List of metadata keys at 'path'.
        """
        return self.__getMetadataKeys(self._layer(layer), path=path)

    @CamomileErrorHandling()
    def setLayerMetadata(self, layer, metadata, path=None):
        """Set Layer metadatas

        Parameters
        ----------
        layer : str
            layer ID
        metadata : dict
            metadatas
        """
        return self.__setMetadata(self._layer(layer), metadata, path=path)

    @CamomileErrorHandling()
    def sendLayerMetadataFile(self, layer, path, filepath):
        """Send layer metadata file

        Parameters
        ----------
        layer : str
            layer ID
        path : str
            metadata path
        filepath : str
            metadata filepath
        """
        return self.__sendMetadataFile(self._layer(layer), path, filepath)

    @CamomileErrorHandling()
    def deleteLayerMetadata(self, layer, path):
        """Delete Layer metadatas

        Parameters
        ----------
        layer : str
            layer ID
        path : str
            delete path
        """
        return self.__deleteMetadata(self._layer(layer), path)

    #
    # MEDIUM
    @CamomileErrorHandling()
    def getMediumMetadata(self, medium, path=None, file=False):
        """Get medium metadata

        Parameters
        ----------
        medium : str
            Medium ID
        path : str, optional
            Metadata path. Defaults to root.
        file : boolean, optional
            If True and metadata is actually a file, returns the file content.
            Defaults to False.

        Returns
        -------
        metadata : object
            Metadata at 'path'.
        """
        return self.__getMetadata(self._medium(medium), path=path, file=file)

    @CamomileErrorHandling()
    def getMediumMetadataKeys(self, medium, path=None):
        """Get medium metadata keys at 'path'

        Parameters
        ----------
        medium : str
            Medium ID
        path : str, optional
            Metadata path. Default to root.

        Returns
        -------
        keys : list
            List of metadata keys at 'path'.
        """
        return self.__getMetadataKeys(self._medium(medium), path=path)

    @CamomileErrorHandling()
    def setMediumMetadata(self, medium, metadata, path=None):
        """Set Medium metadatas

        Parameters
        ----------
        medium : str
            medium ID
        metadata : dict
            metadatas
        path : str, optional
            metadata path
        """
        return self.__setMetadata(self._medium(medium), metadata, path=path)

    @CamomileErrorHandling()
    def sendMediumMetadataFile(self, medium, path, filepath):
        """Send medium metadata file

        Parameters
        ----------
        medium : str
            medium ID
        path : str
            metadata path
        filepath : str
            metadata filepath
        """
        return self.__sendMetadataFile(self._medium(medium), path, filepath)

    @CamomileErrorHandling()
    def deleteMediumMetadata(self, medium, path):
        """Delete Medium metadatas

        Parameters
        ----------
        medium : str
            medium ID
        path : str
            delete path
        """
        return self.__deleteMetadata(self._medium(medium), path)

    def __getMetadata(self, resource, path=None, file=False):

        if path is None:
            metadata = resource.metadata().get()
        else:
            metadata = resource.metadata(path).get()

        if file:
            metadata = b64decode(metadata['data']).decode()

        return metadata

    def __getMetadataKeys(self, resource, path=None):

        if path is None:
            return resource.metadata().get()

        return resource.metadata(path + '.').get()

    def __setMetadata(self, resource, metadata, path=None):

        if path is None:
            return resource.metadata().post(data=metadata)

        data = {}
        pointer = data
        tokens = path.split('.')
        for i in tokens[:-1]:
            pointer[i] = {}
            pointer = pointer[i]
        pointer[tokens[-1]] = metadata

        return resource.metadata().post(data=data)

    def __sendMetadataFile(self, resource, metadata_path, file_path):

        with open(file_path, 'rb') as f:
            content = f.read()

        data = {}
        pointer = data
        for i in metadata_path.split('.'):
            pointer[i] = {}
            pointer = pointer[i]

        pointer['type'] = 'file'
        pointer['filename'] = os.path.basename(file_path)
        pointer['data'] = b64encode(content).decode()

        return resource.metadata().post(data=data)

    def __deleteMetadata(self, resource, path):
        return resource.metadata(path).delete()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # SSE
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @CamomileErrorHandling()
    def __startListener(self):
        if self._thread == None:
            datas = self._api.listen.post();
            self._channel_id = datas.channel_id
            self._sseClient = SSEClient("%s/listen/%s" % (self._url, self._channel_id))
            self._thread = threading.Thread(target=self.__listener, name="SSEClient")
            self._thread.isRun = True
            self._thread.daemon = True
            self._thread.start()
        return


    def __listener(self):
        t = threading.currentThread()
        for msg in self._sseClient:
            if not t.isRun:
                break

            if msg.event in self._listenerCallbacks:
                self._listenerCallbacks[msg.event](json.loads(msg.data)['event'])


    @CamomileErrorHandling()
    def watchCorpus(self, corpus_id, callback):
        """ Watch corpus for:

        - Add and Remove medium `{'corpus': {:corpus}, 'event': {'add_medium': {:medium}}}`
        - Add and Remove layer `{'corpus': {:corpus}, 'event': {'add_layer': {:layer}}}`
        - Update corpus attributes `{'corpus': {:corpus}, 'event': {'update': ['description', 'name']}}}`

        Parameters
        ----------
        corpus_id : str
            corpus ID
        callback : function
            callback function
        """
        self.__startListener()
        result = self._api.listen(self._channel_id).corpus(corpus_id).put()
        if 'event' in result:
            self._listenerCallbacks['corpus:' + corpus_id] = callback
        return result

    @CamomileErrorHandling()
    def unwatchCorpus(self, corpus_id):
        """ UnWatch corpus

        Parameters
        ----------
        corpus_id : str
            corpus ID
        """
        result = self._api.listen(self._channel_id).corpus(corpus_id).delete()
        if 'success' in result:
            del self._listenerCallbacks['corpus:' + corpus_id]
        return result

    @CamomileErrorHandling()
    def watchLayer(self, layer_id, callback):
        """ Watch layer for:

        - Add and Remove annotation `{'layer': {:layer}, 'event': {'add_annotation': {:annotation}}}`
        - Update layer attributes `{'layer': {:layer}, 'event': {'update': ['name']}}}`

        Parameters
        ----------
        layer_id : str
            layer ID
        callback : function
            callback function
        """
        self.__startListener()
        result = self._api.listen(self._channel_id).layer(layer_id).put()
        if 'event' in result:
            self._listenerCallbacks['layer:' + layer_id] = callback
        return result

    @CamomileErrorHandling()
    def unwatchLayer(self, layer_id):
        """ UnWatch layer

        Parameters
        ----------
        layer_id : str
            layer ID
        """
        result = self._api.listen(self._channel_id).layer(layer_id).delete()
        if 'success' in result:
            del self._listenerCallbacks['layer:' + layer_id]
        return result

    @CamomileErrorHandling()
    def watchMedium(self, medium_id, callback):
        """ Watch medium for:

        - Update medium attributes `{'medium': {:medium}, 'event': {'update': ['url']}}}`

        Parameters
        ----------
        medium_id : str
            medium ID
        callback : function
            callback function
        """
        self.__startListener()
        result = self._api.listen(self._channel_id).medium(medium_id).put()
        if 'event' in result:
            self._listenerCallbacks['medium:' + medium_id] = callback
        return result

    @CamomileErrorHandling()
    def unwatchMedium(self, medium_id):
        """ UnWatch medium

        Parameters
        ----------
        medium_id : str
            medium ID
        """
        result = self._api.listen(self._channel_id).medium(medium_id).delete()
        if 'success' in result:
            del self._listenerCallbacks['medium:' + medium_id]
        return result


    @CamomileErrorHandling()
    def watchQueue(self, queue_id, callback):
        """ Watch queue for:

        - Push item in queue `{'queue': {:queue}, 'event': {'push_item': <new_number_of_items_in_queue>}}`
        - Pop item in queue `{'queue': {:queue}, 'event': {'pop_item': <new_number_of_items_in_queue>}}`

        Parameters
        ----------
        queue_id : str
            queue ID
        callback : function
            callback function
        """
        self.__startListener()
        result = self._api.listen(self._channel_id).queue(queue_id).put()
        if 'event' in result:
            self._listenerCallbacks['queue:' + queue_id] = callback
        return result

    @CamomileErrorHandling()
    def unwatchQueue(self, queue_id):
        """ UnWatch queue

        Parameters
        ----------
        queue_id : str
            queue ID
        """
        result = self._api.listen(self._channel_id).queue(queue_id).delete()
        if 'success' in result:
            del self._listenerCallbacks['queue:' + queue_id]
        return result


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # UTILS
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @CamomileErrorHandling()
    def getDate(self):
        return self._api.date.get()
