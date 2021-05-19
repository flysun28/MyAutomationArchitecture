# coding=utf-8


class GlobalVarDescriptor():
    
    def __init__(self, default):
        self.default = default
        self.vars = {}
    
    def __set__(self, instance, value):        
        self.vars[instance] = value    
        
    def __get__(self, instance, owner):
        return self.vars.get(instance, self.default)


class StatisDescriptor(GlobalVarDescriptor):
    '''
    描述符只能当做类变量，放在实例变量中不生效 ————缺失owner
    '''
    pass


class CoordinateDescriptor(GlobalVarDescriptor):
    
    def __get__(self, instance, owner):
        '''        
        :param instance: ExcelParser instance
        '''
        coord = owner.fd_coord.get(self.default)
        self.vars[instance] = coord
        return self.vars.get(instance, coord)
        