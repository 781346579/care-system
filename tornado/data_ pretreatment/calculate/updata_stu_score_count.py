from calculate.orm import *
from datetime import datetime,timedelta
def updataStuScoreCount():
    print('updata stu_score_count')
    day = timedelta(days=1)
    nowdate = datetime.today()-day  #昨天
    old_count = stu_score_count.select(stu_score_count.stuID,stu_score_count.countDate)
    restart = 0  # 用于判断是否要重新更新表
    if len(old_count) > 0:
        if nowdate.date() != old_count[0].countDate.date():  # 判断表里的数据是否是最新的
            query = stu_score_count.delete().where(stu_score_count.countDate != nowdate)#清空表
            query.execute()
            restart = 1  # 要重新更新
    if len(old_count) == 0 or restart == 1:  # 第一次运行或者新的一天
        allStuId = stu_basic_info.select(stu_basic_info.stuID)
        for i in range(len(allStuId)):
            countScoreNum(allStuId[i].stuID)
    print('updata stu_score_count is ok')
    return {'status': 1}

def countScoreNum(stuId):
    nowStuRecord = MyBaseModel.returnList2(exam_results.select(exam_results.examScore).where(exam_results.stuID==stuId))
    day=timedelta(days=1)
    endDate = datetime.today()-day  #今天的前一天
    failnum=0
    for record in nowStuRecord:
        if record.examScore<60:
            failnum=failnum+1
    stu_score_count.create(stuID=stuId,failNum=failnum,countDate=endDate)



