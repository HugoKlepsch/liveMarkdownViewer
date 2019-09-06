"""
Observer pattern implementation
"""
from abc import ABCMeta, abstractmethod

class Observer:
    """Observer mixin"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, observable, arg):
        """
        Called when the observable is updated.
        :param observable: The observable that was updated.
        :param arg: Optional argument from the observable.
        """


class Observable:
    """Observable mixin"""
    def __init__(self):
        """Constructor"""
        self.obs = []

    def add_observer(self, observer):
        """
        Register an observer.
        :param Observer observer: The observer to register.
        """
        if observer not in self.obs:
            self.obs.append(observer)

    def delete_observer(self, observer):
        """
        Deregister an observer.
        :param Observer observer: The observer to deregister.
        """
        self.obs.remove(observer)

    def delete_observers(self):
        """Deregister all observers"""
        self.obs = []

    def count_observers(self):
        """The number of observers"""
        return len(self.obs)

    def notify_observers(self, arg=None):
        """
        Call each registered observer's update() method with this, and an optional arg.
        :param any arg: Optional argument to pass to observers.
        """
        for observer in self.obs:
            observer.update(self, arg)
