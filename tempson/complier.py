# -*- coding: utf-8 -*-

import re
from .error import *

""" Default delimiters
    defaultConfig = {
        'leftDelimiters':          '{{',
        'rightDelimiters':         '}}',
        'leftBlockDelimiters':     '{%',
        'rightBlockDelimiters':    '%}',
        'leftCommentsDelimiters':  '{*',
        'rightCommentsDelimiters': '*}',
        'leftRawDelimiters':       '{{{',
        'rightRawDelimiters':      '}}}'
    }
"""

class complier(object):

    def __init__ (self, template):
        self._template = template

    def regexGen (self):
        return re.compile(r'([\\]*%s.*?[\\]*%s|[\\]*%s.*?[\\]*%s|[\\]*%s.*?[\\]*%s|[\\]*%s.*?[\\]*%s)' % (
            self._config['leftDelimiters'],
            self._config['rightDelimiters'],
            self._config['leftBlockDelimiters'],
            self._config['rightBlockDelimiters'],
            self._config['leftCommentsDelimiters'],
            self._config['rightCommentsDelimiters'],
            self._config['leftRawDelimiters'],
            self._config['rightRawDelimiters']
        ))

    def splitTemplate (self, regex):
        return regex.split(self._template)

    def tokenize (self):
        # template string
        t = self._template

        # throw a error when template is not a string
        if not isinstance(t, str):
            raise TemplateTypeError(type(t))

        # template length
        t_length = len(t)
        # current offset
        cur = 0
        # token list
        tokens = []
        token = {
            'type': None,
            'value': ''
        }
        # string template
        isString = False

        while cur < t_length:
            # switch string flag if test string symbol: '/"
            if t[cur] == '\'' or t[cur] == '\"':
                isString = not isString

            # jump every symbol if string flag is True
            if isString:
                token['value'] += t[cur]
                cur += 1
                continue

            # delimiter end
            if t[cur] == '}':
                if t[cur + 1] == '}':
                    if t[cur + 2] == '}':
                        token['value'] += '}}}'
                        cur += 3
                        tokens.append(token)
                        token = {
                            'type': None,
                            'value': ''
                        }
                    else:
                        token['value'] += '}}'
                        cur += 2
                        tokens.append(token)
                        token = {
                            'type': None,
                            'value': ''
                        }

            if t[cur] == '%':
                if t[cur + 1] == '}':
                    token['value'] += '%}'
                    cur += 2
                    tokens.append(token)
                    token = {
                        'type': None,
                        'value': ''
                    }

            if t[cur] == '*':
                if t[cur + 1] == '}':
                    token['value'] += '*}'
                    cur += 2
                    tokens.append(token)
                    token = {
                        'type': None,
                        'value': ''
                    }

            # delimiter start
            if t[cur] == '{':

                # varible expression
                if t[cur + 1] == '{':
                    # save last token
                    if token['type'] == 'HTML':
                        tokens.append(token)

                    if t[cur + 2] == '{':
                        # define a new token
                        token = {
                            'type': 'RAWEXP',
                            'value': '{{{'
                        }

                        # next char
                        cur += 3
                    else:
                        # define a new token
                        token = {
                            'type': 'VAREXP',
                            'value': '{{'
                        }
                        
                        # next char
                        cur += 2

            if t[cur] == '{':

                # varible expression
                if t[cur + 1] == '%':
                    # save last token
                    if token['type'] == 'HTML':
                        tokens.append(token)

                    # define a new token
                    token = {
                        'type': 'VAREXP',
                        'value': '{%'
                    }

                    # next char
                    cur += 2

            if t[cur] == '{':

                # varible expression
                if t[cur + 1] == '*':
                    # save last token
                    if token['type'] == 'HTML':
                        tokens.append(token)

                    # define a new token
                    token = {
                        'type': 'COMEXP',
                        'value': '{*'
                    }

                    # next char
                    cur += 2

            # default is HTML
            if token['type'] == None:
                token = {
                    'type': 'HTML',
                    'value': ''
                }

            token['value'] += t[cur]

            cur += 1

            if cur == t_length:
                tokens.append(token)

        return tokens
