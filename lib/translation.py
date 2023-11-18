#!/usr/bin/python3
# -*- coding:utf-8 -*-

def init():
    global zh_global_dict
    zh_global_dict = {}
    global en_global_dict
    en_global_dict = {}


def changeLanguage(l):
    global language
    if l in ['zh', 'en']:
        language = l


def set_values_for_key(key, zh, en):
    set_zh_value(key, zh)
    set_en_value(key, en)


def set_zh_value(key, value):
    zh_global_dict[key] = value


def set_en_value(key, value):
    en_global_dict[key] = value


def get_value(key):
    try:
        return zh_global_dict[key] if language == 'zh' else en_global_dict[key]
    except Exception:
        print(f'Read {key}' + ' Failed\r\n')
        return key
