import pytest

from src.configmanager import ConfigManager


class TestConfigManager:
    def test_inits_ok(self):
        c = ConfigManager()
        assert c._ConfigManager__namespace == ''

    def test_init_with_namespace_ok(self):
        c = ConfigManager('.namespace')
        assert c._ConfigManager__namespace == '.namespace'

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
        assert c.a == 2
