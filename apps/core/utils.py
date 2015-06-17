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
