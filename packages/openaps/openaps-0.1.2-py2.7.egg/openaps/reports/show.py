
"""
show   - show all reports
"""

from openaps.devices.device import Device
from openaps.reports.report import Report

from openaps.cli import helpers
import argparse

class Formatter (object):
  def __init__ (self, app):
    self.app = app
  def __call__ (self, thing):
    return self.format_cli(thing)

  def format_cli (self, report):
    usage = self.app.devices[report.fields.get('device')]
    task = self.app.actions.commands['add'].usages.commands[usage.name].method.commands[report.fields['use']]

    line = [ 'openaps', 'use', usage.name, report.fields.get('use') ]
    params = [ ]

    for act in task.method.parser._actions:
      if act.dest in report.fields:
        if act.option_strings:

          if report.fields.get(act.dest):
            if type(act) in [argparse._StoreTrueAction, argparse._StoreFalseAction ]:
              expected = act.const
              found = report.fields.get(act.dest)
              if type(act) is argparse._StoreFalseAction:
                found = not found

              if expected != found:
                params.append(act.option_strings[0])
            else:
              params.append(act.option_strings[0] + ' "' + report.fields.get(act.dest) + '"')
        else:
          params.append(report.fields.get(act.dest))


    return ' '.join(line + params)
def configure_app (app, parser):
  parser.set_defaults(report='*')
  parser._actions[-1].nargs = '?'
  if parser._actions[-1].choices:
    parser._actions[-1].choices.append('*')
  helpers.install_show_arguments(parser)
  parser.add_argument('--cli_only', action='store_const', default=False, const=True)

def main (args, app):
  format_cli = Formatter(app)
  for device in Report.FromConfig(app.config):
    if args.report in [ '*', device.name ]:
      if args.cli_only:
        print format_cli(device)
      else:
        print args.format(device)

