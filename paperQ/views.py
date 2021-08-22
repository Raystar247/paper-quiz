# 次にやること
# adminでの名称変更
# 模範解答の表示
# 登録段階での名前の重複の検出

## 企画書に書くべき注意事項
## ブラウザバック等で前の問題に戻ることは禁止とする。また、書き換えた場合にはシステムが強制終了する仕様になっている
## 名前欄には半角英数字を用いること、全角文字を入力した際には正しく動作しない。
## また、問題セット欄にはこちらが指定する文字列(半角)を入力すること。
## 問題に進む前に、使用する名前をこちらにgoogle form等で送信すること。
## 必ず、問題を解く前に送信すること。解き始めた後にgoogle formを送信した場合得点を認めないことがある。
## googleformの送信は当該の名前を用いた解答を１度に限定するためのものである。

from io import TextIOWrapper
from .models import *
from django.shortcuts import render
from django.http import HttpResponseRedirect
import datetime
import csv
import re


# use in each function
def discern_string(str):
    p = re.compile('[a-zA-Z0-9_]+')
    return p.fullmatch(str)

# Create your views here.
def startpage(request):
    return render(request, 'UserMain.html')

def register_person(request):
    q_group = QuestionGroup.objects.get(name=request.POST['question_group'])
    if Question.objects.filter(group=q_group).count() <= 0:
        context = {
            'caption': 'Error: Empty Question Group',
            'message': '問題の存在しない問題群です'
        }
        return render(request, 'Message.html', context)
    name = request.POST['name']
    if not discern_string(name):
        context = {
            'caption': 'Error: Unusable Name',
            'message': '使用できない文字が含まれています'
        }
        return render(request, 'Message.html', context)
    if Person.objects.filter(name=name, question_group=q_group).exists():
        context = {
            'caption': 'Error: Duplicated Name',
            'message': '指定した名称は既に存在します'
        }
        return render(request, 'Message.html', context)
    person = Person(
        name = request.POST['name'],
        question_group = q_group,
        rest_time = q_group.answer_time,
    )
    person.save()
    return HttpResponseRedirect(f'/answerpage/{person.name}/{q_group.name}/1/')

def start_answer(request, person_name, groupname, index):
    try:
        question_group = QuestionGroup.objects.get(name=groupname)
        person = Person.objects.get(name=person_name, question_group=question_group)
        question = Question.objects.get(index=index, group=question_group)
    except:
        context = {
            'caption': 'Error: Not Found',
            'message': '問題データが見つかりません'
        }
        return render(request, 'Message.html', context)
    print(request.build_absolute_uri('/finishpage/'))
    person.rest_time = question_group.answer_time - (datetime.datetime.now(datetime.timezone.utc) - person.start_time)
    person.save()
    context = {
        'person':           person, 
        'question':         question, 
        'rest_seconds':     person.rest_time.seconds,
        'finishpage_uri':   request.build_absolute_uri('/finishpage/'),
    }
    print(person.rest_time)
    # 時間制限に達した場合、finishpageに誘導して終了する
    if person.rest_time.days < 0:
        return HttpResponseRedirect('/finishpage/')
    return render(request, 'Question.html', context)

def register_answer(request, person_name, groupname, index):
    try:
        question_group = QuestionGroup.objects.get(name=groupname)
        person = Person.objects.get(name=person_name, question_group=question_group)
        question = Question.objects.get(index=index, group=question_group)
    except:
        context = {
            'caption': 'Error: Not Found',
            'message': '問題データが見つかりません'
        }
        return render(request, 'Message.html', context)
    answer = Answer(
        person = person,
        question = question,
        ans_text = request.POST['answer']
    )
    #同じ人が２回目同じ問題に解答した場合、不正検知として強制終了
    if Answer.objects.filter(person=person, question=question).exists():
        context = {
            'caption': 'Detected Unauthorized Action',
            'message': '不正操作が検知されました'
        }
        return render(request, 'Message.html', context)
    answer.save()
    # 問題数上限に到達した場合、終了する
    num_question = Question.objects.filter(group=question_group).count()
    if index == num_question:
        context = {
            'caption': 'Congratulations!!!',
            'message': f'全{num_question}問の解答が終了しました'
        }
        return render(request, 'Message.html', context)
    index_next = index + 1
    return HttpResponseRedirect(f'/answerpage/{person.name}/{question_group.name}/{index_next}/')

def finishpage(request):
    context = {
        'caption': 'Time Up...',
        'message': '指定時間が経過しました'
    }
    return render(request, 'Message.html', context)

def answer_check(request, person_name, question_group):
    group = QuestionGroup.objects.get(name=question_group)
    person = Person.objects.get(name=person_name, question_group=group)
    context = {
        'person':       person,
        'group':        group,
        'answer_list':  Answer.objects.filter(person=person)
    }
    return render(request, 'AnswerCheck.html', context)

def show_upload(request):
    return render(request, 'Upload.html')

def upload(request):
    if 'csv' in request.FILES:
        formdata = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(formdata)
        groupname = request.POST['name']
        print(f'groupname: {groupname}')
        if not discern_string(groupname):
            context = {
            'caption': 'Error: Unusable Name',
            'message': '使用できない文字が含まれています'
            }
            return render(request, 'Message.html', context)
        if QuestionGroup.objects.filter(name=groupname).exists():
            context = {
                'caption': 'Error: Duplicated Name',
                'message': '指定した名称の問題群が既に存在します'
            }
            return render(request, 'Message.html', context)
        minutes = int(request.POST['minutes'])
        seconds = int(request.POST['seconds'])
        answer_time = datetime.timedelta(minutes=minutes, seconds=seconds)
        if answer_time.seconds <= 0:
            context = {
                'caption': 'Error: Incorrect time setting',
                'message': '指定した時間に不正があります'
            }
            return render(request, 'Message.html', context)
        question_group = QuestionGroup(
            name = groupname,
            answer_time = answer_time
        )
        question_group.save()
        for line in csv_file:
            question, be_created = Question.objects.get_or_create(q_text=line[1])
            question.index = line[0]
            question.group = question_group
            question.q_text = line[1]
            question.correct_answer = line[2]
            question.save()
        context = {
            'caption': 'Regiter Succeeded',
            'message': f'問題群{question_group.name}が登録されました'
        }
        return render(request, 'Message.html', context)
    else:
        context = {
            'caption': 'Error: can\'t find CSV file',
            'message': 'CSVファイルが見つかりませんでした'
        }
        return render(request, 'Message.html', context)