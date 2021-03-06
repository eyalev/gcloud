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
"""Command for creating VPN tunnels."""

import argparse
import re

from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.command_lib.compute import flags


_PRINTABLE_CHARS_PATTERN = r'[ -~]+'


class DeprecatedArgumentException(exceptions.ToolException):

  def __init__(self, arg, msg):
    super(DeprecatedArgumentException, self).__init__(
        u'{0} is deprecated. {1}'.format(arg, msg))


def ValidateSimpleSharedSecret(possible_secret):
  """ValidateSimpleSharedSecret checks its argument is a vpn shared secret.

  ValidateSimpleSharedSecret(v) returns v iff v matches [ -~]+.

  Args:
    possible_secret: str, The data to validate as a shared secret.

  Returns:
    The argument, if valid.

  Raises:
    ArgumentTypeError: The argument is not a valid vpn shared secret.
  """

  if not possible_secret:
    raise argparse.ArgumentTypeError(
        '--shared-secret requires a non-empty argument.')

  if re.match(_PRINTABLE_CHARS_PATTERN, possible_secret):
    return possible_secret

  raise argparse.ArgumentTypeError(
      'The argument to --shared-secret is not valid it contains '
      'non-printable charcters.')


class _BaseCreate(object):
  """Create a VPN Tunnel."""

  # Placeholder to indicate that a detailed_help field exists and should
  # be set outside the class definition.
  detailed_help = None

  @staticmethod
  def Args(parser):
    """Adds arguments to the supplied parser."""

    parser.add_argument(
        '--description',
        help='An optional, textual description for the target VPN tunnel.')

    ike_version = parser.add_argument(
        '--ike-version',
        choices=[1, 2],
        type=int,
        help='Internet Key Exchange protocol version number.')
    ike_version.detailed_help = """\
        Internet Key Exchange protocol version number.
        Valid options are 1 and 2.  Default is 2.
        """

    parser.add_argument(
        '--peer-address',
        required=True,
        help='A valid IP-v4 address representing the remote tunnel endpoint')

    # TODO(user) Add other group members
    shared_secret = parser.add_argument(
        '--shared-secret',
        type=ValidateSimpleSharedSecret,
        required=True,
        help='A shared secret consisting of printable characters')
    shared_secret.detailed_help = (
        'A shared secret consisting of printable characters.  Valid '
        'arguments match the regular expression ' +
        _PRINTABLE_CHARS_PATTERN)

    parser.add_argument(
        '--target-vpn-gateway',
        required=True,
        help='A reference to a target vpn gateway')

    parser.add_argument(
        '--ike-networks',
        type=arg_parsers.ArgList(min_length=1),
        action=arg_parsers.FloatingListValuesCatcher(),
        help=argparse.SUPPRESS)

    parser.add_argument(
        '--local-traffic-selector',
        type=arg_parsers.ArgList(min_length=1),
        action=arg_parsers.FloatingListValuesCatcher(),
        metavar='CIDR',
        help=('Traffic selector is an agreement between IKE peers to permit '
              'traffic through a tunnel if the traffic matches a specified pair'
              ' of local and remote addresses.\n\n'
              'local_traffic_selector allows to configure the local addresses '
              'that are permitted. The value should be a comma separated list '
              'of CIDR formatted strings. '
              'Example: 192.168.0.0/16,10.0.0.0/24.'))

    # TODO(b/29072646): autocomplete --router argument
    parser.add_argument(
        '--router',
        help='The Router to use for dynamic routing.')

    flags.AddRegionFlag(
        parser,
        resource_type='VPN Tunnel',
        operation_type='create')

    parser.add_argument(
        'name',
        help='The name of the VPN tunnel.')

  @property
  def service(self):
    return self.compute.vpnTunnels

  @property
  def method(self):
    return 'Insert'

  @property
  def resource_type(self):
    return 'vpnTunnels'

_BaseCreate.detailed_help = {
    'brief': 'Create a VPN tunnel',
    'DESCRIPTION': """
        *{command}* is used to create a VPN tunnel between a VPN Gateway
        in Google Cloud Platform and an external gateway that is
        identified by --peer-address.
     """
    }


@base.ReleaseTracks(base.ReleaseTrack.GA)
class CreateGA(_BaseCreate, base_classes.BaseAsyncCreator):
  """Create a VPN tunnel."""

  @staticmethod
  def Args(parser):
    _BaseCreate.Args(parser)

  def CreateRequests(self, args):
    """Builds API requests to construct VPN Tunnels."""

    if args.ike_networks is not None:
      raise DeprecatedArgumentException(
          '--ike-networks',
          'It has been renamed to --local-traffic-selector.')

    vpn_tunnel_ref = self.CreateRegionalReference(
        args.name, args.region, resource_type='vpnTunnels')

    # The below is a hack.  The code below ensures that the following two
    # properties hold:
    #   1) scope prompting occurs at most once for the vpn tunnel and gateway
    #   2) if the user gives exactly one of the vpn tunnel and gateway as a URL
    #        and one as short name we do still check --region or prompt as
    #        usual.
    #
    # TODO(user) Change the semantics of the scope prompter so that a
    # single prompt can set the region for resources of multiple types with a
    # single user prompt.  See b/18313268.

    # requested by args or prompt?
    if args.region:
      requested_region = args.region
    elif not args.name.startswith('https://'):
      requested_region = vpn_tunnel_ref.region
    else:
      requested_region = None

    target_vpn_gateway_ref = self.CreateRegionalReference(
        args.target_vpn_gateway, requested_region,
        resource_type='targetVpnGateways')

    router_link = None
    if args.router is not None:
      router_ref = self.CreateRegionalReference(
          args.router, requested_region,
          resource_type='routers')
      router_link = router_ref.SelfLink()

    request = self.messages.ComputeVpnTunnelsInsertRequest(
        project=self.project,
        region=vpn_tunnel_ref.region,
        vpnTunnel=self.messages.VpnTunnel(
            description=args.description,
            router=router_link,
            localTrafficSelector=args.local_traffic_selector or [],
            ikeVersion=args.ike_version,
            name=vpn_tunnel_ref.Name(),
            peerIp=args.peer_address,
            sharedSecret=args.shared_secret,
            targetVpnGateway=target_vpn_gateway_ref.SelfLink()))

    return [request]


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.ALPHA)
class CreateBeta(_BaseCreate, base_classes.BaseAsyncCreator):
  """Create a VPN tunnel."""

  @staticmethod
  def Args(parser):
    CreateGA.Args(parser)
    parser.add_argument(
        '--remote-traffic-selector',
        type=arg_parsers.ArgList(min_length=1),
        action=arg_parsers.FloatingListValuesCatcher(),
        metavar='CIDR',
        help=('Traffic selector is an agreement between IKE peers to permit '
              'traffic through a tunnel if the traffic matches a specified pair'
              ' of local and remote addresses.\n\n'
              'remote_traffic_selector allows to configure the remote addresses'
              ' that are permitted. The value should be a comma separated list '
              'of CIDR formatted strings. '
              'Example: 192.168.0.0/16,10.0.0.0/24.'))

  def CreateRequests(self, args):
    """Builds API requests to construct VPN Tunnels."""

    if args.ike_networks is not None:
      raise DeprecatedArgumentException(
          '--ike-networks',
          'It has been renamed to --local-traffic-selector.')

    vpn_tunnel_ref = self.CreateRegionalReference(
        args.name, args.region, resource_type='vpnTunnels')

    # The below is a hack.  The code below ensures that the following two
    # properties hold:
    #   1) scope prompting occurs at most once for the vpn tunnel and gateway
    #   2) if the user gives exactly one of the vpn tunnel and gateway as a URL
    #        and one as short name we do still check --region or prompt as
    #        usual.
    #
    # TODO(user) Change the semantics of the scope prompter so that a
    # single prompt can set the region for resources of multiple types with a
    # single user prompt.  See b/18313268.

    # requested by args or prompt?
    if args.region:
      requested_region = args.region
    elif not args.name.startswith('https://'):
      requested_region = vpn_tunnel_ref.region
    else:
      requested_region = None

    target_vpn_gateway_ref = self.CreateRegionalReference(
        args.target_vpn_gateway, requested_region,
        resource_type='targetVpnGateways')

    router_link = None
    if args.router is not None:
      router_ref = self.CreateRegionalReference(
          args.router, requested_region,
          resource_type='routers')
      router_link = router_ref.SelfLink()

    request = self.messages.ComputeVpnTunnelsInsertRequest(
        project=self.project,
        region=vpn_tunnel_ref.region,
        vpnTunnel=self.messages.VpnTunnel(
            description=args.description,
            router=router_link,
            localTrafficSelector=args.local_traffic_selector or [],
            remoteTrafficSelector=args.remote_traffic_selector or [],
            ikeVersion=args.ike_version,
            name=vpn_tunnel_ref.Name(),
            peerIp=args.peer_address,
            sharedSecret=args.shared_secret,
            targetVpnGateway=target_vpn_gateway_ref.SelfLink()))

    return [request]
