from questions.models import Question
from answers.models import Answer
from quizes.models import Quiz
from results.models import Result
from users.models import Users
from django.contrib.auth.models import User

def build_test(quiz_id):
    current_quiz = Quiz.objects.all().filter(pk = quiz_id)[0]
    questions = Question.objects.all().filter(quiz=current_quiz)
    results = {}
    for question in questions:
        current_question_answers = list(Answer.objects.all().filter(question = question))
        results[question] = current_question_answers
    
    return results

def evaluate_test(request,quiz_id):
    current_quiz = Quiz.objects.all().filter(pk = quiz_id)[0]
    questions = Question.objects.all().filter(quiz=current_quiz)
    results = {}
    mark = 0
    total = len(questions)
    for question in questions:
        current_question_answers = list(Answer.objects.all().filter(question = question).filter(is_correct='T'))
        results[question] = [current_question_answers,Answer.objects.all().filter(pk = request.POST.get(str(question.id)))[0]]
        for answer in current_question_answers:
            if int(request.POST.get(str(question.id))) == answer.id:
                mark += 1
    
    percentage = round((mark/total)*100,2)

    current_user = Users.objects.get(user=request.user)

    current_test_result = Result.objects.all().filter(attendee = current_user).get(progress = 'O')
    current_test_result.progress = 'C'
    current_test_result.time_taken = request.POST["time"]
    current_test_result.percentage = percentage
    current_test_result.save()

    return results,percentage,current_test_result

def get_results(quiz_id):
    current_quiz = Quiz.objects.all().filter(pk = quiz_id)[0]
    results = Result.objects.all().filter(quiz = current_quiz).filter(progress = 'C').order_by("-id")
    out= []
    for result in results:
        temp = {}
        temp["percentage"] = result.percentage
        temp["time_taken"] = result.time_taken
        user = User.objects.all().get(id = result.attendee.user.id)
        temp["username"] = user.username
        temp.items()
        out.append(temp)

    print(out)
    return out