from django.shortcuts import render, HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from datetime import datetime
import datetime as dt
from django.core.files.storage import default_storage
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import login
from .models import Register

# Create your views here.


def index(request):
    return render(request, "index.html")


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


def userLogin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]

            user = authenticate(username=email, password=password)

            if user is not None:
                login(request, user)
                request.session["uid"] = user.id
                messages.success(request, "Login Success")
                return redirect("/main_index")
            else:
                messages.error(request, "Invalid Username/Password")
        else:
            messages.error(request, "Login Failed")
    else:
        form = LoginForm()

    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("c_password")
        image = request.FILES.get("file")

        if not email or not name or not password or not confirm_password:
            messages.error(request, "All fields are required")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif Login.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
        else:
            # Create a new User object (for authentication) and a User Profile
            user = Login.objects.create_user(
                username=email, password=password, email=email
            )
            user_profile = Register(name=name, email=email, loginid=user, image=image)
            user_profile.save()
            messages.success(request, "Your account has been created")
            return redirect("/login")

    return render(request, "register.html")


def main_index(request):
    view = Questions.objects.all()
    uid = request.session["uid"]
    Uid = Register.objects.get(loginid=uid)
    
    if request.method == "POST":
        questions = request.POST.get("questions")

        insert = Questions.objects.create(question=questions, uid=Uid)
        insert.save()

    return render(request, "Main/index.html", {"view": view})


def delete_question(request):
    uid = request.session["uid"]
    try:
        get_qid = request.GET.get("qid")
        print(get_qid)
        question = Questions.objects.get(id=get_qid, uid=uid)
        question.delete()

        return redirect("/main_index")
    except Questions.DoesNotExist:
        return messages.success("Question not found.")


def answers(request):
    uid = request.session["uid"]
    Uid = Register.objects.get(loginid=uid)
    qid = request.GET.get("qid")
    # print(qid)
    question_id = Questions.objects.get(id=qid)
    answers = Answers.objects.filter(qid=qid)
    # new code
    count = Answers.objects.filter(qid=qid).count()
    # print(single.question)
    regid = Register.objects.get(loginid=uid)
    if Likes.objects.filter(user_id=regid.id).exists():
        print("Yes, the user has likes")
    else:
        print("No, the user does not have likes")

    liked_answer_ids = Likes.objects.filter(user_id=regid).values_list(
        "answer_id", flat=True
    )

    if request.method == "POST":
        answer = request.POST.get("answer")

        insert = Answers.objects.create(answers=answer, uid=Uid, qid=question_id)
        insert.save()

        return redirect("/answers?qid=" + str(qid))

    return render(
        request,
        "Main/answers.html",
        {"view": question_id, "answers": answers, "liked_answer_ids": liked_answer_ids,"count":count},
    )


def addLike(request):
    uid = request.session["uid"]
    uuid = Register.objects.get(loginid=uid)
    qid = request.GET["qid"]
    qqid = Questions.objects.get(id=qid)
    aid = request.GET["aid"]
    aaid = Answers.objects.get(id=aid)

    # print("aid", aid, "qid", qid, "uid", uid)
    if not Likes.objects.filter(answer_id=aid, user_id=uuid).exists():
        like = Likes(question_id=qqid, answer_id=aaid, user_id=uuid)
        like.save()
        answer = Answers.objects.get(id=aid, qid=qid)
        answer.like += 1
        answer.save()
        return redirect("/answers?qid=" + str(qid))
    else:
        # print("hiiiiiiiiiiiiiiiiii")
        messages.error(request, "Already Liked")

    return redirect("/answers?qid=" + str(qid))


def removeLike(request):
    uid = request.session["uid"]
    aid = request.GET["aid"]
    qid = request.GET["qid"]
    regid = Register.objects.get(loginid=uid)

    dislike = Likes.objects.filter(answer_id=aid, user_id=regid, question_id=qid).delete()
    likeUpdate = Answers.objects.get(id=aid,qid=qid)
    likeUpdate.like-=1
    likeUpdate.save()
    return redirect("/answers?qid=" + str(qid))
