from django.forms import CharField, ModelForm, TextInput
from .models import Quote, Author, Tag


class QuoteForm(ModelForm):
    quote = CharField(min_length=10, max_length=450, required=True, widget=TextInput())
    tag = CharField(min_length=5, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ["quote"]
        exclude = ["tag"]


class AuthorForm(ModelForm):
    fullname = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    born_date = CharField(max_length=50, required=True, widget=TextInput())
    born_location = CharField(max_length=150, required=True, widget=TextInput())
    description = CharField(
        min_length=5, max_length=500, required=True, widget=TextInput()
    )

    class Meta:
        model = Author
        fields = [
            "fullname",
            "born_date",
            "born_location",
            "description",
        ]
