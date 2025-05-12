from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def redirect_to_login(request):
    return redirect('users:login')

def redirect_to_register(request):
    return redirect('users:register')

def redirect_to_logout(request):
    return redirect('users:logout')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # Form validation
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'base/contact.html', {
                'form_data': request.POST
            })
        
        # Construct email message
        email_message = f"Name: {name}\nEmail: {email}\n\n{message}"
        
        try:
            # In production, this would send an actual email
            # For now, we'll simulate success
            
            # send_mail(
            #     f"Contact Form: {subject}",
            #     email_message,
            #     email,
            #     [settings.DEFAULT_FROM_EMAIL],
            #     fail_silently=False,
            # )
            
            messages.success(request, 'Your message has been sent. We will get back to you soon!')
            return redirect('contact')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return render(request, 'base/contact.html')

def privacy(request):
    return render(request, 'base/privacy.html')

def terms(request):
    return render(request, 'base/terms.html')

def faq(request):
    return render(request, 'base/faq.html')
