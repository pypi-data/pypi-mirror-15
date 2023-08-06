#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django.test.client

from .base import TestCase


class TestAdminBasic(TestCase):

    def setUp(self):
        self.browser = django.test.client.Client()

    def test_admin_basic(self):
        for tab in [
            'demo',
            'sessions',
            'rooms',
            'create_session',
            'server_check',
        ]:
            response = self.browser.get('/{}/'.format(tab), follow=True)
            self.assertEqual(response.status_code, 200)
