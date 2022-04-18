from django import forms

heights=[]
class Filter_Age(forms.Form):
	age_f = forms.CharField(max_length = 2, label="Age?", required = False)
	h_feet = forms.CharField(max_length = 1, label= "Feet", required = False)
	h_inches= forms.CharField(max_length = 2, label = "Inches", required = False)
