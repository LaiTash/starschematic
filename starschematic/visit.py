# visit.py

class Visitor(object):
    def visit(self, item, *args, **kwargs):
        for cls in item.__class__.mro():
            method_name = 'visit_%s' % cls.__name__
            method = getattr(self, method_name, None)
            if method:
                return method(item, *args, **kwargs)
        raise KeyError(item.__class__.__name__)