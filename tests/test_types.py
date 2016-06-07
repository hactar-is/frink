# -*- coding: utf-8 -*-

from app.models import Parent, Child


kid_dict = {
    'name': 'Charlie'
}


mum_dict = {
    'name': 'Alice'
}


dad_dict = {
    'name': 'Bob'
}


def test_create_child():
    obj = Child(kid_dict)
    obj.save()
    assert obj.id is not None
    assert obj.name == kid_dict['name']


def test_create_mum():
    obj = Parent(mum_dict)
    obj.save()
    assert obj.id is not None
    assert obj.name == mum_dict['name']


def test_create_dad():
    obj = Parent(dad_dict)
    obj.save()
    assert obj.id is not None
    assert obj.name == dad_dict['name']
