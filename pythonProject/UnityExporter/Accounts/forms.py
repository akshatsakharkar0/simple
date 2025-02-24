from django import forms
from django.contrib.auth.models import User
from .models import CartItem


class UserRegistrationForm(forms.ModelForm):
    # Adding password fields for registration
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),

        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        # Check if both password fields match
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        # Return the second password field value after validation
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Set the password using set_password
        if commit:
            user.save()  # Save the user instance
        return user



class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity', 'size_in_kg']

    quantity = forms.IntegerField(min_value=1, initial=1, required=True)
    size_in_kg = forms.DecimalField(max_digits=5, decimal_places=2, initial=1.0, required=True)
