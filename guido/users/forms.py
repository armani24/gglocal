from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


from .models import MyUser

class OwnerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    buzzer = forms.CharField(initial='customer', max_length=8)
    class Meta:
        model = MyUser
        fields = ['name','buzzer', 'email', 'phone', 'password']


from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))


class PassForm(forms.Form):
    #send email to who waant to contact_us
    old_pass = forms.CharField(min_length=8, widget=forms.PasswordInput)
    pass1 = forms.CharField(min_length=8, widget=forms.PasswordInput)
    pass2 = forms.CharField(min_length=8, widget=forms.PasswordInput)
    class Meta:
        fields = ['old_pass','pass1','pass2']
    

    def clean_password2(self):
            # Check that the two password entries match
        pass1 = self.cleaned_data.get("pass1")
        pass2 = self.cleaned_data.get("pass2")

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Passwords don't match")
        return pass2


class EmailChangeForm(forms.Form):
    #send email to who waant to contact_us
    email1 = forms.EmailField(help_text='A valid email address, please.')
    email2 = forms.EmailField()
    # password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    class Meta:
        fields = ['Email1','Email2']

    def clean_email2(self):
            # Check that the two password entries match
        email1 = self.cleaned_data.get("email1")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError("Emails does not match")
        return email2

from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get("image")
        try:
            if image.width < 716 and image.height < 456:
                raise forms.ValidationError("Please enter bigger size image.")
        except:
            pass
        
        return image

from django.core.validators import RegexValidator
phone_regex = RegexValidator(regex=r'^[0-9]*$', message="Phone number must contain only digits.")

class NameForm(forms.Form):
    name = forms.CharField(max_length=100)    
    phone = forms.CharField(max_length=20, validators=[phone_regex])

    class Meta:
        fields = ['name', 'phone']