from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# pyrefly: ignore [missing-import]
from .models import Location, AppUser, Vendor


# ─────────────────────────────────────────
# VENDOR ADMIN
# ─────────────────────────────────────────
def remove_vendors(modeladmin, request, queryset):
    """Custom action: Remove selected vendors from the system."""
    count = queryset.count()
    from .models import Turf, AppUser
    
    for vendor in queryset:
        # 1. Set turfs to retire=1 and detach vendor
        Turf.objects.filter(vendor=vendor).update(retire=1, vendor=None)
        # 2. Delete the associated AppUser account
        AppUser.objects.filter(email=vendor.email).delete()
        
    queryset.delete()
    modeladmin.message_user(request, f" {count} vendor(s) and their user accounts removed, turfs retired successfully.")

remove_vendors.short_description = "🗑️ Remove selected vendors"


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'vendor_id', 'ownername', 'venuename',
        'email', 'phone', 'location',
        'status_badge', 'created_at'
    )
    list_filter = ('status', 'location')
    search_fields = ('vendor_id', 'ownername', 'email', 'venuename', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('vendor_id', 'created_at')
    actions = [remove_vendors]

    fieldsets = (
        ('Vendor Info', {
            'fields': ('vendor_id', 'ownername', 'venuename', 'email', 'phone')
        }),
        ('Location', {
            'fields': ('location', 'address', 'pincode')
        }),
        ('Business Details', {
            'fields': ('totalturf', 'availablegames', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'Approved': '#28a745',
            'Pending':  '#ffc107',
            'Rejected': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;'
            'border-radius:12px;font-size:12px;font-weight:600;">{}</span>',
            color, obj.status
        )
    status_badge.short_description = 'Status'


# ─────────────────────────────────────────
# APP USER ADMIN
# ─────────────────────────────────────────
@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ('email', 'name', 'role', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'mobile', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobile', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.register(Location)
