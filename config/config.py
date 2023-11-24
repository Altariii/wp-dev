#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of WP-DEV, check the LICENSE file for more information
# Copyright (c) 2024 /Sirvelia

import json

GITHUB_URL          = ''
CONFIG_FILE_PATH    = './config/config.json'

def get_config() -> dict:
    config_file = open(CONFIG_FILE_PATH)
    config = json.load(config_file)
    config_file.close()

    return config

def version() -> str:
    config = get_config()
    return config['version']