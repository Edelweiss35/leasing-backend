# -*- coding: utf-8 -*-
from __future__ import unicode_literals



# Custom authentication models for leasing
# begin here


class LeasingUserManager(BaseUserManager):
    """
    custom user manager for leasing user 
    this user manager is responsible for all 
    CRUD operation over custom user models  
    """

    def create_user(self, username=None, email=None, password=None):
        if not username or username is None:
            raise ValidationError("User must have username")
        if not email or email is None:
            raise ValidationError("User must have email address")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username,
                                email=email,
                                password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class LeasingUser(AbstractBaseUser):
    """
    parent class for all users in leasing application
    """
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True, db_index=True)
    username = models.CharField(max_length=255, null=False, blank=False, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = LeasingUserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    # def __str__(self):
    #     return self.get_full_name

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        else:
            return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def display_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.email


class LeasingClient(LeasingUser):
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Leasing Client'

    def __str__(self):
        return self.get_full_name()


class LeasingClientInviteToken(models.Model):
    client = models.OneToOneField(LeasingClient, related_name="client_token", null=True, blank=True, on_delete=models.SET_NULL)
    invite_token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "%s %s" % (self.id, self.invite_token)

@receiver(post_save, sender=LeasingClient, dispatch_uid="create_auth_token_for_client")
def create_auth_token_for_client(sender, instance, created, **kwargs):
    if(created):
        instance.email = instance.email.lower()
        instance.username = instance.username.lower()
        instance.save()
        Token.objects.create(user=instance)
        ClientSetting.objects.create(client=instance)
