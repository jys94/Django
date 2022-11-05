from django.urls import path
from . import views


app_name = "product"
urlpatterns =[
    path('index/', views.index, name="index"),
    path('detail/<bpk>', views.detail, name="detail"),
    path('delete/<bpk>', views.delete, name="delete"),
    path('create/', views.create, name="create"),
    path('update/<bpk>', views.update, name="update"),
    path('creview/<bpk>', views.creview, name="creview"),
    path('dreview/<bpk>/<rpk>', views.dreview, name="dreview"),
]