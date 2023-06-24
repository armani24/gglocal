from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from users.models import MyUser
from .models import City, ListingCategory, Listing, Review, Messages
from .decorator import owner_required
from django.core.paginator import Paginator
from django.db.models import Max, Min, Avg, Sum, Count
from mina.models import HomeSlider, HomeListing, AboutUS, ContactUs_info

# Create your views here.
def banner():
    contact_info = ContactUs_info.objects.last()

    categories = ListingCategory.objects.all()[:6]
    cities = City.objects.all()[:6]
    listing_bycity = Listing.objects.values('city__name', 'city__city_img').annotate(list_city=Count('id'))
    return [listing_bycity, categories, contact_info]


def home(request):
    bycity = banner()[0]
    all_cats = banner()[1]
    homeslide = HomeSlider.objects.filter(active=True).first().image1.url
    cities = City.objects.all()
    categories =  ListingCategory.objects.all()[:6]
    homelisting = HomeListing.objects.filter(active=True)
    cat = request.GET.get('categories')
    cit = request.GET.get('cities')
    if cat and cit:
        if cat == 'Guides':
            return redirect('myapp:guides_list_city', cit)
        return redirect('myapp:listing_list_filter', cat, cit)
    else:
        pass
    city = {
        'name':'amine',
        'frak':'liko',
    }
    context = {
        'homeslide':homeslide,'homelisting':homelisting,
        'bycity':bycity,'city':cities,
        'all_cats':all_cats,'contact_info':banner()[2],'categories':categories,
    }
    # messages.success(request, _("welcome home"))

    return render(request, 'myapp/home.html', context)


from .forms import ListingForm, Filt_Form, ReviewForm, MessageForm, EditListingForm

def create_listing(request):
    user = get_object_or_404(MyUser, id=request.user.id)
    bycity = banner()[0]
    all_cats = banner()[1]
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        
        if form.is_valid():
            q_form = form.save(commit=False)
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            if email:
                q_form.email = email
            if phone:
                q_form.phone = phone
            q_form.author = user
            
            q_form.save()
            messages.success(request, _("Listing created successfully"))
            return redirect('myapp:home')  # Replace 'listing_success' with your desired success URL
    else:
        form = ListingForm()
    
    return render(request, 'myapp/create_listing.html', {'form': form,'bycity':bycity,
        'all_cats':all_cats,'contact_info':banner()[2],})

def edit_listing(request, id):
    user = get_object_or_404(MyUser, id=request.user.id)
    listing = Listing.objects.filter(author=user).filter(id=id)
    obj = listing.first()
    bycity = banner()[0]
    all_cats = banner()[1]
    if listing.exists():
        if request.method == 'POST':
            form = EditListingForm(request.POST, request.FILES, instance=obj)
            
            if form.is_valid():
                q_form = form.save(commit=False)
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                if email:
                    q_form.email = email
                if phone:
                    q_form.phone = phone
                q_form.author = user
                
                q_form.save()
                messages.success(request, _("Listing Edited successfully"))
                return redirect('myapp:listing_details',id)  # Replace 'listing_success' with your desired success URL
        else:
            form = EditListingForm(instance=obj)
    else:
        return redirect('users:owner_dash')
    
    return render(request, 'myapp/edit_listing.html', {'form': form, 'image1_url':obj.image1.url,
                    'image2_url':obj.image2.url,'image3_url':obj.image3.url,'image4_url':obj.image4.url,
                    'bycity':bycity,
        'all_cats':all_cats,'contact_info':banner()[2],
    })


def listing_list(request, categ=None, city=None):
    categories = ListingCategory.objects.exclude(name='Guides')
    cities = City.objects.all()
    listing = Listing.objects.exclude(category__name="Guides")
    bycity = banner()[0]
    all_cats = banner()[1]
    cat = request.GET.get('category')
    cit = request.GET.get('city')
    if cat and cit:
        listing = listing.filter(category__id=cat).filter(city__id=cit)
    if city and city != 'None':
        listing = listing.filter(city__name=city)
    if categ:
        listing = listing.filter(category__name=categ)
    else:
        pass
    context = {
        'listing':listing,
        'categories':categories,
        'cities':cities,
        'city_value':cit,
        'cat_value':cat,
        'bycity':bycity,
        'all_cats':all_cats,'contact_info':banner()[2],
    }
    
    return render(request, "myapp/listing.html", context)
    

from .models import GuidesReview
from .forms import GuidesReviewForm, MsgGuideForm    
        
def listing_details(request, id):
    bycity = banner()[0]
    all_cats = banner()[1]
    listing = Listing.objects.exclude(category__name="Guides").filter(id=id).first()
    if request.user.is_authenticated:    
        if request.method == 'POST' and request.user.is_customer:
            form = ReviewForm(request.POST)
            msg_form = MsgGuideForm(request.POST)
            try:
                if request.POST['content']:

                    if form.is_valid():
                        rating = form.cleaned_data['rating']
                        content = form.cleaned_data['content']
                        review = Review(listing=listing, customer=request.user, rating=rating, content=content)
                        review.save()
                        messages.success(request, _("Review added!"))
                        return redirect('myapp:listing_details', id)
            except:
                pass

            try:
                if request.POST['message']:
                    if msg_form.is_valid():
                        p_form = msg_form.save(commit=False)
                        p_form.customer = request.user
                        p_form.o_receiver = listing
                        sentby = 'owner'
                        msg_form.save()
                        messages.success(request, _("Message sent!")) 
                        return redirect('myapp:listing_details', id)
            except:
                pass
        else:
            form = ReviewForm()
            msg_form = MsgGuideForm()
    else:
         form = ReviewForm()
         messages.warning(request, _("please login or create custome account!"))
    
    context = {
        'listing':listing,
        'form':form,'image1':listing.image1.url,
        'bycity':bycity,
        'all_cats':all_cats,'contact_info':banner()[2],
    }
     
    return render(request, "myapp/listing_details.html", context)


@owner_required
def my_listings(request):
    bycity = banner()[0]
    all_cats = banner()[1]
    user = get_object_or_404(MyUser, id=request.user.id)
    my_listing = Listing.objects.exclude(category__name="Guides").filter(author=user)

    paginator = Paginator(my_listing, 5)
    page = request.GET.get('page')
    my_listing = paginator.get_page(page)

    context = {
        'my_listing':my_listing,
        'my_listings':True,
        'bycity':bycity,
        'all_cats':all_cats,'contact_info':banner()[2],        
    }
    return render(request, 'users/owner/my_listings.html', context)

@owner_required
def delete_listing(request, id):
    user = get_object_or_404(MyUser, id=request.user.id)
    my_listing = Listing.objects.exclude(category__name="Guides").filter(author=user).filter(id=id)
    if my_listing.exists():
        my_listing.delete()
        messages.success(request, _("Listing deleted!"))
        return redirect('myapp:my_listings')
    return redirect('myapp:my_listings')
    
from .models import Guides

def guides_list(request, city=None):
    bycity = banner()[0]
    all_cats = banner()[1]
    guides = Guides.objects.filter(approved=True)
    cities = City.objects.all()
    cit = request.GET.get('city')
    try:
        if cit and cit != 'All':
            guides = guides.filter(city__name=cit)
        if city:
            guides = guides.filter(city__name=city)
        else:
            pass
    except:
        pass
    tot_guides = len(guides)
    paginator = Paginator(guides, 12)
    page = request.GET.get('page')
    guides = paginator.get_page(page)

    context = {
        'guides':guides,'tot_guides':tot_guides,
        'cities':cities,
        'bycity':bycity,'cit':cit,'city':city,
        'all_cats':all_cats,'contact_info':banner()[2], 
    }
    return render(request, 'myapp/guides_list.html', context)


def guide_details(request, id):

    bycity = banner()[0]
    all_cats = banner()[1]
    guides = Guides.objects.filter(id=id).first()
    reviews = GuidesReview.objects.filter(guides=guides)
    reviews_len = len(reviews)
    rating = reviews.aggregate(tot_rate=Sum('rating'))['tot_rate']/reviews_len
    if request.user.is_authenticated:    
        if request.method == 'POST' and request.user.is_customer:
            form = GuidesReviewForm(request.POST)
            msg_form = MsgGuideForm(request.POST)
            try:
                if request.POST['content']:

                    if form.is_valid():
                        rating = form.cleaned_data['rating']
                        content = form.cleaned_data['content']
                        review = GuidesReview(guides=guides, customer=request.user, rating=rating, content=content)
                        review.save()
                        messages.success(request, _("Review added!"))
                        return redirect('myapp:guide_details', id)
            except:
                pass

            try:
                if request.POST['message']:
                    if msg_form.is_valid():
                        p_form = msg_form.save(commit=False)
                        p_form.customer = request.user
                        p_form.guide_info = guides
                        sentby = 'customer'
                        msg_form.save()
                        messages.success(request, _("Message sent!")) 
                        return redirect('myapp:guide_details', id)
            except:
                pass
            
        else:
            form = GuidesReviewForm()
            msg_form = MsgGuideForm()

    else:
         form = GuidesReviewForm()
         messages.warning(request, _("please login or create customer account!"))
    
    context = {
        'guides':guides,'reviews':reviews,'reviews_len':reviews_len,
        'form':form,'image1':guides.image1.url,'rating':rating,
        'bycity':bycity,
        'all_cats':all_cats,'contact_info':banner()[2],
    }

    return render(request, "myapp/guide_details.html", context)

def del_revguide(request, id):
    user = get_object_or_404(MyUser, id=request.user.id)
    rev = GuidesReview.objects.filter(customer=user)
    if rev.exists():
        rev.delete()
        messages.warning(request, _("Review deleted!"))
        return redirect('myapp:guide_details', id)
    return redirect('myapp:guide_details', id)


def about_us(request):
    bycity = banner()[0]
    all_cats = banner()[1]
    context = {
        'about_us':AboutUS.objects.last(),
        'bycity':bycity,
        'all_cats':all_cats,'contact_info':banner()[2],
    }
    return render(request, 'myapp/about_us.html', context)