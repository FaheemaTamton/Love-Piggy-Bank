from django.urls import path
from . import views

app_name = 'savings'

urlpatterns = [
    path('report/', views.report, name='report'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),
]
