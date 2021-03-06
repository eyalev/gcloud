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

"""Command to set IAM policy for a resource."""

from googlecloudsdk.api_lib.projects import util
from googlecloudsdk.api_lib.util import http_error_handler
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.projects import flags
from googlecloudsdk.command_lib.projects import util as command_lib_util
from googlecloudsdk.core.iam import iam_util


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.GA)
class SetIamPolicy(base.Command):
  """Set IAM policy for a project.

  Sets the IAM policy for a project, given a project ID and a file that
  contains the JSON-encoded IAM policy.
  """

  detailed_help = {
      'EXAMPLES': """
          The following command reads an IAM policy defined in a JSON file
          `policy.json` and sets it for a project with the ID
          `example-project-id-1`:

            $ {command} example-project-id-1 policy.json
          """,
  }

  def Collection(self):
    return command_lib_util.PROJECTS_COLLECTION

  def GetUriFunc(self):
    return command_lib_util.ProjectsUriFunc

  @staticmethod
  def Args(parser):
    flags.GetProjectFlag('set IAM policy for').AddToParser(parser)
    parser.add_argument('policy_file', help='JSON file with the IAM policy')

  # util.HandleKnownHttpErrors needs to be the first one to handle errors.
  # It needs to be placed after http_error_handler.HandleHttpErrors.
  @http_error_handler.HandleHttpErrors
  @util.HandleKnownHttpErrors
  def Run(self, args):
    projects = util.GetClient()
    messages = util.GetMessages()

    project_ref = command_lib_util.ParseProject(args.id)

    policy = iam_util.ParseJsonPolicyFile(args.policy_file, messages.Policy)

    policy_request = messages.CloudresourcemanagerProjectsSetIamPolicyRequest(
        resource=project_ref.Name(),
        setIamPolicyRequest=messages.SetIamPolicyRequest(policy=policy))
    return projects.projects.SetIamPolicy(policy_request)
