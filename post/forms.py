from django import forms
from post.models import Post 

from django.forms import ClearableFileInput

class NewPostForm(forms.ModelForm):

	AVAILABILITY_CATEGORY = [
    ('Available', 'Available'),
	('Not Available', 'Not Available')
]

	CLASS_CATEGORY =  [
    ('Depression', 'Depression'),
    ('Anxiety disorders', 'Anxiety disorders'),
    ('Postpartum depression', 'Postpartum depression'),
    ('Postpartum anxiety', 'Postpartum anxiety'),
    ('Premenstrual dysphoric disorder', 'Premenstrual dysphoric disorder'),
    ('Eating disorders', 'Eating disorders'),
    ('Borderline personality disorder', 'Borderline personality disorder'),
    ('Obsessive-compulsive disorder', 'Obsessive-compulsive disorder'),
    ('Trauma-related disorders', 'Trauma-related disorders'),
    ('Bipolar disorder', 'Bipolar disorder'),
    ('Body dysmorphic disorder', 'Body dysmorphic disorder'),
    ('Perinatal mood & anxiety', 'Perinatal mood & anxiety'),
    ('Seasonal affective disorder', 'Seasonal affective disorder'),
    ('Substance use disorders', 'Substance use disorders'),
    ('Self-harm behaviors', 'Self-harm behaviors'),
    ('Dissociative disorders', 'Dissociative disorders'),
    ('Adjustment disorders', 'Adjustment disorders'),
    ('Psychotic disorders', 'Psychotic disorders')
]

	content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
	lessonLink= forms.URLField(widget=forms.TextInput(), max_length=50, required=False, initial='youtube.com')
	codeSourceOfTheProject = forms.ChoiceField(widget=forms.Select, choices=AVAILABILITY_CATEGORY, required=False, initial='classCategory')
	authorOfTheVideo = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-small'}), required=False, initial='example@gmail.com')
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
	classCategory = forms.ChoiceField(widget=forms.Select, choices=CLASS_CATEGORY, required=False, initial='classCategory')
	tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-small'}), required=True, initial='mental')


	class Meta:
		model = Post
		fields = ('content', 'lessonLink', 'codeSourceOfTheProject', 'caption', 'authorOfTheVideo', 'classCategory', 'tags')


