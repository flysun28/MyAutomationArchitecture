import requests as request
import time


# 代码统计地址
url = "http://code.oppoer.me/api/git/statistics/contribution_statistics"
# 登录cookie
cookie = "user=80264408; SESSION=OWJkNmU0NDEtZWZhYS00YjlmLTk0NDctZWU5MWZkYTYxZTc0"
# 本月bug总数
bugnum = 100
# 统计开始时间
start_time = "2021-06-01"
# 统计截至时间
end_time = "2021-06-30"
# 项目与id
projects = {
    "hworder-server": 2497
}


def requests(projectId):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Cookie": cookie
    }
    payload = {
        "startTime": int(time.mktime(time.strptime(start_time, "%Y-%m-%d")) * 1000),
        "endTime": int(time.mktime(time.strptime(end_time, "%Y-%m-%d")) * 1000),
        "interval": 86400000,
        "projectId": projectId
    }
    res = request.get(url, headers=headers, params=payload)
    return res.json()


def staticOneProject(result, project):
    sumneweline = 0
    sumdeleteline = 0
    try:
        newallcode = result.get("data").get("all")
        for newcode in newallcode:
            sumneweline = sumneweline + newcode.get('newLine')
            sumdeleteline = sumdeleteline + newcode.get('deleteLine')
    except Exception:
        print(project, "解析结果异常：")
    return sumneweline, sumdeleteline


def calcAllProjectCode(projects):
    addcodelines = 0
    deletecodelines = 0
    for (project, projectId) in projects.items():
        someRequestResult = requests(projectId)
        somneStaticResult = staticOneProject(someRequestResult, project)
        print(project,"新增代码行数:", somneStaticResult[0])
        print(project,"删除代码行数:", somneStaticResult[1])
        addcodelines = addcodelines + somneStaticResult[0]
        deletecodelines = deletecodelines + somneStaticResult[1]
    print("所有项目代码新增行数:", addcodelines)
    print("所有项目代码删除行数:", deletecodelines)
    print("所有项目代码改动行数（新增代码行数+删除代码行数）:", addcodelines + deletecodelines)
    print("千行代码覆盖率：", bugnum/(addcodelines + deletecodelines)/1000)


calcAllProjectCode(projects)
