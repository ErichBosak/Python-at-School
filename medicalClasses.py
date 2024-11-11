from datetime import date
from enum import Enum
from typing import Optional

# Allgemeine Personenklasse
class Person:
    def __init__(self, id, pseudonym, birthdate: date, gender) -> None:
        self.id = id
        self.pseudonym = pseudonym
        self.birthdate = birthdate
        self.gender = gender
    def __str__(self) -> str:
        return f"Person: | {self.id} | {self.pseudonym} | {self.birthdate} | {self.gender} |"
    def __repr__(self):
        return f"Person(id = {self.id}, pseudonym = {self.pseudonym}, birthdate = {self.birthdate}, gender = {self.gender})"

# Patient
class Patient(Person):
    def __init__(self, id, pseudonym, birthdate : date, gender) -> None:
        super().__init__(id, pseudonym, birthdate, gender)
        self.appointments: list[Appointment] = []
    def __str__(self) -> str:
        return f"Patient: | {self.id} | {self.pseudonym} | {self.birthdate} | {self.gender} |"
    def __repr__(self):
        return f"Patient(id = {self.id}, pseudonym = {self.pseudonym}, birthdate = {self.birthdate}, gender = {self.gender}, appointments = {self.appointments})"
    def addEmployees(self, appointment):
        self.appointments.append(appointment)
        

# Praxisangehörige        
class Staff(Person):
    def __init__(self, id, pseudonym, birthdate : date, gender, office) -> None:
        super().__init__(id, pseudonym, birthdate, gender)
        self.office = office

# Arzt
class Doctor(Staff): 
    def __init__(self, id, pseudonym, birthdate : date, gender, office) -> None:
        super().__init__(id, pseudonym, birthdate, gender, office)

# Pflegepersonal
class Nurse(Staff):
    def __init__(self, id, pseudonym, birthdate : date, gender, office) -> None:
        super().__init__(id, pseudonym, birthdate, gender, office)
        
class DoctorOffice:
    def __init__(self, id, position ) -> None:
        self.id = id
        self.position = position
        self.employees: list[Staff] = []

    def hire(self, employee: Staff):
        self.employees.append(employee)
        employee.office = self.id

class AppointmentType(Enum):
    ERSTGESPRÄCH = 1
    FOLGEGESPRÄCH = 2
    NOTFALL = 3
    ROUTINE = 4

class Appointment:
    def __init__(self, date : date, type : AppointmentType, reason, patient : Patient) -> None:
        self.employees: list[Staff] = []
        self.date = date
        self.type = type
        self.reason = reason
        self.patient = patient
        self.documentation: Optional[Documentation] = None
        
class Anamnesis:
    def __init__(self, description : str, date : date):
        self.description = description
        self.date = date
        
class Treatment:
    def __init__(self, type, description : str, date : date):
        self.type = type
        self.description = description
        self.date = date

class Documentation:
    def __init__(self, appointment : Appointment) -> None:
        self.appointment = appointment
        self.treatments: list[Treatment] = []
        self.anamnesisList: list[Anamnesis] = []
        appointment.documentation = self
        