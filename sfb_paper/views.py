from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from models import Issue, Article
from django.core import serializers
from os import path

# Create your views here.


def get_issue_from_id(request, issue_pk):
    issue = Issue.objects.get(pk=int(issue_pk))
    index = issue.article_set.all().order_by('page')
    return render(request, path.join('plugins', 'paper', 'issue_single.html'), {
        'issue': issue,
        'index': index
    })


def get_articles_from_tags(request, tags):
    tags = tags.split('/')
    qs = Article.objects
    for tag in tags:
        qs = qs.filter(tags__name__iexact=tag)
    return HttpResponse(serializers.serialize('json', qs, use_natural_keys=True), mimetype='application/json')
    #return render(request, path.join('plugins', 'paper', 'article.html'), {
    #   'articles': qs
    #})
    # return HttpResponse("Hello test, you sent me " + str(tags))


def get_issues_by_date(request, amount):
    issues = Issue.objects.all()
    return render(request, path.join('plugins', 'paper', 'tag.html'), {
        'issues': issues
    })