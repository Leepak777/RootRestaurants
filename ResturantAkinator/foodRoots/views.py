from django.shortcuts import render
from django import forms

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

import csv
from os import path
from typing import List

QUESTIONS = {
    "chinese": ["Would you like to try Congee?", "What about dimsum?"
                , "Are you feeling noodles?", "Feeling a little spicy?"],
    "japanese": [
            "Would you like to try raw cuisine?",
            "Are you feeling some ramen?"
        ]
}

VALUES = {
    "chinese": ["congee", "dimsum"
                , "noodles", "spicy", "seafood"],
    "japanese": [
        "sushi", "ramen", "tempura"
        ]
}


class CultureForm(forms.Form):
    CHOICES = [("chinese", "Chinese"),
               ("japanese", "Japaense"),
               ]

    answer = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'custom'}),
        choices=CHOICES,
        label="")

class YesOrNoForm(forms.Form):
    CHOICES = [("yes", "Yes"),
               ("no", "No"),
               ]
    answer = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'custom'}),
        choices=CHOICES,
        label="")

def index(request):
    return render(request, "foodRoots/index.html")

def start(request):
    if request.method == "GET":
        reset(request)

        if len(request.session["answers"]) == 0:
            form = CultureForm()

        return render(request, "foodRoots/start.html", {
        "current_question_num": request.session["current_question_num"]+1,
        "current_question": request.session["current_question"],
        "form": form
        })

    elif request.method == "POST":
        if len(request.session["answers"]) == 0:

            post_form = CultureForm(request.POST)
            form = CultureForm()
        else:
            post_form = YesOrNoForm(request.POST)
            form = YesOrNoForm()

        if not post_form.is_valid():
            return render(request, "foodRoots/start.html", {
                "question_num": request.session["current_question_num"]+1,
                "question": request.session["current_question"],
                "form": form
            })

        answer = post_form.cleaned_data["answer"]
        request.session["answers"].append(answer)
        request.session.modified = True

        form = YesOrNoForm()

        if len(request.session["answers"]) == len(QUESTIONS[request.session["answers"][0]])+1 or request.session["answers"][-1] == "yes":
            if request.session["answers"][-1] == "no":
                sub_value = 1
            else:
                sub_value = 2

            print(len(request.session["answers"]))
            print(sub_value)

            resturants = _get_list_of_resturants(VALUES[request.session["answers"][0]][len(request.session["answers"])-sub_value])

            return render(request, "foodRoots/resturants.html", {
                "resturants": resturants
            })

        request.session["current_question_num"] = len(request.session["answers"])
        request.session["current_question"] = QUESTIONS[request.session["answers"][0]][request.session["current_question_num"]-1]

        return render(request, "foodRoots/start.html", {
        "current_question_num": request.session["current_question_num"]+1,
        "current_question": request.session["current_question"],
        "form": form
        })

def reset(request):
    request.session["answers"] = []
    request.session["current_question_num"] = 0
    request.session["current_question"] = "What is your cultural background?"
    return HttpResponseRedirect(reverse("foodRoots:start"))

def _get_list_of_resturants(attr: str) -> List[str]:
    with open(path.abspath("./foodRoots/food_db/food.csv")) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        print(attr)
        resturants = []
        for row in csv_reader:
            if attr in row:
                resturants.append((row[0], row[-1]))

        return resturants
