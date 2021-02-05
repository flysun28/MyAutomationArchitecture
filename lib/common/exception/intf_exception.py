# coding=utf-8


class ArgumentException(Exception):
    
    def __str__(self, *args):
        return f'Arguments {args} error!'
        