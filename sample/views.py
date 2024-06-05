from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Share, Budget, Favorite, Category
from .forms import ItemForm, BudgetForm, CustomUserCreationForm, FavoriteForm, CustomAuthenticationForm, PasswordResetForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, get_user_model
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db.models import Sum





@login_required
def home_view(request):
    favorites = Favorite.objects.filter(user=request.user)
    
    # 最初のfavorite_idを取得（必要に応じて変更）
    favorite_id = favorites.first().id if favorites.exists() else None
    
    return render(request, 'sample/home.html', {
        'favorites': favorites,
        'favorite_id': favorite_id
    })


@login_required
def favorite_create(request):
    if request.method == 'POST':
        form = FavoriteForm(request.POST)
        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = request.user  # お気に入りを作成するユーザーを設定
            favorite.save()
            return redirect('sample:home')  # 作成後はホームページにリダイレクト
    else:
        form = FavoriteForm()
        # favorite_idがNoneまたは空文字列の場合にデフォルト値を設定
    return render(request, 'sample/favorite_create.html', {'form': form})



@login_required
def add_to_favorites(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    Favorite.objects.get_or_create(user=request.user, item=item)
    return redirect('sample:home')


#推し編集

@login_required
def favorite_edit(request, favorite_id):
    favorite = get_object_or_404(Favorite, pk=favorite_id, user=request.user)
    if request.method == 'POST':
        form = FavoriteForm(request.POST, instance=favorite)
        if form.is_valid():
            form.save()
            return redirect('sample:home')  # 保存後はホームページにリダイレクト
    else:
        form = FavoriteForm(instance=favorite)
    return render(request, 'sample/favorite_edit.html', {'form': form})


#推し削除
@login_required
def favorite_delete(request, favorite_id):
    favorite = get_object_or_404(Favorite, pk=favorite_id, user=request.user)
    favorite.delete()
    return redirect('sample:home')


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('item')
    return render(request, 'sample/home.html', {'favorites': favorites})

@login_required
def remove_from_favorites(request, favorite_id):
    favorite = get_object_or_404(Favorite, pk=favorite_id, user=request.user)
    favorite.delete()
    return redirect('sample:home')



@login_required
def item_create(request, favorite_id):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            # form.save() は、フォームのデータから Item インスタンスを作成し、データベースに保存します。
            # commit=False は、まだ保存しないことを意味し、ユーザー情報を追加するために使います。
            item = form.save(commit=False)
            item.user = request.user  # アイテムの所有者を現在のユーザーに設定
            # カテゴリー名をテキストフィールドから取得し、データベースで検索、存在しない場合は新規作成
            category_name = form.cleaned_data.get('category_name')
            if category_name:
                category, created = Category.objects.get_or_create(name=category_name)
                item.category = category
                item.save()  # カテゴリーを割り当てた後でアイテムを保存
                
                # お気に入りリストにアイテムを追加
                favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
                favorite.items.add(item)  # 多対多フィールドにアイテムを追加
                favorite.save()
                
                messages.success(request, 'アイテムが正常に登録されました。')
                return redirect('sample:item_list_with_favorite', favorite_id=favorite_id)
            else:
                form.add_error('category_name', 'カテゴリー名が入力されていません。')
                # エラーメッセージをフォームに直接追加
        # フォームのバリデーションエラーまたはカテゴリー名が空の場合
        messages.error(request, '入力内容にエラーがあります。')
    else:
        form = ItemForm()  # GET リクエストの場合は空のフォームを生成

    return render(request, 'sample/item_create.html', {'form': form,  'favorite_id': favorite_id})


User = get_user_model()

@login_required
def share_item(request, item_id):
    username = request.GET.get('username')
    if not username:
        return HttpResponse("Username is required", status=400)
    user_to_share_with = get_object_or_404(User, username=username)
    item = get_object_or_404(Item, pk=item_id, user=request.user)

    Share.objects.create(item=item, owner_user=request.user, shared_with_user=user_to_share_with)
    messages.success(request, f'"{item.name}" を "{username}" と共有しました。')
    
    # favorite_idを取得
    favorite_id = item.favorite_set.first().id if item.favorite_set.exists() else None
    if favorite_id:
        return redirect('sample:item_list_with_favorite', favorite_id=favorite_id)
    return redirect('sample:home')  # favorite_idが存在しない場合はホームへリダイレクト
    

    

def shared_items(request, favorite_id):
    if request.method == 'POST':
        share_id = request.POST.get('share_id')
        share = get_object_or_404(Share, id=share_id, shared_with_user=request.user)
        share.delete()
        messages.success(request, '共有されたアイテムが削除されました。')
        return redirect('sample:shared_items', favorite_id=favorite_id)
    
    # 現在のユーザーに共有されたアイテムのクエリセットを取得します。
    shared_with_me = Share.objects.filter(shared_with_user=request.user).select_related('item', 'owner_user')

    return render(request, 'sample/shared_items.html', {'shared_with_me': shared_with_me, 'favorite_id': favorite_id})


# 予算登録
@login_required
def budget_create(request):
    if request.method == 'POST':
        favorite_id = request.POST.get('favorite_id')
    else:
        favorite_id = request.GET.get('favorite_id')
    
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    
    today = timezone.now()
    budget = Budget.objects.filter(user=request.user, favorite=favorite, month__year=today.year, month__month=today.month).first()

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.favorite = favorite
            budget.save()
            return redirect('sample:item_list_with_favorite', favorite_id=favorite_id)
    else:
        if budget:
            initial_data = {'budget': int(budget.budget)}
            form = BudgetForm(instance=budget, initial=initial_data)
        else:
            form = BudgetForm(instance=budget)

    return render(request, 'sample/budget_create.html', {'form': form, 'favorite_id': favorite_id})
            


@login_required
def item_list_with_favorite(request, favorite_id):
    categories = Category.objects.all()  # 全てのカテゴリーを取得
    category_id = request.GET.get('category_id')  # URLからカテゴリーIDを取得
    
    # 特定のお気に入りに関連するアイテムのみを取得
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    items = favorite.items.filter(user=request.user, purchased=False)
        
    
    if category_id:
        items = items.filter(category_id=category_id)
        
        
    # ソート条件の取得と適用
    sort = request.GET.get('sort', '')
    if sort == 'release_date':
        items = items.order_by('release_date')
    elif sort == 'price_desc':
        items = items.order_by('-price')
    elif sort == 'price_asc':
        items = items.order_by('price')
        
        
    # アイテムの合計金額と予算の計算
    today = timezone.now()
    budget = Budget.objects.filter(user=request.user, favorite=favorite, month__year=today.year, month__month=today.month).first()
    # budget = Budget.objects.filter(user=request.user, month__year=today.year, month__month=today.month).first()
    total_amount = items.aggregate(Sum('price'))['price__sum'] or 0
    remaining_budget = budget.budget - total_amount if budget else 0
    
    
    context = {
        'items': items,
        'categories': categories,  # カテゴリー情報を追加
        'selected_category_id': category_id,  # テンプレートで選択されたカテゴリーIDを表示
        'total_amount': total_amount,
        'budget': budget,
        'remaining_budget': remaining_budget,
        'favorite_id': favorite_id,  # favorite_idをコンテキストに追加
        'sort': sort  # 現在のソート方法をコンテキストに追加
    }
    
    return render(request, 'sample/item_list.html', context)



#アイテム編集ページ
@login_required
def item_edit(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    favorite = item.favorite_set.first() if item.favorite_set.exists() else None
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            # 更新処理のログを追加して何が保存されているか確認
            updated_item = form.save()
            messages.success(request, f'"{updated_item.name}"が更新されました。カテゴリー: "{updated_item.category}"')
            if favorite:
                return redirect('sample:item_list_with_favorite', favorite_id=favorite.id)
        else:
            messages.error(request, 'フォームにエラーがあります。')
    else:
        form = ItemForm(instance=item)  # 既存のアイテムデータでフォームを初期化

    return render(request, 'sample/item_edit.html', {'form': form, 'item': item, 'favorite': favorite})



#アイテム削除ページ
@login_required
def item_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    favorite = item.favorite_set.first()  # 削除後のリダイレクト先のfavorite_idを取得
    item.delete()
    messages.success(request, 'アイテムが正常に削除されました。')
    return redirect('sample:item_list_with_favorite', favorite_id=favorite.id)


#アイテム購入済みページ
@login_required
def purchased_items(request):
    favorite_id = request.GET.get('favorite_id')
    
    if favorite_id and favorite_id.isdigit():
        favorite = get_object_or_404(Favorite, id=int(favorite_id), user=request.user)
        purchased_items = favorite.items.filter(user=request.user, purchased=True)
    else:
        purchased_items = Item.objects.filter(user=request.user, purchased=True)
        favorite_id = None  # favorite_idがNoneの場合の処理
    
    total_amount = purchased_items.aggregate(Sum('price'))['price__sum'] or 0  # 購入済みアイテムの合計金額を計算

    context = {
        'purchased_items': purchased_items,
        'total_amount': total_amount,  # 合計金額をテンプレートに渡す
        'favorite_id': favorite_id  # favorite_idをテンプレートに渡す
    }
    
    return render(request, 'sample/purchased_items.html', context)



@require_POST
@login_required
def mark_item_purchased(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    item.purchased = True
    item.save()
    
    # favorite_idを取得してリダイレクトに使用
    favorite_id = request.POST.get('favorite_id')
    if favorite_id:
        return redirect('sample:item_list_with_favorite', favorite_id=favorite_id)
    return redirect('sample:purchased_items')
    
    
    
    
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'sample/login.html'

    def get_success_url(self):
        return reverse_lazy('sample:home')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('sample:home')
    template_name = 'sample/signup.html'
    
    def form_valid(self, form):
        response = super(SignUpView, self).form_valid(form)
        login(self.request, self.object)  # 新規ユーザーをログインさせる
        return response
        
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('sample:login')  # ログアウト後にログインページへリダイレクト
    
    
    

User = get_user_model()

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            new_password = form.cleaned_data.get('new_password')

            user = get_object_or_404(User, email=email)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "パスワードが正常にリセットされました。")
            return HttpResponseRedirect(reverse_lazy('sample:login'))
    else:
        form = PasswordResetForm()

    return render(request, 'sample/password_reset.html', {'form': form})
