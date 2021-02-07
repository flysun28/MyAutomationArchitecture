# coding=utf-8


class GlobalVarDescriptor():
    
    def __init__(self, default):
        self.default = default
        self.vars = {}
    
    def __set__(self, instance, value):
        self.vars[instance] = value
        
    def __get__(self, instance, owner):
        return self.vars.get(instance, self.default)
    
