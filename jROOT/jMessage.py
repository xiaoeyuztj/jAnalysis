#!/usr/bin/env python

def jInfo(topic, contents):
    print("\033[32m[" + topic + "]\033[0m "+ contents)

def jWarn(topic, contents):
    print("\033[33m[" + topic + "]\033[0m "+ contents)

def jError(topic, contents):
    print("\033[31m[" + topic + "]\033[0m "+ contents)
