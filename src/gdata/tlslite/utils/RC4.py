"""Abstract class for RC4."""
from __future__ import absolute_import
from __future__ import unicode_literals
from future.builtins import object

from .compat import * #For False

class RC4(object):
    def __init__(self, keyBytes, implementation):
        if len(keyBytes) < 16 or len(keyBytes) > 256:
            raise ValueError()
        self.isBlockCipher = False
        self.name = "rc4"
        self.implementation = implementation

    def encrypt(self, plaintext):
        raise NotImplementedError()

    def decrypt(self, ciphertext):
        raise NotImplementedError()
