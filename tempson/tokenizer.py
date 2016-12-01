# -*- coding: utf-8 -*-

import re

class tokenizer (object):

    def __init__ (self, template, config):
        self._template = template
        self._config = config

    def regexGen (self):
        return re.compile(r'(%s.*?%s|%s.*?%s)' % (  
            self._config['leftDelimiters'],
            self._config['rightDelimiters'],
            self._config['leftBlockDelimiters'],
            self._config['rightBlockDelimiters']
        ))

    def splitTemplate (self, regex):
        return regex.split(self._template)

    def tokenGen (self):
        regex = self.regexGen()
        return self.splitTemplate(regex)
