from django.shortcuts import render
from django import forms

from django.http import HttpResponseRedirect
from django.urls import reverse

questions = ["What is your cultural background?",
             "Placeholder question #1?",
             "Placeholder question #2?",
            ]

class AnswerForm(forms.Form):
    answer = forms.CharField(label="", widget=forms.TextInput(attrs={'id': 'answer_field'}))

def index(request):
    return render(request, "foodRoots/index.html")

def start(request):
    if "answers" not in request.session:
        request.session["answers"] = []

    if request.method == "POST":
        if len(request.session["answers"]) == len(questions):
            #TODO: do the actual algorithm that determines a list of resturants
            pass

        form = AnswerForm(request.POST)

        if not form.is_valid():
            return render(request, "foodRoots/start.html", {
                "question_num": current_question_num,
                "question": current_question,
                "form": AnswerForm()
            })

        answer = form.cleaned_data["answer"]
        request.session["answers"].append(answer)
        request.session.modified = True

    current_question_num = len(request.session["answers"])
    current_question = questions[current_question_num]
    print(current_question_num)
    print(current_question)

    return render(request, "foodRoots/start.html", {
        "current_question_num": current_question_num+1,
        "current_question": current_question,
        "form": AnswerForm()
    })

def reset(request):
    request.session["answers"] = []
    return HttpResponseRedirect(reverse("foodRoots:start"))