from get_password_length import *

def detect_sequential_characters(password):
    length = get_password_length(password)
    for i in range(length-2):
        if ord(password[i])+1  == ord(password[i+1]) and ord(password[i+1])+1 == ord(password[i+2]):
            return True
    return False