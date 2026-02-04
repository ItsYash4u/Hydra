from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactSupportForm
from greeva.hydroponics.models_custom import UserDevice

def get_user_data(request):
    """Helper to get user data from session or DB if logged in"""
    user_id = request.session.get('user_id')
    initial_data = {}
    
    if user_id:
        try:
            # Try getting from DB for freshest data
            user = UserDevice.objects.get(User_ID=user_id)
            initial_data['name'] = user.Name
            initial_data['email'] = user.Email_ID
            initial_data['phone'] = user.Phone
        except UserDevice.DoesNotExist:
            # Fallback to session
            initial_data['name'] = request.session.get('name', '')
            initial_data['email'] = request.session.get('email', '')
            
    return initial_data

def contact_support_view(request):
    if request.method == 'POST':
        form = ContactSupportForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone'] or '--'
            message = form.cleaned_data['message']
            
            # Prepare Email
            subject = f"New Support Message from {name}"
            email_body = f"""
Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
"""
            recipient_list = [settings.DEFAULT_FROM_EMAIL] # Send to admin/OTP email
            
            try:
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL, # From address
                    recipient_list,
                    fail_silently=False
                )
                messages.success(request, "Your message has been sent successfully.")
                return redirect('support:contact')
            except Exception as e:
                print(f"[SUPPORT ERROR] Email failed: {e}")
                messages.error(request, "Failed to send message. Please try again later.")
    else:
        # Pre-fill form if user is logged in
        initial_data = get_user_data(request)
        form = ContactSupportForm(initial=initial_data)

    return render(request, 'support/contact.html', {'form': form})

def faq_view(request):
    return render(request, 'support/faq.html')

def terms_view(request):
    return render(request, 'support/terms.html')

def privacy_view(request):
    return render(request, 'support/privacy.html')
