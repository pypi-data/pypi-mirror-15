import base64
import hashlib


from cryptography.fernet import Fernet


def _generate_token(shared_secret):
    """
    Generates a Fernet token from a shared secret of any length.
    """
    if hasattr(shared_secret, 'encode'):
        shared_secret = shared_secret.encode('utf-8')

    # Turn any shared secret into a 32 byte hash.
    m = hashlib.md5()
    m.update(shared_secret)
    md5sum = m.hexdigest()

    # Base64 encode the hash and use it as the token
    return base64.b64encode(md5sum.encode('ascii'))


def encrypt(data, shared_secret):
    """
    Encrypts the data in an urlsafe format.
    """
    if hasattr(data, 'encode'):
        data = data.encode('utf-8')

    token = _generate_token(shared_secret)
    fernet = Fernet(token)
    enc_data = fernet.encrypt(data)
    return enc_data


def decrypt(encrypted_data, shared_secret):
    """
    Decrypts the encrypted data.
    Raises cryptography.fernet.InvalidToken when shared_secret is wrong.
    """
    token = _generate_token(shared_secret)
    fernet = Fernet(token)
    dec_data = fernet.decrypt(encrypted_data)
    return dec_data.decode(encoding='UTF-8')
