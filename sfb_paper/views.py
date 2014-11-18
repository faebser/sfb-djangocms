from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from models import Issue
from os import path

# Create your views here.


def get_issue_from_id(request, issue_pk):
    return HttpResponse("Hello test, you sent me " + str(issue_pk))
    pass


def get_articles_from_tags(request, tags):
    tags = tags.split('/')
    return HttpResponse("Hello test, you sent me " + str(tags))


def get_issues_by_date(request, amount):
    issues = Issue.object().all()
    return render(request, path.join('plugins', 'paper', 'tag.html'), {
        'issues': issues
    })