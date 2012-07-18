#! usr/bin/env python

from ..components.subscriber_pattern import Observable
from ..components.subscriber_pattern import Observer

import random

"""
Sample use of the observer pattern.
"""

class Magazine(Observable):
	
	def __init__(self, magazine_name):
		super(Magazine, self).__init__()
		self.__name = magazine_name
	
	@property
	def name(self):
		return self.__name
	
	@name.setter
	def name(self, n):
		self.__name = n
	
	def make_issue(self):
		super(Magazine,self).notify_subscribers(self.name)

class Subscriber(Observer):
	
	def __init__(self, name):
		self.__name = name
	
	def notify(self, o, arg_bundle):
		print self.__name + " got an issue of " + arg_bundle + " from " + str(o)

subscribers = [Subscriber("Homer"), Subscriber("Lenny"), Subscriber("Karl"), Subscriber("Barney")]
magazines = [Magazine("MAD"), Magazine("Scientific American"), Magazine("Reader's Digest")]

for mag in magazines:
	for person in subscribers:
		mag.subscribe(person)

for i in range(5):
	mag_index = random.randint(0, 2)
	magazines[mag_index].make_issue()
