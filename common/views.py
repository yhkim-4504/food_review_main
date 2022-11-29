from django.shortcuts import render
from .forms import UserForm, UserInfoForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_info_form = UserInfoForm(request.POST)
        
        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.save()
    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    context = {
        'user_form': user_form,
        'user_info_form': user_info_form
    }

    return render(request, 'common/signup.html', context)