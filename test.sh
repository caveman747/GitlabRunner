#!/bin/bash

userdel gitlab-runner -r

pkexec rm -rf /etc/sudoers.d/gitlab-runner


python3 main.py 
