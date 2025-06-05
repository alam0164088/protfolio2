from django.contrib import admin
from .models import ContactMessage, Skill, Project, ProjectImage, Technology, SkillType
from django.utils import timezone

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3

class TechnologyInline(admin.TabularInline):
    model = Project.technologies.through
    extra = 1

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'status', 'created_at', 'replied_at']
    list_filter = ['status', 'created_at', 'replied_at']
    search_fields = ['name', 'email', 'subject', 'message', 'reply']
    readonly_fields = ['created_at', 'updated_at', 'replied_at']
    fieldsets = (
        ('Message Information', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Reply', {
            'fields': ('reply', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'replied_at'),
            'classes': ('collapse',)
        })
    )
    actions = ['mark_as_replied', 'mark_as_closed']

    def mark_as_replied(self, request, queryset):
        queryset.update(status='replied', is_replied=True, replied_at=timezone.now())
    mark_as_replied.short_description = "Mark selected messages as replied"

    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
    mark_as_closed.short_description = "Mark selected messages as closed"

@admin.register(SkillType)
class SkillTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'skill_type', 'level', 'experience_years', 'percentage', 'last_used', 'used_in_projects', 'created_at')
    list_filter = ('skill_type', 'level', 'used_in_projects')
    search_fields = ('name', 'skill_type__name', 'certification', 'skill_description')
    filter_horizontal = ('related_skills',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'skill_type', 'icon', 'level', 'percentage', 'experience_years')
        }),
        ('Project Details', {
            'fields': ('used_in_projects', 'project_list', 'last_used')
        }),
        ('Additional Information', {
            'fields': ('certification', 'related_skills', 'skill_description')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    ordering = ('skill_type', 'name')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'has_frontend_demo', 'has_backend_demo']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    inlines = [ProjectImageInline, TechnologyInline]
    exclude = ['technologies']
    
    def has_frontend_demo(self, obj):
        return bool(obj.frontend_demo)
    has_frontend_demo.boolean = True
    has_frontend_demo.short_description = 'Frontend Demo'

    def has_backend_demo(self, obj):
        return bool(obj.backend_demo)
    has_backend_demo.boolean = True
    has_backend_demo.short_description = 'Backend Demo'

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption']
    list_filter = ['project']
    search_fields = ['project__title', 'caption']