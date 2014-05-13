import pytest
import mock

from mock import MagicMock
from hamcrest import *

import etcd

@mock.patch('etcd.client.requests')
def test_etcd_instance_with_host_port(requests_mock):
  """
  Should get pass the test
  """
  requests_mock.get.return_value = MagicMock(status_code=200)

  client = etcd.Client(host="myhost", port=8997)
  assert_that(client.peers[0], has_entries(host="myhost", port=8997))
  assert_that(len(client.peers), equal_to(1))
