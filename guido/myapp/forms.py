from django import forms
from .models import Listing, ListingCategory, Messages, Guides, Message_Guide
from django.forms import inlineformset_factory
from django.core.validators import RegexValidator


phone_regex = RegexValidator(regex=r'^[0-9]*$', message="Phone number must contain only digits.")

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'category', 'city', 'price', 'description','highlights', 'image1',
        'image2','image3','image4','email','phone',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'category': forms.Select(attrs={'class':"selectpicker", "data-live-search":"true", "data-width":"100%"}),
            'city': forms.Select(attrs={'class':"selectpicker", "data-live-search":"true", "data-width":"100%"}),
            'highlights': forms.CheckboxSelectMultiple(attrs={"class":"add_listing selectable-list"}),  # For multiple selection

        
        }
    
    
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        
        self.fields['category'].queryset = ListingCategory.objects.exclude(name="Guides")
    
    def clean_image1(self):
        image1 = self.cleaned_data.get("image1")
        if image1.image.width < 716 and image1.image.height < 456:
            raise forms.ValidationError("Please enter bigger size image.")
        return image1
    
    def clean_image2(self):
        image2 = self.cleaned_data.get("image2")
        if image2.image.width < 716 and image2.image.height < 456:
            raise forms.ValidationError("Please enter bigger size image.")
        return image2
    
    def clean_image3(self):
        image3 = self.cleaned_data.get("image3")
        if image3.image.width < 716 and image3.image.height < 456:
            raise forms.ValidationError("Please enter bigger size image.")
        return image3
    
    def clean_image4(self):
        image4 = self.cleaned_data.get("image4")
        if image4.image.width < 716 and image4.image.height < 456:
            raise forms.ValidationError("Please enter bigger size image.")
        return image4
        

class EditListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'category', 'city', 'price', 'description','highlights', 'image1',
        'image2','image3','image4','email','phone',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'category': forms.Select(attrs={'class':"selectpicker", "data-live-search":"true", "data-width":"100%"}),
            'city': forms.Select(attrs={'class':"selectpicker", "data-live-search":"true", "data-width":"100%"}),
            'highlights': forms.CheckboxSelectMultiple(attrs={"class":"add_listing selectable-list"}),  # For multiple selection
        }
    
    
    def __init__(self, *args, **kwargs):
        super(EditListingForm, self).__init__(*args, **kwargs)
        
        self.fields['category'].queryset = ListingCategory.objects.exclude(name="Guides")
    
    def clean_image1(self):
        image1 = self.cleaned_data.get("image1")
        try:
            if image1.width < 716 and image1.height < 456:
                raise forms.ValidationError("Please enter bigger size image.")
        except:
            pass
        
        return image1
        
    def clean_image2(self):
        image2 = self.cleaned_data.get("image2")
        try:
            if image2.width < 716 and image2.height < 456:
                raise forms.ValidationError("Please enter bigger size image.")
        except:
            pass
        
        return image2
        
    
    def clean_image3(self):
        image3 = self.cleaned_data.get("image3")
        try:
            if image3.width < 716 and image3.height < 456:
                raise forms.ValidationError("Please enter bigger size image.")
        except:
            pass
        
        return image3
    
    def clean_image4(self):
        image4 = self.cleaned_data.get("image4")
        try:
            if image4.width < 716 and image4.height < 456:
                raise forms.ValidationError("Please enter bigger size image.")
        except:
            pass
        
        return image4
        



class Filt_Form(forms.Form):
    category = forms.Select()
    city = forms.Select()
    
    class Meta:
        fields = ['category', 'city']
        



RATING_CHOICES = (
    (1, '1 🌟'),
    (2, '2 🌟🌟'),
    (3, '3 🌟🌟🌟'),
    (4, '4 🌟🌟🌟🌟'),
    (5, '5 🌟🌟🌟🌟🌟'),
)
class ReviewForm(forms.Form):
    rating = forms.ChoiceField(choices=RATING_CHOICES)
    content = forms.CharField(widget=forms.Textarea)
    widgets = {

            'rating': forms.Select(attrs={'class':"form-control"}),

        }


class MessageForm(forms.Form):
    class Meta:
        model = Messages
        fields = ["messege"]


class GuidesForm(forms.ModelForm):
    class Meta:
        model = Guides
        fields = ['name', 'city', 'price', 'description', 'image1','email','phone',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'city': forms.Select(attrs={'class':"selectpicker", "data-live-search":"true", "data-width":"100%"}),
        }



RATING_CHOICES = (
    (1, '1 🌟'),
    (2, '2 🌟🌟'),
    (3, '3 🌟🌟🌟'),
    (4, '4 🌟🌟🌟🌟'),
    (5, '5 🌟🌟🌟🌟🌟'),
)
class GuidesReviewForm(forms.Form):
    rating = forms.ChoiceField(choices=RATING_CHOICES)
    content = forms.CharField(widget=forms.Textarea)
    widgets = {

            'rating': forms.Select(attrs={'class':"form-control"}),

        }

class MsgGuideForm(forms.ModelForm):
    class Meta:
        model = Message_Guide
        fields = ['message']

    
