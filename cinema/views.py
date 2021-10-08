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


class HomeView(generic.ListView):
    template_name = 'home.html'
    model = Movie
    context_object_name = 'movie_list'
    queryset = Movie.objects.filter(movie_comming_soon=True)


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
    queryset = Movie.objects.filter(movie_comming_soon=False)


class MovieNameView(generic.ListView):
    template_name = 'movies.html'
    model = Movie
    context_object_name = 'movie_list'
    paginate_by = 5
    queryset = Movie.objects.filter(movie_comming_soon=False).order_by('movie_name')


class MoviePriceView(generic.ListView):
    template_name = 'movies.html'
    model = Movie
    context_object_name = 'movie_list'
    paginate_by = 5
    queryset = Movie.objects.filter(movie_comming_soon=False).order_by('movie_price')


class MovieCreateView(generic.CreateView):
    model = Movie
    fields = ['movie_name', 'movie_genre', 'movie_description', 'movie_price', 'movie_rating', 'movie_photo',
              'movie_num_of_tickets', 'movie_time', 'movie_day','movie_comming_soon']
    template_name = 'movie_template.html'
    success_url = reverse_lazy('cinema:movie')


class MovieDetailView(generic.DetailView):
    template_name = 'movie_details.html'
    model = Movie

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        movie = context['object']
        if movie.movie_num_of_tickets == 50:
            context['error_message'] = 'All tickets are sold. Come next week or choose another movie.'
        context['time'] = movie.movie_time.strftime("%H:%M")
        return context


class MovieDeleteView(generic.DeleteView):
    model = Movie
    success_url = reverse_lazy('cinema:movie')


class MovieUpdateView(generic.UpdateView):
    model = Movie
    fields = ['movie_name', 'movie_genre', 'movie_description', 'movie_price', 'movie_rating', 'movie_photo',
              'movie_num_of_tickets', 'movie_time', 'movie_day','movie_comming_soon']
    template_name = 'movie_template.html'
    success_url = reverse_lazy('cinema:movie')


def movieOrder(request, pk):
    user = request.user
    movie = Movie.objects.get(id=pk)
    price = movie.movie_price
    if user.is_active and user.is_authenticated:
        if movie.movie_num_of_tickets < 50:
            try:
                ticket_code = random.randint(100000, 1000000)
                send_mail('Ticket order',
                          f'Your ticket code: {ticket_code}\n'
                          f'On: {movie.movie_day} at: {movie.movie_time.strftime("%H:%M")}\n'
                          f'Total: ${price}\n'
                          f'Enjoy!!! :)',
                          'cinema.nikolina@gmail.com',
                          [user.email])
                movie.movie_num_of_tickets += 1
                movie.save()
            except SMTPException:
                return HttpResponse('Invalid')
            return render(request, 'order_succesfull.html')
        else:
            return redirect('cinema:movie_details', movie.id)
    else:
        return redirect('cinema:login')
