from django import forms
from django.core.files.images import get_image_dimensions

from program.models import MusicFocus, ShowInformation, ShowTopic

class FormWithButton(forms.ModelForm):
    def clean_button(self):
        button = self.cleaned_data.get('button')
        if button:
            width, height = get_image_dimensions(button)
            if width != 11 or height != 11:
                raise forms.ValidationError("width or height is not 11, (11x11)")
        return button

    def clean_button_hover(self):
        button_hover = self.cleaned_data.get('button_hover')
        if button_hover:
            width, height = get_image_dimensions(button_hover)
            if width != 11 or height != 11:
                raise forms.ValidationError("width or height is not 11, (11x11)")
        return button_hover

    def clean_big_button(self):
        big_button = self.cleaned_data.get('big_button')
        if big_button:
            width, height = get_image_dimensions(big_button)
            if width != 17 or height != 17:
                raise forms.ValidationError("width or height is not 17, (17x17)")
        return big_button

class MusicFocusForm(FormWithButton):
    class Meta:
        model = MusicFocus

class ShowInformationForm(FormWithButton):
    class Meta:
        model = ShowInformation

class ShowTopicForm(FormWithButton):
    class Meta:
        model = ShowTopic

