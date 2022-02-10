#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/19 17:08
# comment:
import time
import simplejson
from lib.common.file_operation.config_operation import Config
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.globals import GlobalVar
from lib.config.path import common_sql_path


class Voucher:
    def __init__(self, in_out="inland"):
        self.in_out = in_out
        if in_out == "inland":
            self.mysql = GlobalVar.MYSQL_IN
            server_info = GlobalVar.ZK_CLIENT_IN.get_node_info("com.oppo.voucher.api.CouponBatchGrant")
            self.conn = DubRunner(server_info['ip_port'][0], server_info['ip_port'][1])
        if in_out == "oversea":
            self.mysql_out = GlobalVar.MYSQL_OUT
            server_info = GlobalVar.ZK_CLIENT_OUT.get_node_info("com.oppo.voucher.api.CouponBatchGrant")
            self.conn = DubRunner(server_info['ip_port'][0], server_info['ip_port'][1])

    def grantVoucher(self, bizNo, couponType, couponDiscountType, conditionAmount, cutAmount, ssoid, country="",
                     currency='', ratio=0, maxCutAmount='0'):
        """
        优惠券申请
        :param currency: 海外需要传
        :param country: 海外需要传
        :param bizNo:
        :param couponType:
        :param couponDiscountType:
        :param conditionAmount:
        :param cutAmount:
        :param ssoid:
        :param ratio:
        :param maxCutAmount:
        :return:
        """
        scopeId = ''
        if self.in_out == "inland":
            scopeId = self.mysql.select_one(str(Config(common_sql_path).read_config("voucher", "scope_id")).
                                            format("all"))['scopeId']
        elif self.in_out == "oversea":
            scopeId = self.mysql_out.select_one(str(Config(common_sql_path).read_config("voucher", "scope_id_oversea")).
                                                format("all"))['scopeId']
        data = {
            "couponName": "anto_grant" + str(int(round(time.time() * 1000))),
            "useableFromTime": "2020-01-01 00:00:00",
            "useableEndTime": "2022-12-31 00:00:00",
            "settleType": "1",
            # "2031"
            "bizNo": bizNo,
            "scopeId": scopeId,
            "blackScopeId": "",
            "subScopeId": "",
            # "KB_COUPON"
            "couponType": couponType,
            # "DIKOU"
            "couponDiscountType": couponDiscountType,
            # 满（折扣券/消费折扣券最低消费金额）
            "conditionAmount": str(conditionAmount),
            # 减
            "cutAmount": str(cutAmount),
            # 折扣券打折
            "ratio": ratio,
            # 折扣券最高抵扣金额
            "maxCutAmount": maxCutAmount,
            "applyCount": "1",
            "ssoidList": [ssoid],
            "batchId": ""
        }
        if self.in_out == "oversea":
            # 海外需要额外的字段
            data['country'] = country
            data['currency'] = currency
            data["timezone"] = "GMT+07:00"
            data["isAdmin"] = "true"
            data["applyUserName"] = "80264408"
        result = self.conn.invoke(
            "com.oppo.voucher.api.CouponBatchGrant",
            "batchGrant",
            data
        )
        return {"batchId": result['data']['batchId'], "vouId": int(result['data']['batchVouCreateResList'][0]['vouId'])}

    def checkVoucher(self, couponBatchId):
        """
        优惠券审核
        :return:
        """
        data = {"couponBatchId": couponBatchId, "batchOperateType": "PASS"}
        self.conn.invoke(
            "com.oppo.voucher.api.admin.CouponBatchInfoAdmin",
            "operate",
            data
        )
    
    def grant_check_voucher(self, bizNo, couponType, couponDiscountType, conditionAmount, cutAmount, ssoid, country="",
                                currency='', ratio=0, maxCutAmount='0'):
        vou_info = self.grantVoucher(bizNo, couponType, couponDiscountType, conditionAmount, cutAmount, ssoid, country, currency, ratio, maxCutAmount)
        time.sleep(0.5)
        self.checkVoucher(vou_info['batchId'])
    
    def query_voucher_by_id(self, ssoid, vou_id):
        data = ssoid, vou_id
        self.conn.invoke(
            "com.oppo.voucher.api.CouponQuery",
            "queryVoucherById",
            data,
            flag='STRING'
        )
    
    def query_all_useable(self, ssoid, order_amount=0, discount_type='', partner_id='2031'):
        '''
        :param ssoid:
        :param order_amount: 订单金额，为0不校验
        :param discount_type: one choice of [DAZHE, XIAOFEI, DIKOU]
        :param partner_id:
        '''
        req = {
            'country': 'CN',
            'currency': 'CNY',
            'ssoid': ssoid,
            'orderAmount': order_amount or 0,
            'couponType': 'KB_COUPON',
            'couponDiscountType': '',   # DAZHE, XIAOFEI, DIKOU, XIAOFEI_DAZHE
            'couponName': '',
            'couponStatus': '',    # NORMAL, WAIT, ABANDON, REJECT, EXPIRED, USED
            'grantTimeFrom': '',    # yyyy-MM-dd HH:mm:ss
            'grantTimeTo': '',      # yyyy-MM-dd HH:mm:ss
            'couponCode': '',
            'bizNo': partner_id,
            'appPackage': 'com.example.pay_demo',
            'factor': '',
            'showUnuseable': 'false',
            'bizNoList': []
        }
        if not discount_type:
            req.pop('couponDiscountType')
        result = self.conn.invoke(
            'com.oppo.voucher.api.CouponQuery',
            'useableKbCoupons',
            req,
            flag='JSON'
        )
        for vou in result['data']:
            print(vou)
#             print(simplejson.dumps(vou, indent=3, ensure_ascii=False))
        return result


if __name__ == '__main__':
    flag = "0"
    vou = Voucher()
    # vou.query_all_useable('2086776969')
    if flag == "1":
        # 满减
        vou_info = vou.grantVoucher("2031", "KB_COUPON", "DIKOU", "10", "9.99", "2076075925")
        vou.checkVoucher(vou_info['batchId'])
        # 消费
    if flag == "2":
        vou_info = vou.grantVoucher("2031", "KB_COUPON", "XIAOFEI", "0", "10", "2076075925")
        vou.checkVoucher(vou_info['batchId'])
    if flag == "3":
        # 红包券
        vou_info = vou.grantVoucher("5456925", "KB_COUPON", "RED_PACKET_COUPON", "0", "10", "2076075925")
        vou.checkVoucher(vou_info['batchId'])
    if flag == "4":
        # 海外满减
        vou_info = Voucher("oversea").grantVoucher("9809089", "KB_COUPON", "DIKOU", "10000", "7500", "2076075925", "VN",
                                                   "VND")
        Voucher("oversea").checkVoucher(vou_info['batchId'])
    
    