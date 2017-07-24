from django import forms

from lists.models import Item


EMPTY_ITEM_ERROR = "You cannot have an empty list item"


class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ("text",)
        widgets = {
            "text": forms.fields.TextInput(attrs={
                "placeholder": "Enter a word",
                "class": "form-control pure-input-1",
            }),
        }
        error_messages = {
            "text": {"required": EMPTY_ITEM_ERROR}
        }
