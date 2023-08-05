# Copyright 2016 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging

from keystoneclient import exceptions

from cloudferry.lib.os import clients
from cloudferry.lib.os.discovery import model

LOG = logging.getLogger(__name__)


@model.type_alias('tenants')
class Tenant(model.Model):
    class Schema(model.Schema):
        object_id = model.PrimaryKey('id')
        name = model.String(required=True)
        enabled = model.Boolean(required=True)
        description = model.String(allow_none=True)

    @classmethod
    def load_missing(cls, cloud, object_id):
        identity_client = clients.identity_client(cloud)
        try:
            raw_tenant = identity_client.tenants.get(object_id.id)
            return cls.load_from_cloud(cloud, raw_tenant)
        except exceptions.NotFound:
            return None

    @classmethod
    def discover(cls, cloud):
        identity_client = clients.identity_client(cloud)
        with model.Session() as session:
            for tenant in identity_client.tenants.list():
                session.store(Tenant.load_from_cloud(cloud, tenant))

    def equals(self, other):
        # pylint: disable=no-member
        return self.name.lower() == other.name.lower()
