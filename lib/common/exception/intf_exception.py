# coding=utf-8

NO_FILE_PARSER = -1


class ArgumentException(Exception):
    
    def __str__(self, *args):
        return f'Arguments {args} error!'


class ExcelException(Exception):
    
    def __str__(self, arg):
        if type(arg).__base__ is Exception:
            return str(arg)
        elif isinstance(arg, str):
            return 'Excel file IOError: ' + arg
        

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "Error: %s" % msg
        
    def __str__(self):
        return self.msg

