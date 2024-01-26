from django.db import models
from django.contrib.auth.models import User

class ExpressionHistory(models.Model):
    """
    Эта модель предназначена для хранения истории математических выражений и их результатов.
    expression: Поле типа CharField с максимальной длиной 255 символов. В этом поле хранится строка, представляющая математическое выражение.
    result: Поле типа IntegerField. Здесь хранится числовой результат вычисления выражения expression.
    created_at: Поле типа DateTimeField. Это поле автоматически устанавливается в момент создания записи и хранит дату и время создания записи.
    """
    expression = models.CharField(max_length=255)
    result = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expression} = {self.result}"

class StringQuery(models.Model):
    """
    модель используется для хранения информации о запросах пользователей, связанных с обработкой и анализом строк.
    user: Поле типа ForeignKey, связанное с моделью User. Это поле указывает на пользователя, который сделал запрос.
    query_date: Поле типа DateField, которое автоматически устанавливает текущую дату, когда был сделан запрос.
    query_time: Поле типа TimeField, которое автоматически устанавливает текущее время, когда был сделан запрос.
    input_string: Поле типа TextField, предназначенное для хранения входящей строки, подлежащей обработке.
    word_count: Поле типа IntegerField, в котором хранится количество слов, найденных в input_string.
    char_count: Поле типа IntegerField, в котором хранится количество символов в input_string.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query_date = models.DateField(auto_now_add=True)
    query_time = models.TimeField(auto_now_add=True)
    input_string = models.TextField()
    word_count = models.IntegerField()
    char_count = models.IntegerField()