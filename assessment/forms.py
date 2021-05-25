from django import forms

class UserForm(forms.Form):
    account = forms.CharField(label="account", max_length=40)
    password = forms.CharField(label="password", max_length=40, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    account = forms.CharField(label="account", max_length=40)
    password = forms.CharField(label="password", max_length=40, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="confirm_password", max_length=40, widget=forms.PasswordInput)
    email = forms.EmailField(label='email')
    phone = forms.CharField(label='phone', max_length=40)
    status = forms.ChoiceField(label='status',
                               choices=(
                                   ('1', 'employee'), ('2', 'enterprise')
                               ))

class EmployeeForm(forms.Form):
    name = forms.CharField(label='name', max_length=40)
    account = forms.CharField(label='account', max_length=40, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    password = forms.CharField(label='password', max_length=40)
    education = forms.ChoiceField(label='education',
                                  choices=(
                                      ('1', '专科'),('2', '本科'),('3', '211'),('4', '985'),
                                  ))
    english = forms.ChoiceField(label='english',
                                  choices=(
                                      ('1', '四级以下'),('2', '四级'),('3', '六级'),('4', '六级以上'),
                                  ))
    email = forms.EmailField(label='email')
    phone = forms.CharField(label='phone', max_length=40)
    info = forms.CharField(label='info', max_length=200)

class EnterpriseForm(forms.Form):
    name = forms.CharField(label='name', max_length=40)
    account = forms.CharField(label='account', max_length=40, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    password = forms.CharField(label='password', max_length=40)
    email = forms.EmailField(label='email')
    phone = forms.CharField(label='phone', max_length=40)
    info = forms.CharField(label='info', max_length=200)

class JobForm(forms.Form):
    name = forms.CharField(label='name', max_length=40)
    enterprise = forms.CharField(label='enterprise', max_length=40, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    salary = forms.IntegerField(label='salary')
    personalityType = forms.ChoiceField(label='personalityType',
                                        choices=(
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
                                        ))
    educationWeight = forms.IntegerField(label='educationWeight')
    englishWeight = forms.IntegerField(label='englishWeight')
    EIweight = forms.IntegerField(label='EIweight')
    SNweight = forms.IntegerField(label='SNweight')
    TFweight = forms.IntegerField(label='TFweight')
    JPweight = forms.IntegerField(label='JPweight')
    city = forms.ChoiceField(label='city',
                             choices=(
                                 ('1', 'Beijing'), ('2', 'Shanghai'), ('3', 'Guangzhou')
                             ))
    questionSource = forms.ChoiceField(label='questionSource',
                                     choices=(
                                         ('0', 'system'), ('1', 'enterprise')
                                     ))

class RequestForm(forms.ModelForm):
    aspect = forms.ChoiceField(label='aspect',
                               choices=(
                                   ('1', 'Java'), ('2', 'Python'), ('3', 'Mysql'), ('4', 'Web')
                               ))
    level = forms.ChoiceField(label='level',
                              choices=(
                                  ('1', 'easy'), ('2', 'normal'), ('3', 'difficult')
                              ))
    weight = forms.IntegerField(label='weight')

class QuestionForm(forms.Form):
    title = forms.CharField(label='title', max_length=200)
    choiceA = forms.CharField(label='A', max_length=40)
    choiceB = forms.CharField(label='B', max_length=40)
    choiceC = forms.CharField(label='C', max_length=40)
    choiceD = forms.CharField(label='D', max_length=40)
    level = forms.ChoiceField(label='level', choices=(
        ('1', '简单'),
        ('2', '一般'),
        ('3', '困难'),
    ))
    aspect = forms.ChoiceField(label='aspect', choices=(
        ('1', 'Java'),
        ('2', 'Python'),
        ('3', 'Mysql'),
        ('4', 'Web'),
    ))
    answer = forms.ChoiceField(label='answer', choices=(
        ('1', 'A'),
        ('2', 'B'),
        ('3', 'C'),
        ('4', 'D'),
    ))

class MessageForm(forms.Form):
    job = forms.CharField(label='job', max_length=40,
                                 widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    employee = forms.CharField(label='employee', max_length=40,
                                 widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    time = forms.DateTimeField(label='time')
    mode = forms.CharField(label='mode', max_length=40)

class FileForm(forms.Form):
    file = forms.FileField(label='file')