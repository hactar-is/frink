# -*- coding: utf-8 -*-

from app.models import Parent, Child


kid_dict = {
    'name': 'Charlie'
}


mum_dict = {
    'name': 'Alice',
}


dad_dict = {
    'name': 'Bob'
}


def test_create_child(base):
    obj = Child(kid_dict)
    obj.save()
    assert obj.id is not None
    assert obj.name == kid_dict['name']


def test_create_mum(base):
    obj = Parent(mum_dict)
    obj.save()
    assert obj.id is not None
    assert obj.name == mum_dict['name']


def test_create_dad(base):
    obj = Parent(dad_dict)
    kid = Child(kid_dict)
    obj.child = kid
    obj.save()
    assert obj.id is not None
    assert obj.name == dad_dict['name']
    assert kid.id is not None
    assert kid.name == kid_dict['name']
    # test to make sure we can load that child
    kid_loaded = Child.query.first(name=kid_dict['name'])
    dad_loaded = Parent.query.first(name=dad_dict['name'])
    assert kid_loaded is not None
    assert dad_loaded is not None
    assert dad_loaded.child == kid_loaded
