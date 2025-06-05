from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import ContactForm, EmailSearchForm, ReplyForm
from .models import ContactMessage, Project, Skill

# Contact Form View
def contact_view(request):
    """Handle contact form submission and display success message."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your message, we'll get back to you soon!")
            return redirect('contact')
        else:
            print(form.errors)
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})

# Reply Form View (for admins/staff)
def contact_reply_form(request, message_id):
    """Display reply form for a specific contact message."""
    message = get_object_or_404(ContactMessage, id=message_id)
    return render(request, 'core/contact_reply_form.html', {'message': message})

# Reply to Message View (for admins/staff)
def reply_to_message(request, message_id):
    """Save reply to a contact message."""
    message = get_object_or_404(ContactMessage, id=message_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            message.reply = form.cleaned_data['reply']
            message.save()
            messages.success(request, 'Reply saved successfully!')
            return redirect('contact_replies')
    else:
        form = ReplyForm(initial={'reply': message.reply if message.reply else ''})
    return render(request, 'core/contact_reply_form.html', {'message': message, 'form': form})

# View for Displaying Messages with Replies (for admins/staff)
def contact_replies(request):
    """Display all contact messages with replies."""
    contact_messages = ContactMessage.objects.filter(reply__isnull=False)
    return render(request, 'core/contact_replies.html', {'messages': contact_messages})

# Customer Messages View (for customers)
def customer_messages(request):
    """Display contact messages for a specific email."""
    user_messages = None
    form = EmailSearchForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        user_messages = ContactMessage.objects.filter(email=email).order_by('-created_at')
        
        if not user_messages.exists():
            messages.warning(request, "No messages found for this email address.")
    
    return render(request, 'core/customer_messages.html', {
        'form': form,
        'messages': user_messages
    })

# Home Page View
def home(request):
    """Display home page with skills and projects."""
    skills = Skill.objects.select_related('skill_type').order_by('skill_type__name', 'name')
    projects = Project.objects.all().order_by('-created_at')[:6]  # Show latest 6 projects
    return render(request, 'core/home.html', {
        'skills': skills,
        'projects': projects,
    })

# About Page View
def about(request):
    """Display about page."""
    return render(request, 'core/about.html')

# Services Page View
def services(request):
    """Display services page."""
    return render(request, 'core/services.html')

# Projects View
def projects(request):
    """Display all projects with pagination."""
    project_list = Project.objects.all().order_by('-created_at')
    paginator = Paginator(project_list, 6)  # 6 projects per page
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    return render(request, 'core/projects.html', {'projects': projects})

def project_detail(request, project_id):
    """Display project details."""
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'core/project_detail.html', {'project': project})