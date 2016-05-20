#!/bin/bash

git -c color.status=always status | /home/kszumny/Devel/git-st/git_smart_status.py /tmp/$BASH_SESSION_ID.env

