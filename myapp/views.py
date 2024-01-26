from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from .forms import RegisterUserForm, LoginUserForm
from .models import ExpressionHistory, StringQuery
import random
from django.http import HttpResponseForbidden
import re
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def index(request):
    """
    Обработчик запроса для главной страницы.
    При вызове этой функции пользователю отображается главная страница.
    :param Объект HttpRequest от Django.
    :return Рендер главной страницы 'index.html'.
    """
    return render(request, 'index.html')


def riddle(request):
    """
    Обработчик запроса для главной страницы.
    При вызове этой функции пользователю отображается главная страница.
    :param Объект HttpRequest от Django.
    :return HttpResponse: Рендер главной страницы 'index.html'.
    """
    return render(request, 'riddle.html')


def answer(request):
    """
    Обработчик запроса для страницы с ответами на загадки.
    Показывает пользователю страницу с ответами на предыдущие загадки.

    :param Объект HttpRequest от Django.
    :return: HttpResponse: Рендер страницы 'answer.html' с ответами на загадки.
    """
    return render(request, 'answer.html')


def multiply(request):
    """
    Обработчик запроса для страницы умножения числа.
    На этой странице пользователь может ввести число, и функция
    вернет результат его умножения на числа от 1 до 10.
    :param Объект HttpRequest от Django.
    :return: HttpResponse: Рендер страницы 'multiply.html' с результатами умножения или сообщением об ошибке.
    """
    context = {}
    value = request.GET.get('value')

    if value:
        try:
            num = int(value)
            context['results'] = [(i, i * num) for i in range(1, 11)]
            context['value'] = num
        except ValueError:
            context['error'] = "Некорректное значение"

    return render(request, 'multiply.html', context)


def generate_expression(request):
    """
    Обработчик запроса для генерации и оценки математических выражений.

    При POST запросе пользователь отправляет математическое выражение,
    которое оценивается и записывается в историю. При GET запросе
    генерируется случайное выражение.
    :param request: Объект HttpRequest от Django.
    :return: HttpResponse: Рендер страницы 'expression.html' с результатом выражения или сообщением об ошибке.
    """
    if request.method == 'POST':
        user_expression = request.POST.get('user_expression', '').strip()

        if is_safe_expression(user_expression):
            try:
                result = eval(user_expression)
                ExpressionHistory.objects.create(expression=user_expression, result=result)
                return render(request, 'expression.html', {'expression': user_expression, 'result': result})
            except Exception as e:
                return render(request, 'expression.html', {'error': "Invalid expression"})
        else:
            return HttpResponseForbidden("Unsafe expression")

    else:
        num_terms = random.randint(2, 4)
        expression = ""
        total = 0
        for i in range(num_terms):
            number = random.randint(10, 99)
            operation = random.choice(['+', '-']) if i != 0 else ''
            expression += f" {operation} {number}"
            total = total + number if operation != '-' else total - number
        expression = expression.strip()
        result = total
        ExpressionHistory.objects.create(expression=expression, result=result)
        return render(request, 'expression.html', {'expression': expression, 'result': result})


def is_safe_expression(expr):
    """
    Проверяет, является ли математическое выражение безопасным для оценки.

    :param expr: Строка, содержащая математическое выражение.
    :return: Возвращает True, если выражение безопасно для оценки
    """
    safe_pattern = re.compile(r'^[\d+\-*/\(\) ]+$')
    return bool(safe_pattern.match(expr))


def expression_history(request):
    """
    Обработчик запроса для отображения истории математических выражений.
    Отображает все сохраненные выражения и их результаты.


    :param request:  Объект HttpRequest от Django.
    :return: HttpResponse: Рендер страницы 'history.html' с историей выражений.
    """
    history = ExpressionHistory.objects.all().order_by('-created_at')
    return render(request, 'history.html', {'history': history})


@login_required
def str2words_view(request):
    """
    Обработчик запроса для анализа строки и извлечения слов и чисел.
    Анализирует строку, введенную пользователем, извлекая слова и числа,
    и сохраняет запрос в базу данных. Доступен только аутентифицированным пользователям.

    :param request: Объект HttpRequest от Django.
    :return: HttpResponse: Рендер страницы 'str2words.html' с результатами анализа.
    """
    if request.method == 'POST':
        input_str = request.POST.get('input_str', '')
        words = re.findall(r'\b(?!\d+\b)\w+', input_str)
        numbers = re.findall(r'\b\d+\b', input_str)

        context = {
            'words_count': len(words),
            'numbers_count': len(numbers),
            'words': words,
            'numbers': numbers,
            'input_str': input_str,
        }
        StringQuery.objects.create(
            user=request.user,
            input_string=input_str,
            word_count=len(numbers),
            char_count=len(input_str)
        )
        return render(request, 'str2words.html', context)

    return render(request, 'str2words.html')


@login_required
def str_history(request):
    """
    Обработчик запроса для отображения истории запросов пользователя.
    Отображает историю запросов на анализ строк, сделанных текущим пользователем.
    Доступен только аутентифицированным пользователям.

    :param request: Объект HttpRequest от Django.
    :return: Рендер страницы 'str_history.html' с историей запросов.
    """
    history = StringQuery.objects.filter(user=request.user).order_by('-query_date', '-query_time')
    return render(request, 'str_history.html', {'history': history})


class RegisterUser(CreateView):
    """
    Класс представления для регистрации нового пользователя.
    Позволяет новым пользователям зарегистрироваться в системе.

    :param form_class: Форма для регистрации пользователя.
    :param template_name: Шаблон для отображения страницы регистрации.
    :param success_url: URL для перенаправления после успешной регистрации.
    """
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    """
    Класс представления для входа пользователя в систему.
    Позволяет пользователям войти в систему, используя свои учетные данные.

    :param form_class: Форма для входа пользователя.
    :param template_name: Шаблон для отображения страницы входа.
    """
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    """
    Обработчик запроса для выхода пользователя из системы.
    Позволяет пользователю выйти из системы и перенаправляет его на страницу входа.

    :param request: Объект HttpRequest от Django.
    :return: HttpResponse: Перенаправление на страницу входа.
    """
    logout(request)
    return redirect('login')
