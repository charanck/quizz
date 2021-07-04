from users.models import Users
from results.models import Result

def clean_unsubmited_test(request):
    current_user = Users.objects.get(user=request.user)
    possible_pending_tests = Result.objects.all().filter(attendee = current_user).filter(progress = 'O')
    for result in possible_pending_tests:
        result.delete()
    