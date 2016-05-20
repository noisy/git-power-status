#!/usr/bin/python

import sys
import re

BOLD = '\033[1m'

RED = '\033[31m'
LIGHT_RED = '\033[31m' + BOLD

GREEN = '\033[32m'
LIGHT_GREEN = '\033[32m' + BOLD

YELLOW = '\033[33m'
LIGHT_YELLOW = '\033[33m' + BOLD

YELLOW = '\033[33m'
LIGHT_YELLOW = '\033[33m' + BOLD

BLUE = '\033[34m'
LIGHT_BLUE = '\033[34m' + BOLD

PURPLE = '\033[35m'
LIGHT_PURPLE = '\033[35m' + BOLD

AZURE = '\033[36m'
LIGHT_AZURE = AZURE + BOLD

END = '\033[0m'

# fp = open('/tmp/gitstatus2')
# status = fp
status = sys.stdin

deleted = []
deleted_staged = []
modified = []
modified_staged = []
new_files = []
untracked = []

untracked_on = False

for line in status:

    #    deleted:    README.md

    m = re.match("^\s*.\[31mdeleted:\s*(.*).\[m\s*$", line)
    if m:
        filepath = m.groups()[0]
        deleted.append(filepath)
        line = line.replace('{}deleted:'.format(RED), '{}[d{}]{}{} deleted:'.format(LIGHT_RED, len(deleted), END, RED))

    m = re.match("^\s*.\[32mdeleted:\s*(.*).\[m\s*$", line)
    if m:
        filepath = m.groups()[0]
        deleted_staged.append(filepath)
        line = line.replace('{}deleted:'.format(GREEN), '{}[D{}]{}{} deleted:'.format(LIGHT_YELLOW, len(deleted_staged), END, YELLOW))



    #    modified:   requirements.txt
    m = re.match("^\s*.\[31mmodified:\s*(.*).\[m\s*$", line)
    if m:
        filepath = m.groups()[0]
        modified.append(filepath)
        line = line.replace('{}modified:'.format(RED), '{}[m{}]{}{} modified:'.format(LIGHT_RED, len(modified), END, RED))

    #    modified:   requirements.txt
    m = re.match("^\s*.\[32mmodified:\s*(.*).\[m\s*$", line)
    if m:
        filepath = m.groups()[0]
        modified_staged.append(filepath)
        line = line.replace('{}modified:'.format(GREEN), '{}[M{}]{}{} modified:'.format(LIGHT_GREEN, len(modified_staged), END, GREEN))


    #    new file:   y
    m = re.match("^\s*.\[32mnew file:\s*(.*).\[m\s*$", line)
    if m:
        filepath = m.groups()[0]
        new_files.append(filepath)
        line = line.replace('{}new file:'.format(GREEN),
                            '{}[N{}]{}{} new file:'.format(LIGHT_AZURE, len(new_files), END, AZURE))

    if line == 'Untracked files:\n':
        untracked_on = True

    if untracked_on:
        m = re.match("^\s*.\[31m(.*).\[m\s*$", line)
        if m:
            filepath = m.groups()[0]
            untracked.append(filepath)
            line = line.replace('{}'.format(RED),
                        '{}[u{}]{}{} '.format(LIGHT_PURPLE, len(untracked), END, PURPLE))

    print line,


to_export = {
    'd': deleted,
    'D': deleted_staged,
    'm': modified,
    'M': modified_staged,
    'u': untracked,
    'N': new_files
}

envs = []

for symbol, files in to_export.items():
    for i, f in enumerate(files, start=1):
        envs.append('export {}{}="{}"'.format(symbol, i, f))

    envs.append('export {}="{}"'.format(symbol, '\n'.join(files)))

with open(sys.argv[1], 'w') as f:
    f.write('\n'.join(envs))

# fp.close()
