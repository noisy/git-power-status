#!/bin/bash


if [ -z "$GIT_PREFIX" ]
then
      :  #$GIT_PREFIX is empty
else
      cd $GIT_PREFIX
fi

git -c color.status=always status | /home/kszumny/Devel/git-st/git_smart_status.py /tmp/$BASH_SESSION_ID.env

