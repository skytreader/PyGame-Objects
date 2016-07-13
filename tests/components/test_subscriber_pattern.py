import unittest

from components.subscriber_pattern import Publisher, Subscriber

class PublisherMock(Publisher):
    
    def __init__(self):
        super(PublisherMock, self).__init__()

class SubscriberMock(Subscriber):
    
    def __init__(self):
        self.notified = False

    def notify(self, observed, arg_bundle=None):
        self.notified = True

class SubscriberPatternTest(unittest.TestCase):
    
    def setUp(self):
        self.publisher = PublisherMock()
        self.subscriber = SubscriberMock()

    def test_no_sub(self):
        self.assertFalse(self.subscriber.notified)
        self.publisher.notify_subscribers()
        self.assertFalse(self.subscriber.notified)

    def test_sub(self):
        self.assertFalse(self.subscriber.notified)
        self.publisher.subscribe(self.subscriber)
        self.publisher.notify_subscribers()
        self.assertTrue(self.subscriber.notified)
