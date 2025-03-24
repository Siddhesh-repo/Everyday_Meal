from faker import Faker
from .models import*
import random
fake = Faker()

def seed_db(n=10)->None:
    try:
        for i in range(0,n):
            depart_obj=Department.objects.all()
            index=random.randint(0,len(depart_obj)-1)
            department=depart_obj[index]
            student_id=random.randint(2002,2500)
            student_name=fake.name()
            student_email=fake.email()
            student_age=random.randint(18,30)
            student_address=fake.address()

            student_id_obj=StudentID.objects.create(student_id=student_id)
            student_obj=Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
            )
    except Exception as e:
        print(e)


