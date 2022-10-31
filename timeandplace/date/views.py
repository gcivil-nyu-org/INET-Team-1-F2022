from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def datePage(request):
    # users = Profile.objects.all()
    # user = req.user
    # unreadMessages = Message.objects.filter(
    #     receiver=user).filter(status=False).count()

    # myFilter = UserFilter(req.GET, queryset=users)
    # users = myFilter.qs

    # context = {
    #     'users': users,
    #     'userIn': user,
    #     'filter': myFilter,
    #     'unreadmsgs': unreadMessages
    # }
    return render(request=request, template_name="date-page.html")