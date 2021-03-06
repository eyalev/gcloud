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

"""Command to update an organization."""

import textwrap

from googlecloudsdk.api_lib.organizations import errors
from googlecloudsdk.api_lib.organizations import orgs_base
from googlecloudsdk.calliope import base
from googlecloudsdk.core import list_printer
from googlecloudsdk.core import log


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Update(orgs_base.OrganizationCommand):
  """Update the name of an organization.

  Updates the given organization with new name.

  This command can fail for the following reasons:
      * There is no organization with the given ID.
      * The active account does not have permission to update the given
        organization.
  """

  detailed_help = {
      'EXAMPLES': textwrap.dedent("""\
          The following command updates an organization with the ID
          `123456789` to have the name "Foo Bar and Grill":

            $ {command} 123456789 --display_name="Foo Bar and Grill"
    """),
  }

  @staticmethod
  def Args(parser):
    orgs_base.OrganizationCommand.IdArg(
        parser, 'ID for the organization you want to update.')
    parser.add_argument('--display-name', required=True,
                        help='New display name for the organization.')

  @errors.HandleHttpError
  def Run(self, args):
    client = self.OrganizationsClient()
    org_ref = self.GetOrganizationRef(args.id)
    org = client.Get(org_ref.Request())
    org.displayName = args.display_name
    result = client.Update(org)
    log.UpdatedResource(org_ref)
    return result

  def Display(self, args, result):
    """This method is called to print the result of the Run() method.

    Args:
      args: The arguments that command was run with.
      result: The value returned from the Run() method.
    """
    list_printer.PrintResourceList(self.Collection(), [result])
