import unittest
import os
from HW10 import Repository
from HW10 import Student
from HW10 import Instructor
from HW10 import Major
  
class RepositoryTest (unittest.TestCase):
    
    def test_good_input(self):
        
        directory = r'C:\workspace\SSW810\Data_Repository_Files'   
        test_file = os.path.join(directory, 'Good_Test')
        student_test = {'12345': Student('12345', 'Lebron,J', 'SFEN'), '12346': Student('12346', 'AFK,A', 'SFEN')}
        instructor_test = {'66666': Instructor('66666', 'Einstein, A', 'SFEN'), '77777': Instructor('77777', 'Feynman, R', 'SFEN')}
        majors_test = {'SFEN': Major('SFEN'), 'SYEN': Major('SYEN')}
        self.assertTrue(student_test.keys() == Repository(test_file).students.keys())               
        self.assertTrue(instructor_test.keys() == Repository(test_file).instructors.keys())         
        self.assertTrue(majors_test.keys() == Repository(test_file).majors.keys())                  
      

    def test_bad_input(self):       

        path = r'C:\workspace\SSW810\Data_Repository_Files'
        
        with self.assertRaises(ValueError):
            Repository(os.path.join(path, "Bad_Student"))                  # the format for students.txt is wrong
        with self.assertRaises(ValueError):    
            Repository(os.path.join(path, "New_Student_from_grade"))       # has a grade with wrong name which is not in students
        with self.assertRaises(ValueError):
            Repository(os.path.join(path, "Major_not_offered"))            # major doesn't exist
        with self.assertRaises(FileNotFoundError):    
            Repository(os.path.join(path, "Folder_has_no_files"))          # no file in this folder^
        with self.assertRaises(FileNotFoundError):
            test = Repository(path)
            test.open_stud_file("not_a_real_file.txt", '\t')                    #file doesnt exist
      


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
