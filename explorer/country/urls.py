from django.urls import path
from .views import HomeView, CountryListView, CountryDetailView, CountrySearchView, FetchCountryDataView, login_view, logout_view, register_view, toggle_favorite, add_review, my_favorites

app_name = 'country'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('countries/', CountryListView.as_view(), name='country_list'),
    path('countries/<int:country_id>/', CountryDetailView.as_view(), name='country_detail'),
    path('search/', CountrySearchView.as_view(), name='search'),
    path('fetch-countries/', FetchCountryDataView.as_view(), name='fetch_countries'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('countries/<int:country_id>/favorite/', toggle_favorite, name='toggle_favorite'),
    path('countries/<int:country_id>/review/', add_review, name='add_review'),
    path('my-favorites/', my_favorites, name='my_favorites'),
]