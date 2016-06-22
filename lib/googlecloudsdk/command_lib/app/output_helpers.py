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

"""This module holds exceptions raised by commands."""

from googlecloudsdk.api_lib.app import deploy_command_util
from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_io


DEPLOY_MESSAGE_TEMPLATE = """\
{project}/{service}/{version} (from [{file}])
"""

DEPLOYED_URL_TEMPLATE = """\
     Deployed URL: [{url}]
"""

PROMOTE_MESSAGE_TEMPLATE = """\
     (add --promote if you also want to make this service available from
     [{default_url}])
"""


def DisplayProposedDeployment(project, app_config, version, promote):
  """Prints the details of the proposed deployment.

  Args:
    project: The name of the current project.
    app_config: yaml_parsing.AppConfigSet, The configurations being deployed.
    version: The version identifier of the application to be deployed.
    promote: Whether the newly deployed version will receive all traffic
      (this affects deployed URLs).

  Returns:
    dict (str->str), a mapping of service names to deployed service URLs

  This includes information on to-be-deployed services (including service name,
  version number, and deployed URLs) as well as configurations.
  """
  deployed_urls = {}

  if app_config.Services():
    printer = console_io.ListPrinter(
        'You are about to deploy the following services:')
    deploy_messages = []

    for service, info in app_config.Services().iteritems():
      use_ssl = deploy_command_util.UseSsl(info.parsed.handlers)
      deploy_message = DEPLOY_MESSAGE_TEMPLATE.format(
          project=project, service=service, version=version, file=info.file)

      if ':' not in project:
        url = deploy_command_util.GetAppHostname(
            project, service=info.module, version=None if promote else version,
            use_ssl=use_ssl)
        deployed_urls[service] = url
        deploy_message += DEPLOYED_URL_TEMPLATE.format(url=url)
      if not promote:
        default_url = deploy_command_util.GetAppHostname(
            project, service=info.module, use_ssl=use_ssl)
        deploy_message += PROMOTE_MESSAGE_TEMPLATE.format(
            default_url=default_url)
      deploy_messages.append(deploy_message)
    printer.Print(deploy_messages, output_stream=log.status)

  if app_config.Configs():
    printer = console_io.ListPrinter(
        'You are about to deploy the following configurations:')
    printer.Print(
        ['{0}/{1}  (from [{2}])'.format(project, c.config, c.file)
         for c in app_config.Configs().values()], output_stream=log.status)

  return deployed_urls
