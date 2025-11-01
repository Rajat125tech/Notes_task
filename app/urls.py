from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <h1>Welcome to Notes & Tasks API</h1>
        <p>Available endpoints:</p>
        <ul>
            <li><a href="/api/tasks/">Tasks</a></li>
            <li><a href="/api/notes/">Notes</a></li>
            <li><a href="/api/docs/">Swagger Docs</a></li>
        </ul>
    """)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # 👈 this connects your core app's URLs
]
