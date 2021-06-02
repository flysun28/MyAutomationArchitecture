
#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/13 17:28
# comment:

from lib.common.utils.globals import HTTPENCJSON_IN


# case_data = {
#     "token": "TOKEN_eyJhbGciOiJFQ0RTQSIsInYiOiIxIn0.eyJleHAiOjE2MjA1NDM4MDkzMjMsImlkIjoiMjA3NjA3NTkyNSIsImlkYyI6InNob3VtaW5nIiwidGlkIjoiZGZmcm05L1hRQzhkRmVBL0R1aFI4azVKTG45Z3lLK2RPTVh6RnJVZys1ekdNNGdCQ0JzMlpBVmxldE0yUmd2K3EwOVNLbzIwcjI1Ymk3S2gyMEpiRjR3RDNVc3EvODZpcnNSOGlaUm5kdzQ9In0.MEUCIEUd99uIVdBvuz73Qt_MbqUVHotDdAsxkbtuCCORqs00AiEAjnZp2KhF2Njc8ZvrGXwYPwWG3b-_z3zRhQsLYYOVEso",
#     "appId": "2033",
#     "appPackage": "com.oppo.usercenter",
#     "partnerCode": "80009",
#     "platform": "ATLAS"
# }
case_data = {'token': '',
             'appId': '',
             'appPackage': 'com.oppo.usercenter',
             'partnerCode': '2031',
             'platform': 'ATLAS'
}

if __name__ == '__main__':
    result = HTTPENCJSON_IN.post('/api/pay-flow/v290/get-process-token', case_data)
    print(result)