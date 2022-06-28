from django.shortcuts import render
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_image
from .models import Report
#from .forms import ReportForm
from django.views.generic import ListView, DetailView

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'


def create_report_view(request):
    #form = ReportForm(request.Post or None)
    if request.is_ajax():
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')

        image = request.POST.get('image')
        img = get_report_image(image)
        author =Profile.objects.get(user=request.user) 

        #if form.is_valid():
            #instance = form.save(commit=False)
            #instance.image = img
            #instance.author = author
            #instance.save()
        Report.objects.create(name=name, remarks=remarks, image=img, author=author)
        return JsonResponse({'msg': 'send'})
    return JsonResponse({})


def render_pdf_view(request):
    template_path = 'user_printer.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response