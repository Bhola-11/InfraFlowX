import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

USER_ROLE_CHOICES = [
    ('super_admin', _('Super Admin')),
    ('organization_admin', _('Organization Admin')),
    ('infrastructure_manager', _('Infrastructure Manager')),
    ('asset_manager', _('Asset Manager')),
    ('project_manager', _('Project Manager')),
    ('maintenance_manager', _('Maintenance Manager')),
    ('inspector', _('Inspector')),
    ('field_engineer', _('Field Engineer')),
    ('contractor_manager', _('Contractor Manager')),
    ('finance_manager', _('Finance Manager')),
    ('support_agent', _('Support Agent')),
    ('analyst', _('Analyst')),
    ('viewer', _('Viewer')),
]

class User(AbstractUser):
    """
    Custom Enterprise User model supporting multi-tenant organizations, 13 enterprise roles,
    UUID identification, and security telemetry.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    role = models.CharField(
        max_length=50,
        choices=USER_ROLE_CHOICES,
        default='viewer',
        db_index=True,
        verbose_name=_('Enterprise Role')
    )
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        verbose_name=_('Primary Organization')
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_('Phone Number')
    )
    job_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Official Job Title')
    )
    badge_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_('Employee / Badge ID')
    )
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_('Profile Picture')
    )
    is_two_factor_enabled = models.BooleanField(
        default=False,
        verbose_name=_('2FA Security Enabled')
    )
    last_activity = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Last Activity Timestamp')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Administrative Notes')
    )

    class Meta:
        ordering = ['username']
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return f"{full_name} ({self.get_role_display()})"
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_super_admin(self):
        return self.is_superuser or self.role == 'super_admin'

    @property
    def is_org_admin(self):
        return self.is_super_admin or self.role == 'organization_admin'

    @property
    def is_manager_level(self):
        return self.role in [
            'super_admin', 'organization_admin', 'infrastructure_manager',
            'asset_manager', 'project_manager', 'maintenance_manager',
            'contractor_manager', 'finance_manager'
        ]

    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/images/default-avatar.svg'


class UserProfile(models.Model):
    """
    Extended user profile settings and interface preferences.
    """
    THEME_CHOICES = [
        ('dark', _('Dark Matrix Theme (Default)')),
        ('light', _('Clean Enterprise Light')),
        ('high_contrast', _('High Contrast Mode')),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User')
    )
    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default='dark',
        verbose_name=_('UI Color Theme')
    )
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        verbose_name=_('Timezone')
    )
    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_('Receive Email Notifications')
    )
    sms_notifications = models.BooleanField(
        default=False,
        verbose_name=_('Receive SMS Notifications')
    )
    compact_tables = models.BooleanField(
        default=False,
        verbose_name=_('Compact Data Tables')
    )
    bio = models.TextField(
        blank=True,
        verbose_name=_('Professional Bio')
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Office Address')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"Profile of {self.user.username}"


class UserLoginSession(models.Model):
    """
    Audit record of user login sessions and device fingerprints.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_sessions',
        verbose_name=_('User')
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('IP Address')
    )
    user_agent = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Browser User Agent')
    )
    session_key = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Session Key')
    )
    login_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Login Timestamp')
    )
    logout_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Logout Timestamp')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Session Active')
    )

    class Meta:
        ordering = ['-login_time']
        verbose_name = _('User Login Session')
        verbose_name_plural = _('User Login Sessions')

    def __str__(self):
        return f"{self.user.username} @ {self.ip_address} on {self.login_time.strftime('%Y-%m-%d %H:%M')}"
