from django.urls import path, include

urlpatterns = [
    path('index/', include('index.urls')),
]

# API versioning
urlpatterns = [
    path('v0/', include(urlpatterns))
]
