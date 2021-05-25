from django.db import models

# Create your models here.
from django.utils import timezone

SKILLLEVEL = (
        ('1', '简单'),
        ('2', '一般'),
        ('3', '困难'),
)
SKILLASPECT = (
        ('1', 'Java'),
        ('2', 'Python'),
        ('3', 'Mysql'),
        ('4', 'Web'),
)
PERSONALITYASPECT = (
        ('1', 'E-I'),
        ('2', 'S-N'),
        ('3', 'T-F'),
        ('4', 'J-P'),
)
PERSONALITYTYPE = (
        ('0', 'ESTJ大男人型'),
        ('1', 'ESTP挑战型'),
        ('10', 'ESFJ主人型'),
        ('11', 'ESFP表演型'),
        ('100', 'ENTJ将军型'),
        ('101', 'ENTP发明家型'),
        ('110', 'ENFJ教育家型'),
        ('111', 'ENFP记者型'),
        ('1000', 'ISTJ公务型'),
        ('1001', 'ISTP冒险家型'),
        ('1010', 'ISFJ照顾型'),
        ('1011', 'ISFP艺术家型'),
        ('1100', 'INTJ专家型'),
        ('1101', 'INTP学者型'),
        ('1110', 'INFJ作家型'),
        ('1111', 'INFP哲学家型'),
)
ANSWER = (
    ('1', 'A'),
    ('2', 'B'),
    ('3', 'C'),
    ('4', 'D'),
)
CITY = (
    ('1', 'Beijing'),
    ('2', 'Shanghai'),
    ('3', 'Guangzhou'),
)
EDUCATION = (
    ('1', '专科'),
    ('2', '本科'),
    ('3', '211'),
    ('4', '985'),
)
ENGLISH = (
    ('1', '四级以下'),
    ('2', '四级'),
    ('3', '六级'),
    ('4', '六级以上'),
)
SOURCE = (
    ('0', 'system'),
    ('1', 'enterprise'),
)
class Employee(models.Model):
    name = models.CharField('name', max_length=40)
    account = models.CharField('account', max_length=40, unique=True)
    password = models.CharField('password', max_length=40)
    education = models.CharField('education', max_length=40, choices=EDUCATION, default='1')
    english = models.CharField('english', max_length=40, choices=ENGLISH, default='1')
    email = models.EmailField('email')
    phone = models.CharField('phone', max_length=40)
    info = models.TextField()

    class Meta:
        db_table='Employee'
        verbose_name='employee'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

class Enterprise(models.Model):
    name = models.CharField(max_length=40)
    account = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=40)
    email = models.EmailField('email')
    phone = models.CharField('phone', max_length=40)
    info = models.TextField()

    class Meta:
        db_table='Enterprise'
        verbose_name='enterprise'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

class Job(models.Model):
    name = models.CharField(max_length=40)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    salary = models.IntegerField('salary', default=0)
    city = models.CharField('city', choices=CITY, max_length=40, default='1')
    educationWeight = models.IntegerField('educationWeight', default=1)
    englishWeight = models.IntegerField('englishWeight', default=1)
    questionSource = models.CharField('questionSource', max_length=1, choices=SOURCE, default='0')

    class Meta:
        db_table='Job'
        verbose_name='job'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

class PersonalityRequest(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    type = models.CharField('personality', choices=PERSONALITYTYPE, max_length=40, default='0')
    EIweight = models.IntegerField('EIweight', default=1)
    SNweight = models.IntegerField('SNweight', default=1)
    TFweight = models.IntegerField('TFweight', default=1)
    JPweight = models.IntegerField('JPweight', default=1)

    class Meta:
        db_table='PersonalityRequest'
        verbose_name='personalityRequest'
        verbose_name_plural=verbose_name

class SkillRequest(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    aspect = models.CharField('aspect', choices=SKILLASPECT, max_length=40, default='1')
    level = models.CharField('level', choices=SKILLLEVEL, max_length=40, default='1')
    weight = models.IntegerField('weight', default=1)

    class Meta:
        db_table='SkillRequest'
        verbose_name='skillRequest'
        verbose_name_plural=verbose_name

class PersonalityQuestion(models.Model):
    title = models.TextField('title')
    choiceA = models.CharField('A', max_length=40)
    choiceB = models.CharField('B', max_length=40)
    choiceC = models.CharField('C', max_length=40)
    choiceD = models.CharField('D', max_length=40)
    aspect = models.CharField('aspect', choices=PERSONALITYASPECT, max_length=40, default='1')
    scoreA = models.IntegerField('scoreA', default=1)
    scoreB = models.IntegerField('scoreB', default=2)
    scoreC = models.IntegerField('scoreC', default=3)
    scoreD = models.IntegerField('scoreD', default=4)

    class Meta:
        db_table='PersonalityQuestion'
        verbose_name='personalityQuestion'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title

class PersonalityPaper(models.Model):
    employeeName = models.CharField(max_length=40)
    pid = models.ManyToManyField(PersonalityQuestion)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)

    class Meta:
        db_table='PersonalityPaper'
        verbose_name='personalityPaper'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.employeeName

class PersonalityGrade(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    gradeEI = models.IntegerField(default=0)
    gradeSN = models.IntegerField(default=0)
    gradeTF = models.IntegerField(default=0)
    gradeJP = models.IntegerField(default=0)
    type = models.CharField('type', choices=PERSONALITYTYPE, max_length=40, default='1')

    class Meta:
        db_table='PersonalityGrade'
        verbose_name='personalityGrade'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '<%s:%s>'%(self.employee, self.type)

class SkillQuestion(models.Model):
    title = models.TextField('title')
    choiceA = models.CharField('A', max_length=40)
    choiceB = models.CharField('B', max_length=40)
    choiceC = models.CharField('C', max_length=40)
    choiceD = models.CharField('D', max_length=40)
    level = models.CharField('level', choices=SKILLLEVEL, max_length=40, default='1')
    aspect = models.CharField('aspect', choices=SKILLASPECT, max_length=40, default='1')
    answer = models.CharField('answer', choices=ANSWER, max_length=40)
    score = models.IntegerField('score', default=1)
    enterpriseID = models.IntegerField('enterpriseID', default=0)


    class Meta:
        db_table='SkillQuestion'
        verbose_name='skillQuestion'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '<%s,%s:%s>'%(self.aspect, self.level, self.title)

class SkillPaper(models.Model):
    pid = models.ManyToManyField(SkillQuestion)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    class Meta:
        db_table='SkillPaper'
        verbose_name='skillPaper'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.employee.name

class SkillGrade(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    paper = models.OneToOneField(SkillPaper, on_delete=models.CASCADE)
    grade = models.IntegerField(default=0)

    class Meta:
        db_table='SkillGrade'
        verbose_name='skillGrade'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '<%s,%s:%s>'%(self.job, self.employee, self.grade)

class SkillScore(models.Model):
    grade = models.ForeignKey(SkillGrade, on_delete=models.CASCADE)
    aspect = models.CharField('aspect', choices=SKILLASPECT, max_length=40, default='1')
    score = models.IntegerField('score', default=0)

    class Meta:
        db_table='SkillScore'
        verbose_name='skillScore'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '<%s:%s>'%(self.aspect, self.score)

class MatchingScore(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    score = models.FloatField('score', default=0)

class MessageInform(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    time = models.DateTimeField('time', default=timezone.now)
    mode = models.CharField('mode', max_length=40)

class MessageApplication(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)