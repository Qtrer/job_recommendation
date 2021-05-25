"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from assessment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('employee/<int:id>', views.employeeIndex, name='employeeIndex'),
    path('employee/<int:id>-<int:eid>', views.orderbyEnterprise, name='orderbyEnterprise'),
    path('employee/<int:id>-<str:city>', views.orderbyCity, name='orderbyCity'),
    path('enterprise/<int:id>', views.enterpriseIndex, name='enterpriseIndex'),
    path('enterprise/<int:id>-<str:education>', views.orderbyEducation, name='orderbyEducation'),
    path('enterprise/<int:id>//<str:english>', views.orderbyEnglish, name='orderbyEnglish'),
    path('enterprise/<int:id><personalityType>', views.orderbyPersonalityType, name='orderbyPersonalityType'),
    path('employee/<int:id>/employee_update', views.employeeUpdate, name='employeeUpdate'),
    path('employee/<int:id>/employee_update_handler', views.employeeUpdateHandler, name='employeeUpdateHandler'),
    path('enterprise/<int:id>/enterprise_update', views.enterpriseUpdate, name='enterpriseUpdate'),
    path('enterprise/<int:id>/enterprise_update_handler', views.enterpriseUpdateHandler, name='enterpriseUpdateHandler'),
    path('employee/<int:id>/personality_test', views.personalityTest, name='personalityTest'),
    path('employee/<int:id>/personality_test_re', views.rePersonalityTest, name='rePersonalityTest'),
    path('employee/<int:id>/personality_grade_cal', views.calPersonalityGrade, name='calPersonalityGrade'),
    path('employee/<int:id>/skill_test/<int:jid>', views.skillTest, name='skillTest'),
    path('employee/<int:id>/skill_grade_list', views.skillGradeList, name='skillGradeList'),
    path('employee/<int:id>/skill_test_re/<int:jid>', views.reSkillTest, name='reSkillTest'),
    path('employee/<int:id>/skill_grade_cal/<int:jid>', views.calSkillGrade, name='calSkillGrade'),
    path('enterprise/<int:id>/job_list', views.enterpriseJobList, name='enterpriseJobList'),
    path('employee/<int:id>/job/<int:jid>', views.employeeJobDetail, name='employeeJobDetail'),
    path('enterprise/<int:id>/job/<int:jid>', views.enterpriseJobDetail, name='enterpriseJobDetail'),
    path('enterprise/<int:id>/employee/<int:eid>', views.employeeDetail, name='employeeDetail'),
    path('enterprise/<int:id>/job_update/<int:jid>', views.jobUpdate, name='jobUpdate'),
    path('enterprise/<int:id>/job_create', views.jobCreate, name='jobCreate'),
    path('enterprise/<int:id>/job_update_handler/<int:jid>', views.jobUpdateHandler, name='jobUpdateHandler'),
    path('enterprise/<int:id>/create_request/<int:jid>', views.createRequest, name='createRequest'),
    path('enterprise/<int:id>/del_job/<int:n>', views.delJob, name='delJob'),
    path('enterprise/<int:id>/del_request/<int:jid>/<int:n>', views.delRequest, name='delRequest'),
    path('enterprise/<int:id>/question_list', views.questionList, name='questionList'),
    path('enterprise/<int:id>/question_upload', views.uploadFile, name='uploadFile'),
    path('enterprise/<int:id>/question/<int:qid>', views.questionDetail, name='questionDetail'),
    path('enterprise/<int:id>/question_update/<int:qid>', views.questionUpdate, name='questionUpdate'),
    path('enterprise/<int:id>/question_create', views.questionCreate, name='questionCreate'),
    path('enterprise/<int:id>/question_update_handler/<int:qid>', views.questionUpdateHandler, name='questionUpdateHandler'),
    path('enterprise/<int:id>/del_question/<int:n>', views.delQuestion, name='delQuestion'),
    path('enterprise/<int:id>/job_recommendation_list', views.jobRecommendationList, name='jobRecommendationList'),
    path('enterprise/<int:id>/job_recommendation_detail/<int:jid>', views.jobRecommendationDetail, name='jobRecommendationDetail'),
    path('employee/<int:id>/employee_recommendation_list', views.employeeRecommendationList, name='employeeRecommendationList'),
    path('enterprise/<int:id>/inform_list', views.informList, name='informList'),
    path('enterprise/<int:id>/inform/<int:iid>', views.informDetail, name='informDetail'),
    path('enterprise/<int:id>/inform_update/<int:iid>', views.informUpdate, name='informUpdate'),
    path('enterprise/<int:id>/inform_create/<int:jid>/<int:eid>', views.informCreate, name='informCreate'),
    path('enterprise/<int:id>/inform_update_handler/<int:iid>', views.informUpdateHandler, name='informUpdateHandler'),
    path('employee/<int:id>/inform_list', views.employeeInformList, name='employeeInformList'),
    path('employee/<int:id>/inform/<int:iid>', views.employeeInformDetail, name='employeeInformDetail'),
    path('employee/<int:id>/application_create<int:jid>', views.applicationCreate, name='applicationCreate'),
    path('enterprise/<int:id>/del_application/<int:n>', views.delApplication, name='delApplication'),
    path('enterprise/<int:id>/application_accept/<int:jid>/<int:eid>', views.applicationAccept, name='applicationAccept'),
]
