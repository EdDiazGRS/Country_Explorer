import requests
import json
import datetime
from django.views.generic import ListView, TemplateView, DetailView, View
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.http import require_POST
from .models import Country, Favorite, Review
from .utils import refresh_country_data


class HomeView(TemplateView):
    template_name = 'country/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country_count'] = Country.objects.count()
        # You could add more stats here
        return context
    
class CountryListView(ListView):
    model = Country
    template_name = 'country/country_list.html'
    context_object_name = 'countries'
    ordering = ['name']

class CountryDetailView(DetailView):
    model = Country
    template_name = 'country/country_detail.html'
    context_object_name = 'country'
    pk_url_kwarg = 'country_id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(
                user=self.request.user, 
                country=self.object
            ).exists()
            context['user_review'] = Review.objects.filter(
                user=self.request.user,
                country=self.object
            ).first()
        context['reviews'] = Review.objects.filter(country=self.object).select_related('user')
        context['avg_rating'] = Review.objects.filter(country=self.object).aggregate(Avg('rating'))['rating__avg']
        return context

class CountrySearchView(ListView):
    model = Country
    template_name = 'country/country_search.html'
    context_object_name = 'countries'
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        query = self.request.GET.get('q', '')
        population_filter = self.request.GET.get('population','')
        
        if query:
            queryset = queryset.filter(name__icontains=query)
        if population_filter:
            if population_filter == 'small':
                queryset = queryset.filter(population__lt=1000000) # less than 1 mil
            elif population_filter == 'medium':
                queryset = queryset.filter(population__gte=1000000, population__lt=100000000) # between 1 mil and 100 mil
            elif population_filter == 'large':
                queryset = queryset.filter(population__gte=100000000) # greater than 100 mil

        if not query and not population_filter:
            queryset = queryset[:10]  #limit to 10 if no search specified
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['population_filter'] = self.request.GET.get('population', '')
        return context
    
class FetchCountryDataView(View):
    def get(self, request):
        result = refresh_country_data()
        if result['success']:
            messages.success(request, result['message'])
            request.session['last_refresh']= {
                'time': str(datetime.datetime.now()),
                'created': result['created'],
                'updated': result['updated'],
                'total': result['total']
            }
        else:
            messages.error(request, result['message'])
        return redirect(request.META.get('HTTP_REFERER', 'country:home'))
    

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('country:home')
    else:
            form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form})
    
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('country:home')
    else:
            form = UserCreationForm()
    return render(request, 'registration/register.html', {'form':form})
    
@login_required 
def logout_view(request):
    logout(request)
    return redirect('country:login')


@require_POST
@login_required
def toggle_favorite(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        country=country
    )
    
    if not created:
        favorite.delete()
        is_favorite = False
        messages.success(request, f"{country.name} removed from favorites")
    else:
        is_favorite = True
        messages.success(request, f"{country.name} added to favorites")
    return redirect('country:country_detail', country_id=country_id)


@login_required
def add_review(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        if not rating:
            messages.error(request, 'Rating is required')
            return redirect('country:country_detail', country_id=country_id)
        
        review, created = Review.objects.update_or_create(
            user=request.user,
            country=country,
            defaults={
                'rating': rating,
                'comment': comment
            }
        )
        
        if created:
            messages.success(request, 'Review added successfully')
        else:
            messages.success(request, 'Review updated successfully')
    return redirect('country:country_detail', country_id=country_id)
            
@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('country')
    return render(request, 'country/my_favorites.html', {'favorites':favorites})