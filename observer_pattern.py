#! usr/bin/env python

"""
Classes necessary for the Observer pattern. Slightly patterned
after Java's Observer pattern framework.
"""

class Observable(object):
	
	def __init__(self):
		self.__observers = []
	
	def subscribe(self, observer):
		"""
		@param observer
		  An instance of Observer.
		"""
		self.__observers.append(observer)
	
	def unsubscribe(self, observer):
		i = 0
		
		for o in self.__observers:
			if o.__eq__(observer):
				self.__observers.pop(i)
				return
	
	def notify_subscribers(self, arg_bundle = None):
		for o in self.__observers:
			o.notify(self, arg_bundle)

class Observer(object):
	
	def notify(self, o, arg_bundle = None):
		"""
		@param o
		  The observable object that trigerred the function call.
		@param arg_bundle
		  Holds data which implementors may need responding to the notification.
		"""
		pass
