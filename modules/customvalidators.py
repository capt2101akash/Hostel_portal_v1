#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
class IS_IIITS():
    def __init__(self, mail_addr, error_message="Invalid Domain"):
        self.mail_addr = mail_addr
        self.error_message = error_message

    def __call__(self, value):
        error = None
        value = value.strip()
        if not value.endswith("iiits.in"):
            error = self.error_message
        return (value, error)
