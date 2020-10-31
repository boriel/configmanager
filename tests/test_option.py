import pytest

from src.configmanager import Option


class TestOption:
    def test_create_option_with_no_type_and_no_value(self):
        Option()

    def test_create_option_with_a_type(self):
        option = Option(type_=int)
        assert option.value is None
        assert option.type == int

    def test_create_option_with_a_value(self):
        option = Option(value=1)
        assert option.value == 1
        assert option.type == int

    def test_create_option_with_a_type_and_assert_type(self):
        with pytest.raises(TypeError):
            option = Option(type_=int)
            option.value = 'a'

    def test_create_option_with_a_default_value_and_assert_type(self):
        with pytest.raises(TypeError):
            option = Option(1)
            option.value = 'a'

    def test_create_option_with_no_default_value_nor_type_accepts_anything(self):
        option = Option()
        option.value = 'a'
        option.value = 1

    def test_create_option_with_default_value_and_different_type_is_not_allowed(self):
        with pytest.raises(TypeError):
            Option(value='', type_=int)

    def test_create_option_with_default_value_and_different_type_is_allowed_with_typecast(self):
        option = Option(value=1, type_=str)
        assert option.value == '1'
