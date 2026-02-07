from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import ContactSupportForm
from greeva.hydroponics.models_custom import UserDevice
from greeva.utils.email_utils import send_templated_email

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
            recipient_list = [settings.DEFAULT_FROM_EMAIL] # Send to admin/OTP email
            
            try:
                send_templated_email(
                    subject=subject,
                    to_emails=recipient_list,
                    template_name='emails/contact_message.html',
                    text_template_name='emails/contact_message.txt',
                    context={
                        'subject': subject,
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'message': message,
                        'source_label': 'Support',
                        'brand_name': 'Smart IOT IITG',
                        'brand_tagline': 'Hydroponics Monitoring Platform',
                        'footer_note': 'You can reply to this email to reach the sender.',
                    },
                    reply_to=[email],
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
