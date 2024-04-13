from django import forms
from post_StartUp.models import Post_StartUp

from django.forms import ClearableFileInput
 
class NewPostForm_StartUp(forms.ModelForm):

	AVAILABILITY_CATEGORY = [
    ('Available', 'Available'),
	('Not Available', 'Not Available')
]

	CLASS_CATEGORY = [
    ('Breast cancer', 'Breast cancer'),
    ('Heart disease', 'Heart disease'),
    ('Osteoporosis', 'Osteoporosis'),
    ('Cervical cancer', 'Cervical cancer'),
    ('Ovarian cancer', 'Ovarian cancer'),
    ('Urinary tract infections', 'Urinary tract infections'),
    ('Polycystic ovary syndrome', 'Polycystic ovary syndrome'),
    ('Endometriosis', 'Endometriosis'),
    ('Thyroid disorders', 'Thyroid disorders'),
    ('Menstrual disorders', 'Menstrual disorders'),
    ('Menopause-related issues', 'Menopause-related issues'),
    ('Anemia', 'Anemia'),
    ('Migraines', 'Migraines'),
    ('Autoimmune diseases', 'Autoimmune diseases'),
    ('Diabetes', 'Diabetes'),
    ('Pelvic floor disorders', 'Pelvic floor disorders'),
    ('Gynecological cancers', 'Gynecological cancers'),
    ('Fibroids', 'Fibroids'),
    ('Depression', 'Depression')
]

	content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
	lessonLink= forms.URLField(widget=forms.TextInput(), max_length=50, required=False, initial='youtube.com')
	codeSourceOfTheProject = forms.ChoiceField(widget=forms.Select, choices=AVAILABILITY_CATEGORY, required=False, initial='classCategory')
	authorOfTheVideo = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-small'}), required=False, initial='example@gmail.com')
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
	classCategory = forms.ChoiceField(widget=forms.Select, choices=CLASS_CATEGORY, required=False, initial='classCategory')
	tagsStartUp = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-small'}), required=True, initial='physical') 


	class Meta:
		model = Post_StartUp
		fields = ('content', 'lessonLink', 'codeSourceOfTheProject', 'caption', 'authorOfTheVideo', 'classCategory', 'tagsStartUp')
