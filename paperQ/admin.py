from django.contrib import admin

# Register your models here.
from paperQ.models import *

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('index', 'group', 'correct_answer')
    list_filter = ('group',)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'question_group')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('q_index', 'group', 'person', 'ans_text')
    list_filter = ('person', 'question',)

    def q_index(self, obj):
        return obj.question.index
    
    def group(self, obj):
        return obj.question.group.name

    q_index.short_description = '問題番号'
    group.short_description = '問題群'



admin.site.register(QuestionGroup)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Answer, AnswerAdmin)
