#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from collections import OrderedDict
import string

def lexical_features(token):
    """
    Extract lexical features from given token
    """
    lowercase = token.lower()
    first4 = lowercase[:4]
    last4 = lowercase[-4:]
    return OrderedDict([
            ('lowercase', lowercase), 
            ('first4', first4),
            ('last4', last4)
            ])
            
def _char_shape(char):
    if char in string.ascii_uppercase:
        return 'A'
    if char in string.ascii_lowercase:
        return 'a'
    if char in string.digits:
        return '0'
    else:
        return char

def _shape(token):
    return ''.join([_char_shape(char) for char in token])

def _contains_a_letter(token):
    shape = _shape(token)
    return 'a' in shape.lower()
    
def _contains_a_capital(token):
    shape = _shape(token)
    return 'A' in shape

def _begins_with_capital(token):
    return _char_shape(token[0]) == 'A'

def _all_capital(token):
    return set(_shape(token)) == set('A')

def _contains_a_digit(token):
    shape = _shape(token)
    return '0' in shape

def _all_digit(token):
    shape = _shape(token)
    return set(shape) == set('0')

def _contains_a_punctuation(token):
    return len(set(string.punctuation) & set(token)) > 0

def _consists_letters_n_digits(token):
    shape = _shape(token)
    return set(shape.lower()) == set('a0')

def _consists_digits_n_punctuations(token):
    shape = _shape(token)
    lower_shape = shape.lower()
    return set(lower_shape) <= set(string.punctuation+'0') and len(lower_shape) >= 2
    
def orthographic_features(token):
    """
    Extract orthographic features from given token
    """

    return OrderedDict([
                    ('shape', _shape(token)), 
                    ('length', len(token)), 
                    ('contains_a_letter', _contains_a_letter(token)), 
                    ('contains_a_capital', _contains_a_capital(token)),
                    ('begins_with_capital', _begins_with_capital(token)), 
                    ('all_capital', _all_capital(token)), 
                    ('contains_a_digit', _contains_a_digit(token)),
                    ('all_digit', _all_digit(token)),
                    ('contains_a_punctuation', _contains_a_punctuation(token)),
                    ('consists_letters_n_digits', _consists_letters_n_digits(token)),
                    ('consists_digits_n_punctuations', _consists_digits_n_punctuations(token)),
                   ])