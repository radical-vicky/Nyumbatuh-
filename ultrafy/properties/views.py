from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import Property, PropertyInquiry
from .forms import PropertyForm, PropertyImageFormSet, PropertyInquiryForm


def home(request):
    featured = Property.objects.filter(is_featured=True, is_active=True)[:6]
    recent = Property.objects.filter(is_active=True)[:8]
    total_properties = Property.objects.filter(is_active=True).count()
    partner_count = Property.objects.filter(ultrafy_partner=True, is_active=True).count()
    context = {
        'featured': featured,
        'recent': recent,
        'total_properties': total_properties,
        'partner_count': partner_count,
        'title': 'Find Your Next Space — Ultrafy Fiber Network',
    }
    return render(request, 'properties/home.html', context)


def property_list(request):
    qs = Property.objects.filter(is_active=True)
    q = request.GET.get('q', '')
    city = request.GET.get('city', '')
    ptype = request.GET.get('type', '')
    listing = request.GET.get('listing', '')
    partner = request.GET.get('partner', '')

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(address__icontains=q) | Q(city__icontains=q))
    if city:
        qs = qs.filter(city__icontains=city)
    if ptype:
        qs = qs.filter(property_type=ptype)
    if listing == 'rent':
        qs = qs.filter(is_for_rent=True)
    elif listing == 'sale':
        qs = qs.filter(is_for_sale=True)
    if partner == '1':
        qs = qs.filter(ultrafy_partner=True)

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    cities = Property.objects.filter(is_active=True).values_list('city', flat=True).distinct()
    context = {
        'page_obj': page_obj,
        'q': q,
        'city': city,
        'ptype': ptype,
        'listing': listing,
        'partner': partner,
        'cities': cities,
        'title': 'Browse Properties',
    }
    return render(request, 'properties/list.html', context)


def property_detail(request, slug):
    prop = get_object_or_404(Property, slug=slug, is_active=True)
    prop.views_count += 1
    prop.save(update_fields=['views_count'])

    inquiry_form = PropertyInquiryForm()
    if request.method == 'POST':
        inquiry_form = PropertyInquiryForm(request.POST)
        if inquiry_form.is_valid():
            inquiry = inquiry_form.save(commit=False)
            inquiry.property = prop
            if request.user.is_authenticated:
                inquiry.inquirer = request.user
            inquiry.save()
            try:
                send_mail(
                    subject=f"New inquiry for {prop.title}",
                    message=f"From: {inquiry.name} <{inquiry.email}>\n\n{inquiry.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[prop.contact_email or prop.owner.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, 'Your inquiry has been sent. The owner will contact you shortly.')
            return redirect('property_detail', slug=slug)

    related = Property.objects.filter(
        city=prop.city, is_active=True
    ).exclude(pk=prop.pk)[:3]

    context = {
        'property': prop,
        'images': prop.images.all(),
        'amenities': prop.amenities.all(),
        'inquiry_form': inquiry_form,
        'related': related,
        'title': prop.title,
    }
    return render(request, 'properties/detail.html', context)


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            prop.save()
            # Handle image uploads
            images = request.FILES.getlist('images')
            for i, img in enumerate(images):
                from .models import PropertyImage
                PropertyImage.objects.create(
                    property=prop,
                    image=img,
                    is_primary=(i == 0),
                    order=i,
                )
            # Handle amenities
            amenities_raw = request.POST.get('amenities', '')
            if amenities_raw:
                from .models import PropertyAmenity
                for a in amenities_raw.split(','):
                    a = a.strip()
                    if a:
                        PropertyAmenity.objects.create(property=prop, name=a)
            messages.success(request, 'Property listed successfully. Our team will review it shortly.')
            return redirect('property_detail', slug=prop.slug)
    else:
        form = PropertyForm()
    return render(request, 'properties/create.html', {'form': form, 'title': 'List Your Property'})


@login_required
def my_properties(request):
    props = Property.objects.filter(owner=request.user)
    return render(request, 'properties/my_properties.html', {'properties': props, 'title': 'My Properties'})


@login_required
def property_delete(request, slug):
    prop = get_object_or_404(Property, slug=slug, owner=request.user)
    if request.method == 'POST':
        prop.is_active = False
        prop.save()
        messages.success(request, 'Property removed from listings.')
        return redirect('my_properties')
    return render(request, 'properties/confirm_delete.html', {'property': prop})
