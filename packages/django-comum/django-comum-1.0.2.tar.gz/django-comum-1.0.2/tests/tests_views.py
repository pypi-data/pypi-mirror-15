# coding: utf-8
from django.test import TestCase


class FooTestCase(TestCase):

    def test_foo(self):
        self.assertEqual(1, 1)
