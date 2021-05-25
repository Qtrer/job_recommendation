from django.utils.datetime_safe import datetime
from django_pandas.io import read_frame
from django.shortcuts import render, redirect
from django.urls import reverse
import random
from sklearn import preprocessing
from assessment.models import *
from assessment.forms import *
from django.forms.models import modelformset_factory
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np
import math

# Create your views here.
P_TEST_NUM = 25                          #default = 25
P_TEST_SCORE = 2*P_TEST_NUM
S_TEST_NUM = 100                         #default = 100

def index(request):
    employee = Employee.objects.get(id=1)
    return render(request, 'index.html', locals())

def register(request):
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            account = registerForm.cleaned_data['account']
            password = registerForm.cleaned_data['password']
            confirm_password = registerForm.cleaned_data['confirm_password']
            email = registerForm.cleaned_data['email']
            phone = registerForm.cleaned_data['phone']
            status = registerForm.cleaned_data['status']
            if password != confirm_password:
                message = '两次密码不一致'
                registerForm = RegisterForm()
                return render(request, 'register.html', locals())
            if status == '1':
                try:
                    employee = Employee.objects.get(account=account)
                except Employee.DoesNotExist:
                    employee = Employee.objects.create(account=account, password=password, email=email, phone=phone)
                    employee.save()
                    messages = '注册成功'
                    loginForm = UserForm()
                    return render(request, 'login.html', locals())
                message = '账号已存在'
                registerForm = RegisterForm()
                return render(request, 'register.html', locals())
            else:
                try:
                    enterprise = Enterprise.objects.get(account=account)
                except Enterprise.DoesNotExist:
                    enterprise = Enterprise.objects.create(account=account, password=password, email=email, phone=phone)
                    enterprise.save()
                    messages = '注册成功'
                    loginForm = UserForm()
                    return render(request, 'login.html', locals())
                message = '账号已存在'
                registerForm = RegisterForm()
                return render(request, 'register.html', locals())
    registerForm = RegisterForm()
    return render(request, 'register.html', locals())

def login(request):
    if request.method == 'POST':
        loginForm = UserForm(request.POST)
        if loginForm.is_valid():
            account = loginForm.cleaned_data['account']
            password = loginForm.cleaned_data['password']
            try:
                employee = Employee.objects.get(account=account)
                if password == employee.password:
                    return redirect('employeeIndex', id = employee.id)
                else:
                    message = '密码错误'
                    return render(request, 'login.html', locals())
            except Employee.DoesNotExist:
                try:
                    enterprise = Enterprise.objects.get(account=account)
                    if password == enterprise.password:
                        return redirect('enterpriseIndex', id = enterprise.id)
                    else:
                        message = '密码错误'
                        return render(request, 'login.html', locals())
                except Enterprise.DoesNotExist:
                    message = '用户不存在'
                    return render(request, 'login.html', locals())
    loginForm = UserForm()
    return render(request, 'login.html', locals())

def logout(request):
    return render(request, 'login.html')

def employeeIndexFilter(employee, jobs):
    grades = []
    enterprises = ['---']
    citys = ['---']
    for job in jobs:
        grade = SkillGrade.objects.filter(employee=employee).filter(job=job)
        grades.append(grade)
        enterprise = job.enterprise
        if enterprise not in enterprises:
            enterprises.append(enterprise)
        city = job.get_city_display()
        if city not in citys:
            citys.append(city)
    jg = zip(jobs, grades)
    return enterprises, citys, jg

def employeeIndex(request, id):
    employee = Employee.objects.get(id=id)
    jobs = Job.objects.all().order_by('-salary')
    enterprises, citys, jg = employeeIndexFilter(employee, jobs)
    return render(request, 'employee/employee_index.html', locals())

def orderbyEnterprise(request, id, eid):
    employee = Employee.objects.get(id=id)
    enterprise = Enterprise.objects.get(id=eid)
    jobs = Job.objects.filter(enterprise=enterprise).order_by('-salary')
    enterprises, citys, jg = employeeIndexFilter(employee, jobs)
    return render(request, 'employee/employee_index.html', locals())

def orderbyCity(request, id, city):
    employee = Employee.objects.get(id=id)
    jobs = Job.objects.all().order_by('-salary')
    a=[]
    for job in jobs:
        if job.get_city_display() == city:
            a.append(job)
    jobs = a
    enterprises, citys, jg = employeeIndexFilter(employee, jobs)
    return render(request, 'employee/employee_index.html', locals())

def employeeUpdate(request, id):
    employee = Employee.objects.get(id=id)
    employeeForm = EmployeeForm()
    employeeForm.fields['name'].initial = employee.name
    employeeForm.fields['account'].initial = employee.account
    employeeForm.fields['password'].initial = employee.password
    employeeForm.fields['education'].initial = employee.education
    employeeForm.fields['english'].initial = employee.english
    employeeForm.fields['email'].initial = employee.email
    employeeForm.fields['phone'].initial = employee.phone
    employeeForm.fields['info'].initial = employee.info
    return render(request, 'employee/employee_update.html', locals())

def employeeUpdateHandler(request, id):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            education = form.cleaned_data['education']
            english = form.cleaned_data['english']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            info = form.cleaned_data['info']
            employee = Employee.objects.get(id=id)
            employee.name = name
            employee.password = password
            employee.education = education
            employee.english = english
            employee.email = email
            employee.phone = phone
            employee.info = info
            employee.save()
    return redirect(reverse('employeeIndex', args=(id,)))

def personalityTest(request, id):
    employee = Employee.objects.get(id=id)
    try:
        grade = PersonalityGrade.objects.get(employee=employee)
    except PersonalityGrade.DoesNotExist:
        try:
            paper = PersonalityPaper.objects.get(employee=employee)
        except PersonalityPaper.DoesNotExist:
            paper = createPersonalityPaper(request, id)
        newPaper = paper
        return render(request, 'employee/personality_test.html', locals())
    return render(request, 'employee/personality_grade.html', locals())

def createPersonalityPaper(request, id):
    employee = Employee.objects.get(id=id)
    newPaper = PersonalityPaper()
    newPaper.employee = employee
    newPaper.employeeName = employee.name
    newPaper.save()
    for i in range(1, 5):
        questionID = PersonalityQuestion.objects.filter(aspect='%s' % i).values_list('id', flat=True)
        questionID = list(questionID)
        randID = random.sample(questionID, P_TEST_NUM)
        newPaper.pid.add(*PersonalityQuestion.objects.filter(id__in=randID).all())
        newPaper.save()
    return newPaper

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

def rePersonalityTest(request, id):
    employee = Employee.objects.get(id=id)
    PersonalityPaper.objects.filter(employee=employee).delete()
    PersonalityGrade.objects.filter(employee=employee).delete()
    try:
        paper = PersonalityPaper.objects.get(employee=employee)
    except PersonalityPaper.DoesNotExist:
        paper = createPersonalityPaper(request, id)
    newPaper = paper
    return render(request, 'employee/personality_test.html', locals())

def calPersonalityGrade(request, id):
    if request.method == 'POST':
        employeeID = request.POST.get('employeeID')
        paperID = request.POST.get('paperID')
        employee = Employee.objects.get(id=employeeID)
        paper = PersonalityPaper.objects.get(id=paperID)
        try:
            grade = PersonalityGrade.objects.get(employee=employee)
        except PersonalityGrade.DoesNotExist:
            grade = PersonalityGrade()
            grade.employee = employee
            grade.save()
        grade = grade
        question = PersonalityPaper.objects.filter(id=paperID).values('pid')\
            .values('pid__id', 'pid__aspect', 'pid__scoreA', 'pid__scoreB', 'pid__scoreC', 'pid__scoreD')
        scoreEI=scoreSN=scoreTF=scoreJP=0
        for q in question:
            qid = str(q['pid__id'])
            asp = q['pid__aspect']
            ans = request.POST.get(qid)
            if ans == 'A':
                if asp == '1':
                    scoreEI += q['pid__scoreA']
                elif asp == '2':
                    scoreSN += q['pid__scoreA']
                elif asp == '3':
                    scoreTF += q['pid__scoreA']
                elif asp == '4':
                    scoreJP += q['pid__scoreA']
            elif ans == 'B':
                if asp == '1':
                    scoreEI += q['pid__scoreB']
                elif asp == '2':
                    scoreSN += q['pid__scoreB']
                elif asp == '3':
                    scoreTF += q['pid__scoreB']
                elif asp == '4':
                    scoreJP += q['pid__scoreB']
            elif ans == 'C':
                if asp == '1':
                    scoreEI += q['pid__scoreC']
                elif asp == '2':
                    scoreSN += q['pid__scoreC']
                elif asp == '3':
                    scoreTF += q['pid__scoreC']
                elif asp == '4':
                    scoreJP += q['pid__scoreC']
            elif ans == 'D':
                if asp == '1':
                    scoreEI += q['pid__scoreD']
                elif asp == '2':
                    scoreSN += q['pid__scoreD']
                elif asp == '3':
                    scoreTF += q['pid__scoreD']
                elif asp == '4':
                    scoreJP += q['pid__scoreD']
        grade.gradeEI = scoreEI
        grade.gradeSN = scoreSN
        grade.gradeTF = scoreTF
        grade.gradeJP = scoreJP
        grade.save()
        gnb = train_bayes()
        train_X = [[scoreEI, scoreSN, scoreTF, scoreJP]]
        gradeType = gnb.predict(train_X)
        gradeType = gradeType[0]
        grade.type = gradeType
        grade.save()
        grade.get_type_display = grade.get_type_display
    return render(request, 'employee/personality_grade.html', locals())

def createSkillPaper(request, id, jid):
    employee = Employee.objects.get(id=id)
    job = Job.objects.get(id=jid)
    newPaper = SkillPaper()
    newPaper.employee = employee
    newPaper.job = job
    newPaper.save()
    requests = SkillRequest.objects.filter(job=job).values_list('id', flat=True)
    requests = list(requests)
    questionSize = int(S_TEST_NUM / len(requests))
    for i in requests:
        aspect = SkillRequest.objects.get(id=i).aspect
        level = SkillRequest.objects.get(id=i).level
        questionID = SkillQuestion.objects.filter(aspect='%s'%aspect)
        if job.questionSource == '0':
            questionID = questionID.filter(enterpriseID=0)
        else:
            questionID = questionID.filter(enterpriseID=job.enterprise.id)
        questionID1 = questionID.filter(level='1').values_list('id', flat=True)
        questionID2 = questionID.filter(level='2').values_list('id', flat=True)
        questionID3 = questionID.filter(level='3').values_list('id', flat=True)
        questionID1 = list(questionID1)
        questionID2 = list(questionID2)
        questionID3 = list(questionID3)
        if level == '1':
            randID1 = random.sample(questionID1, int(questionSize / 2))
            randID2 = random.sample(questionID2, int(questionSize / 3))
            randID3 = random.sample(questionID3, int(questionSize / 6))
        elif level == '2':
            randID1 = random.sample(questionID1, int(questionSize / 3))
            randID2 = random.sample(questionID2, int(questionSize / 3))
            randID3 = random.sample(questionID3, int(questionSize / 3))
        elif level == '3':
            randID1 = random.sample(questionID1, int(questionSize / 6))
            randID2 = random.sample(questionID2, int(questionSize / 3))
            randID3 = random.sample(questionID3, int(questionSize / 2))
        newPaper.pid.add(*SkillQuestion.objects.filter(id__in=randID1).all())
        newPaper.pid.add(*SkillQuestion.objects.filter(id__in=randID2).all())
        newPaper.pid.add(*SkillQuestion.objects.filter(id__in=randID3).all())
    newPaper.save()
    return newPaper

def skillTest(request, id, jid):
    employee = Employee.objects.get(id=id)
    job = Job.objects.get(id=jid)
    try:
        grade = SkillGrade.objects.filter(job=job).get(employee=employee)
    except SkillGrade.DoesNotExist:
        try:
            paper = SkillPaper.objects.filter(job=job).get(employee=employee)
        except SkillPaper.DoesNotExist:
            paper = createSkillPaper(request, id, jid)
        newPaper = paper
        return render(request, 'employee/skill_test.html', locals())
    scores = SkillScore.objects.filter(grade=grade)
    return render(request, 'employee/skill_grade.html', locals())

def skillGradeList(request, id):
    employee = Employee.objects.get(id=id)
    grades = SkillGrade.objects.filter(employee=employee)
    return render(request, 'employee/skill_grade_list.html', locals())

def calSkillGrade(request, id, jid):
    if request.method == 'POST':
        employeeID = request.POST.get('employeeID')
        paperID = request.POST.get('paperID')
        jobID = request.POST.get('jobID')
        employee = Employee.objects.get(id=employeeID)
        paper = SkillPaper.objects.get(id=paperID)
        job = Job.objects.get(id=jid)
        try:
            grade = SkillGrade.objects.get(paper=paper)
        except SkillGrade.DoesNotExist:
            grade = SkillGrade.objects.create(employee=employee, job=job, paper=paper)
            grade.grade = 0
            grade.save()
        grade = grade
        question = SkillPaper.objects.filter(id=paperID).values('pid')\
            .values('pid__id', 'pid__aspect', 'pid__score', 'pid__answer')
        requests = SkillRequest.objects.filter(job=job)
        totalGrade = 0
        realGrade = 0
        for r in requests:
            score = SkillScore.objects.create(grade=grade, aspect=r.aspect, score=0)
            totalScore = 0
            realScore = 0
            for q in question:
                if q['pid__aspect'] == r.aspect:
                    qid = str(q['pid__id'])
                    ans = request.POST.get(qid)
                    totalGrade += q['pid__score']
                    totalScore += q['pid__score']
                    if ans == q['pid__answer']:
                        realGrade += q['pid__score']
                        realScore += q['pid__score']
            score.score = int((realScore/totalScore)*100)
            score.save()
        grade.grade = int((realGrade/totalGrade)*100)
        grade.save()
        scores = SkillScore.objects.filter(grade=grade)
        print(SkillScore.objects.all())
        if grade.grade >= 60:
            calMatchingScore(id, jid)
    return render(request, 'employee/skill_grade.html', locals())

def calMatchingScore(id, jid):
    employee = Employee.objects.get(id=id)
    job = Job.objects.get(id=jid)
    employees = Employee.objects.filter(skillgrade__job=job, skillgrade__grade__gte=60)
    if employees.exists():
        requests = SkillRequest.objects.filter(job=job)
        totalData = get_data(job)
        flag = 0
        count = 6
        for r in requests:
            count += 1
        if job.personalityrequest.EIweight == job.personalityrequest.SNweight == job.personalityrequest.TFweight \
                == job.personalityrequest.JPweight == job.educationWeight == job.englishWeight == 1:
            flag = 1
        for r in requests:
            if r.weight != 1:
                flag = 0
        if flag == 1:
            weight = entropy(totalData)
        else:
            w = [(job.educationWeight / count), (job.englishWeight / count),
                 (job.personalityrequest.EIweight / count), (job.personalityrequest.SNweight / count),
                 (job.personalityrequest.TFweight / count), (job.personalityrequest.JPweight / count)]
            for r in requests:
                w.append((r.weight / count))
            weight = w
            print(weight)
        weight = weight
        jobData = [4, 4, 25, 25, 25, 25]
        jType = job.personalityrequest.type
        if jType == '1':
            jobData[5] = 100
        elif jType == '10':
            jobData[4] = 100
        elif jType == '11':
            jobData[5] = 100
            jobData[4] = 100
        elif jType == '100':
            jobData[3] = 100
        elif jType == '101':
            jobData[5] = 100
            jobData[3] = 100
        elif jType == '110':
            jobData[4] = 100
            jobData[3] = 100
        elif jType == '111':
            jobData[5] = 100
            jobData[4] = 100
            jobData[3] = 100
        elif jType == '1000':
            jobData[2] = 100
        elif jType == '1001':
            jobData[5] = 100
            jobData[2] = 100
        elif jType == '1010':
            jobData[4] = 100
            jobData[2] = 100
        elif jType == '1011':
            jobData[5] = 100
            jobData[4] = 100
            jobData[2] = 100
        elif jType == '1100':
            jobData[3] = 100
            jobData[2] = 100
        elif jType == '1101':
            jobData[5] = 100
            jobData[3] = 100
            jobData[2] = 100
        elif jType == '1110':
            jobData[4] = 100
            jobData[3] = 100
            jobData[2] = 100
        elif jType == '1111':
            jobData[5] = 100
            jobData[4] = 100
            jobData[3] = 100
            jobData[2] = 100
        for r in requests:
            jobData.append(100)
        print(jobData)
        for e in employees:
            num = 0
            for i in range(len(totalData)):
                if totalData.loc[i]['id'] == e.id:
                    employeeData = totalData.loc[i].values.tolist()
                    del employeeData[0]
                    print(employeeData)
                    for j in range(len(employeeData)):
                        distance = jobData[j] - employeeData[j]
                        distance2 = math.pow(distance, 2)
                        num += weight[j] * distance2
                    num = math.sqrt(num)
                    num = (1 / num) * 100
                    try:
                        score = MatchingScore.objects.filter(employee=e).get(job=job)
                        score.score = num
                        score.save()
                    except MatchingScore.DoesNotExist:
                        score = MatchingScore.objects.create(employee=e, job=job, score=num)

def reSkillTest(request, id, jid):
    employee = Employee.objects.get(id=id)
    job = Job.objects.get(id=jid)
    SkillPaper.objects.filter(employee=employee).filter(job=job).delete()
    SkillGrade.objects.filter(employee=employee).filter(job=job).delete()
    SkillScore.objects.filter(grade__employee=employee).filter(grade__job=job).delete()
    try:
        paper = SkillPaper.objects.get(employee=employee)
    except SkillPaper.DoesNotExist:
        paper = createSkillPaper(request, id, jid)
    newPaper = paper
    return render(request, 'employee/skill_test.html', locals())

def enterpriseIndexFilter(enterprise, employees):
    educations = ['---']
    englishs = ['---']
    personalityTypes = ['---']
    for e in employees:
        education = e.get_education_display()
        english = e.get_english_display()
        Ptype = e.personalitygrade.get_type_display()
        if education not in educations:
            educations.append(education)
        if english not in englishs:
            englishs.append(english)
        if Ptype not in personalityTypes:
            personalityTypes.append(Ptype)
    return educations, englishs, personalityTypes

def enterpriseIndex(request, id):
    enterprise = Enterprise.objects.get(id=id)
    employees = Employee.objects.filter(personalitygrade__isnull=False)
    educations, englishs, personalityTypes = enterpriseIndexFilter(enterprise, employees)
    return render(request, 'enterprise/enterprise_index.html', locals())

def orderbyEducation(request, id, education):
    print(1)
    enterprise = Enterprise.objects.get(id=id)
    employees = Employee.objects.filter(personalitygrade__isnull=False)
    a = []
    for employee in employees:
        if employee.get_education_display() == education:
            a.append(employee)
    employees = a
    educations, englishs, personalityTypes = enterpriseIndexFilter(enterprise, employees)
    return render(request, 'enterprise/enterprise_index.html', locals())

def orderbyEnglish(request, id, english):
    enterprise = Enterprise.objects.get(id=id)
    employees = Employee.objects.filter(personalitygrade__isnull=False)
    a = []
    for employee in employees:
        if employee.get_english_display() == english:
            a.append(employee)
    employees = a
    educations, englishs, personalityTypes = enterpriseIndexFilter(enterprise, employees)
    return render(request, 'enterprise/lower_index.html', locals())

def orderbyPersonalityType(request, id, personalityType):
    enterprise = Enterprise.objects.get(id=id)
    employees = Employee.objects.filter(personalitygrade__isnull=False)
    a = []
    for employee in employees:
        if employee.personalitygrade.get_type_display() == personalityType:
            a.append(employee)
    employees = a
    educations, englishs, personalityTypes = enterpriseIndexFilter(enterprise, employees)
    return render(request, 'enterprise/lower_index.html', locals())

def enterpriseUpdate(request, id):
    enterprise = Enterprise.objects.get(id=id)
    enterpriseForm = EnterpriseForm()
    enterpriseForm.fields['name'].initial = enterprise.name
    enterpriseForm.fields['account'].initial = enterprise.account
    enterpriseForm.fields['password'].initial = enterprise.password
    enterpriseForm.fields['email'].initial = enterprise.email
    enterpriseForm.fields['phone'].initial = enterprise.phone
    enterpriseForm.fields['info'].initial = enterprise.info
    return render(request, 'enterprise/enterprise_update.html', locals())

def enterpriseUpdateHandler(request, id):
    if request.method == 'POST':
        form = EnterpriseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            info = form.cleaned_data['info']
            enterprise = Enterprise.objects.get(id=id)
            enterprise.name = name
            enterprise.password = password
            enterprise.email = email
            enterprise.phone = phone
            enterprise.info = info
            enterprise.save()
    return redirect(reverse('enterpriseIndex', args=(id,)))

def enterpriseJobList(request, id):
    enterprise = Enterprise.objects.get(id=id)
    jobs = Job.objects.filter(enterprise=enterprise)
    return render(request, 'enterprise/enterprise_job_list.html', locals())

def employeeJobDetail(request, id, jid):
    employee = Employee.objects.get(id=id)
    job = Job.objects.get(id=jid)
    requests = SkillRequest.objects.filter(job=job)
    return render(request, 'employee/job_detail.html', locals())

def enterpriseJobDetail(request, id, jid):
    enterprise = Enterprise.objects.get(id=id)
    job = Job.objects.get(id=jid)
    requests = SkillRequest.objects.filter(job=job)
    return render(request, 'enterprise/job_detail.html', locals())

def employeeDetail(request, id, eid):
    enterprise = Enterprise.objects.get(id=id)
    employee = Employee.objects.get(id=eid)
    return render(request, 'enterprise/employee_detail.html', locals())

def jobUpdate(request, id, jid):
    enterprise = Enterprise.objects.get(id=id)
    job = Job.objects.get(id=jid)
    jobForm = JobForm()
    jobForm.fields['name'].initial = job.name
    jobForm.fields['enterprise'].initial = job.enterprise
    jobForm.fields['salary'].initial = job.salary
    jobForm.fields['city'].initial = job.city
    jobForm.fields['educationWeight'].initial = job.educationWeight
    jobForm.fields['englishWeight'].initial = job.englishWeight
    jobForm.fields['personalityType'].initial = job.personalityrequest.type
    jobForm.fields['EIweight'].initial = job.personalityrequest.EIweight
    jobForm.fields['SNweight'].initial = job.personalityrequest.SNweight
    jobForm.fields['TFweight'].initial = job.personalityrequest.TFweight
    jobForm.fields['JPweight'].initial = job.personalityrequest.JPweight
    jobForm.fields['questionSource'].initial = job.questionSource
    requests = SkillRequest.objects.filter(job=job)
    formsetcls = modelformset_factory(model=SkillRequest, form=RequestForm, fields=['aspect', 'level', 'weight'], extra=0)
    formset = formsetcls(queryset=requests)
    return render(request, 'enterprise/job_update.html', locals())

def jobUpdateHandler(request, id, jid):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            salary = form.cleaned_data['salary']
            city = form.cleaned_data['city']
            educationWeight = form.cleaned_data['educationWeight']
            englishWeight = form.cleaned_data['englishWeight']
            personalityType = form.cleaned_data['personalityType']
            EIweight = form.cleaned_data['EIweight']
            SNweight = form.cleaned_data['SNweight']
            TFweight = form.cleaned_data['TFweight']
            JPweight = form.cleaned_data['JPweight']
            questionSource = form.cleaned_data['questionSource']
            job = Job.objects.get(id=jid)
            job.name = name
            job.salary = salary
            job.city = city
            job.educationWeight = educationWeight
            job.englishWeight = englishWeight
            job.personalityrequest.type = personalityType
            job.personalityrequest.EIweight = EIweight
            job.personalityrequest.SNweight = SNweight
            job.personalityrequest.TFweight = TFweight
            job.personalityrequest.JPweight = JPweight
            job.questionSource = questionSource
            job.save()
            job.personalityrequest.save()
            requests = SkillRequest.objects.filter(job=job)
            formsetcls = modelformset_factory(model=SkillRequest, form=RequestForm,
                                              fields=['aspect', 'level', 'weight'], extra=0)
            formset = formsetcls(request.POST, queryset=requests)
            if formset.is_valid():
                formset.save()
    return redirect(reverse('enterpriseJobList', args=(id,)))

def createRequest(request, id, jid):
    enterprise = Enterprise.objects.get(id=id)
    job = Job.objects.get(id=jid)
    requests = SkillRequest.objects.filter(job=job)
    if len(requests) < 3:
        newrequest = SkillRequest()
        newrequest.job = job
        newrequest.save()
    return redirect(reverse('jobUpdate', args=(id,jid)))

def delRequest(request, id, jid,  n):
    enterprise = Enterprise.objects.get(id=id)
    job = Job.objects.get(id=jid)
    requests = SkillRequest.objects.filter(job=job).values_list('id', flat=True)
    requests = list(requests)
    if len(requests) > 1:
        delID = requests[n-1]
        SkillRequest.objects.get(id=delID).delete()
    return redirect(reverse('jobUpdate', args=(id,jid)))

def jobCreate(request, id):
    enterprise = Enterprise.objects.get(id=id)
    job = Job.objects.create(enterprise=enterprise)
    job.save()
    personalityRequest = PersonalityRequest.objects.create(job=job)
    personalityRequest.save()
    skillRequest = SkillRequest.objects.create(job=job)
    skillRequest.save()
    jobForm = JobForm()
    jobForm.fields['enterprise'].initial = job.enterprise
    jobForm.fields['educationWeight'].initial = 1
    jobForm.fields['englishWeight'].initial = 1
    jobForm.fields['EIweight'].initial = 1
    jobForm.fields['SNweight'].initial = 1
    jobForm.fields['TFweight'].initial = 1
    jobForm.fields['JPweight'].initial = 1
    requests = SkillRequest.objects.filter(job=job)
    formsetcls = modelformset_factory(model=SkillRequest, form=RequestForm, fields=['aspect', 'level', 'weight'],
                                      extra=0)
    formset = formsetcls(queryset=requests)
    return render(request, 'enterprise/job_update.html', locals())

def delJob(request, id, n):
    enterprise = Enterprise.objects.get(id=id)
    jobs = Job.objects.filter(enterprise=enterprise).values_list('id', flat=True)
    jobs = list(jobs)
    delID = jobs[n-1]
    Job.objects.get(id=delID).delete()
    return redirect(reverse('enterpriseJobList', args=(id,)))

def questionList(request, id):
    enterprise = Enterprise.objects.get(id=id)
    questions = SkillQuestion.objects.filter(enterpriseID=id)
    form = FileForm()
    return render(request, 'enterprise/question_list.html', locals())

def questionDetail(request, id, qid):
    enterprise = Enterprise.objects.get(id=id)
    question = SkillQuestion.objects.get(id=qid)
    return render(request, 'enterprise/question_detail.html', locals())

def questionUpdate(request, id, qid):
    enterprise = Enterprise.objects.get(id=id)
    question = SkillQuestion.objects.get(id=qid)
    questionForm = QuestionForm()
    questionForm.fields['title'].initial = question.title
    questionForm.fields['choiceA'].initial = question.choiceA
    questionForm.fields['choiceB'].initial = question.choiceB
    questionForm.fields['choiceC'].initial = question.choiceC
    questionForm.fields['choiceD'].initial = question.choiceD
    questionForm.fields['aspect'].initial = question.aspect
    questionForm.fields['level'].initial = question.level
    questionForm.fields['answer'].initial = question.answer
    return render(request, 'enterprise/question_update.html', locals())

def questionUpdateHandler(request, id, qid):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            choiceA = form.cleaned_data['choiceB']
            choiceB = form.cleaned_data['choiceB']
            choiceC = form.cleaned_data['choiceC']
            choiceD = form.cleaned_data['choiceD']
            aspect = form.cleaned_data['aspect']
            level = form.cleaned_data['level']
            answer = form.cleaned_data['answer']
            question = SkillQuestion.objects.get(id=qid)
            question.title = title
            question.choiceA = choiceA
            question.choiceB = choiceB
            question.choiceC = choiceC
            question.choiceD = choiceD
            question.aspect = aspect
            question.level = level
            question.answer = answer
            question.save()
    return redirect(reverse('questionList', args=(id,)))

def questionCreate(request, id):
    enterprise = Enterprise.objects.get(id=id)
    question = SkillQuestion.objects.create(enterpriseID=id)
    question.save()
    questionForm = QuestionForm()
    return render(request, 'enterprise/question_update.html', locals())

def delQuestion(request, id, n):
    enterprise = Enterprise.objects.get(id=id)
    questions = SkillQuestion.objects.filter(enterpriseID=id).values_list('id', flat=True)
    questions = list(questions)
    delID = questions[n-1]
    SkillQuestion.objects.get(id=delID).delete()
    return redirect(reverse('questionList', args=(id,)))

def uploadFile(request, id):
    enterprise = Enterprise.objects.get(id=id)
    questions = SkillQuestion.objects.filter(enterpriseID=id)
    if request.method == 'POST':
        print(1)
        form = FileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            print(2)
            file = request.FILES['file']
            data = pd.read_excel(file)
            existQuestions = []
            for i in range(len(data)):
                print(3)
                title = data.loc[i]['title']
                try:
                    question = SkillQuestion.objects.filter(enterpriseID=id).get(title=title)
                    existQuestions.append(title)
                except SkillQuestion.DoesNotExist:
                    print(4)
                    choiceA = data.loc[i]['choiceA']
                    choiceB = data.loc[i]['choiceB']
                    choiceC = data.loc[i]['choiceC']
                    choiceD = data.loc[i]['choiceD']
                    aspect = data.loc[i]['aspect']
                    level = data.loc[i]['level']
                    answer = data.loc[i]['answer']
                    score = data.loc[i]['score']
                    SkillQuestion.objects.create(title=title, choiceA=choiceA, choiceB=choiceB, choiceC=choiceC,
                                                 choiceD=choiceD,
                                                 aspect=aspect, level=level, answer=answer, score=score,
                                                 enterpriseID=id)
    form = FileForm()
    return render(request, 'enterprise/question_list.html', locals())

def scaler(data):
    for i in data.columns:
        df = data[i].values.reshape(-1, 1)
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0.01, 0.99))
        x_minmax = min_max_scaler.fit_transform(df)
        np.set_printoptions(threshold=np.inf)
        data[i] = x_minmax
    return data

def get_data(job):
    employees = Employee.objects.filter(skillgrade__job=job, skillgrade__grade__gte=60)
    requests = SkillRequest.objects.filter(job=job)
    employeesFrame = read_frame(qs=employees, fieldnames=['id', 'education', 'english',
                                                          'personalitygrade__gradeEI', 'personalitygrade__gradeSN',
                                                          'personalitygrade__gradeTF', 'personalitygrade__gradeJP'])
    skillGradesFrame = read_frame(qs=employees,
                                  fieldnames=['id', 'skillgrade__skillscore__aspect', 'skillgrade__skillscore__score'])
    data = pd.DataFrame(employeesFrame)
    for r in requests:
        aspect = r.get_aspect_display()
        data[aspect] = ''
    for i in range(len(data)):
        if data.loc[i]['education'] == '专科':
            data.at[i, 'education'] = 1
        elif data.loc[i]['education'] == '本科':
            data.at[i, 'education'] = 2
        elif data.loc[i]['education'] == '211':
            data.at[i, 'education'] = 3
        elif data.loc[i]['education'] == '985':
            data.at[i, 'education'] = 4
        if data.loc[i]['english'] == '四级以下':
            data.at[i, 'english'] = 1
        elif data.loc[i]['english'] == '四级':
            data.at[i, 'english'] = 2
        elif data.loc[i]['english'] == '六级':
            data.at[i, 'english'] = 3
        elif data.loc[i]['english'] == '六级以上':
            data.at[i, 'english'] = 4
        for s in range(len(skillGradesFrame)):
            if data.loc[i]['id'] == skillGradesFrame.loc[s]['id']:
                for r in requests:
                    aspect = r.get_aspect_display()
                    if skillGradesFrame.loc[s]['skillgrade__skillscore__aspect'] == aspect:
                        score = skillGradesFrame.loc[s]['skillgrade__skillscore__score']
                        score = int(score)
                        data.at[i, aspect] = score
    return data

def entropy(totalData):
    data = totalData.drop(['id'], axis=1)
    print(data)
    data = scaler(data)
    print(data)
    rnum = data.index.size
    cnum = data.columns.size
    k = 1.0 / math.log(rnum)
    inf = [[None] * cnum for i in range(rnum)]
    x = np.array(data)
    inf = np.array(inf)
    for i in range(rnum):
        for j in range(cnum):
            p = x[i][j] / x.sum(axis=0)[j]
            infij = math.log(p) * p * (-k)
            inf[i][j] = infij
    inf = pd.DataFrame(inf)
    d = 1 - inf.sum(axis=0)
    w = [[None] * 1 for i in range(cnum)]
    for i in range(cnum):
        wi = d[i] / sum(d)
        w[i] = wi
    w = pd.DataFrame(w)
    w.columns = ['weight']
    w = w['weight'].values.tolist()
    print(w)
    return w

def jobRecommendationList(request, id):
    enterprise = Enterprise.objects.get(id=id)
    jobs = Job.objects.filter(enterprise=enterprise).filter(skillgrade__employee__isnull=False).distinct()
    num = []
    goodNum = []
    for job in jobs:
        employees = Employee.objects.filter(skillgrade__job=job)
        goodEmployees = Employee.objects.filter(skillgrade__job=job, skillgrade__grade__gte=60)
        num.append(len(employees))
        goodNum.append(len(goodEmployees))
    jobs = zip(jobs, num, goodNum)
    return render(request, 'enterprise/job_recommendation_list.html', locals())

def jobRecommendationDetail(request, id, jid):
    enterprise = Enterprise.objects.get(id=id)
    job = Job.objects.get(id=jid)
    employees = Employee.objects.filter(skillgrade__job=job, skillgrade__grade__gte=60)
    scores = MatchingScore.objects.filter(job=job).filter(employee__in=employees).order_by('-score')
    employees = []
    grades = []
    for score in scores:
        employee = score.employee
        grade = score.employee.skillgrade_set.get(job=job)
        employees.append(employee)
        grades.append(grade)
    employees = zip(employees, grades, scores)
    return render(request, 'enterprise/job_recommendation_detail.html', locals())
    #     for e in employees:
    #         num = 0
    #         for i in range(len(totalData)):
    #             if totalData.loc[i]['id'] == e.id:
    #                 employeeData = totalData.loc[i].values.tolist()
    #                 del employeeData[0]
    #                 print(employeeData)
    #                 for j in range(len(employeeData)):
    #                     distance = jobData[j] - employeeData[j]
    #                     distance2 = math.pow(distance, 2)
    #                     num += weight[j] * distance2
    #                 num = math.sqrt(num)
    #                 num = (1 / num) * 100
    #                 try:
    #                     score = MatchingScore.objects.filter(employee=e).get(job=job)
    #                     score.score = num
    #                     score.save()
    #                 except MatchingScore.DoesNotExist:
    #                     score = MatchingScore.objects.create(employee=e, job=job, score=num)
    #     scores = MatchingScore.objects.filter(job=job).order_by('-score')
    #     em = []
    #     sg = []
    #     sc = []
    #     for s in scores:
    #         em.append(s.employee)
    #         sg.append(s.employee.skillgrade_set.get(job=job))
    #         sc.append(s.score)
    #     employees = zip(em, sg, sc)
    # return  render(request, 'enterprise/job_recommendation_detail.html', locals())

def employeeRecommendationList(request, id):
    employee = Employee.objects.get(id=id)
    scores = MatchingScore.objects.filter(employee=employee).order_by('-score')
    jobs = []
    for s in scores:
        job = s.job
        jobs.append(job)
    scores = zip(jobs, scores)
    return render(request, 'employee/employee_recommendation_list.html', locals())

def informList(request, id):
    enterprise = Enterprise.objects.get(id=id)
    # MessageInform.objects.filter(time__lt=datetime.now()).delete()
    informs = MessageInform.objects.filter(job__enterprise=enterprise)
    applications = MessageApplication.objects.filter(job__enterprise=enterprise)
    return render(request, 'enterprise/inform_list.html', locals())

def informUpdate(request, id, iid):
    enterprise = Enterprise.objects.get(id=id)
    inform = MessageInform.objects.get(id=iid)
    informForm = MessageForm()
    informForm.fields['employee'].initial = inform.employee
    informForm.fields['job'].initial = inform.job
    informForm.fields['time'].initial = inform.time
    informForm.fields['mode'].initial = inform.mode
    return render(request, 'enterprise/inform_update.html', locals())

def informUpdateHandler(request, id, iid):
    enterprise = Enterprise.objects.get(id=id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            time = form.cleaned_data['time']
            mode = form.cleaned_data['mode']
            inform = MessageInform.objects.get(id=iid)
            inform.time = time
            inform.mode = mode
            inform.save()
    return redirect(reverse('informList', args=(id,)))

def informCreate(request, id, jid, eid):
    enterprise = Enterprise.objects.get(id=id)
    job = Job.objects.get(id=jid)
    employee = Employee.objects.get(id=eid)
    inform = MessageInform.objects.create(employee=employee, job=job)
    informForm = MessageForm()
    return render(request, 'enterprise/inform_update.html', locals())

def employeeInformList(request, id):
    employee = Employee.objects.get(id=id)
    MessageInform.objects.filter(time__lt=datetime.now()).delete()
    informs = MessageInform.objects.filter(employee=employee).filter(time__gte=datetime.now())
    applications = MessageApplication.objects.filter(employee=employee)
    return render(request, 'employee/inform_list.html', locals())

def applicationCreate(request, id, jid):
    employee = Employee.objects.get(id=id)
    job = Job.objects.get(id=jid)
    try:
        application = MessageApplication.objects.filter(employee=employee).get(job=job)
    except MessageApplication.DoesNotExist:
        application = MessageApplication.objects.create(employee=employee, job=job)
    return render(request, 'employee/inform_list.html', locals())

def delApplication(request, id, n):
    enterprise = Enterprise.objects.get(id=id)
    applications = MessageApplication.objects.filter(job__enterprise=enterprise).values_list('id', flat=True)
    applications = list(applications)
    delID = applications[n-1]
    MessageApplication.objects.get(id=delID).delete()
    return redirect(reverse('informList', args=(id,)))

def applicationAccept(request, id, jid, eid):
    enterprise = Enterprise.objects.get(id=id)
    job = Job.objects.get(id=jid)
    employee = Employee.objects.get(id=eid)
    MessageApplication.objects.filter(employee=employee).get(job=job).delete()
    inform = MessageInform.objects.create(employee=employee, job=job)
    informForm = MessageForm()
    return render(request, 'enterprise/inform_update.html', locals())

def informDetail(request, id, iid):
    enterprise = Enterprise.objects.get(id=id)
    inform = MessageInform.objects.get(id=iid)
    return render(request, 'enterprise/inform_detail.html', locals())

def employeeInformDetail(request, id, iid):
    employee = Employee.objects.get(id=id)
    inform = MessageInform.objects.get(id=iid)
    return render(request, 'employee/inform_detail.html', locals())