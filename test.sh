#!/bin/bash

userdel gitlab-runner -r

pkexec rm -rf /etc/sudoers.d/gitlab-runner


sudo python3 main.py 
