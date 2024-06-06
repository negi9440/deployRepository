from django import forms
from .models import Item, Share, Budget, Favorite, Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ItemForm(forms.ModelForm):
    category_name = forms.CharField(max_length=100, label='カテゴリー')
    
    category_name = forms.CharField(
        max_length=100,
        label='カテゴリー',
        error_messages={'required': 'このフィールドは必須です。'}
    )

    name = forms.CharField(
        max_length=100,
        label='アイテム名',
        error_messages={'required': 'このフィールドは必須です。'}
    )

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='価格',
        error_messages={'required': 'このフィールドは必須です。'}
    )

    release_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='リリース日',
        error_messages={'required': 'このフィールドは必須です。'}
    )


    class Meta:
        model = Item
        fields = ['name', 'price', 'release_date', 'category_name']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("価格は0以上でなければなりません。")
        return price
    
    
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.category:
            self.fields['category_name'].initial = self.instance.category.name
            

    def save(self, commit=True):
        instance = super(ItemForm, self).save(commit=False)
        # category_name から Category オブジェクトを取得または作成
        category_name = self.cleaned_data.get('category_name')
        if category_name:
            category, created = Category.objects.get_or_create(name=category_name)
            instance.category = category
        if commit:
            instance.save()
        return instance    
    
    

class ShareForm(forms.ModelForm):
    class Meta:
        model = Share
        fields = ['shared_with_user']

class BudgetForm(forms.ModelForm):
    month = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='月',
        error_messages={'required': 'このフィールドは必須です。'}
    )
    budget = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='予算',
        error_messages={'required': 'このフィールドは必須です。'}
    )
    
    class Meta:
        model = Budget
        fields = ['month', 'budget']
        labels = {
            'month': '月',
            'budget': '予算'
        }
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month'}),
            'budget': forms.NumberInput(attrs={'step': '0.01'})
        }
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date'}),
            'budget': forms.NumberInput(attrs={'step': '0.01'})
        }
        
    def clean_budget(self):
        budget = self.cleaned_data['budget']
        if budget < 0:
            raise forms.ValidationError("予算は0以上の値でなければなりません。")
        return budget
        

# 新規登録フォーム


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='ユーザー名',  # フィールドのラベルを設定
        help_text='',  # ヘルプテキストを削除
        error_messages={  # エラーメッセージのカスタマイズ
            'required': 'この項目は必須です。',
            'invalid': '有効なユーザー名を入力してください。'
        }
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("このメールアドレスは既に使用されています。")
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and ' ' in password1:
            raise ValidationError("パスワードに半角スペースを含めることはできません。")
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("パスワードが一致しません。")
        if password2 and ' ' in password2:
            raise ValidationError("パスワードに半角スペースを含めることはできません。")
        return password2
            
#ログインフォーム
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="アドレス", widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="パスワード",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )
    
    error_messages = {
        'invalid_login': _(
            "正しいメールアドレスとパスワードを入力してください。"
        ),
        'inactive': _("このアカウントは無効です。"),
    }

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


        
class FavoriteForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        label='名前',
        error_messages={'required': 'このフィールドは必須です。'}
    )

    class Meta:
        model = Favorite
        fields = ['name']  # お気に入りの名前を登録するためのフィールド
        labels = {
            'name': '名前',
        }



class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="メールアドレス")
    new_password = forms.CharField(label="新しいパスワード", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="新しいパスワード(確認)", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("パスワードが一致しません。")

        return cleaned_data