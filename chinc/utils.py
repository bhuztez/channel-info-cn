from operator import itemgetter


class NamedTupleBase(type):

    def __new__(klass, name, bases, attrs):
        if bases == (tuple,):
            return type.__new__(klass, name, bases, attrs)

        fields = attrs.get('__fields__', ())

        for i, field in enumerate(fields):
            attrs[field] = property(itemgetter(i), doc='field {i:d}'.format(i=i))

        return type.__new__(klass, name, bases, attrs)


class NamedTuple(tuple):
    __metaclass__ = NamedTupleBase

    def __new__(_cls, **kwargs):
        return tuple.__new__(_cls, (kwargs.get(f, None) for f in _cls.__fields__))

    def __repr__(self):
        return "{type}({fields})".format(
            type=self.__class__.__name__,
            fields=", ".join(
                "{name}={value!r}".format(name=name, value=value)
                for name, value in zip(self.__fields__, self)))

    def __call__(self, **kwargs):
        d = dict(zip(self.__fields__, self))
        d.update(kwargs)
        return self.__class__(**d)
