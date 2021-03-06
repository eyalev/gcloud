# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Backend service."""

from googlecloudsdk.api_lib.compute import utils


class BackendService(object):
  """Abstracts BackendService resource."""

  def __init__(self, ref, compute_client=None):
    self.ref = ref
    self._compute_client = compute_client

  @property
  def _client(self):
    return self._compute_client.apitools_client

  @property
  def _messages(self):
    return self._compute_client.messages

  def _MakeGetRequestTuple(self):
    return (self._client.backendServices,
            'Get',
            self._messages.ComputeBackendServicesGetRequest(
                project=self.ref.project,
                backendService=self.ref.Name()))

  def _MakeDeleteRequestTuple(self):
    return (self._client.backendServices,
            'Delete',
            self._messages.ComputeBackendServicesDeleteRequest(
                project=self.ref.project,
                backendService=self.ref.Name()))

  def _MakeGetHealthRequestTuple(self, group):
    return (self._client.backendServices,
            'GetHealth',
            self._messages.ComputeBackendServicesGetHealthRequest(
                resourceGroupReference=self._messages.ResourceGroupReference(
                    group=group),
                project=self.ref.project,
                backendService=self.ref.Name()))

  def Delete(self, only_generate_request=False):
    requests = [self._MakeDeleteRequestTuple()]
    if not only_generate_request:
      return self._compute_client.MakeRequests(requests)
    return requests

  def Get(self, only_generate_request=False):
    """Fetches the backend service resource."""
    requests = [self._MakeGetRequestTuple()]
    if not only_generate_request:
      responses = self._compute_client.MakeRequests(requests)
      return responses[0]
    return requests

  def GetHealth(self):
    """Issues series of gethealth requests for each backend group.

    Yields:
      {'backend': backend.group, 'status': backend_service.GetHealthResponse}
    """
    backend_service = self.Get()
    # Call GetHealth for each group in the backend service
    # Instead of batching-up all requests and making a single
    # request_helper.MakeRequests call, go one backend at a time.
    # We do this because getHealth responses don't say what resource
    # they correspond to.  It's not obvious how to reliably match up
    # responses and backends when there are errors.  Additionally the contract
    # for batched requests doesn't guarantee response order will match
    # request order.
    #
    # TODO(b/25015230): Make a single batch request once the response
    # can be mapped back to resource.
    errors = []
    for backend in backend_service.backends:
      # The list() call below is itended to force the generator returned by
      # MakeRequests.  If there are exceptions the command will abort, which is
      # expected.  Having a list simplifies some of the checks that follow.
      resources = self._compute_client.MakeRequests(
          [self._MakeGetHealthRequestTuple(backend.group)], errors)

      #  For failed request error information will accumulate in errors
      if resources:
        yield {'backend': backend.group, 'status': resources[0]}

    if errors:
      utils.RaiseToolException(
          errors,
          error_message='Could not get health for some groups:')

