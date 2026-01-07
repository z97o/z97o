from django import forms

class KPIImportForm(forms.Form):
    file = forms.FileField(label="Upload KPI CSV")
