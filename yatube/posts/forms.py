from django import forms
from posts.models import Post
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'group',)
        help_texts = {
            'text': _('Введите текст поста.'),
            'group': _('Укажите группу, к которой относится данный пост '
                '           (или оставьте это поле пустым'),
        }
