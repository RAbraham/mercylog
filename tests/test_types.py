import pytest
from mercylog.types import is_safe, v, relation

def test_safety():
    X = v('X')
    Y = v('Y')
    person = relation('person')
    man = relation('man')

    assert is_safe(person(X), [man(X)])
    assert not is_safe(person(X, Y), [man(X)])
    assert is_safe(person(X), [man(X, Y)])
    assert is_safe(person('Rajiv'), [])
