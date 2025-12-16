"""Sorting utilities"""
import re

def natural_sort_key(s):
    """Natural sorting key for strings with numbers"""
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', s)]
