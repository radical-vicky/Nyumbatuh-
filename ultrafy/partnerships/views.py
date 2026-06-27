from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import PartnershipRequest
from .forms import PartnershipRequestForm


def partnership_landing(request):
    return render(request, 'partnerships/landing.html', {'title': 'Become a Partner — Ultrafy'})


@login_required
def partnership_apply(request):
    if request.method == 'POST':
        form = PartnershipRequestForm(request.POST)
        if form.is_valid():
            pr = form.save(commit=False)
            pr.applicant = request.user
            pr.save()
            try:
                send_mail(
                    subject='New Partnership Application — Ultrafy Fiber',
                    message=f"New application from {pr.contact_name}\nProperty: {pr.property_name}\nCity: {pr.city}\nUnits: {pr.unit_count}\nContact: {pr.contact_email} / {pr.contact_phone}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
                send_mail(
                    subject='We received your partnership application — Ultrafy Fiber',
                    message=f"Hi {pr.contact_name},\n\nThank you for applying to become an Ultrafy Fiber Network partner.\n\nWe will review your application for {pr.property_name} and contact you within 2 business days.\n\nBest regards,\nUltrafy Fiber Network Team",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[pr.contact_email],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, 'Application submitted. We will reach out within 2 business days.')
            return redirect('partnership_status')
    else:
        form = PartnershipRequestForm()
    return render(request, 'partnerships/apply.html', {'form': form, 'title': 'Apply for Partnership'})


@login_required
def partnership_status(request):
    requests = PartnershipRequest.objects.filter(applicant=request.user)
    return render(request, 'partnerships/status.html', {'requests': requests, 'title': 'Partnership Status'})
