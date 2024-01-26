from django.http import HttpResponse
from django.shortcuts import render
from .models import ExpressionHistory
import random
from django.http import HttpResponseForbidden
import re


def index(request):
    return render(request, 'index.html')


def riddle(request):
    return render(request, 'riddle.html')


def answer(request):
    return render(request, 'answer.html')


def multiply(request):
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
    safe_pattern = re.compile(r'^[\d+\-*/\(\) ]+$')
    return bool(safe_pattern.match(expr))


def expression_history(request):
    history = ExpressionHistory.objects.all().order_by('-created_at')
    return render(request, 'history.html', {'history': history})


def str2words_view(request):
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

        return render(request, 'str2words.html', context)

    return render(request, 'str2words.html')
