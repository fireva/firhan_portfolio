from django.shortcuts import render, get_object_or_404, redirect
from .models import PersonalInfo, Experience, SocialLink,Article
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from collections import defaultdict
from .forms import CommentForm  # Create this form
import time 
# Create your views here.
def about(request):
    # Fetch the data for the About Me page
    personal_info = PersonalInfo.objects.first()  # Assume one record for personal info
    experiences = Experience.objects.all()

    social_links = [
        {"platform": "Twitter", "url": "https://twitter.com/FirhanDragneel", "icon": "fab fa-twitter"},
        {"platform": "Facebook", "url": "https://facebook.com/firhan.huzaefa", "icon": "fab fa-facebook-f"},
        {"platform": "Instagram", "url": "https://instagram.com/firhanhz", "icon": "fab fa-instagram"},
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
        'form': form,
    })