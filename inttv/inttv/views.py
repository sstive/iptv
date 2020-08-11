from django.shortcuts import render


def index(req):
    content = {
        'welcome': 'Hello, World!'
    }
    return render(req, 'index.html', content)
