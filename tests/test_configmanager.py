import pytest

from src.configmanager import ConfigManager


class TestConfigManager:
    def test_inits_ok(self):
        assert ConfigManager() is not None

    def test_get_undefined_attr_raises_attribute_error(self):
        with pytest.raises(AttributeError):
            c = ConfigManager()
            c.x()

    def test_define_attribute_with_no_type_and_no_value(self):
        c = ConfigManager()
        c('a')
        assert c.a is None

    def test_define_attribute_with_no_type_and_no_value_can_be_set_any_value(self):
        c = ConfigManager()
        c('a')
        c.a = 1
        assert c.a == 1
        c.a = 'str'
        assert c.a == 'str'
        c.a = None
        assert c.a is None

    def test_define_attribute_with_value_and_no_type_and_update_it(self):
        c = ConfigManager()
        c('a', 1)
        assert c.a == 1
        c.a = 2
        assert c.a == 2

    def test_define_attribute_with_value_and_no_type_and_update_it_with_different_type(self):
        with pytest.raises(TypeError):
            c = ConfigManager()
            c('a', 1)
            assert c.a == 1
            c.a = 'str'
            assert c.a == 2

    def test_define_attribute_with_value_type_and_no_type_and_update_it(self):
        c = ConfigManager()
        c('a', 1, type_=float)
        assert c.a == 1
        c.a = 2
        assert c.a == 2.0

    def test_define_attribute_with_2_levels(self):
        c = ConfigManager()
        c('a.b', 1)
        assert c.a.b == 1

    def test_define_attribute_with_2_levels_and_typecast(self):
        c = ConfigManager()
        c('a.b', 1, str)
        assert c.a.b == '1'

    def test_define_attribute_with_2_levels_and_raise_type_error(self):
        with pytest.raises(TypeError):
            c = ConfigManager()
            c('a.b', 1)
            c.a.b = 'a'

    def test_define_attribute_with_2_levels_and_prevent_parent_to_be_overwritten(self):
        with pytest.raises(AttributeError):
            c = ConfigManager()
            c('a.b', 1, str)
            c.a = 1

    def test_define_attribute_and_get_it_as_dict(self):
        c = ConfigManager()
        c('a')
        c.a = 1
        assert c['a'] == 1

    def test_define_2_level_attribute_and_get_it_as_dict(self):
        c = ConfigManager()
        c('a.b')
        c.a.b = 1
        assert c['a'].b == 1
        assert c['a.b'] == 1

    def test_set_1_level_item(self):
        c = ConfigManager()
        c('a')
        assert c.a is None
        c['a'] = 1
        assert c.a == 1

    def test_set_1_level_non_existing_item_raises_error(self):
        with pytest.raises(KeyError):
            c = ConfigManager()
            c['a'] = 1

    def test_set_2_level_setting_item(self):
        c = ConfigManager()
        c('a.b', type_=int)
        c['a.b'] = '1'
        assert c.a.b == 1
        assert c['a.b'] == 1
        assert c.a['b'] == 1
        assert c['a'].b == 1

    def test_del_attr(self):
        c = ConfigManager()
        c('a.b', 1)
        del c.a
        with pytest.raises(AttributeError):
            assert c.a is None

    def test_del_2_level_attr(self):
        c = ConfigManager()
        c('a.b', 1)
        del c.a.b
        with pytest.raises(AttributeError):
            assert c.a.b == 1
