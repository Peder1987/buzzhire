from class_registry import Registry
from collections import OrderedDict


class WeightedRegistry(Registry):
    """A registry that returns registered classes in
    weight order.  The classes that are registered should have
    a 'weight' attribute.
    """
    def __init__(self, *args, **kwargs):
        self._ordered_dict = OrderedDict()
        super(WeightedRegistry, self).__init__(*args, **kwargs)

    def register(self, klass):
        super(WeightedRegistry, self).register(klass)
        key = self._get_key_from_class(klass)
        self._ordered_dict[key] = klass
        self._ordered_dict = OrderedDict(
            sorted(self._ordered_dict.iteritems(),
                   key=lambda item: item[1].weight))

    def __iter__(self):
        return self._ordered_dict.__iter__()


class classproperty(object):
    """Decorator for class-level properties.
    
    Usage:
    
        class MyClass(object):
            @classproperty(cls):
                return cls.something
    """
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
