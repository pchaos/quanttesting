# -*- coding: utf-8 -*-
"""
https://myadventuresincoding.wordpress.com/tag/testing/
@Time    : 2020/4/7 下午1:36

@File    : test_mock.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
# from mock import patch, MagicMock
from unittest.mock import Mock, patch
from testing.examples.myclass_mock import MyClass, SomeOtherClassThatUsesMyClass



class MyTestCase(unittest.TestCase):

    @patch.object(MyClass, 'my_method')
    def test_my_method_shouldReturnTrue_whenMyMethodReturnsSomeValue(self, mock_my_method):
        """To mock a method in a class to return a specific value use @patch.object.
        """
        mock_my_method.return_value = True
        some_other_class = SomeOtherClassThatUsesMyClass()
        result = some_other_class.method_under_test()
        self.assertTrue(result)

    @patch.object(MyClass, 'my_method')
    def test_my_method_shouldReturnMultipleValues_whenMyMethodReturnsSomeValue(self, mock_my_method):
        """To mock a method in a class with @patch.object but return a different value each time it is called, use side_effect. Side effect allows you to define a custom method and have that method called each time your mock method is called. The value returned from this method will be used as the return value your mock method.
        """
        list_of_return_values = [True, False, False]

        def side_effect():
            return list_of_return_values.pop()

        mock_my_method.side_effect = side_effect
        some_other_class = SomeOtherClassThatUsesMyClass()
        self.assertFalse(some_other_class.method_under_test())
        self.assertFalse(some_other_class.method_under_test())
        self.assertTrue(some_other_class.method_under_test())

    @patch('testing.examples.myclass_mock.MyClass')
    def test_my_method_shouldCallMyClassMethodMyMethod_whenSomeOtherClassMethodIsCalled(self, mock_class):
        """To mock an entire class to test interactions with that class use @patch.
        """
        some_other_class = SomeOtherClassThatUsesMyClass()
        some_other_class.method_under_test()
        self.assertTrue(mock_class.called)

    @patch('testing.examples.myclass_mock.MyClass',autospec=True)
    def test_my_method_shouldReturnTrue_whenSomeOtherClassMethodIsCalledAndAReturnValueIsSet(self, mock_my_class):
        """To mock an entire class with @patch and still set the return value of a method in that class, grab the instance of the mock object’s return value and set the method’s return value on the instance. There is a section on the patch page explaining how to do this.
        """
        mc = mock_my_class.return_value
        mc.my_method.return_value = True
        some_other_class = SomeOtherClassThatUsesMyClass()
        result = some_other_class.method_under_test()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()

