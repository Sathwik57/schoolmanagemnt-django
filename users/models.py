from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, UserManager,PermissionsMixin
from django.db.models.manager import Manager
from django.utils.translation import gettext_lazy as _
import uuid



from users.managers import StudentManager

# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
	first_name =models.CharField(max_length=20)
	last_name =models.CharField(max_length=20,null=True,blank= True) 
	username = models.CharField(max_length=10,unique=True)
	email = models.EmailField(_('email address'), unique=True)
	is_student = models.BooleanField(default=True)
	profile_image = models.ImageField(default = 'default.png',null=True,blank =True)
	is_male = models.BooleanField(default=False)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	id = models.UUIDField(default = uuid.uuid4 ,unique= True,editable= False ,primary_key=True)

	is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
        'site.'))
	is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'))
	is_superuser = models.BooleanField(_('Superuser'), default=False)
	
	objects  = UserManager()

	class Meta:
		ordering = ['-first_name' ,'-last_name']

	def __str__(self) -> str:
	    return f'{self.first_name} {self.last_name}({self.username})' if self.last_name else f'{self.first_name}({self.username})'

	

class Student(models.Model):
	user =  models.OneToOneField(User, on_delete=models.CASCADE)
	rollno = models.CharField(max_length=15,null=True,blank=True)
	std = models.CharField(max_length=2)
	guardian = models.CharField(max_length=15,null=True,blank=True)
	contact_no = models.IntegerField(null=True)
	address = models.CharField(max_length=250,null= True, blank= True)

	objects = Manager()
	fil = StudentManager()		

	def __str__(self):
		return f'{self.rollno}-{self.user}'

class Teacher(models.Model):
	from subjects.models import Subject
	user =  models.OneToOneField(User, on_delete=models.CASCADE)
	sub = models.OneToOneField(Subject,on_delete=models.SET_NULL,null=True)
	contact_no = models.CharField(max_length=25)

	def __str__(self):
		return f'{self.user.username}({self.sub})'

	@classmethod
	def vacant_posts(cls):
		from subjects.models import Subject
		l = []
		subs = [x['name'] for x in Subject.objects.values('name')]
		fill_subs = [x.sub.name for x in Teacher.objects.all()]
		v = set(subs) - set(fill_subs)
		return v 