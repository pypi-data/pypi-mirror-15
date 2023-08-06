# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock
import os
import testtools

from openstack import connection as sdk_connection
from openstack import profile as sdk_profile

from senlinclient.common import sdk


class TestSdk(testtools.TestCase):

    @mock.patch('senlinclient.common.sdk.ProfileAction.set_option')
    def test_env(self, mock_set_option):
        os.environ['test_senlin_sdk_env'] = '1'
        sdk.ProfileAction.env('test_senlin_sdk_env')
        mock_set_option.assert_called_once_with('test_senlin_sdk_env', '1')

    @mock.patch('senlinclient.common.sdk.ProfileAction.prof')
    def test_set_option_set_name(self, mock_prof):
        mock_prof.ALL = 'mock_prof.ALL'
        sdk.ProfileAction.set_option('name', 'test=val1')
        mock_prof.set_name.assert_called_once_with('test', 'val1')
        mock_prof.reset_mock()
        sdk.ProfileAction.set_option('name', 'val2')
        mock_prof.set_name.assert_called_once_with(mock_prof.ALL, 'val2')

    @mock.patch('senlinclient.common.sdk.ProfileAction.prof')
    def test_set_option_set_region(self, mock_prof):
        mock_prof.ALL = 'mock_prof.ALL'
        sdk.ProfileAction.set_option('OS_REGION_NAME', 'test=val1')
        mock_prof.set_region.assert_called_once_with('test', 'val1')
        mock_prof.reset_mock()
        sdk.ProfileAction.set_option('OS_REGION_NAME', 'val2')
        mock_prof.set_region.assert_called_once_with(mock_prof.ALL, 'val2')

    @mock.patch('senlinclient.common.sdk.ProfileAction.prof')
    def test_set_option_set_version(self, mock_prof):
        mock_prof.ALL = 'mock_prof.ALL'
        sdk.ProfileAction.set_option('version', 'test=val1')
        mock_prof.set_version.assert_called_once_with('test', 'val1')

    @mock.patch('senlinclient.common.sdk.ProfileAction.prof')
    def test_set_option_set_interface(self, mock_prof):
        mock_prof.ALL = 'mock_prof.ALL'
        sdk.ProfileAction.set_option('interface', 'test=val1')
        mock_prof.set_interface.assert_called_once_with('test', 'val1')

    @mock.patch.object(sdk_connection, 'Connection')
    def test_create_connection_with_profile(self, mock_connection):
        mock_prof = mock.Mock()
        mock_conn = mock.Mock()
        mock_connection.return_value = mock_conn
        kwargs = {
            'user_id': '123',
            'password': 'abc',
            'auth_url': 'test_url'
        }
        res = sdk.create_connection(mock_prof, **kwargs)
        mock_connection.assert_called_once_with(profile=mock_prof,
                                                user_agent=None,
                                                user_id='123',
                                                password='abc',
                                                auth_url='test_url')
        self.assertEqual(mock_conn, res)

    @mock.patch.object(sdk_connection, 'Connection')
    @mock.patch.object(sdk_profile, 'Profile')
    def test_create_connection_without_profile(self, mock_profile,
                                               mock_connection):
        mock_prof = mock.Mock()
        mock_conn = mock.Mock()
        mock_profile.return_value = mock_prof
        mock_connection.return_value = mock_conn
        kwargs = {
            'interface': 'public',
            'region_name': 'RegionOne',
            'user_id': '123',
            'password': 'abc',
            'auth_url': 'test_url'
        }
        res = sdk.create_connection(**kwargs)

        mock_prof.set_interface.assert_called_once_with('clustering', 'public')
        mock_prof.set_region.assert_called_once_with('clustering', 'RegionOne')
        mock_connection.assert_called_once_with(profile=mock_prof,
                                                user_agent=None,
                                                user_id='123',
                                                password='abc',
                                                auth_url='test_url')
        self.assertEqual(mock_conn, res)
