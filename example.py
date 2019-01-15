from mock import Mock
import new

class RealClass(object):
    def other_method(self):
        self.attribute_initiated_earlier = "class value"

    def real_method(self):
        return [self.attribute_initiated_earlier, 'password']

fake_object = Mock(spec=RealClass())
class_method = object.__getattribute__(RealClass, 'real_method')
fake_object.real_method = new.instancemethod(class_method, fake_object, Mock)
fake_object.attribute_initiated_earlier = "new value"

print fake_object.real_method()