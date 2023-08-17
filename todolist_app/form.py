from django.forms import ModelForm
from todolist_app.models import TaskList

class TaskForm(ModelForm):
    class Meta:
        model = TaskList
        fields = ['task', 'done']
