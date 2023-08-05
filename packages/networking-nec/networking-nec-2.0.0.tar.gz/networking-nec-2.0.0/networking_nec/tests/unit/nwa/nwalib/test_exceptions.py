# Copyright 2015-2016 NEC Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
from neutron.tests import base

from networking_nec.nwa.nwalib import exceptions as nwa_exc


class TestNwaException(base.BaseTestCase):
    def test___str__(self):
        exc = nwa_exc.NwaException(200, 'msg1', mock.MagicMock())
        self.assertEqual(str(exc), 'http status: 200, msg1')
