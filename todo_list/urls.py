from django.contrib import admin
from django.urls import include, path
from .views import home, todo_list, signup_view, task_list, add_task, edit_task, SerializedView
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'apiTest', SerializedView)

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('teste/', todo_list),
    # path('home/', include('home.urls')),
    path('', LoginView.as_view( template_name='login.html', authentication_form=LoginForm, next_page='tasks'), name='login'), #redirect_authenticated_user=True para ja logar em usuario logado
    path('home/', home, name='home'),  # Página inicial após login
    path('todo_list/', todo_list, name='todo_list'),
    path('signup/', signup_view, name='signup'),
    path('tasks/', task_list, name='tasks'),
    path('new_task/', add_task, name='add_task'),
    path('editar/<int:id>/', edit_task, name='edit_task'),
    path('', include(router.urls))

]
