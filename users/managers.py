from django.db.models import Manager,Max 


class StudentManager(Manager):
    
    def get_max_rollno(self,std):
        return self.values('rollno').filter(rollno__startswith = std).order_by('-rollno')