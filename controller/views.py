from questions.models import Question
from answers.models import Answer
from django.shortcuts import render, redirect
from users.models import Users
from quizes.models import Quiz
from django.contrib.auth import authenticate, login as li, logout as lo
from django.contrib.auth.models import User
from middlewares.auth import verify_login, verify_student, verify_teacher
from middlewares.helpers import build_test, evaluate_test,get_results
from middlewares.verify import clean_unsubmited_test
from results.models import Result


# HOME PAGE VIEW
def home(request):
    if not verify_login(request):
        return redirect('/register')

    current_user = Users.objects.get(user=request.user.id)
    quizes = Quiz.objects.all()
    context = {
        "pagetitle": "Home",
        "user": current_user,
        "quizes": quizes,
    }
    return render(request, 'home/home.html', context)


# REGISTRATION PAGE VIEW
def register(request):
    if verify_login(request):
        return redirect('/')
    
    if request.method == "POST":
        try:
            n = User.objects.create_user(username=request.POST['username'],password=request.POST['password'])
            n.save()
            new_user = Users(user=n,role='S')
            new_user.save()
            current_user = authenticate(username=request.POST['username'],password=request.POST['password'])
            li(request,current_user)
            return redirect('/')

        except:
            return redirect('/')

    return render(request, 'home/register.html', {"pagetitle": "Register"})


# LOGIN PAGE VIEW
def login(request):
    if verify_login(request):
        return redirect('/')

    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            li(request, user)
            return redirect("/")
    context = {
        "pagetitle": "Login"
    }
    return render(request, 'home/login.html', context)


# LOGOUT ROUTE
def logout(request):
    if not verify_login(request):
        return redirect('/register')

    lo(request)
    return redirect('/')


# CREATE QUIZE PAGE VIEW
def create_quiz(request):
    if request.method == "POST":
        current_user = Users.objects.get(user=request.user)
        new_quiz = Quiz(
            name=str(request.POST['quizname']), created_by=current_user)
        new_quiz.save()
        return redirect("/myquizes/edit/"+str(new_quiz.id))
    else:
        current_user = Users.objects.get(user=request.user.id)
        return render(request, 'create/create.html', {"pagetitle": "Create", "user": current_user})


# MY QUIZES PAGE VIEW
def myquizes(request):
    if not verify_teacher(request):
        return redirect('/')

    current_user = Users.objects.get(user=request.user.id)
    quizes = Quiz.objects.all().filter(created_by=current_user)
    context = {
        "pagetitle": "My Quizes",
        "quizes": quizes,
        "user": current_user
    }
    return render(request, "myquizes/myquizes.html", context)


# DELETE QUIZ ROUTE
def delete_quiz(request, id):
    if not verify_teacher(request):
        return redirect('/')

    quiz = Quiz.objects.all().filter(pk=id)[0]
    quiz.delete()
    return redirect("/myquizes")


# EDIT QUIZ PAGE VIEW
def edit_quiz(request, id):
    if not verify_teacher(request):
        return redirect('/')

    quiz = Quiz.objects.all().filter(pk=id)[0]
    current_user = Users.objects.get(user=request.user.id)
    current_quiz_questions = Question.objects.all().filter(quiz=quiz)
    context = {
        "pagetitle": "Edit Quiz",
        "quiz": quiz,
        "user": current_user,
        "questions": current_quiz_questions
    }
    return render(request, "myquizes/edit.html", context)


# ADD QUESTION ROUTE
def add_question(request, id):
    if not verify_teacher(request):
        return redirect('/')

    if request.method == "GET":
        # In get method url id is quiz id
        # ID of quiz to which the question will be added
        current_user = Users.objects.get(user=request.user)
        current_quiz = Quiz.objects.all().filter(pk=id)[0]
        context = {
            "pagetitle": "Add Question",
            "user": current_user,
            "quiz": current_quiz
        }
        return render(request, 'myquizes/addquestion.html', context)
    elif request.method == "POST":
        current_quiz = Quiz.objects.all().filter(pk=id)[0]

        new_question = Question(
            question=request.POST["questionname"], quiz=current_quiz)
        new_question.save()

        new_answer1 = Answer(
            answer=request.POST["option1"], is_correct=request.POST["answer1"][0], question=new_question)
        new_answer2 = Answer(
            answer=request.POST["option2"], is_correct=request.POST["answer2"][0], question=new_question)
        new_answer3 = Answer(
            answer=request.POST["option3"], is_correct=request.POST["answer3"][0], question=new_question)
        new_answer4 = Answer(
            answer=request.POST["option4"], is_correct=request.POST["answer4"][0], question=new_question)

        new_answer1.save()
        new_answer2.save()
        new_answer3.save()
        new_answer4.save()

        return redirect(f"/myquizes/edit/{id}")


# DELETE QUESTION ROUTE
def delete_question(request, id):
    if not verify_teacher(request):
        return redirect('/')

    question = Question.objects.all().filter(pk=id)[0]
    question.delete()
    return redirect("/myquizes")


# VIEW QUESTIONS PAGE
def view_questions(request, id):
    if not verify_teacher(request):
        return redirect('/')

    current_user = Users.objects.get(user=request.user.id)
    current_quiz = Quiz.objects.all().filter(pk=id)[0]
    questions = Question.objects.all().filter(quiz=current_quiz)
    context = {
        "pagetitle": current_quiz.name,
        "user": current_user,
        "questions": questions,
        "quiz": current_quiz
    }
    return render(request, 'home/viewquestions.html', context)

# VIEW TEST PAGE
def take_test(request, quiz_id):
    if not verify_login and verify_student:
        return redirect("/")

    clean_unsubmited_test(request)
    current_user = Users.objects.get(user=request.user)
    current_quiz = Quiz.objects.all().filter(pk=quiz_id)[0]

    new_result = Result(attendee=current_user,quiz=current_quiz,progress='O')
    new_result.save()

    
    quiz = build_test(quiz_id)  # Builds Dictionary Of question with options
    context = {
        "pagetitle": current_quiz.name,
        "user": current_user,
        "quiz": quiz.items(),
        "quiz_id": quiz_id,
    }
    return render(request, 'taketest/test.html', context)


# SUBMIT ANSWER AND RESULTS PAGE
def submit_test(request, quiz_id):
    if not verify_login and verify_student:
        return redirect("/")

    if request.method == "POST":
        print(request.POST)
        result, percentage,current_test_result = evaluate_test(request, quiz_id)
        context = {
            "pagetitle": "Result",
            "user": request.user,
            "quiz_id":quiz_id,
            "result":result.items(),
            "percentage":percentage,
            "time":current_test_result.time_taken,
        }
        return render(request, 'taketest/result.html', context)
    else:
        return redirect("/")

# View Result for the quiz
def view_result(request,quiz_id):
    current_user = Users.objects.get(user=request.user)
    current_quiz = Quiz.objects.all().filter(pk = quiz_id)[0]
    context = {
            "pagetitle": "Result",
            "user": current_user,
            "quiz_id":quiz_id,
            "results":get_results(quiz_id),
            "quiz":current_quiz
        }
    return render(request, 'myquizes/viewresult.html', context)