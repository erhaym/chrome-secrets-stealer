from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad

# this mirrors Chromium Linux legacy encryption
# source.chromium.org/chromium/chromium/src/+/main:components/os_crypt/sync/os_crypt_linux.cc
SALT = b'saltysalt'
HARDCODED_PASS = b'peanuts'
IV = b' ' * 16
BLOCK_LENGTH = 16
ITERATIONS = 1

def remove_padding_bytes(decrypted: bytes, block_size: int = 16) -> bytes:
    """Removes extra bytes added so that the length fits the required block size"""
    return unpad(decrypted, block_size)

def decrypt_secret(secret: str, keyring_secret=None) -> bytes:
    """Decrypts AES-CBC ciphers"""
    if keyring_secret == None:
        key = PBKDF2(HARDCODED_PASS, SALT, BLOCK_LENGTH, ITERATIONS)
    else:
        key = PBKDF2(keyring_secret, SALT, BLOCK_LENGTH, ITERATIONS)

    cipher = AES.new(key, AES.MODE_CBC, IV=IV)
    decrypted_secret = cipher.decrypt(bytes.fromhex(secret[2*3:]))

    return remove_padding_bytes(decrypted_secret)
