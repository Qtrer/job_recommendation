from sklearn.naive_bayes import GaussianNB
from assessment.models import *
import random
from django.core.management.base import BaseCommand
import pandas as pd

def fake_Employee():
    Employee.objects.all().delete()
    for i in range(100):
        employee = Employee.objects.create(name='employee %s'%i, account='em%s'%i, password='em%s'%i, info='employee %s'%i,
                                           education='%s'%random.randint(1,4), english='%s'%random.randint(1,4))

def train_bayes():
    datafile = 'C:/Users/Noisy/Desktop/毕设/train_data.xls'
    data = pd.read_excel(datafile)
    cols = [
        'gradeEI',
        'gradeSN',
        'gradeTF',
        'gradeJP',
    ]
    train_data = data[cols]
    train_target = data['type']
    gnb = GaussianNB()
    gnb.fit(train_data, train_target)
    return gnb

def fake_PersonalityGrade():
    PersonalityGrade.objects.all().delete()
    for i in range(100):
        employee = Employee.objects.get(account='em%s'%i)
        personalityGrade = PersonalityGrade.objects.create(employee=employee,
                                                           gradeEI=random.randint(25, 100), gradeSN=random.randint(25, 100),
                                                           gradeTF=random.randint(25, 100),gradeJP=random.randint(25, 100),)
        gnb = train_bayes()
        train_X = [[personalityGrade.gradeEI, personalityGrade.gradeSN, personalityGrade.gradeTF, personalityGrade.gradeJP]]
        gradeType = gnb.predict(train_X)
        gradeType = gradeType[0]
        personalityGrade.type = gradeType
        personalityGrade.save()

def fake_SkillGrade():
    SkillGrade.objects.all().delete()
    SkillPaper.objects.all().delete()
    jobs = Job.objects.all()
    for job in jobs:
        requests = SkillRequest.objects.filter(job=job)
        for i in range(100):
            employee = Employee.objects.get(account='em%s' % i)
            totalGrade = 99
            realGrade = random.randint(0, totalGrade)
            grade = int((realGrade / totalGrade) * 100)
            totalScore1 = 33
            realScore1 = random.randint(0, totalScore1)
            score1 = int((realScore1 / totalScore1) * 100)
            totalScore2 = 50
            realScore2 = random.randint(0, totalScore2)
            score2 = int((realScore2 / totalScore2) * 100)
            totalScore3 = 16
            realScore3 = random.randint(0, totalScore3)
            score3 = int((realScore3 / totalScore3) * 100)
            score = [score1, score2, score3]
            skillPaper = SkillPaper.objects.create(employee=employee, job=job)
            skillQuestion = SkillQuestion.objects.filter(aspect='1').filter(enterpriseID=0)
            skillPaper.pid.add(*skillQuestion)
            skillGrade = SkillGrade.objects.create(employee=employee, job=job, grade=grade, paper=skillPaper)
            for i in range(len(requests)):
                skillScore = SkillScore.objects.create(grade=skillGrade, aspect=requests[i].aspect, score=score[i])


def fake_Enterprise():
    Enterprise.objects.all().delete()
    for i in range(10):
        enterprise = Enterprise.objects.create(name='enterprise %s'%i, account='en%s'%i, password='en%s'%i, info='enterprise %s'%i)

def fake_job():
    Job.objects.all().delete()
    enterprises = Enterprise.objects.all()
    for enterprise in enterprises:
        for i in range(10):
            job = Job.objects.create(enterprise=enterprise, name='job%s'%i)
            pt = []
            for p in PERSONALITYTYPE:
                pt.append(p[0])
            pty = pt[random.randint(0,15)]
            personalityRequest = PersonalityRequest.objects.create(job=job, type=pty)
            skillRequest = SkillRequest.objects.create(job=job, aspect='%s'%random.randint(1,4), level='%s'%random.randint(1,4))
            if i%3 == 0:
                skillRequest = SkillRequest.objects.create(job=job, aspect='%s' % random.randint(1, 4),
                                                           level='%s' % random.randint(1, 4))
            if i%5 == 0:
                skillRequest = SkillRequest.objects.create(job=job, aspect='%s' % random.randint(1, 4),
                                                           level='%s' % random.randint(1, 4))

def fake_PersonalityQuestion():
    PersonalityQuestion.objects.all().delete()
    for i in range(600):
        s=[]
        while len(s)<4:
            x=random.randint(1,4)
            if x not in s:
                s.append(x)
        pquestion = PersonalityQuestion.objects.create(title='title %s'%i, choiceA='A %s'%i, choiceB='B %s'%i,
                                                       choiceC='C %s' % i, choiceD='D %s'%i, aspect='%s'%random.randint(1,4),
                                                       scoreA=s[0], scoreB=s[1], scoreC=s[2], scoreD=s[3])

def fake_SkillQuestion():
    SkillQuestion.objects.all().delete()
    for i in range(300):
        squestion = SkillQuestion.objects.create(title='title %s'%i, choiceA='A %s'%i, choiceB='B %s'%i,
                                                       choiceC='C %s' % i, choiceD='D %s'%i, aspect='%s'%random.randint(1,4),
                                                       level='%s'%random.randint(1,3), answer='%s'%random.randint(1,4), score=1, enterpriseID=0)
    for i in range(300):
        squestion = SkillQuestion.objects.create(title='etitle %s' % i, choiceA='eA %s' % i, choiceB='eB %s' % i,
                                                 choiceC='eC %s' % i, choiceD='eD %s' % i,
                                                 aspect='%s' % random.randint(1, 4),
                                                 level='%s' % random.randint(1, 3),
                                                 answer='%s' % random.randint(1, 4), score=1, enterpriseID=1)

class Command(BaseCommand):
    help = 'Import personality question data for test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        # fake_Employee()
        # fake_Enterprise()
        # fake_job()
        # fake_PersonalityQuestion()
        # fake_SkillQuestion()
        # fake_PersonalityGrade()
        fake_SkillGrade()
        self.stdout.write(self.style.SUCCESS('end import'))