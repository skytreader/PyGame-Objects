import uuid

"""
Classes necessary for the Observer pattern. Slightly patterned after Java's
Observer pattern framework. But I am calling it Subscriber because I am hipster.

(I even think this is the proper term, with the PUB/SUB pattern referenced more
frequently.)

@author Chad Estioco
"""

class Publisher(object):
    
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
    
    def notify_subscribers(self, **arg_bundle):
        for o in self.__observers:
            o.notify(self, arg_bundle)

class Subscriber(object):
    
    def __init__(self):
        self.id = uuid.uuid1()

    def __eq__(self, subscriber_):
        return self.id == subscriber_.id
    
    def notify(self, observed, **arg_bundle):
        """
        @param observed
          The observable object that trigerred the function call.
        @param arg_bundle
          Holds data which implementors may need responding to the notification.
        """
        pass
