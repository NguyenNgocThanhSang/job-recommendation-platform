from __future__ import unicode_literals

import os
import sys
from subprocess import PIPE, Popen

from django.utils.crypto import get_random_string

def get_random_secret_key():
    """
    Return a 50 character random string usable as a SECRET_KEY setting value.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)

print(get_random_secret_key())