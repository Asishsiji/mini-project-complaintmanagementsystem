from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class people(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    COL = (('College1', 'College1'), ('College2', 'College2'))
    collegename = models.CharField(max_length=29, choices=COL, blank=False)
    
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be entered in the format: Up to 10 digits allowed.")
    contactnumber = models.CharField(validators=[phone_regex], max_length=10, blank=True)
    
    typeuser = (('student', 'student'), ('grievance', 'grievance'))
    type_user = models.CharField(max_length=20, default='student', choices=typeuser)
    
    CB = (('InformationTechnology', "InformationTechnology"), 
          ('ComputerScience', "ComputerScience"), 
          ('InformationScience', "InformationScience"), 
          ('Electronics and Communication', "Electronics and Communication"), 
          ('Mechanical', "Mechanical"))
    Branch = models.CharField(choices=CB, max_length=29, default='InformationTechnology')

    def __str__(self):
        return f"{self.user.username} - {self.collegename}"


class complaints(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    description=models.TextField(max_length=500)
    typ=(('Teachers','Teachers'),('Management','Management'),('collegebus','collegebus'),('hostel','hostel'),('canteen','canteen'),('others','others'))
    type=models.CharField(max_length=20,choices=typ,default='others')
    date=models.DateTimeField(auto_now_add=True)
    stat=(('Pending','Pending'),('Resolved','Resolved'),('In Progress','In Progress'))
    status=models.CharField(max_length=20,choices=stat,default='Pending')
    
    def __str__(self):
        return f"{self.user.username} - {self.subject} - {self.status}"
    
    
    
    