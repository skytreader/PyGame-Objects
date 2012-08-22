#! usr/bin/env python

from ...components.core import GameConfig
from ...components.subscriber_pattern import Observer

"""
Tests the subscriber-patter-related decorator of GameConfig.

TODO: Better tests! (Maybe, unit tests?)

@author Chad Estioco
"""

class ConfigObserver(Observer):
	
	def notify(self, observed, arg_bundle = None):
		print "Configurations has changed!"

config = GameConfig()
config.subscribe(ConfigObserver())
config.clock_rate = 12
config.window_size = [500, 500]
config.window_title = "Config Subscriber Test"
