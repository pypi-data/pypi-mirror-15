# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser


class AdvertiserReport(object):
    def __init__(self, config_filename):
        self.config_parser = ConfigParser()
        self.config_parser.read(config_filename)
        self.api_key = self.config_parser.get('main', 'api_key')
