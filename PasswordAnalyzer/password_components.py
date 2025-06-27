def has_lowercase(password):
    has_lower = False
    for c in password:
        if ord(c)>=97 and ord(c)<=122:
            has_lower = True
            break
    return has_lower

def has_numbers(password):
    has_numbers = False
    for c in password:
        if ord(c)<=57 and ord(c)>=48:
            has_numbers = True
            break
    return has_numbers

def has_symbols(password):
    has_symbols = False
    for c in password:
        if (ord(c)<=47 and ord(c)>=33) or (ord(c)<=64 and ord(c)>=58) or (ord(c)<=91 and ord(c)>=96) or (ord(c)<=126 and ord(c)>=123):
            has_symbols = True
            break
    return has_symbols

def has_uppercase(password):
    has_uppercase = False
    for c in password:
        if ord(c)<=90 and ord(c)>=65:
            has_uppercase = True
            break
    return has_uppercase

