from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from sfb_shop import models as shop
import json
from django import forms

# template strings
cartTemplate = u'<tr> <td>{{parentName}}: {{name}}</td> <td>{{amount}}</td> <td class="right">{{price}} CHF</td> <tr>'
# Create your views here.


class NameForm(forms.Form):
    name = forms.CharField(label=u"Vorname, Nachname", max_length=256)
    street = forms.CharField(label=u'Strasse, Nummer', max_length=256)
    plz = forms.CharField(label=u'PLZ/Ort', max_length=256)
    email = forms.EmailField(label=u'E-Mail', max_length=512)
    comments = forms.CharField(label=u'Bemerkungen', max_length=512)


def get_form(request):
    form = NameForm()
    return render(request, 'form.html', {'form': form})


def index(request):
    return HttpResponse("Hello test, you are at the index.")


def addToCart(request):
    response = dict()
    if request.POST:
        post = request.POST
        session = request.session
        # print "request itemId", post.get('itemId', False)
        # print "request amount", post.get('amount', False)
        itemid = int(post.get('itemId', False))
        amount = int(post.get('amount', False))
        itemtype = post.get('type', False)
        item = None
        if itemid is not False and amount is not False and itemtype is not False:
            if itemtype == 'merch':
                item = shop.Merch.objects.get(pk=itemid)
            elif itemtype == 'card':
                item = shop.Card.objects.get(pk=itemid)

            if item is not None:  # we found a object
                response['price'] = float(item.price * amount)
                response['amount'] = amount
                if session.get(itemid, None) is not None:
                    session[itemid] = session.get(itemid) + amount
                else:
                    session[itemid] = amount
                response['template'] = cartTemplate
                return HttpResponse(json.dumps(response), mimetype='application/json')

    HttpResponseServerError("error")


def checkout(request):
    if request.POST:
        post = request.POST
        form = NameForm(request.POST)
        if form.is_valid():
            pass
    return HttpResponse('success')
