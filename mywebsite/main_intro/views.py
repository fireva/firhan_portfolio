from django.shortcuts import render, get_object_or_404, redirect
from .models import PersonalInfo, Experience, SocialLink,Article
from django.http import HttpResponseRedirect,JsonResponse
from django.core.paginator import Paginator
from collections import defaultdict
from .forms import CommentForm  # Create this form
import time 
import json
# Create your views here.
def about(request):
    # Fetch the data for the About Me page
    personal_info = PersonalInfo.objects.first()  # Assume one record for personal info
    experiences = Experience.objects.all()

    social_links = [
        {"platform": "Facebook", "url": "https://facebook.com/firhan.huzaefa", "icon": "fab fa-facebook-f"},
        {"platform": "Instagram", "url": "https://instagram.com/firhanhz", "icon": "fab fa-instagram"},
        {"platform": "Twitter", "url": "https://twitter.com/FirhanDragneel", "icon": "fab fa-twitter"},
        {"platform": "LinkedIn", "url": "https://linkedin.com/in/firhan-huzaefa-985462147", "icon": "fab fa-linkedin-in"},
    ]
    # Pass the data to the template
    return render(request, 'main_intro/about.html', {
        'personal_info': personal_info,
        'experiences': experiences,
        'social_links': social_links,
    })
    
def home(request):
    return HttpResponseRedirect('/about/')  # Redirect to About Me page

def article_list(request):
    articles = Article.objects.all().order_by('-date_created')
    paginator = Paginator(articles, 10)  # Show 10 articles per page
    page_number = request.GET.get('page')
    page_articles = paginator.get_page(page_number)

    articles_by_month = defaultdict(list)
    for article in articles:
        month = article.date_created.strftime('%B %Y')
        articles_by_month[month].append(article)
    articles_by_month = dict(articles_by_month)
    #time.sleep(5)
    return render(request, 'main_intro/article_list.html', {
        'articles': page_articles,
        'articles_by_month': articles_by_month,
    })

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    # Prepare articles grouped by month
    articles = Article.objects.all().order_by('-date_created')
    articles_by_month = defaultdict(list)
    for art in articles:
        month = art.date_created.strftime('%B %Y')
        articles_by_month[month].append(art)
    articles_by_month = dict(articles_by_month)
    like_dislike_diff = article.likes - article.dislikes
    # Handle comment submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = CommentForm()

    return render(request, 'main_intro/article_detail.html', {
        'article': article,
        'articles_by_month': articles_by_month,
        'like_dislike_diff':like_dislike_diff,
        'form': form,
    })
    

def update_likes_dislikes(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    data = json.loads(request.body)
    action = data.get('action')
    is_toggling_off = data.get('isTogglingOff', False)
    previous_action = data.get('previousAction')

    if is_toggling_off:
        # If toggling off, invalidate the previous action
        if previous_action == 'like':
            article.likes -= 1
        elif previous_action == 'dislike':
            article.dislikes -= 1
    else:
        # Apply the new action and invalidate the previous one if needed
        if action == 'like':
            article.likes += 1
            if previous_action == 'dislike':
                article.dislikes -= 1
        elif action == 'dislike':
            article.dislikes += 1
            if previous_action == 'like':
                article.likes -= 1

    article.save()
    return JsonResponse({'likes': article.likes, 'dislikes': article.dislikes})