from django.shortcuts import render

# Create your views here.
def home_view(request):
    hello = 'hello the truth seeker'
    return render(request, 'sales/home.html', {'hello': hello})