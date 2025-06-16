from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, SignupForm, TaskForm, NewTaskForm
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from .serializer import TaskSerializer
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend


def todo_list(request):
    return render(
        request, 
        'todo_list/index.html')

class ApiManagementMixin(APIView):
    permission_classes = [HasAPIKey | permissions.IsAuthenticated]

    def get(self, request):
        return Response({"mensagem": "Authorized!"})
    
class SerializedView(viewsets.ModelViewSet, ApiManagementMixin):
    queryset = Task.objects.all().order_by('name')
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'status']

    def get_queryset(self):
        return super().get_queryset()


# class LoginView(TemplateView):
#     template_name = 'login/index.html'

#     def get(self, request):
#         form = LoginForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = LoginForm(request.POST)
#         msg = ''
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 print("Logado com sucesso")
#                 login(request, user)
#                 return redirect('tasks')
#             else:
#                 print("Access denied")
#                 msg = 'Usuário ou senha inválidos.'
#             print(username, password)
#         return render(request, self.template_name, {'form': form, 'msg': msg})

def home(request):
    return render(request, 'home.html')

def signup_view(request):
    form = UserCreationForm(request.POST or None)
    msg = ''

    if request.method == 'POST':
        print("POST data:", request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            if User.objects.filter(username=username).exists():
                msg = 'Este nome de usuário já está em uso.'
                print(f"Usuário {username} já existe.")
            else:
                try:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    print(f"Usuário criado: {username}")
                    return redirect('login')
                except Exception as e:
                    msg = f'Erro ao criar usuário: {str(e)}'
                    print("Erro:", str(e))
        else:
            msg = 'Formulário inválido. Verifique os dados fornecidos.'
            print("AQUI")
            print("Erros do formulário:", form.errors)

    return render(request, 'signup.html', {'form': form, 'msg': msg})


def task_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Filtra as tasks apenas do usuário logado
    tasks = Task.objects.filter(user=request.user).order_by('-id')
    form = TaskForm()

    if request.method == 'POST':
        if request.POST.get('action') == 'add_task':
            return redirect('add_task')

        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # associa o task ao usuário
            task.save()
            return redirect('task_list')

    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks.html', context)

def add_task(request):
    form = NewTaskForm(request.POST or None)
    if not request.user.is_authenticated:
        return redirect('login')
    # if request.method == 'POST':
    #     if form.is_valid():
    #         print(form.cleaned_data)
    #         task_name = form.cleaned_data['task_name']
    #         task_description = form.cleaned_data['task_description']
    #         task_status = form.cleaned_data['task_status']

    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            print(form.data, request.user)
            form.instance.user = request.user
            form.save()
            return redirect('tasks')
            

    # print(form.data, request.user)
    # context = {'new_task': task, 'form': form}
    return render(request, 'add_task.html', {'form': form})

def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == 'POST':
        if 'delete' in request.POST:
            task.delete()
            return redirect('tasks')

        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form, 'task': task})