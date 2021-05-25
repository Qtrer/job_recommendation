from django.contrib import admin
from assessment.models import *

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'account', 'password', 'info')
    search_fields = ['name', 'account']
@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'account', 'password', 'info')
    search_fields = ['name', 'account']
# class JobDetailsInline(admin.StackedInline):
#     extra = 0
#     model = SkillRequest
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'salary')
    # inlines = JobDetailsInline
@admin.register(PersonalityQuestion)
class PersonalityQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'choiceA', 'choiceB', 'choiceC', 'choiceD','aspect', 'scoreA', 'scoreB', 'scoreC', 'scoreD')
@admin.register(SkillQuestion)
class SkillQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'choiceA', 'choiceB', 'choiceC', 'choiceD','aspect', 'level', 'answer', 'score')
admin.site.register(PersonalityRequest)
admin.site.register(SkillRequest)