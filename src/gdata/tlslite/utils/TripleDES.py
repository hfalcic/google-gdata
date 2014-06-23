"""Abstract class for 3DES."""
from __future__ import absolute_import
from __future__ import unicode_literals
from future.builtins import object

from .compat import * #For True

class TripleDES(object):
    def __init__(self, key, mode, IV, implementation):
        if len(key) != 24:
            raise ValueError()
        if mode != 2:
            raise ValueError()
        if len(IV) != 8:
            raise ValueError()
        self.isBlockCipher = True
        self.block_size = 8
        self.implementation = implementation
        self.name = "3des"

    #CBC-Mode encryption, returns ciphertext
    #WARNING: *MAY* modify the input as well
    def encrypt(self, plaintext):
        assert(len(plaintext) % 8 == 0)

    #CBC-Mode decryption, returns plaintext
    #WARNING: *MAY* modify the input as well
    def decrypt(self, ciphertext):
        assert(len(ciphertext) % 8 == 0)
