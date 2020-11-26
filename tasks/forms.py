from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, DateField, TextInput, CharField, ChoiceField, Form

from tasks.models import Task


class TaskForm(ModelForm):
    content = CharField(label='Qu\'est-ce qu\'il faut faire ?')
    due_date = DateField(widget=TextInput(
        attrs={'type': 'date'}
    ), label='Pour quand ?')
    status = ChoiceField(label='Où on en est ?', choices=Task.STATUS_CHOICES)

    class Meta:
        model = Task
        fields = ['content', 'due_date', 'status', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AddTaskForm(TaskForm):
    status = ChoiceField(label='Où on en est ?', choices=Task.STATUS_CHOICES, initial=Task.STATUS_TODO)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Ok, c\'est parti ! 🏃'))


class EditTaskForm(TaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Ok, on change ça ! 🏃'))


class DeleteTaskForm(Form):
    pass
