import pytest

from snms.core.db.sqlalchemy.util.models import auto_table_args


@pytest.mark.parametrize(('args', 'kw', 'expected'), (
    # simple tuples
    ([('foo',), ('bar',)],
     {},
     ('foo', 'bar')),
    # simple dicts
    ([{'a': 'b'}, {'c': 'd'}],
     {},
     ({'a': 'b', 'c': 'd'})),
    # all possible types
    ([('foo',), {'a': 'b'}, ('bar', {'a': 'c', 'x': 'y'})],
     {},
     ('foo', 'bar', {'a': 'c', 'x': 'y'})),
    # all empty
    ([], {}, ()),
    ([()], {}, ()),
    # extra kwargs
    ([('foo',), ('bar',)],
     {'troll': 'fish'},
     ('foo', 'bar', {'troll': 'fish'})),
))
def test_auto_table_args(args, kw, expected):
    classes = []
    for i, arg in enumerate(args):
        name = 'Test{}'.format(i)
        classes.append(type(name, (object,), {'_{}__auto_table_args'.format(name): arg}))
    cls = type('Test', tuple(classes), {})
    assert auto_table_args(cls, **kw) == expected
