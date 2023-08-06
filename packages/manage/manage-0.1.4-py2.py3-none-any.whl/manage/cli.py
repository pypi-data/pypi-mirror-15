#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import copy
import code
import json
import yaml
import click
import readline
import rlcompleter
from manage.template import default_manage_dict
from manage.auto_import import import_objects, exec_init, exec_init_script
from manage.commands_collector import load_commands

MANAGE_FILE = 'manage.yml'
HIDDEN_MANAGE_FILE = '.{0}'.format(MANAGE_FILE)
MANAGE_DICT = {}


def load_manage_dict(filename=None):
    manage_filename = None
    if not MANAGE_DICT:
        if filename:
            manage_filename = filename
        elif os.path.exists(MANAGE_FILE):
            manage_filename = MANAGE_FILE
        elif os.path.exists(HIDDEN_MANAGE_FILE):
            manage_filename = HIDDEN_MANAGE_FILE
        else:
            MANAGE_DICT.update(copy.deepcopy(default_manage_dict))
            MANAGE_DICT['shell']['banner']['message'] = (
                "WARNING: This is not a managed project\n"
                "\tPlease `exit()` and \n"
                "\trun `$ manage init`\n"
                "\tand edit `manage.yml` file with desired options"
            )
            MANAGE_DICT['shell']['auto_import']['display'] = False
        if manage_filename:
            with open(manage_filename) as manage_file:
                MANAGE_DICT.update(yaml.load(manage_file))
    return MANAGE_DICT


class Config(object):

    def __init__(self):
        self.filename = None
        self._manage_dict = None

    @property
    def manage_dict(self):
        if not self._manage_dict:
            self._manage_dict = load_manage_dict(self.filename)
        return self._manage_dict


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group(no_args_is_help=False)
@click.option('--filename', type=click.Path())
@pass_config
def cli(config, filename):
    """ Core commands wrapper """
    config.filename = filename


@cli.command()
@click.option('--banner')
@click.option('--hidden/--no-hidden', default=False)
@click.option('--backup/--no-backup', default=True)
@pass_config
def init(config, banner, hidden, backup):
    """Initialize a manage shell in current directory
        $ manage init --banner="My awesome app shell"
        initializing manage...
        creating manage.yml
    """
    manage_file = config.filename or (
        HIDDEN_MANAGE_FILE if hidden else MANAGE_FILE)
    if os.path.exists(manage_file):
        if not click.confirm('Rewrite {0}?'.format(manage_file)):
            return

        if backup:
            bck = '.bck_{0}'.format(manage_file)
            with open(manage_file, 'r') as source, open(bck, 'w') as bck_file:
                bck_file.write(source.read())

    with open(manage_file, 'w') as output:
        data = default_manage_dict
        if banner:
            data['shell']['banner']['message'] = banner
        output.write(yaml.dump(data, default_flow_style=False))


@cli.command()
@pass_config
def debug(config):
    """Shows the parsed manage file"""
    print(json.dumps(config.manage_dict, indent=2))


@cli.command()
@click.option('--ipython/--no-ipython', default=True)
@click.option('--ptpython', default=False, is_flag=True)
@pass_config
def shell(config, ipython, ptpython):
    """Runs a Python shell with context"""
    manage_dict = config.manage_dict
    _vars = globals()
    _vars.update(locals())
    auto_imported = import_objects(manage_dict)
    _vars.update(auto_imported)
    msgs = []
    if manage_dict['shell']['banner']['enabled']:
        msgs.append(
            manage_dict['shell']['banner']['message'].format(**manage_dict)
        )
    if auto_imported and manage_dict['shell']['auto_import']['display']:
        auto_imported_names = [
            key for key in auto_imported.keys()
            if key not in ['__builtins__', 'builtins']
        ]
        msgs.append('\tAuto imported: {0}\n'.format(auto_imported_names))

    banner_msg = u'\n'.join(msgs)

    if manage_dict['shell']['readline_enabled']:
        readline.set_completer(rlcompleter.Completer(_vars).complete)
        readline.parse_and_bind('tab: complete')

    exec_init(manage_dict, _vars)
    exec_init_script(manage_dict, _vars)

    if ptpython:
        try:
            from ptpython.repl import embed
            embed({}, _vars)
        except ImportError:
            click.echo("ptpython is not installed!")
        return

    try:
        if ipython is True:
            from IPython import start_ipython
            from traitlets.config import Config
            c = Config()
            c.TerminalInteractiveShell.banner2 = banner_msg
            start_ipython(argv=[], user_ns=_vars, config=c)
        else:
            raise ImportError
    except ImportError:
        shell = code.InteractiveConsole(_vars)
        shell.interact(banner=banner_msg)


def load_manage_dict_from_sys_args():
    single_option = [item for item in sys.argv if '--filename=' in item]
    if single_option:
        filename = single_option[0].split('=')[-1]
    elif '--filename' in sys.argv:
        filename = sys.argv[sys.argv.index('--filename') + 1]
    else:
        filename = None
    load_manage_dict(filename)


def init_cli(cli_obj, reset=False):
    if reset:
        global MANAGE_DICT
        MANAGE_DICT = {}
    sys.path.insert(0, '.')
    load_manage_dict_from_sys_args()
    cli.help = MANAGE_DICT.get(
        'help_text', '{project_name} Interactive shell!'
    ).format(**MANAGE_DICT)
    load_commands(cli, MANAGE_DICT)


def main():
    init_cli(cli)
    return cli()


if __name__ == '__main__':
    main()
