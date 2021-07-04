def filtering(quizes,results,user):
    out = []
    current_user_results = results.filter(attendee = user)
    for i in quizes:
        is_attended = False
        for j in current_user_results:
            if(i.id == j.quiz):
                is_attended = True
        if not is_attended:
            out.append(i)
    return out

