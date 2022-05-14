import unittest
from app.models import User

class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(password = 'nakuru')
    
    #test whether the password is being hashed    
    def test_password_setter(self):
        self.assertTrue(self.new_user.password_secure is not None)  
        
    #test whether attribute error is raised     
    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password
     
    #test password hash verification with correct password      
    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('nakuru'))