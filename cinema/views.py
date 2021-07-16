import random
from smtplib import SMTPException

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from .forms import UserForm
from .models import Movie


class HomeView(generic.TemplateView):
    template_name = 'home.html'


class UserRegisterFormView(View):
    form_class_user = UserForm
    template_name = 'register.html'

    def get(self, request):
        form_user = self.form_class_user(None)
        return render(request, self.template_name, {'form_user': form_user})

    def post(self, request):
        form_user = self.form_class_user(request.POST)

        if form_user.is_valid():

            user_form = form_user.save(commit=False)

            username = form_user.cleaned_data['username']
            password = form_user.cleaned_data['password']
            user_form.set_password(password)
            user_form.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('cinema:home')

        return render(request, self.template_name, {'form_user': form_user})


class UserLoginFormView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('cinema:home')
        else:
            return render(request, self.template_name, {'error_message': 'Invalid username or password!'})


class UserLogoutView(View):
    template_name = 'logout.html'

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            logout(request)
            return render(request, self.template_name, {'user': user})
        else:
            return redirect('cinema:home')


class MovieView(generic.ListView):
    template_name = 'movies.html'
    model = Movie
    context_object_name = 'movie_list'
    paginate_by = 5


class MovieNameView(generic.ListView):
    template_name = 'movies.html'
    model = Movie
    context_object_name = 'movie_list'
    paginate_by = 5
    queryset = Movie.objects.order_by('movie_name')


class MoviePriceView(generic.ListView):
    template_name = 'movies.html'
    model = Movie
    context_object_name = 'movie_list'
    paginate_by = 5
    queryset = Movie.objects.order_by('movie_price')


class MovieCreateView(generic.CreateView):
    model = Movie
    fields = ['movie_name', 'movie_genre', 'movie_description', 'movie_price', 'movie_rating', 'movie_photo']
    template_name = 'movie_template.html'
    success_url = reverse_lazy('cinema:movie')


class MovieDetailView(generic.DetailView):
    template_name = 'movie_details.html'
    model = Movie


class MovieDeleteView(generic.DeleteView):
    model = Movie
    success_url = reverse_lazy('cinema:movie')


class MovieUpdateView(generic.UpdateView):
    model = Movie
    fields = ['movie_name', 'movie_genre', 'movie_description', 'movie_price', 'movie_rating', 'movie_photo']
    template_name = 'movie_template.html'
    success_url = reverse_lazy('cinema:movie')


def movieOrder(request, pk):
    user = request.user
    movie = Movie.objects.get(id=pk)
    price = movie.movie_price
    if user.is_active and user.is_authenticated:
        try:
            ticket_code = random.randint(100000, 1000000)
            send_mail('Ticket order',
                      f'Movie name: {movie.movie_name}\n'
                      f'Your ticket code: {ticket_code}\n'
                      f'Total: ${price}\n'
                      f'Enjoy!!! :)',
                      'cinema.nikolina@gmail.com',
                      [user.email])
        except SMTPException:
            return HttpResponse('Invalid')
        return render(request, 'order_succesfull.html')
    else:
        return redirect('cinema:login')
