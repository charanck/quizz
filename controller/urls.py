from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home,register,login,logout,create_quiz,myquizes,delete_quiz,edit_quiz,add_question,delete_question,view_questions,take_test,submit_test,view_result

urlpatterns = [
    path('',home),
    path('register',register),
    path('login',login),
    path('logout',logout),

    path('create/quiz',create_quiz),

    path('myquizes',myquizes),
    path('myquizes/edit/<int:id>',edit_quiz),
    path('myquizes/delete/<int:id>',delete_quiz),
    path('myquizes/viewresult/<int:quiz_id>',view_result),

    path('addquestion/<int:id>',add_question),
    path('deletequestion/<int:id>',delete_question),
    path('viewquestions/<int:id>',view_questions),

    path('taketest/<int:quiz_id>',take_test),
    path('submittest/<int:quiz_id>',submit_test),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)