# Copyright 2015 Google Inc. All Rights Reserved.
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

"""Command to get IAM policy for an organization."""

from googlecloudsdk.api_lib.organizations import errors
from googlecloudsdk.api_lib.organizations import orgs_base
from googlecloudsdk.calliope import base


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class GetIamPolicy(orgs_base.OrganizationCommand):
  """Get IAM policy for an organization.

  Gets the IAM policy for an organization, given an organization ID.
  """

  detailed_help = {
      'EXAMPLES': """\
          The following command prints the IAM policy for an organization with
          the ID `123456789`:

            $ {command} 123456789
          """
  }

  @staticmethod
  def Args(parser):
    orgs_base.OrganizationCommand.IdArg(
        parser, 'ID for the organization whose policy you want to get.')

  @errors.HandleHttpError
  def Run(self, args):
    messages = self.OrganizationsMessages()
    policy_request = (
        messages.CloudresourcemanagerOrganizationsGetIamPolicyRequest(
            resource=self.GetOrganizationRef(args.id).Name(),
            getIamPolicyRequest=messages.GetIamPolicyRequest()))
    return self.OrganizationsClient().GetIamPolicy(policy_request)
