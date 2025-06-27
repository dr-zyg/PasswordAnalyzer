from get_password_length import *
from password_components import *
from strip_input import *
import math

def calculate_entropy(password):
    password = strip_input(password)
    length = get_password_length(password)
    range = 0
    if has_lowercase(password):
        range += 26
    if has_uppercase(password):
        range += 26
    if has_numbers(password):
        range += 10
    if has_symbols(password):
        range += 32
    
    entropy  = (length*math.log2(range))
    entropy = round(entropy, 2)
    return entropy
    