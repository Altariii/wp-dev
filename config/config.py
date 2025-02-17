#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of WP-DEV, check the LICENSE file for more information
# Copyright (c) 2024 /Sirvelia

from ..constants.config import CONFIG_FILE_PATH

import json

def get_config() -> dict:
    config_file = open(CONFIG_FILE_PATH)
    config = json.load(config_file)
    config_file.close()

    return config

def save_new_config(config: dict) -> None:
    config_file = open(CONFIG_FILE_PATH, 'w')
    json.dump(config, config_file, indent=4)
    config_file.close()    

def version() -> str:
    config = get_config()
    return config['version']

def workspaces() -> str:
    config = get_config()
    if 'workspaces' in config:
        return config['workspaces']
    return False

def git_accounts() -> list[dict]:
    config = get_config()
    if 'git_accounts' in config:
        return config['git_accounts']
    return False