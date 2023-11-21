from django.urls import path
from . import views

urlpatterns = [
               path('review/<int:pk>', views.AddComments.as_view(), name='add_comments'),
               path('mem/<slug:mem_slug>/', views.MemDetail.as_view(), name='mem'),
               path('category/<slug:cat_slug>/', views.ShowCategory.as_view(), name='category'),
               path('addmem/', views.AddMem.as_view(), name='add_mem'),
               path('login/', views.LoginUser.as_view(), name="login"),
               path('register/', views.RegisterUser.as_view(), name="register"),
               path('logout/', views.logout_user, name="logout"),
               path('contact/', views.ContactFormView.as_view(), name='contact'),
               path('', (views.MemesView.as_view()), name='home')]
