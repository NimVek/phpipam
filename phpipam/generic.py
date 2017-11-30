#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
import json
from mcrypt import MCRYPT
import base64

import logging
__log__ = logging.getLogger(__name__)


class API(object):
    controller = {}

    def __init__(self, url, app_id, key, user, password):
        self.url = url
        self.app_id = app_id
        self.app_key = key
        self.user = user
        self.password = password
        self.token = False

    def __getattr__(self, name):
        if name in API.controller:
            tmp = API.controller[name](self)
            self.__setattr__(name, tmp)
            return tmp
        else:
            raise AttributeError

    def login(self, username, password):
        response = requests.post(
            self.base + 'user/', auth=HTTPBasicAuth(username, password))
        if response.status_code != 200:
            logger.error("Login Problem %s " % response.status_code)
            logger.error(response.text)
        ticket = json.loads(response.text)
        self.token = ticket['data']['token']

    def execute(self, method, controller, ids, parameter):
        url = self.url
        headers = {'Content-Type': 'application/json'}
        data = parameter
        if self.key:
            data = {'controller': controller}
            for idx, value in enumerate(ids):
                key = 'id' % (idx + 1) if idx else 'id'
                data[key] = value
            data.update(parameter)
            cryptor = MCRYPT('rijndael-256', 'ecb')
            cryptor.init(self.app_key)
            data = {
                'app_id':
                self.app_id,
                'enc_request':
                base64.b64encode(bytes(cryptor.encrypt(json.dumps(data))))
            }
        else:
            url += '/'.join([self.app_id, controller] + ids) + '/'
            headers['token'] = self.token
        response = requests.request(
            method, url, headers=headers, data=data)
        tmp = json.loads(response.text)
        result = True if tmp['success'] else False
        if result and 'data' in tmp:
            result = tmp['data']
        else:
            logger.info(tmp['message'])
        return result


class Item(object):
    def __init__(self, controller, item):
        self._controller = controller
        if type(item) in [str, int]:
            self._data = controller.item(_id)
        else:
            self._data = item

    def get(self, name):
        return self._data[name]

    def set(self, name, value):
        self._data[name] = value
        self._controller.patch(self._data['id'], {name: value})


class Controller(object):
    def __init__(self, api, name):
        self.api = api
        self.name = name

    def _execute(self, method, identifiers=[], params=[]):
        return self.api.execute(method, self.name, identifiers, params)

    def get(self, _id):
        return self.api.execute("GET", self.name, _id)

    def patch(self, _id, values):
        assert (type(values) == dict)
        return self.api.execute("PATCH", self.name, _id, values)
