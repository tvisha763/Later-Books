from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('apiCall', views.apiCall, name='apiCall'),
    path('back', views.back, name='back'),
    #path('api/addtoreadinglist', views.add_to_reading_list, name='ad0d_to_readinglist'),
    path('home', views.home, name='home'),
    #path('bookSearch', views.bookSearch, name='bookSearch'),

    path('addToReadingList', views.addToReadingList, name='addToReadingList'),
    path('removeFromReadingList', views.removeFromReadingList, name='removeFromReadingList'),

    path('api/book/<slug:id>/', views.book, name='book'),
    path('comments', views.comments, name='comments'),


]
