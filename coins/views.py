from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from coins.models import Exchange, Coin, ExceptionRule
from scraper.mongo import MongoOperator
from scraper.scraper import Scraper


def dashboard(request):
    return render(request, 'dashboard.html', context={
        'exchanges': Exchange.objects.all(),
        'coins': Coin.objects.all(),
        'trades': MongoOperator().get_latest_record()['record']['trades'][:5]
    })


def issues(request):
    return render(request, 'issues.html', context={
        'issues': MongoOperator().get_latest_record()['record']['issues']
    })


def rules(request):
    return render(request, 'rules.html', context={
        'rules': ExceptionRule.objects.all()
    })


@require_http_methods(["GET", "POST"])
def add_exchange(request):
    if request.method == "GET":
        return render(request, 'add_exchange.html', context={"placeholder": Scraper.COIN_PLACEHOLDER})
    elif request.method == "POST":
        e = Exchange.objects.create(
            name=request.POST['name'],
            website=request.POST['website'],
            markets_page=request.POST['markets_page'],
            base_xpath=request.POST['xpath'],
            wait_xpath=request.POST['wait_xpath']
        )
        messages.success(request, f"Exchange \"{e.name}\" successfully added")
        return redirect(reverse('dashboard'))


@require_http_methods(["GET", "POST"])
def add_coin(request):
    if request.method == "GET":
        return render(request, 'add_coin.html')
    elif request.method == "POST":
        c = Coin.objects.create(
            name=request.POST['name'],
            shorthand=request.POST['shorthand']
        )
        messages.success(request, f"Coin \"{c.name}\" successfully added")
        return redirect(reverse('dashboard'))


@require_http_methods(["GET"])
def add_rule_form(request, coin, exchange):
    return render(request, 'add_rule.html', context={
        'coin': coin,
        'exchange': exchange
    })


@require_http_methods(["POST"])
def add_rule_submit(request):
    coin = Coin.objects.get(shorthand=request.POST['shorthand'])
    exchange = Exchange.objects.get(name=request.POST['exchange'])
    kind = request.POST['kind']
    value = "default"
    if kind in {'NTD', 'DCS'}:
        value = request.POST['value']
    # replace old value if exists
    ExceptionRule.objects.filter(forCoin=coin, forExchange=exchange, kind=kind).delete()
    rule = ExceptionRule.objects.create(
        forCoin=coin,
        forExchange=exchange,
        kind=kind,
        value=value
    )
    messages.success(request,
                     f"Rule for coin \"{rule.forCoin.shorthand}\""
                     f" and exchange \"{rule.forExchange.name}\""
                     f" successfully added")
    return redirect(reverse('dashboard'))


def view_logs(request):
    return render(request, 'logs.html', context={
        'logs': MongoOperator().get_latest_record()['record']['logs'].split("\n")
    })
