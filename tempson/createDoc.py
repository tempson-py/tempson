# -*- coding: utf-8 -*-

class createFragment(object):

    def __init__(self, template):
        self.template = template

    def render(self, variables):
        print self.template
