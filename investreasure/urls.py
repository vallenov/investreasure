from django.urls import path, include

urlpatterns = [
    path('test/', include('test.urls')),
]

# API versioning
urlpatterns = [
    path('api/v0/', include(urlpatterns))
]
