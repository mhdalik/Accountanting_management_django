from django.urls import path
from . import views

urlpatterns = [
    
    path('edit transaction/<int:pk>', views.edit_transaction, name='edit transaction'),
    path('add transaction/<str:entity_name>', views.add_transaction, name='add transaction'),
    path('journal/<str:entity_name>', views.journal_view, name='journal'),
    path('balance sheet/<str:entity_name>', views.balance_sheet, name='balance sheet'),
    
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.index, name='index'),

]

