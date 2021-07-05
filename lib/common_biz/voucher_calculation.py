'''
Created on 2021年6月4日
@author: 80319739
'''
from lib.common_biz.biz_db_operate import get_available_voucher
from lib.common.utils.misc_utils import to_pinyin, is_all_chinese
from lib.common.utils.globals import GlobalVar


class VouCalculator(object):
    '''
    根据优惠券类型，自动计算抵扣金额
    1. 消费券： maxAmount为面额
    2. 抵扣券：满maxAmount，减amount
    3. 折扣券：最低消费amount，单笔最高减maxAmount，ext为折扣
    4. 消费折扣券：同折扣券，usable_amt为剩余额度
    '''    
    def __init__(self, orig_amount=None, ssoid=None):
        self.ssoid = ssoid or GlobalVar.SSOID
        self.orig_amt = orig_amount
        self.vou_info = {}
        self._strategy = None

    @property
    def strategy(self):
        print('可币券扣减金额策略算法:', self._strategy.__qualname__)
        return self._strategy
    
    @strategy.setter
    def strategy(self, vou_type):
        if not self.vou_info:
            self.vou_info = get_available_voucher(self.ssoid, vou_type)
        for k in 'maxAmount', 'amount', 'ext1', 'usable_amt':
            self.vou_info[k] = float(self.vou_info[k]) if self.vou_info[k] else 0
        if is_all_chinese(vou_type):
            vou_type = to_pinyin(vou_type)
        try:
            self._strategy = eval('self.'+vou_type)
        except:
            raise AttributeError('Invalid voucher type: %s'+vou_type)
    
    def consumption_deduct(self, orig_amount):
        '消费券'
        return min(self.orig_amt or orig_amount, self.vou_info['maxAmount']*100)
    
    def deduction_deduct(self, orig_amount):
        '抵扣券'
        return min(self.orig_amt or orig_amount, self.vou_info['amount']*100)
    
    def discount_deduct(self, orig_amount):
        '折扣券'
        orig_amt = self.orig_amt or orig_amount
        return round(float(orig_amt * (1-self.vou_info['ext1'])), 2)
        
    def consumption_discount_deduct(self, orig_amount):
        '消费折扣券'
        orig_amt = self.orig_amt or orig_amount
        return min(round(float(orig_amt * (1-self.vou_info['ext1'])), 2),
                   self.vou_info['usable_amt']*100)
        
    def redpacket_deduct(self, orig_amount):
        '红包券'
        return self.consumption_deduct(orig_amount)
    
    xiaofei = consumption_deduct
    dikou = deduction_deduct
    zhekou = discount_deduct 
    xiaofeizhekou = consumption_discount_deduct
    hongbao = redpacket_deduct