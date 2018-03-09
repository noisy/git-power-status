#!/usr/bin/python

import sys
import re
try:
    from pipes import quote
except:
    from shlex import quite


escape = '\033'

BOLD = escape + '[1m'

RED = escape + '[31m'
LIGHT_RED = escape + '[31m' + BOLD

GREEN = escape + '[32m'
LIGHT_GREEN = escape + '[32m' + BOLD

YELLOW = escape + '[33m'
LIGHT_YELLOW = escape + '[33m' + BOLD

BLUE = escape + '[34m'
LIGHT_BLUE = escape + '[34m' + BOLD

PURPLE = escape + '[35m'
LIGHT_PURPLE = escape + '[35m' + BOLD

AZURE = escape + '[36m'
LIGHT_AZURE = AZURE + BOLD

END = escape + '[0m'

# fp = open('/tmp/gitstatus')
# status = fp
status = sys.stdin

new_files = []
modified_staged = []
deleted_staged = []
deleted = []
modified = []
untracked = []

untracked_on = False

staged_printed = False
not_staged_printed = False
untracked_printed = False

SORT = True


def get_filepath_from_git_status(color, color2, status, line, storage, env_symbol):

    if status:
        status += ":"

    m = re.match(
        "^\s*.\{color}{status}\s*(.*).\[m\s*$".format(
            color=color.replace(escape, ''),
            status=status
        ),
        line
    )

    if m:
        filepath = m.groups()[0]
        line = decorate(line, color, color2, color2, env_symbol, len(storage)+1)
        if line:
            storage.append((filepath, line))
        return True


def print_section(types):

    if types:
        print "\n{}".format("".join(lines for lines in zip(*types)[1]))


def decorate(line, line_color_from, line_color_to, env_color, letter, env_number):
    columns = [col.strip() for col in line.split(":")]
    status = columns[0] if len(columns) == 2 else "untracked"
    filepath = columns[1] if len(columns) == 2 else columns[0].replace(line_color_from, '')

    q = '"' if ' ' in filepath else ''

    env = '{env_color}{quoted_or_not}${env_letter}{env_number}{quoted_or_not}{end_env_color}{line_color} '.format(
        env_color=env_color + BOLD,
        quoted_or_not=q,
        env_letter=letter,
        env_number=env_number,
        end_env_color=END,
        line_color=line_color_to
    )
    status = status.replace(line_color_from,'')

    line = "{:26}{:12}{} \n".format(env, status + ":", filepath)

    if SORT:
        return line
    else:
        print line,


for line in status:

    if get_filepath_from_git_status(GREEN, AZURE, "new file", line, new_files, 'N'):
        continue

    if get_filepath_from_git_status(GREEN, GREEN, "modified", line, modified_staged, 'M'):
        continue

    if get_filepath_from_git_status(GREEN, YELLOW, "deleted", line, deleted_staged, 'D'):
        continue

    if get_filepath_from_git_status(RED, PURPLE, "modified", line, modified, 'm'):
        continue

    if get_filepath_from_git_status(RED, RED, "deleted", line, deleted, 'd'):
        continue

    if untracked_on:
        if get_filepath_from_git_status(RED, BLUE, "", line, untracked, 'u'):
            continue

    if line == 'Untracked files:\n':
        untracked_on = True

        if not staged_printed:
            staged_printed = True
            print_section(new_files + modified_staged + deleted_staged)

        not_staged_printed = True
        print_section(modified + deleted)

    if line == "Changes not staged for commit:\n":
        staged_printed = True
        print_section(new_files + modified_staged + deleted_staged)

    if line.startswith("no changes added to commit") or line.startswith("nothing added to commit but untracked"):
        untracked_printed = True
        print_section(untracked)

    if line != "\n" or not SORT:
        print line,


if not staged_printed:
    print_section(new_files + modified_staged + deleted_staged)

if not not_staged_printed:
    print_section(modified + deleted)

if not untracked_printed:
    print_section(untracked)

to_export = {
    'd': deleted,
    'D': deleted_staged,
    'm': modified,
    'M': modified_staged,
    'u': untracked,
    'N': new_files
}

envs = []


def escape_spaces(filepath):
    return filepath.replace(' ', '\ ')


for symbol, item in to_export.items():
    if item:
        files, lines = zip(*item)
        for i, f in enumerate(files, start=1):
            envs.append('export {}{}={}'.format(symbol, i, escape_spaces(f)))

        envs.append('export {}="{}"'.format(symbol, '\n'.join(map(escape_spaces, files))))

with open(sys.argv[1], 'w') as f:
    f.write('\n'.join(envs))

# fp.close()
