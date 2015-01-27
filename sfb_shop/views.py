from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from sfb_shop import models as shop
import json
from django import forms
from models import Card, Merch
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.utils.html import strip_tags
from decimal import *

# template strings
cartTemplate = u'<tr> <td>{{parentName}}: {{name}}</td> <td>{{amount}}</td> <td class="right">{{price}} CHF</td> <tr>'
# Create your views here.


class NameForm(forms.Form):
    name = forms.CharField(label=u"Vorname, Nachname", max_length=256)
    street = forms.CharField(label=u'Strasse, Nummer', max_length=256)
    plz = forms.CharField(label=u'PLZ/Ort', max_length=256)
    email = forms.EmailField(label=u'E-Mail', max_length=512)
    comments = forms.CharField(label=u'Bemerkungen', max_length=512, required=False)


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
                return HttpResponse(json.dumps(response), content_type='application/json')

    HttpResponseServerError("error")


def checkout(request):
    from django.core.mail import send_mail
    if request.POST:
        post = request.POST
        form = NameForm(post)
        articles_list = list()
        grand_total = Decimal(0.00)
        if form.is_valid():
            # build email template
            # send two emails
            # one to customer and one to sfb
            # name, street, plz, email, comments
            data = form.cleaned_data
            merch = json.loads(post['cart'])
            for key in merch.iterkeys():
                buyable = None
                try:
                    buyable = Card.objects.get(pk=key)
                except ObjectDoesNotExist:
                    buyable = Merch.objects.get(pk=key)
                if buyable is not None:
                    amount = merch[key]['amount']
                    price = buyable.price.items.filter(amount__gte=amount).order_by('amount')[0].price
                    articles_list.append({
                        'name': buyable.name,
                        'desc': strip_tags(buyable.description),
                        'amount': amount,
                        'price': price,
                        'total': price * amount
                    })
                    grand_total += price * amount
                else:
                    # generate error mail to sfb
                    return HttpResponseServerError(json.dumps({'status': 'item not found', 'id': key}), content_type='application/json')
                
            context = {'articles': articles_list, 'total': grand_total, 'data': data}
            print context
            send_mail('Bestellung Webshop', loader.render_to_string('mails/customer-confirmation', context), 'marktplatz@friedensbewegung.ch', [data.email], fail_silently=False)
            send_mail('Bestellung Webshop', loader.render_to_string('mails/sfb-confirmation', context), 'webshop@friedensbewegung.ch', ['sfb@bluewin.ch'], fail_silently=False)
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return render(request, 'form.html', {'form': form})
    return HttpResponse('success')