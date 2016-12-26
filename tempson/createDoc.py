# -*- coding: utf-8 -*-
from .generator import *

class createDoc(generator):

    def __init__(self, path):
        with open(path, 'r') as f:
            self.template = f.read()
        self.tokenizer()
