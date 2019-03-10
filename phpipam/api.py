#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
import json
#from mcrypt import MCRYPT
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
            tmp = API.controller[name](self, name)
            self.__setattr__(name, tmp)
            return tmp
        else:
            raise AttributeError

    def login(self, username, password):
        response = requests.post(
            self.url + '/' + self.app_id + '/user/',
            auth=HTTPBasicAuth(username, password))
        if response.status_code != 200:
            __log__.error("Login Problem %s ", response.status_code)
            __log__.error(response.text)

        __log__.debug(response.text)
        ticket = json.loads(response.text)
        self.token = ticket['data']['token']

    def execute(self, method, controller, ids, parameter):
        url = self.url
        headers = {'Content-Type': 'application/json'}
        data = parameter
        if self.app_key:
            data = {'controller': controller}
            for idx, value in enumerate(ids):
                key = 'id' % (idx + 1) if idx else 'id'
                data[key] = value
            data.update(parameter)
            #            cryptor = MCRYPT('rijndael-256', 'ecb')
            #            cryptor.init(self.app_key)
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
            method, url, headers=headers, data=json.dumps(data))
        tmp = json.loads(response.text)
        __log__.debug(url)
        __log__.debug(headers)
        __log__.debug(data)
        __log__.debug(tmp)
        result = True if tmp['success'] else False
        if result and 'data' in tmp:
            result = tmp['data']
        else:
            __log__.info(tmp['message'])
        return result
