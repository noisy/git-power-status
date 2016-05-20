#!/usr/bin/python

import sys, re

# fp = open('/tmp/gitstatus')
# status = fp
status = sys.stdin

deleted = []
modified = []

for line in status:

    #    deleted:    README.md

    m = re.match("^\s*.\[31mdeleted:\s*(.*).\[m\s*$", line)
    if m:
        filepath = m.groups()[0]
        deleted.append(filepath)
        line = line.replace('deleted:', '[D{}] deleted:'.format(len(deleted)))

    #    modified:   requirements.txt
    m = re.match("^\s*.\[31mmodified:\s*(.*).\[m\s*$", line)
    if m:
        filepath = m.groups()[0]
        modified.append(filepath)
        line = line.replace('modified:', '[M{}] modified:'.format(len(modified)))


    print line,

# fp.close()
