from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('replied', 'Replied'),
        ('closed', 'Closed')
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_replied = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.reply and not self.is_replied:
            self.is_replied = True
            self.status = 'replied'
            self.replied_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} - {self.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

class SkillType(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Skill(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    ICON_CHOICES = [
        ('fab fa-python', 'Python'),
        ('fab fa-js', 'JavaScript'),
        ('fab fa-react', 'React'),
        ('fab fa-html5', 'HTML5'),
        ('fab fa-css3-alt', 'CSS3'),
        ('fab fa-bootstrap', 'Bootstrap'),
        ('fab fa-git-alt', 'Git'),
        ('fab fa-github', 'GitHub'),
        ('fab fa-docker', 'Docker'),
        ('fab fa-aws', 'AWS'),
        ('fab fa-node', 'Node.js'),
        ('fab fa-php', 'PHP'),
        ('fab fa-laravel', 'Laravel'),
        ('fab fa-angular', 'Angular'),
        ('fab fa-vuejs', 'Vue.js'),
        ('fab fa-sass', 'Sass'),
        ('fab fa-wordpress', 'WordPress'),
        ('fab fa-java', 'Java'),
        ('fas fa-database', 'Database'),
        ('fas fa-server', 'Backend'),
        ('fas fa-mobile-alt', 'Mobile'),
        ('fas fa-desktop', 'Frontend'),
        ('fas fa-code', 'Programming'),
        ('fas fa-terminal', 'Terminal'),
        ('fas fa-tools', 'Tools'),
        ('fas fa-cogs', 'System'),
        ('fas fa-cloud', 'Cloud'),
        ('fas fa-network-wired', 'Network'),
        ('fas fa-shield-alt', 'Security'),
        ('fas fa-project-diagram', 'Architecture'),
        ('fas fa-feather-alt', 'Django'),  
        ('fas fa-plug', 'REST API'),      
        ('fas fa-stream', 'DRF'),         
        ('fas fa-database', 'PostgreSQL'), 
        ('fas fa-table', 'SQLite'), 
        ('fas fa-flask', 'Flask'),
        ('fas fa-database', 'MySQL'),
        ('fas fa-database', 'MongoDB'),
        ('fas fa-database', 'Firebase'),
        ('fas fa-database', 'Redis'),
        ('fas fa-database', 'Elasticsearch'),
        ('fas fa-database', 'Cassandra'),
    ]

    name = models.CharField(max_length=100)
    skill_type = models.ForeignKey(SkillType, on_delete=models.SET_NULL, null=True, blank=True, related_name='skills')
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fas fa-code')
    percentage = models.IntegerField(default=0)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    experience_years = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    used_in_projects = models.BooleanField(default=False)
    project_list = models.TextField(blank=True)
    certification = models.CharField(max_length=255, blank=True)
    last_used = models.DateField(null=True, blank=True)
    related_skills = models.ManyToManyField('self', blank=True)
    skill_description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.skill_type.name if self.skill_type else 'No Type'}"
    
    class Meta:
        ordering = ['skill_type', 'name']

class Technology(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', default='defaults/placeholder.jpg', blank=True, null=True)
    frontend_demo = models.URLField(blank=True, null=True)
    backend_demo = models.URLField(blank=True, null=True)
    source_code = models.URLField(blank=True, null=True)
    features = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    technologies = models.ManyToManyField(Technology, blank=True)

    def has_frontend_demo(self):
        return bool(self.frontend_demo)
    
    def has_backend_demo(self):
        return bool(self.backend_demo)

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')
    caption = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.project.title}"