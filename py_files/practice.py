class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
    
    def get_grade(self):
        self.g = "hi"
        return self.grade
    
class Course:
    def __init__(self, name, max_students):
        self.name = name
        self.max = max_students
        self.students = []

    def add_student(self, student):
        if len(self.students) < self.max:
            self.students.append(student)
            return True
        return False
    
    def get_average(self):
        total = 0
        for i in self.students:
            total += i.get_grade()
        return total / len(self.students)
    
s1 = Student("Tim", 19, 96)
s2 = Student("Grim", 19, 50)
s3 = Student("Jim", 19, 75)

course = Course("Science", 2)
course.add_student(s1)
course.add_student(s2)
print(course.get_average())
print(course.students[0].name)
print(s1.g)