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
"""Command for adding IAM policy bindings for service accounts."""

import httplib

from googlecloudsdk.api_lib.iam import utils
from googlecloudsdk.api_lib.util import http_retry
from googlecloudsdk.command_lib.iam import base_classes
from googlecloudsdk.core.iam import iam_util
from googlecloudsdk.third_party.apitools.base.py import exceptions


class AddIamPolicyBinding(base_classes.BaseIamCommand):
  """Add an IAM policy binding to a service account.

  This command adds a policy binding to the IAM policy of a service account,
  given an IAM-ACCOUNT and the binding.
  """

  detailed_help = iam_util.GetDetailedHelpForAddIamPolicyBinding(
      'service account', 'my-iam-account@somedomain.com')

  @staticmethod
  def Args(parser):
    parser.add_argument('account',
                        metavar='IAM-ACCOUNT',
                        help='The service account whose policy to '
                        'add bindings to.')
    iam_util.AddArgsForAddIamPolicyBinding(parser)

  @http_retry.RetryOnHttpStatus(httplib.CONFLICT)
  def Run(self, args):
    try:
      policy = self.iam_client.projects_serviceAccounts.GetIamPolicy(
          self.messages.IamProjectsServiceAccountsGetIamPolicyRequest(
              resource=utils.EmailToAccountResourceName(args.account)))

      iam_util.AddBindingToIamPolicy(self.messages, policy, args)

      return self.iam_client.projects_serviceAccounts.SetIamPolicy(
          self.messages.IamProjectsServiceAccountsSetIamPolicyRequest(
              resource=utils.EmailToAccountResourceName(args.account),
              setIamPolicyRequest=self.messages.SetIamPolicyRequest(
                  policy=policy)))
    except exceptions.HttpError as error:
      raise utils.ConvertToServiceAccountException(error, args.account)
