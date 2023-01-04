from django.urls import include, path

app_name = 'v1'
urlpatterns = [
    path('theater/', include('api.v1.theater.urls', namespace='theater')),
]