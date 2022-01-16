from django.shortcuts import render


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')


def add_exchange(request):
    return render(request, 'add_exchange.html')


def add_coin(request):
    return render(request, 'add_coin.html')


def issues(request):
    return render(request, 'issues.html')


def rules(request):
    return render(request, 'rules.html')


def add_rule(request):
    return render(request, 'add_rule.html')