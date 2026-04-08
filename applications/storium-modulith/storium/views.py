from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class StoriumUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "username",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "new-password"},
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "new-password"},
        )


class RegisterView(CreateView):
    form_class = StoriumUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Hesabınız oluşturuldu. Giriş yapabilirsiniz.",
        )
        return super().form_valid(form)
