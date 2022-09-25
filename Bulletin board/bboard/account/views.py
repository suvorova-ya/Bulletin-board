from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView,View
from .forms import RegisterUserForm
from project.models import Author

class RegisterUserViews(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'account/profile.html'
    success_url = 'otp_code/'

    def form_valid(self, form):
        form.instance.is_active = False
        self.request.session['activation_state'] = ''
        return super(RegisterUserViews, self).form_valid(form)


@login_required
def profile(request):
    return render(request, 'project/profile.html')

class ActivationView(View):
    template_name = 'account/activation.html'

    def send_otp(request):
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            author = Author.objects.get(author=user)
            if author.otp[:6] == otp:
                if int(author.otp[-10:]):
                    user.is_active = True
                    user.save()
                    request.session['activation_state'] = 'success'
                else:
                    author.delete()
                    user.delete()
                    request.session['activation_state'] = 'reregister'
            else:
                request.session['activation_state'] = 'reenter_code'
        else:
            request.session['activation_state'] = 'reenter_email'
        return redirect('/otp_code/')

    def get(self, request):
        return render(request, 'account/activation.html')

