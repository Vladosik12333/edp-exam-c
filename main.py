
queue = []

class Event:
    def __init__(self, name, payload):
        self.name = name
        self.payload = payload

class StudentApplyEvent(Event):
    def __init__(self, passport_number):
        super().__init__("apply_to_university_event", {"passport_number": passport_number})

class UniversityDecisionEvent(Event):
    def __init__(self, passport_number, is_accepted):
        super().__init__("university_decision_event", {"passport_number": passport_number, "is_accepted": is_accepted})

class Student:
    def __init__(self, first_name, last_name, phone_number, passport_number):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.passport_number = passport_number

    def apply_to_university(self):
        event = StudentApplyEvent(self.passport_number)

        queue.append(event)

        print("Student#apply_to_university : student applied for studying in a university. StudentApplyEvent fired!")

    def handle_response(self, event):
        if event.payload['is_accepted']:
            print("Student#handle_response : Prepare for studying")
        else:    
            print("Student#handle_response : Oh no! I rejected. I have to find another university")


class University:
    def __init__(self, name, address, phone_number, email):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email

    def handle_application(self, event):
        decision_event = UniversityDecisionEvent(event.payload["passport_number"], is_accepted=True)

        queue.append(decision_event)

        print("University#handle_application : University handled the student application and sent a decision. UniversityDecisionEvent fired!")

student1 = Student("Vladyslav", "Babiak", '5435345345', 'ED4234323')
university1 = University('ATA', 'Olszewska 12', '343242344', 'ata_contact@akademiata.edu.pl')


student1.apply_to_university()

while queue:
    event = queue.pop(0) 

    if isinstance(event, StudentApplyEvent):
        university1.handle_application(event) 
    elif isinstance(event, UniversityDecisionEvent):
        student1.handle_response(event)
