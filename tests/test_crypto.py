from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import pytest
from flask_common.crypto import (
    AuthenticationError,
    aes_decrypt,
    aes_encrypt,
    aes_generate_key,
)


def test_with_unversioned_data():
    data = 'test'

    # These were generated using the old encrypt functions.
    # We make sure the new functions can still decypher the old
    # encrypted data.
    key = b"\xe6\xb53\x90\xb8\x8f'-=e\x86z\xc3\x90\xff\xb8*\xf5\xd9\xaf\xb8\xad\x81\xcadl\xed\xf4\t\xe8\x9c*\r\x16\xd2\x00/\xd8\x86@)\xc1\x9b\x8d\xabo\xf7E\xbc\xf8\xae@\x98O\xf0\xd8[\xd0\xe1\x9a\xf5w\x03r"
    encrypted_data = b'o\x15\n\xef\x9a\xd62\x86\x81\x9cBS%\xfa\xf7\xdb\x1a\x9a9\xd2\xf8;\xe5\xc1\xd8l\x16\xdeH?\xcd\xd7D\x9d\xcd\xc2\x1ej\xabb\x86\xa4u@\x9f\x1b\xe2}FtQ\xd9\x1f\xd7\xa4\xc1\xe8\x94N\n\xe9\xb2\xa0\xccD2\xe9)'

    assert aes_decrypt(key, encrypted_data) == data


def test_with_unversioned_corrupted_data():
    data = 'test'

    # These were generated using the old encrypt functions.
    # We make sure the new functions can still decypher the old
    # encrypted data.
    key = b"\xe6\xb53\x90\xb8\x8f'-=e\x86z\xc3\x90\xff\xb8*\xf5\xd9\xaf\xb8\xad\x81\xcadl\xed\xf4\t\xe8\x9c*\r\x16\xd2\x00/\xd8\x86@)\xc1\x9b\x8d\xabo\xf7E\xbc\xf8\xae@\x98O\xf0\xd8[\xd0\xe1\x9a\xf5w\x03r"
    encrypted_data = b'a\x15\n\xef\x9a\xd62\x86\x81\x9cBS%\xfa\xf7\xdb\x1a\x9a9\xd2\xf8;\xe5\xc1\xd8l\x16\xdeH?\xcd\xd7D\x9d\xcd\xc2\x1ej\xabb\x86\xa4u@\x9f\x1b\xe2}FtQ\xd9\x1f\xd7\xa4\xc1\xe8\x94N\n\xe9\xb2\xa0\xccD2\xe9)'

    with pytest.raises(AuthenticationError):
        assert aes_decrypt(key, encrypted_data) == data


def test_with_versioned_data():
    data = 'test'
    key = aes_generate_key()
    assert aes_decrypt(key, aes_encrypt(key, data)) == data


def test_with_versioned_corrupted_data():
    data = 'test'
    key = aes_generate_key()
    encrypted_data = aes_encrypt(key, data)[3:]
    with pytest.raises(AuthenticationError):
        assert aes_decrypt(key, encrypted_data) == data


def test_with_unversioned_data_that_starts_with_byte_0():
    data = 'test'

    # These were generated using the old encrypt functions.
    # We make sure the new functions can still decypher the old
    # encrypted data.
    key = 'E2\x02\x18\xe5\xb9\xba5V.Z\x8d}\\\xa0\x1a\x1b=\x89]}\xe4\xcf\x92_\xe2\x83\xeaI\xcb\xdd\xabo\xbc\xad\r\xef\xa2\xa2\xfa\xd0\x03\x98$\x8aM\xe5\x88l\x80\xadl\xef\x08t\xc8\xfd\x9b\t\x98\x7f\xcb\x10\x85'
    encrypted_data = '\x00\x04\xa0\x01H\x00\x85eO{\x00\xe1\x05\xb1\xf4\xbc\x849\x16\x94\x96%\x9d<y\x07I\x05\xdf\xd1\x07\x94-t\x806-\x06#\x00\x93\xfew\x12\x84\xf4\xc1\xe7\x18\x81\xd2\xb1\xe0_\xed/\x99\xa8\x1d;Z\x93\x18h t\xf4\x91'

    assert aes_decrypt(key, encrypted_data) == data
