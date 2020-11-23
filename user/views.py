from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages

from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.owner import *
from .forms import SignUpForm, UserUpdateForm, ProfilePicForm
from blog.models import Blog

# Create your views here.
class SignUpView(View):
    template_name = 'registration/login.html'
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('blogs:all')
        else:
            ctx = {'form':form}
            return render(request, self.template_name, ctx)


    def get(self, request):
        form = SignUpForm()
        ctx = {'form':form}
        return render(request, self.template_name, ctx)


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'user/profile.html'
    success_url = reverse_lazy('user:profile')


    def get(self, request):
        user = self.request.user
        user_form = UserUpdateForm(instance=user)
        pic_form = ProfilePicForm(instance=user.person)

        your_blogs = Blog.objects.filter(owner=request.user)[:5]
        ctx = {'user_form': user_form, 'pic_form': pic_form, 'your_blogs':your_blogs}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        user = self.request.user
        user_form = UserUpdateForm(request.POST, instance=user)
        # print(user.person.profile_pic)
        pic_form = ProfilePicForm(request.POST, request.FILES, instance=user.person)
        
        if user_form.is_valid() and pic_form.is_valid():
            user_form.save()
            pic_form.save()
            messages.success(request, 'Data Updated successfully.')
            return redirect(self.success_url)
    
        your_blogs = Blog.objects.filter(owner=request.user)[:5]
        ctx = {'user_form': user_form, 'pic_form': pic_form, 'your_blogs':your_blogs}
        return render(request, self.template_name, ctx)
        
class UserBlogsView(LoginRequiredMixin, View):
    template_name = 'user/user_blogs.html'

    def get(self, request):
        user = request.user
        blogs = Blog.objects.filter(owner=user)
        your_blogs = blogs[:5]
        ctx = {'blog_list':blogs, 'your_blogs':your_blogs}
        return render(request, self.template_name, ctx)
    



from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def sendEmail(request):

	if request.method == 'POST':

		template = render_to_string('user/email_template.html', {
			'name':request.POST['name'],
			'email':request.POST['email'],
			'message':request.POST['message'],
			})

		email = EmailMessage(
			request.POST['subject'],
			template,
			settings.EMAIL_HOST_USER,
			['shiv71290@gmail.com']
			)

		email.fail_silently=False
		email.send()

	return render(request, 'user/email_sent.html')