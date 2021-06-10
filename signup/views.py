from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib import auth
from .forms import *
from .models import *
import datetime
# Create your views here.


def signup(request):
    """
    signup user
    input: user_type,user_name,password,phone number
    """
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                if user:
                    return render(request, 'accounts/signup.html')
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'],
                    first_name=request.POST['name'])
                auth.login(request, user)
                return redirect('list')
        else:
            return render(request, 'accounts/signup.html')
    return render(request, 'accounts/signup.html')

def logout(request):
    """
    logout user
    """
    if request.method == "POST":
        auth.logout(request)
        return render(request, 'login.html')
    auth.logout(request)
    return render(request, 'login.html')



class Home(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["destinations"] = Destinations.objects.all()
        if self.request.user.is_authenticated:
            context['repliesc'] = Reply.objects.filter(message__user = self.request.user, read=False).count()
        return context
    
class DestinationView(DetailView):
    model = Destinations
    template_name="about.html"
    form_class=TourForm

    def get_context_data(self, **kwargs):
        context = super(DestinationView, self).get_context_data(**kwargs)
        context['form'] = TourForm()
        return context
    def post(self, request, *args, **kwargs):
        print(kwargs['pk'])
        Tour.objects.create(destination = Destinations.objects.get(pk = kwargs['pk']),user = request.user,datefrom = request.POST["datefrom"],dateto = request.POST["dateto"],people = request.POST["people"])
        return redirect('destination', pk=kwargs['pk'])

class Contactcreate(CreateView):
    form_class= ContactForm
    success_url = reverse_lazy('list')
    template_name = 'contact.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class TourDeleteView(DeleteView):
    template_name = 'delete.html'
    success_url = reverse_lazy('tour')
    queryset = Tour.objects.all()

class AdminView(LoginRequiredMixin, TemplateView):
    template_name="admin/index.html"
    def get(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect('list')
        return super().get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdminView, self).get_context_data(**kwargs)
        temp = Tour.objects.filter(datefrom__year=datetime.date.today().year)
        val = list()
        for i in range(1,13):
            val.append(temp.filter(datefrom__month=i).aggregate(Sum('people'))['people__sum'] if temp.filter(datefrom__month=i).aggregate(Sum('people'))['people__sum'] is not None else 0)   
        t = Tour.objects.filter(datefrom=datetime.date.today())
        t2 = Tour.objects.filter(dateto=datetime.date.today())
        li = [t.filter(arriving=False).aggregate(Sum('people'))['people__sum'], t.filter(arriving=True).aggregate(Sum('people'))['people__sum'], t2.filter(leaving=False).aggregate(Sum('people'))['people__sum'], t2.filter(leaving=True).aggregate(Sum('people'))['people__sum']]
        for i in range(0,4):
            if li[i] == None:
                li[i]=0
        context['piedata'] = li
        context['data'] = val
        context['messages'] = Contact.objects.filter(read=False)
        context['messagescount'] = Contact.objects.all().count()
        context['tour'] = Tour.objects.filter(read=False)
        context['arrivingcount'] = Tour.objects.filter(datefrom=datetime.date.today()).aggregate(Sum('people'))['people__sum'] if Tour.objects.filter(datefrom=datetime.date.today()).aggregate(Sum('people'))['people__sum'] is not None else 0
        context['leavingcount'] = Tour.objects.filter(dateto=datetime.date.today()).aggregate(Sum('people'))['people__sum'] if Tour.objects.filter(dateto=datetime.date.today()).aggregate(Sum('people'))['people__sum'] is not None else 0
        return context
    # def get(self, *args, **kwargs):
    #     if 'val' in self.request.GET:
            
    #     return super().get(self,*args,**kwargs)


class TourView(LoginRequiredMixin, ListView):
    model = Tour
    template_name="admin/tables.html"
    def get_queryset(self, *args, **kwargs):
        qs = super(TourView, self).get_queryset(*args, **kwargs)
        if 'Approve' in self.request.GET:
            return qs.filter(approve=True)
        elif 'Rejected' in self.request.GET: 
            return qs.filter(approve=False)
        elif 'Today' in self.request.GET:
            return qs.filter(approve=True, datefrom = datetime.date.today())
        elif 'Todayleaving' in self.request.GET:
            return qs.filter(approve=True, dateto = datetime.date.today())
        else:
            return qs.filter(approve=None)
        
    
    def get_context_data(self, **kwargs):
        context = super(TourView, self).get_context_data(**kwargs)
        context['tp'] = True
        t = Tour.objects.all()
        t.update(read=True)
        context['messages'] = Contact.objects.filter(read=False)
        return context



class ContactView(LoginRequiredMixin, ListView):
    model = Contact
    template_name="admin/contacttable.html"
    def get(self, *args, **kwargs):
        t = Contact.objects.all()
        t.update(read=True)
        return super().get(self, *args, **kwargs)


def Approve(request, id):
    t = Tour.objects.get(pk=id)
    t.approve=True
    t.save()
    return redirect('tour')

def Reject(request, id):
    t = Tour.objects.get(pk=id)
    print(t.approve)
    t.approve=False
    t.save()
    return redirect('tour')
def Arrived(request, id):
    t = Tour.objects.get(pk=id)
    print(t.approve)
    t.arriving=True
    t.save()
    return redirect('tour')
def Left(request, id):
    t = Tour.objects.get(pk=id)
    print(t.approve)
    t.leaving=True
    t.save()
    return redirect('tour')

def Replyc(request):
    print(request.POST)
    Reply.objects.create(message = Contact.objects.get(pk=request.POST['msgid']), reply = request.POST['message'])
    return redirect('contact')

def inbox(request):
    replies = Reply.objects.filter(message__user = request.user)
    print(request.user)
    tours = Tour.objects.filter(user = request.user)
    print(tours)
    return render(request, 'inbox.html', {'replies' : replies, 'tours': tours})