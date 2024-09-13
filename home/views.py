from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse 
from home.models import Tweet
from home.forms import TweetForm,UserRegistraionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
# Create your views here.
def index(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request,"index.html",{"tweets":tweets})

@login_required
def user_home(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.filter(user=request.user)
    else:
        tweets = Tweet.objects.all()
    
    context = {
        'tweets': tweets
    }
    return render(request, 'user_home.html', context)

@login_required
def tweet_create(request):
    if request.method == "POST":
        form =TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("user_home")
    else:
        form = TweetForm()
    return render(request,"tweet_form.html",{"form":form})
@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user = request.user)
    if request.method == "POST":
        form = TweetForm(request.POST , request.FILES ,instance=tweet)
        form.save(commit=False)
        request.user = tweet.user
        form.save()
        return redirect("user_home")
    else:
        form = TweetForm(instance=tweet)
    return render(request,"tweet_form.html",{"form":form})

@login_required
def tweet_delete(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk =tweet_id , user = request.user)
    if request.method == "POST":
        tweet.delete()  
        return redirect("user_home")
    return render(request,"tweet_confirm_delete.html",{"tweet":tweet})
    return render(request,"tweet_confirm_delete.html",{"tweet":tweet})


def register(request):
    if request.method == "POST":
        form = UserRegistraionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('user_home')
    else:
        form = UserRegistraionForm()
    return render(request,"registration/register.html",{"form":form})

def search(request):
    query = request.GET.get('query', '')  # Get the search query from the URL
    if query:
        # Filter the results based on the query
        results = Tweet.objects.filter(
            Q(title__icontains=query) | Q(desc__icontains=query))  # Change 'field_name' to your model field
    else:
        results = Tweet.objects.none()  # Return an empty queryset if no query

    context = {
        'results': results,
        'query': query
    }
    return render(request, 'search_results.html', context)