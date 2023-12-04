#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 /Sirvelia

import sys

if sys.version_info[0] < 3:
    print("\nPython3 is needed to run wp-dev. Try \"python3 wp-dev.py\" instead\n")
    sys.exit(2)
elif sys.version_info[0] == 3 and sys.version_info[1] < 9:
    print("\nPython 3.9 or superior is needed to run wp-dev\n")
    sys.exit(2)

import os
import json

from .modules.argument_handler import define_args
from .modules.commands_handler import CommandList
from .utils.signals import handle_signals
from .utils import console

# Define WP-DEV Arguments
define_args()

# Handle console signals
handle_signals()

# Main Menu
command_list = CommandList()
command_list.choice()