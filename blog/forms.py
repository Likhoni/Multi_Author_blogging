from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Category, Tag

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email address'})
    )
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'})
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Tell us a bit about yourself (optional)'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-input'


class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter post title'})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 10, 'placeholder': 'Write your post content here...'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="-- Select Category --"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tag-checkbox-list'}),
        required=False,
        help_text="Select tags for this post"
    )
    featured_image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-file-input'}),
        required=True,
        help_text="Upload a cover/featured image for your post"
    )
    status = forms.ChoiceField(
        choices=Post.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'featured_image', 'category', 'tags', 'status')


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            'class': 'form-input comment-textarea',
            'rows': 3,
            'placeholder': 'Share your thoughts on this post...'
        })
    )

    class Meta:
        model = Comment
        fields = ('text',)


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Category Name'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Optional Description'})
    )

    class Meta:
        model = Category
        fields = ('name', 'description')


class TagForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tag Name'})
    )

    class Meta:
        model = Tag
        fields = ('name',)

