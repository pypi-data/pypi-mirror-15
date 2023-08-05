"""Integration tests for nested attributes."""
# pylint: disable=missing-docstring,no-self-use,attribute-defined-outside-init,no-member,misplaced-comparison-constant


from unittest.mock import patch
import logging

from expecter import expect

import yorm

from . import strip


@yorm.attr(status=yorm.types.Boolean)
@yorm.attr(checked=yorm.types.Integer)
class StatusDictionary(yorm.types.Dictionary):

    def __init__(self, status, checked):
        self.status = status
        self.checked = checked
        if self.checked == 42:
            raise RuntimeError


@yorm.attr(all=yorm.types.Float)
class NestedList3(yorm.types.List):

    def __repr__(self):
        return "<nested-list-3 {}>".format((id(self)))


@yorm.attr(nested_list_3=NestedList3)
@yorm.attr(number=yorm.types.Float)
class NestedDictionary3(yorm.types.AttributeDictionary):

    def __init__(self):
        super().__init__()
        self.number = 0
        self.nested_list_3 = []

    def __repr__(self):
        print(self.number)  # trigger a potential recursion issue
        return "<nested-dictionary-3 {}>".format((id(self)))


@yorm.attr(all=yorm.types.Float)
class NestedList2(yorm.types.List):

    def __repr__(self):
        return "<nested-list-2 {}>".format((id(self)))


@yorm.attr(nested_dict_3=NestedDictionary3)
@yorm.attr(number=yorm.types.Float)
class NestedDictionary2(yorm.types.AttributeDictionary):

    def __init__(self):
        super().__init__()
        self.number = 0

    def __repr__(self):
        print(self.number)  # trigger a potential recursion issue
        return "<nested-dictionary-2 {}>".format((id(self)))


@yorm.attr(nested_list_2=NestedList2)
@yorm.attr(number=yorm.types.Float)
class NestedDictionary(yorm.types.AttributeDictionary):

    def __init__(self):
        super().__init__()
        self.number = 0
        self.nested_list_2 = []

    def __repr__(self):
        return "<nested-dictionary {}>".format((id(self)))


@yorm.attr(all=NestedDictionary2)
class NestedList(yorm.types.List):

    def __repr__(self):
        return "<nested-list {}>".format((id(self)))


@yorm.attr(nested_dict=NestedDictionary)
@yorm.attr(nested_list=NestedList)
@yorm.sync("sample.yml")
class Top:

    def __init__(self):
        self.nested_list = []
        self.nested_dict = {}

    def __repr__(self):
        return "<top {}>".format((id(self)))


@patch('yorm.settings.fake', True)
class TestNestedOnce:

    def test_append_triggers_save(self):
        top = Top()
        logging.info("Appending dictionary to list...")
        top.nested_list.append({'number': 1})
        assert strip("""
        nested_dict:
          nested_list_2: []
          number: 0.0
        nested_list:
        - nested_dict_3:
            nested_list_3: []
            number: 0.0
          number: 1.0
        """) == top.__mapper__.text

    def test_set_by_index_triggers_save(self):
        top = Top()
        top.nested_list = [{'number': 1.5}]
        assert strip("""
        nested_dict:
          nested_list_2: []
          number: 0.0
        nested_list:
        - nested_dict_3:
            nested_list_3: []
            number: 0.0
          number: 1.5
        """) == top.__mapper__.text
        top.nested_list[0] = {'number': 1.6}
        assert strip("""
        nested_dict:
          nested_list_2: []
          number: 0.0
        nested_list:
        - nested_dict_3:
            nested_list_3: []
            number: 0.0
          number: 1.6
        """) == top.__mapper__.text

    def test_get_by_index_triggers_load(self):
        top = Top()
        top.__mapper__.text = strip("""
        nested_list:
        - number: 1.7
        """)
        assert 1.7 == top.nested_list[0].number

    def test_delete_index_triggers_save(self):
        top = Top()
        top.nested_list = [{'number': 1.8}, {'number': 1.9}]
        assert strip("""
        nested_dict:
          nested_list_2: []
          number: 0.0
        nested_list:
        - nested_dict_3:
            nested_list_3: []
            number: 0.0
          number: 1.8
        - nested_dict_3:
            nested_list_3: []
            number: 0.0
          number: 1.9
        """) == top.__mapper__.text
        del top.nested_list[0]
        assert strip("""
        nested_dict:
          nested_list_2: []
          number: 0.0
        nested_list:
        - nested_dict_3:
            nested_list_3: []
            number: 0.0
          number: 1.9
        """) == top.__mapper__.text

    def test_set_dict_as_attribute_triggers_save(self):
        top = Top()
        top.nested_dict.number = 2
        assert strip("""
        nested_dict:
          nested_list_2: []
          number: 2.0
        nested_list: []
        """) == top.__mapper__.text


@patch('yorm.settings.fake', True)
class TestNestedTwice:

    def test_nested_list_item_value_change_triggers_save(self):
        top = Top()
        top.nested_list = [{'number': 3}]
        assert strip("""
        nested_dict:
          nested_list_2: []
          number: 0.0
        nested_list:
        - nested_dict_3:
            nested_list_3: []
            number: 0.0
          number: 3.0
        """) == top.__mapper__.text
        top.nested_list[0].number = 4
        assert strip("""
        nested_dict:
          nested_list_2: []
          number: 0.0
        nested_list:
        - nested_dict_3:
            nested_list_3: []
            number: 0.0
          number: 4.0
        """) == top.__mapper__.text

    def test_nested_dict_item_value_change_triggers_save(self):
        top = Top()
        top.nested_dict = {'nested_list_2': [5]}
        assert strip("""
        nested_dict:
          nested_list_2:
          - 5.0
          number: 0.0
        nested_list: []
        """) == top.__mapper__.text
        top.nested_dict.nested_list_2.append(6)
        assert strip("""
        nested_dict:
          nested_list_2:
          - 5.0
          - 6.0
          number: 0.0
        nested_list: []
        """) == top.__mapper__.text

    def test_dict_in_list_value_change_triggers_save(self):
        top = Top()
        top.nested_list.append(None)
        top.nested_list[0].nested_dict_3.number = 8
        assert strip("""
        nested_dict:
          nested_list_2: []
          number: 0.0
        nested_list:
        - nested_dict_3:
            nested_list_3: []
            number: 8.0
          number: 0.0
        """) == top.__mapper__.text

    def test_list_in_dict_append_triggers_save(self):
        top = Top()
        top.nested_list.append(None)
        top.nested_list.append(None)
        for nested_dict_2 in top.nested_list:
            nested_dict_2.number = 9
            nested_dict_2.nested_dict_3.nested_list_3.append(10)
        assert strip("""
        nested_dict:
          nested_list_2: []
          number: 0.0
        nested_list:
        - nested_dict_3:
            nested_list_3:
            - 10.0
            number: 0.0
          number: 9.0
        - nested_dict_3:
            nested_list_3:
            - 10.0
            number: 0.0
          number: 9.0
        """) == top.__mapper__.text


@patch('yorm.settings.fake', True)
class TestAliases:

    @yorm.attr(var4=NestedList3)
    @yorm.attr(var5=StatusDictionary)
    @yorm.sync("fake/path")
    class Sample:

        def __repr__(self):
            return "<sample {}>".format(id(self))

    def setup_method(self, _):
        self.sample = self.Sample()

    @staticmethod
    def _log_ref(name, var, ref):
        logging.info("%s: %r", name, var)
        logging.info("%s_ref: %r", name, ref)
        logging.info("%s ID: %s", name, id(var))
        logging.info("%s_ref ID: %s", name, id(ref))
        assert id(ref) == id(var)
        assert ref == var

    def test_alias_list(self):
        var4_ref = self.sample.var4
        self._log_ref('var4', self.sample.var4, var4_ref)
        assert [] == self.sample.var4

        logging.info("Appending 42 to var4_ref...")
        var4_ref.append(42)
        self._log_ref('var4', self.sample.var4, var4_ref)
        assert [42] == self.sample.var4

        logging.info("Appending 2015 to var4_ref...")
        var4_ref.append(2015)
        assert [42, 2015] == self.sample.var4

    def test_alias_dict(self):
        var5_ref = self.sample.var5
        self._log_ref('var5', self.sample.var5, var5_ref)
        assert {'status': False, 'checked': 0} == self.sample.var5

        logging.info("Setting status=True in var5_ref...")
        var5_ref['status'] = True
        self._log_ref('var5', self.sample.var5, var5_ref)
        assert {'status': True, 'checked': 0} == self.sample.var5

        logging.info("Setting status=False in var5_ref...")
        var5_ref['status'] = False
        self._log_ref('var5', self.sample.var5, var5_ref)
        assert {'status': False, 'checked': 0} == self.sample.var5

    def test_alias_dict_in_list(self):
        top = Top()
        top.nested_list.append(None)
        ref1 = top.nested_list[0]
        ref2 = top.nested_list[0].nested_dict_3
        ref3 = top.nested_list[0].nested_dict_3.nested_list_3
        assert id(ref1) == id(top.nested_list[0])
        assert id(ref2) == id(top.nested_list[0].nested_dict_3)
        assert id(ref3) == id(top.nested_list[0].nested_dict_3.nested_list_3)

    def test_alias_list_in_dict(self):
        top = Top()
        logging.info("Updating nested attribute...")
        top.nested_dict.number = 1
        logging.info("Grabbing refs...")
        ref1 = top.nested_dict
        ref2 = top.nested_dict.nested_list_2
        assert id(ref1) == id(top.nested_dict)
        assert id(ref2) == id(top.nested_dict.nested_list_2)

    def test_custom_init_is_invoked(self):
        self.sample.__mapper__.text = "var5:\n  checked: 42"
        with expect.raises(RuntimeError):
            print(self.sample.var5)
