import decimal
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Account, Lender, Borrower, Tranfer
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import TransferForm, SignupForm, BorrowersForm, LenderForm
from django.contrib.auth.forms import User


def Home(request):
    return render(request, 'index.html', )

def about(request):
    return render(request, 'about.html', )


def dashboard(request):
    return render(request, 'dashboard.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {'error': 'Invalid login details'}
            return render(request, 'login2.html', context)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'login2.html')


def acceptAccount(request):
    form = TransferForm()
    if request.method == 'POST':
        form = TransferForm(request.POST)
        user = request.POST.get('user')
        username = request.user(user=user)
        amount = request.POST.get('amount')
        money = request.POST.get(amount=amount)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'accept.html', {'form':form})


def Logout(request):
    logout(request)
    return redirect('login')


class Signup(SuccessMessageMixin, generic.CreateView):
    form_class = SignupForm
    template_name = 'register2.html'

    def get_success_url(self):
        messages.success(self.request, 'Your account has being created successfully, Please login')
        return reverse('login')


class borrowers(ListView):
    model = Borrower
    template_name = 'borrowers.html'
    ordering = '-date_created'

    def get_queryset(self):
        return Borrower.objects.filter(Lender_approval=False).order_by('-date_created')


class LenderList(ListView):
    model = Lender
    template_name = 'lender.html'
    ordering = '-date_created'

    def get_queryset(self):
        return Lender.objects.filter(Borrower_approval=False).order_by('-date_created')


def transfer(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        amount = request.POST['amount']

        senderUser = User.objects.get(username=request.user)
        receiverUser = User.objects.get(username=username)

        sender = Account.objects.get(user=senderUser)
        reciever = Account.objects.get(user=receiverUser)

        if sender.balance < int(amount):
            msg = "Sorry, You don't have enough fund to perfrom this operation"
        else:
            sender.balance = sender.balance - int(amount)
            reciever.balance = reciever.balance + int(amount)
            sender.save()
            reciever.save()
            msg = "Transaction successful"
    return render(request, 'transfer.html', {'msg': msg})


def confirmation(request):
    return render(request, 'confrimation.html', )


class CreateBorrower(CreateView):
    model = Borrower
    template_name = 'create_borrow.html'
    form_class = BorrowersForm
    success_url = reverse_lazy('loan_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateBorrower, self).form_valid(form)


class CreateLender(CreateView):
    model = Lender
    template_name = 'create_lender.html'
    form_class = LenderForm
    success_url = reverse_lazy('lenders_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateLender, self).form_valid(form)


def LenderDetail(request, id=id):
    lenders = get_object_or_404(Lender, id=id)
    return render(request, 'lender-details.html', {'lenders':lenders})


class DeleteBorrowers(DeleteView):
    model = Borrower
    template_name = 'delete_borrower.html'


class DeleteLender(DeleteView):
    model = Lender
    template_name = 'delete_lender.html'
    success_url = reverse_lazy('lenders_list')

