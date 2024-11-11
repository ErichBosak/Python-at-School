import medicalClasses as medical
import datetime

patient1 = medical.Patient(1,"Bingus", datetime.date(2005,3,15), "Male")

print(patient1.__str__())

print(patient1.__repr__()) 