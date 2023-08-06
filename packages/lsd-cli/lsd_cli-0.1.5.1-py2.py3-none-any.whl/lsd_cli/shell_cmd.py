import logging
import os
import re
import tempfile
from subprocess import call

import click
from lsd_cli.print_utils import (clear, print_json_result,
                                 print_leaplog_result, underline)
from xtermcolor import colorize

RE_CMD = re.compile(r'(\w+)\((.*)\)$')
RE_LLOG = re.compile(r'^(\?|\+\+|\-\-)(.*.)')
RE_DIRECTIVE = re.compile(r'^(@prefix|@include)\s+(.*.)')
RE_PREFIX = re.compile(r'^\s*(\w+|\s*):\s*(\<.*\>).$')


def process_input(shell_ctx, input):
    cmd = None
    args = []
    match_llog = RE_LLOG.match(input)
    match_cmd = RE_CMD.match(input)

    if not input or input.startswith('%'):  # comment pass
        logging.debug('+++ comment or empty')
        return
    elif match_llog:  # leaplog sentence (++ | -- | ?)
        if match_llog.group(1) == '?':
            logging.debug('+++ prefix select')
            cmd = 'select'
            args = [input]
        elif match_llog.group(1) == '++':
            logging.debug('+++ write assert')
            cmd = 'write_assert'
            args = [input]
        elif match_llog.group(1) == '--':
            logging.debug('+++ write retract')
            cmd = 'write_retract'
            args = [input]
        else:
            raise Exception('Invalid leaplog sentence: {}'.format(input))
    elif not match_cmd:  # shell directive
        match_dir = RE_DIRECTIVE.match(input)

        if match_dir:  # prefix/include definition
            logging.debug('+++ prefix directive')
            cmd = match_dir.group(1)
            args = [match_dir.group(2)]
        else:  # rule
            logging.debug('+++ rule directive')
            cmd = 'rule'
            args = [input]
    else:  # shell cmd
        logging.debug('+++ built-in cmd')
        cmd = match_cmd.group(1)
        params = match_cmd.group(2)

        if params:
            args = [x.strip() for x in params.split(',')]
        else:
            args = []

    __dispatch_cmd(shell_ctx, cmd, args)


def __exec_leaplog(shell_ctx, filename):
    lsd_api = shell_ctx['lsd_api']

    try:
        with open(filename, 'r') as file:
            content = file.read()
    except Exception as e:
        raise Exception("ERROR: could not read {0}".format(filename))

    result = lsd_api.leaplog(content)
    print_leaplog_result(shell_ctx, result)


def __exec_ruleset(shell_ctx, uri, filename):
    lsd_api = shell_ctx['lsd_api']

    try:
        with open(filename, 'r') as file:
            ruleset = file.read()
    except Exception as e:
        raise Exception("ERROR: could not read {0}".format(filename))

    result = lsd_api.create_ruleset(uri, ruleset)
    click.echo(result)
    print_json_result(shell_ctx, result)


def __help(_):
    shell_help = []
    shell_help.append(underline(colorize('LSD-CLI\n', rgb=0x71d1df)))
    shell_help.append("""
The following are the list of built-in command and leaplog sentences
& directives supported. Directives  (@prefix or @include) or explicit rules
(head :- body) are added to the current shell session context without actually
getting to lsd. Shell context is used on selects (?), write assert (++) and
write detract (--).\n\n""")

    for _, value in __COMMANDS.items():
        shell_help.append(colorize(value['name'], rgb=0x71d1df))
        shell_help.append('\n')
        shell_help.append('  ')
        shell_help.append(value['help'])
        shell_help.append('\n\n')

    click.echo_via_pager(''.join(shell_help))


# built-in commands
def __clear(_):
    click.clear()


def __loadll(shell_ctx, filename):
    __exec_leaplog(shell_ctx, filename)


def __loadrs(shell_ctx, uri, filename):
    __exec_ruleset(shell_ctx, uri, filename)


def __listrs(shell_ctx):
    lsd_api = shell_ctx['lsd_api']
    result = lsd_api.rulesets()
    print_json_result(shell_ctx, result)


def __listm(shell_ctx):
    print_json_result(shell_ctx, shell_ctx['prefix_mapping'])


def __edit(shell_ctx):
    editor = os.environ.get('EDITOR', 'vim')

    with tempfile.NamedTemporaryFile(suffix='.tmp') as tf:
        tf.write(bytes(__dump_conext(shell_ctx), 'UTF-8'))
        tf.flush()
        call([editor, tf.name])

        # clear current shell context
        shell_ctx['prefix_mapping'] = {}
        shell_ctx['includes'] = []
        shell_ctx['rules'] = []

        # load new context
        _loadconf(shell_ctx, tf.name)


def __limit(shell_ctx, limit):
    shell_ctx['limit'] = int(limit)


# leaplog commands & directives
def __prefix(shell_ctx, params):
    match = RE_PREFIX.match(params)

    if not match:
        raise Exception(
            'Error: invalid prefix, syntax "@prefix prefix: <uri>."')

    prefix = match.group(1)
    uri = match.group(2)
    shell_ctx['prefix_mapping'][prefix] = uri
    logging.debug(shell_ctx['prefix_mapping'])


def __include(shell_ctx, params):
    shell_ctx['includes'].append('@include: {}'.format(params))
    logging.debug(shell_ctx['includes'])


def __rule(shell_ctx, params):
    shell_ctx['rules'].append(params)
    logging.debug(shell_ctx['rules'])


def __import(shell_ctx, params):
    _loadconf(shell_ctx, params)


def __export(shell_ctx, params):
    context = __dump_conext(shell_ctx)

    with open(params, 'w') as file:
        file.write(context)


def __dump_ruleset(shell_ctx):
    includes = '\n'.join(shell_ctx['includes'])
    rules = '\n'.join(shell_ctx['rules'])

    return includes + rules


def __dump_conext(shell_ctx):
    prefixes = ''
    for prefix, uri in shell_ctx['prefix_mapping'].items():
        prefixes = prefixes + '@prefix {}: {}.\n'.format(prefix, uri)

    ruleset = __dump_ruleset(shell_ctx)

    comment = '% This file is imported one line at a time. Do not split lines!\n'
    context = '%(prefixes)s%(ruleset)s' % locals()

    return comment + context


def _loadconf(shell_ctx, filename):
    with open(filename, 'r') as file:
        lineno = 0

        for line in file:
            lineno += 1

            try:
                logging.debug('Importing line: "%s"', line)
                process_input(shell_ctx, line.strip())
            except Exception as e:
                logging.error(e)
                logging.error('Importing line: "%s"', line)


def __select(shell_ctx, params):
    prefix_mapping = shell_ctx['prefix_mapping']
    limit = shell_ctx['limit'] if shell_ctx['limit'] > 0 else 'infinity'
    ruleset = __dump_ruleset(shell_ctx)
    prog = '%(params)s' % locals()
    result = shell_ctx['lsd_api'].leaplog(
        prog, prefix_mapping=prefix_mapping, ruleset=ruleset, limit=limit)

    print_leaplog_result(shell_ctx, result)


def __write(shell_ctx, params):
    prefix_dirs = __dump_conext(shell_ctx)
    prog = '%(prefix_dirs)s\n\n%(params)s' % locals()
    result = shell_ctx['lsd_api'].leaplog(prog)

    print_leaplog_result(shell_ctx, result)


def __write_assert(shell_ctx, params):
    __write(shell_ctx, params)


def __write_retract(shell_ctx, params):
    __write(shell_ctx, params)


def __noc(shell_ctx):
    click.echo(colorize("Not implemented!", rgb=0xE11500))


# shell commands dispatch table
__COMMANDS = {
    'help': {'cmd': __help, 'name': 'help()', 'help': 'Prints this help.'},
    'clear': {'cmd': __clear, 'name': 'clear()', 'help': 'Clears the terminal.'},
    'edit': {'cmd': __edit, 'name': 'edit()', 'help': 'Edits current shell contex.'},
    'loadll': {'cmd': __loadll, 'name': 'll(filename)',
               'help': 'Loads an execute a leaplog program from filename.'},
    'loadrs': {'cmd': __loadrs, 'name': 'loadrs(uri, filename)',
               'help': 'Loads a ruleset from filename to LSD with the given uri name.'},
    'listrs': {'cmd': __listrs, 'name': 'listrs()', 'help': 'Lists LSD defined rulesets.'},
    'limit': {'cmd': __limit, 'name': 'limit(n)', 'help': 'Limit results to n rows.'},
    'import': {'cmd': __import, 'name': 'import(filename>)',
               'help': "Import the given <filename> to the shell session."},
    'export': {'cmd': __export, 'name': 'export(filename>)',
               'help': "Export the current shell session to <filename>."},
    'edit': {'cmd': __edit, 'name': 'edit(filename)',
             'help': "Export the current shell session to <filename>."},
    'listm': {'cmd': __listm, 'name': 'listm()',
              'help': "List prefix mapping definitions in the current shell session."},
    'loadconf': {'cmd': _loadconf, 'name': 'loadm(filename)',
                 'help': "Load url prefix mapping and rules from filename."},
    'select': {'cmd': __select, 'name': '?().',
               'help': 'Perform a select on lsd.'},
    'write_assert': {'cmd': __write_assert, 'name': '++().',
                     'help': 'Write an assert on lsd.'},
    'write_retract': {'cmd': __write_retract, 'name': '--().',
                      'help': 'Write an retract on lsd.'},
    'rule': {'cmd': __rule, 'name': '().',
             'help': 'Partial rule definition for the current shell session.'},
    '@prefix': {'cmd': __prefix, 'name': '@prefix prefix: <uri>.',
                'help': "Define a new url prefix to use during the shell session."},
    '@include': {'cmd': __include, 'name': '@include <uri>.',
                 'help': "Use the given ruleset during the shell session."}
}


def __dispatch_cmd(shell_ctx, cmd, args):
    logging.debug('%s: %s', cmd, args)
    __COMMANDS[cmd]['cmd'](shell_ctx, *args)
