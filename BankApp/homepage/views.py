from django.shortcuts import render,redirect
# Create your views here.
def Home(request):
    return render(request,'home.html')

def About(request):
    return render(request, 'about.html')

# login page 
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib import messages

def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # redirect to a home or dashboard view
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# signup
from .forms import SignupForm

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Log the user in after signup
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# logout
def Logout(request):
    logout(request)
    return redirect('home')

# create an account
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account
from .forms import AccountCreationForm

@login_required
def create_account(request):
    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            # Create a new account for the logged-in user
            account = form.save(commit=False)
            account.user = request.user  # Link the account to the logged-in user
            # Set the balance to the initial deposit entered by the user
            account.balance = form.cleaned_data['initial_deposit']
            account.save()

            # Success message
            messages.success(request, f"{account.get_account_type_display()} created successfully! Your account number is {account.account_number}. Initial deposit of ${account.balance} has been added.")
            return redirect("account_list")
    else:
        form = AccountCreationForm()
    return render(request, "create_account.html", {"form": form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def account_list(request):
    # Retrieve all accounts for the logged-in user
    accounts = request.user.accounts.all()
    return render(request, "account_list.html", {"accounts": accounts})



from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def balance(request,account_number):
    try:
        # Fetch the account linked to the logged-in user
        account = Account.objects.get(account_number=account_number, user=request.user)
    except Account.DoesNotExist:
        messages.error(request, "Account not found.")
        return redirect('account_list')
    return render(request, "balance.html", {'account': account})

@login_required
def deposit(request, account_number):
    
    try:
        # Fetch the account linked to the logged-in user
        account = Account.objects.get(account_number=account_number, user=request.user)
    except Account.DoesNotExist:
        messages.error(request, "Account not found.")
        return redirect('account_list')
    
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, transaction_type="deposit", amount=amount)
            messages.success(request, f"${amount} deposited successfully!")
            return redirect('balance',account_number=account.account_number)
    else:
        form = DepositForm()
    return render(request, "deposit.html", {"form": form})

@login_required
def withdraw(request, account_number):
    try:
        # Fetch the account linked to the logged-in user
        account = Account.objects.get(account_number=account_number, user=request.user)
    except Account.DoesNotExist:
        messages.error(request, "Account not found.")
        return redirect('account_list')
    
    if request.method == "POST":
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, transaction_type="withdraw", amount=amount)
                messages.success(request, f"${amount} withdrawn successfully!")
                return redirect('balance',account_number=account.account_number)
            else:
                messages.error(request, "Insufficient funds!")
    else:
        form = WithdrawForm()
    return render(request, "withdraw.html", {"form": form})


