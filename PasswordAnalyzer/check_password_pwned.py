import requests
import hashlib

def check_password_pwned(password):
    password_hash = hashlib.sha1(password.encode()).hexdigest().upper()

    prefix = password_hash[:5]
    suffix = password_hash[5:]
    url = "https://api.pwnedpasswords.com/range/"+prefix
    req = requests.get(url)
    resp = req.text

    hashes = resp.split("\n")
    for hash in hashes:
        if hash[:35] == suffix:
            return True
    return False