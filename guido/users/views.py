
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Max, Min, Avg, Sum, Count
from myapp.views import banner
from myapp.decorator import owner_required, guide_required, customer_required
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse

# Create your views here.

def login_view(request):
    bycity = banner()[0]
    all_cats = banner()[1]
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('myapp:home')  # Replace 'home' with the URL name of your desired homepage
                else:
                    form.add_error(None, 'Invalid email or password.')
        else:
            form = LoginForm()
        return render(request, 'users/login.html', {'form': form, 'bycity':bycity,'all_cats':all_cats})
    return redirect('myapp:home')


def logout_view(request):
    logout(request)
    return redirect('myapp:home')  # Replace 'home' with the URL name of your desired homepage



from .forms import OwnerRegistrationForm

def register_owner(request):
    bycity = banner()[0]
    all_cats = banner()[1]
    if request.method == 'POST':
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['buzzer'] == "owner":
                user.is_owner = True
            elif form.cleaned_data['buzzer'] == "customer":
                user.is_customer = True
            elif form.cleaned_data['buzzer'] == "guide":
                user.is_guid = True
            else:
                messages.warning(request, _("please select account type"))
                return redirect("users:register_owner")
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request, _("Account created successfully"))
            return redirect('myapp:home')  # Redirect to the desired page after registration
    else:
        form = OwnerRegistrationForm()
    return render(request, 'users/register.html', {'form': form,'bycity':bycity,'all_cats':all_cats})

from myapp.models import Listing, Messages

@owner_required
def owner_dash(request):
    bycity = banner()[0]
    all_cats = banner()[1]
    user = request.user
    listing = Listing.objects.filter(author=user)
    l_en = len(listing)
    context = {
        'listing_len':l_en,
        'owner_dash':True,
         'bycity':bycity,
        'all_cats':all_cats,'contact_info':banner()[2],
    }
    return render(request, 'users/owner/owner_dash.html', context)

from myapp.forms import GuidesForm
from myapp.models import Guides
@guide_required
def guide_dash(request):
    bycity = banner()[0]
    all_cats = banner()[1]
    user = get_object_or_404(MyUser, id=request.user.id)
    guidemsg_len = len(Message_Guide.objects.filter(guide_info__author=user))
    obj = Guides.objects.filter(author=user).first()
    if request.method == 'POST':
            form = GuidesForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                q_form = form.save(commit=False)
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                if email:
                    q_form.email = email
                if phone:
                    q_form.phone = phone
                q_form.author = user
                user.name = form.cleaned_data['name']
                user.save()
                q_form.save()
                messages.success(request, _("Infos Updated successfully"))
                return redirect('users:guide_dash')  # Replace 'listing_success' with your desired success URL
    else:
        form = GuidesForm(instance=obj)
    context = {
        'guide_dash':True,
         'bycity':bycity,
         'guidemsg_len':guidemsg_len,
        'all_cats':all_cats,'contact_info':banner()[2],
        'form':form,
    }
    return render(request, 'users/guide/guide_dash.html', context)

@guide_required
def guide_msgs(request, id=None):
    bycity = banner()[0]
    all_cats = banner()[1]
    user = get_object_or_404(MyUser, id=request.user.id)
    guidemsg = Message_Guide.objects.filter(guide_info__author=user)
    guidemsg_byg = guidemsg.values('customer__name', 'guide_info__id').annotate(tot=Count('id'))
    form=None
    msg_len = len(guidemsg)
    msg_details = None
    if guidemsg.exists():
        msg_details = guidemsg.filter(id=guidemsg.last().id)
    if id and guidemsg.filter(guide_info__id=id).exists():
        msg_details = guidemsg.filter(guide_info__id=id)
        msg_details.update(viewed=True)
    
    if request.method  == 'POST':
        msgi = request.POST.get('msgi')
        n = Message_Guide.objects.create(
                    customer=msg_details.first().customer,
                    message=msgi,
                    sentby='guide',
                    guide_info=msg_details.first().guide_info,
                    o_receiver=None,
                )
        if n.guide_info:
            n_id = n.guide_info.id
        return redirect('users:guide_msg_details', n_id)
     
    context = {
        'guide_msgs':True,
         'guidemsg':guidemsg,'guidemsg_byg':guidemsg_byg,
         'msg_details':msg_details,
        'all_cats':all_cats,'contact_info':banner()[2],
        'form':form,
        'msg_len':msg_len,
    }
    return render(request, 'users/guide/msgs.html', context)

@owner_required
def owner_msgs(request, id=None):
    bycity = banner()[0]
    all_cats = banner()[1]
    user = get_object_or_404(MyUser, id=request.user.id)
    guidemsg = Message_Guide.objects.filter(o_receiver__author=user)
    guidemsg_byg = guidemsg.values('o_receiver__name','customer__name','customer__id','o_receiver_id').annotate(tot=Count('id'))
    form=None
    msg_len = len(guidemsg)
    msg_details = None
    if guidemsg.exists():
        msg_details = guidemsg.filter(id=guidemsg.last().id)
    if id and guidemsg.filter(customer__id=id).exists():
        msg_details = guidemsg.filter(customer__id=id)
        msg_details.update(viewed=True)
    
    if request.method  == 'POST':
        msgi = request.POST.get('msgi')
        n = Message_Guide.objects.create(
                    customer=msg_details.first().customer,
                    message=msgi,
                    sentby='owner',
                    guide_info=None,
                    o_receiver=msg_details.first().o_receiver,
                )
        if n.o_receiver:
            n_id = n.customer.id
        return redirect('users:owner_msgs_details', n_id)
     
    context = {
        'guide_msgs':True,
         'guidemsg':guidemsg,'guidemsg_byg':guidemsg_byg,
         'msg_details':msg_details,
        'all_cats':all_cats,'contact_info':banner()[2],
        'form':form,
        'msg_len':msg_len,
        'bycity':bycity,
    }
    return render(request, 'users/owner/o_msgs.html', context)



from .models import Profile, MyUser
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import EmailChangeForm, ProfileUpdateForm, NameForm

@owner_required
def owner_profile(request):
    bycity = banner()[0]
    all_cats = banner()[1]
    user = get_object_or_404(MyUser, id=request.user.id)
    if request.method == 'POST':
        form_pass = PasswordChangeForm(request.user, request.POST)
        form_email = EmailChangeForm(request.POST)
        form_name = NameForm(request.POST)
        if request.FILES:
            p_form = ProfileUpdateForm(request.POST,
                                       request.FILES,
                                       instance=request.user.profile,
                                       )
            if p_form.is_valid():
                p_form.save()
                messages.success(request, _('Profile image has been updated!'))
                return redirect('users:owner_profile')
        try:
            if request.POST['old_password']:
                if form_pass.is_valid():
                    user = form_pass.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, _('Your password updated successfuly'))
                    return redirect('users:owner_profile')
                else:
                    messages.error(request, _('Please correct the error below'))
        except:
            pass
        
        try:
            if request.POST['email1']:
                if form_email.is_valid():
                    user.email = form_email.cleaned_data['email2']
                    user.save()
                    messages.success(request, _('Your Email updated successfuly'))
                    return redirect('users:owner_profile')
                else:
                    messages.error(request, _('Please correct the error below'))
        except:
            pass
        
        try:
            if request.POST['name']:
                if form_name.is_valid():
                    user.name = form_name.cleaned_data['name']
                    user.phone = form_name.cleaned_data['phone']
                    user.save()
                    messages.success(request, _('Info updated successfuly'))
                    return redirect('users:owner_profile')
                else:
                    messages.error(request, _('Please correct the error below'))
        except:
            pass
        
        
    else:
        form_pass = PasswordChangeForm(request.user)
        form_email = EmailChangeForm()
        p_form = ProfileUpdateForm()
        form_name = NameForm()
    context = {
        'form_pass':form_pass,
        'form_name':form_name,
        'form_email':form_email,
         'bycity':bycity,
        'all_cats':all_cats,'contact_info':banner()[2],
    }
    return render(request, 'users/owner/profile.html', context)

from myapp.models import Messages, Message_Guide
@customer_required
def customer_dash(request, id=None):
    bycity = banner()[0]
    all_cats = banner()[1]
    user = get_object_or_404(MyUser, id=request.user.id)
    guidemsg = Message_Guide.objects.filter(customer=user)
    guidemsg_byg = guidemsg.values('guide_info__name','guide_info__id','o_receiver__id', 'o_receiver__name','o_receiver__author__name').annotate(tot=Count('id'))
    form=None
    msg_len = len(guidemsg)
    msg_details = None
    if guidemsg.exists():
        msg_details = guidemsg.filter(id=guidemsg.last().id)
    if id and guidemsg.filter(guide_info__id=id).exists():
        msg_details = guidemsg.filter(guide_info__id=id)
        msg_details.update(viewed=True)
    if id and guidemsg.filter(o_receiver__id=id).exists():
        msg_details = guidemsg.filter(o_receiver__id=id)
        msg_details.update(viewed=True)
    
    if request.method  == 'POST':
        msgi = request.POST.get('msgi')
        n = Message_Guide.objects.create(
                    customer=user,
                    message=msgi,
                    sentby='customer',
                    guide_info=msg_details.first().guide_info,
                    o_receiver=msg_details.first().o_receiver,
                )
        if n.guide_info:
            n_id = n.guide_info.id
        if n.o_receiver:
            n_id = n.o_receiver.id
        return redirect('users:msg_details', n_id)
     
    context = {
        'guide_dash':True,
         'guidemsg':guidemsg,'guidemsg_byg':guidemsg_byg,
         'msg_details':msg_details,
        'all_cats':all_cats,'contact_info':banner()[2],
        'bycity':bycity,
        'form':form,
        'msg_len':msg_len,
    }
    return render(request, 'users/customer/dash.html', context)


@guide_required
def guide_profile(request):
    bycity = banner()[0]
    all_cats = banner()[1]
    user = get_object_or_404(MyUser, id=request.user.id)
    if request.method == 'POST':
        form_pass = PasswordChangeForm(request.user, request.POST)
        form_email = EmailChangeForm(request.POST)
        form_name = NameForm(request.POST)

        if request.FILES:
            p_form = ProfileUpdateForm(request.POST,
                                       request.FILES,
                                       instance=request.user.profile,
                                       )
            if p_form.is_valid():
                p_form.save()
                messages.success(request, _('Profile image has been updated!'))
                return redirect('users:owner_profile')

        try:
            if request.POST['old_password']:
                if form_pass.is_valid():
                    user = form_pass.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, _('Your password updated successfuly'))
                    return redirect('users:guide_profile')
                else:
                    messages.error(request, _('Please correct the error below'))
        except:
            pass
        
        try:
            if request.POST['email1']:
                if form_email.is_valid():
                    user.email = form_email.cleaned_data['email2']
                    user.save()
                    messages.success(request, _('Your Email updated successfuly'))
                    return redirect('users:guide_profile')
                else:
                    messages.error(request, _('Please correct the error below'))
        except:
            pass
        
        try:
            if request.POST['name']:
                if form_name.is_valid():
                    user.name = form_name.cleaned_data['name']
                    user.phone = form_name.cleaned_data['phone']
                    user.save()
                    messages.success(request, _('Info updated successfuly'))
                    return redirect('users:guide_profile')
                else:
                    messages.error(request, _('Please correct the error below'))
        except:
            pass
    else:
        form_pass = PasswordChangeForm(request.user)
        form_email = EmailChangeForm()
        p_form = ProfileUpdateForm()
        form_name = NameForm()
    context = {
        'form_pass':form_pass,
        'form_name':form_name,
        'form_email':form_email,
         'bycity':bycity,
        'all_cats':all_cats,'contact_info':banner()[2],
    }
    return render(request, 'users/guide/g_profile.html', context)

@customer_required
def customer_profile(request):
    bycity = banner()[0]
    all_cats = banner()[1]
    user = get_object_or_404(MyUser, id=request.user.id)
    if request.method == 'POST':
        form_pass = PasswordChangeForm(request.user, request.POST)
        form_email = EmailChangeForm(request.POST)
        form_name = NameForm(request.POST)
        if request.FILES:
            p_form = ProfileUpdateForm(request.POST,
                                       request.FILES,
                                       instance=request.user.profile,
                                       )
            if p_form.is_valid():
                p_form.save()
                messages.success(request, _('Profile image has been updated!'))
                return redirect('users:owner_profile')
        try:
            if request.POST['old_password']:
                if form_pass.is_valid():
                    user = form_pass.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, _('Your password updated successfuly'))
                    return redirect('users:customer_profile')
                else:
                    messages.error(request, _('Please correct the error below'))
        except:
            pass
        
        try:
            if request.POST['email1']:
                if form_email.is_valid():
                    user.email = form_email.cleaned_data['email2']
                    user.save()
                    messages.success(request, _('Your Email updated successfuly'))
                    return redirect('users:owner_profile')
                else:
                    messages.error(request, _('Please correct the error below'))
        except:
            pass
        
        try:
            if request.POST['name']:
                if form_name.is_valid():
                    user.name = form_name.cleaned_data['name']
                    user.phone = form_name.cleaned_data['phone']
                    user.save()
                    messages.success(request, _('Info updated successfuly'))
                    return redirect('users:customer_profile')
                else:
                    messages.error(request, _('Please correct the error below'))
        except:
            pass
    else:
        form_pass = PasswordChangeForm(request.user)
        form_email = EmailChangeForm()
        p_form = ProfileUpdateForm()
        form_name = NameForm()
    context = {
        'form_pass':form_pass,
        'form_name':form_name,
        'form_email':form_email,
         'bycity':bycity,
        'all_cats':all_cats,'contact_info':banner()[2],
    }
    return render(request, 'users/customer/c_profile.html', context)
