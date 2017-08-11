from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm


User = get_user_model()


def home(request):
    return render(request, "home.html", {"form": ItemForm()})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, "list.html", {"list": list_, "form": form})


def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        email = request.POST.get("sharee", "")
        try:
            sharee = User.objects.get(email=email)
        except User.DoesNotExist:
            sharee = User.objects.create(email=email)
        list_.shared_with.add(sharee)
        return redirect(list_)
    return render(request, "list.html", {"list": list_, "form": form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, "my_lists.html", {"owner": owner})
