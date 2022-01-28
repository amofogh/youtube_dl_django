from django import forms
from re import match


class link_form(forms.Form):
    link = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'Paste your link here',
                                                       'class': 'form-control p-3 shadow-lg border-0',
                                                       'onpaste': 'Pasted()',
                                                       'id': 'input-link'}))

    # link = forms.CharField(max_length=500,
    #                        widget=forms.TextInput(attrs={'placeholder': 'Paste your link here',
    #                                                      'class': 'form-control p-3 shadow-lg border-0',
    #                                                      'onpaste': 'Pasted()'}))
    def clean_link(self):
        link = self.cleaned_data['link']
        regex = r'^.*www.youtube.com.*'
        if match(regex, link):
            return link
        raise forms.ValidationError('The link is not belong to youtube.com')


class download_video_form(forms.Form):
    quality = forms.CharField(max_length=100, widget=forms.HiddenInput())
    link = forms.URLField(widget=forms.HiddenInput())
    file_type = forms.CharField(max_length=100, widget=forms.HiddenInput())
