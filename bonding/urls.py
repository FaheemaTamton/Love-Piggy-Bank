from django.urls import path
from . import views

app_name = 'bonding'

urlpatterns = [
    path('', views.bonding_view, name='bonding'),      # Log Bonding
    path('quarrel/', views.quarrel_view, name='quarrel'),  # Log Quarrel
]
