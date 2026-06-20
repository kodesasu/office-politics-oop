import logging, os, random
from abc import ABC, abstractmethod
from logging.handlers import RotatingFileHandler
from functools import total_ordering
from faker import Faker

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Enterprise_Employee_Management_System.log")

log_handle = RotatingFileHandler(
    file_path,
    maxBytes=5*1024*1024,
    backupCount=3,
    encoding="utf-8"

)

log_handle.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logging.basicConfig(level=logging.DEBUG,
                    handlers=[log_handle])



class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email



@total_ordering
class Employee(Person, ABC):
    def __init__(self, name, email, employee_id, salary,admin_password="admin123"):
        super().__init__(name, email)
        self.employee_id = employee_id
        self._salary = salary
        self.__password = admin_password
        self.vl = ValidationLayer()

    @abstractmethod
    def get_salary(self, password):
        pass


    @abstractmethod
    def set_salary(self, value, password=None):
        pass


    @abstractmethod
    def add_salary(self, new_salary, password=None):
        pass

    @abstractmethod
    def calculate_bonus(self):
        pass

    @abstractmethod
    def compare_salaries(self, other, password, other_password):
        pass



    def __repr__(self):
        logging.info(f"Returning repr for class:{self.__class__.__name__}\n")

        attrs = []
        for k, v in self.__dict__.items():
            if "password" in k.lower() or k.lower() in ["_salary", "vl"]:
                attrs.append(f"{k} = [HIDDEN]")
            else:
                attrs.append(f"{k} = {v!r}")
        attr = ", ".join(attrs)
        return f"{self.__class__.__name__}({attr})"

    def __str__(self):
        logging.info(f"Returning str for class:{self.__class__.__name__}\n")

        attrs = []
        for k, v in self.__dict__.items():
            if "password" in k.lower() or k.lower() in ["_salary", "vl"]:
                continue
            attrs.append(f"{v}")
        attr = ", ".join(attrs)
        return f"{self.__class__.__name__}({attr})"

    def __lt__(self, other):
        logging.debug("Trying to compare salaries (with __lt__())")
        if isinstance(other, Employee):
            logging.info("Returning True| salaries compared\n")
            return self._salary < other._salary

        logging.warning("Invalid Instance | NotImplemented Raised\n")
        return NotImplemented


class Manager(Employee):
    def __init__(self, name, email, employee_id, salary, team_size, mang_pass):
        super().__init__(name, email, employee_id, salary)
        self.team_size = team_size
        self.__password = mang_pass

    def get_salary(self, password=None):
        logging.debug("Trying to return Salary")
        logging.debug("Authenticating password")

        if password != self.__password:
            logging.warning(f"Password Mismatch[{password} != {self.__password}] | Raised PermissionError")
            raise PermissionError("Access Denied [Incorrect Password]")
        logging.info("Password Matched | Returning Salary")
        return self._salary

    def set_salary(self, value, password=None):
        logging.debug("Trying to Set Salary")
        logging.debug("Authenticating password")

        if password != self.__password:
            logging.warning(f"Password Mismatch[{password} != {self.__password}] | Raised PermissionError")
            raise NotImplementedError("Access Denied [Incorrect Password]")
        logging.info("Password Matched | Validating Input")

        is_valid, data = self.vl.validate_integer(value)
        if not is_valid:
            logging.warning(f"Invalid input [{data}]| Raised NotImplementedError")
            raise NotImplementedError(data)

        logging.info("Input Validated | Setting Salary")
        self._salary += data


    def calculate_bonus(self):
        logging.info("Returning calculated bonus")
        return 0.1 * int(self.team_size)

    def add_salary(self, new_salary, password=None):
        logging.debug("Trying to Add Salary")
        logging.debug("Authenticating password")

        if password is None:
            logging.warning(f"No Password Entered | NotImplementedError")
            raise NotImplementedError("Access Denied [Enter Password]")
        bonus = self.calculate_bonus()
        self.set_salary(bonus * new_salary, password=password)
        logging.info("\n")

    def compare_salaries(self, other, password, other_password):
        logging.debug(f"Trying to Compare Salaries for class :{self.__class__.__name__}")
        logging.debug("Trying to Get Salaries")

        if isinstance(other, (Manager, Developer)):
            my_salary = self.get_salary(password=password)
            other_salary = other.get_salary(password=other_password)
            logging.info("Salary Compared | Returning Results")
            return my_salary < other_salary

        logging.warning("Invalid Instance| NotImplemented Returned")
        return NotImplemented





class Developer(Employee):
    def __init__(self, name, email, employee_id, salary, programming_languages, dev_pass):
        super().__init__(name, email, employee_id, salary)
        self.programming_languages = programming_languages
        self.__password = dev_pass


    def get_salary(self, password=None):
        logging.debug("Trying to return Salary")
        logging.debug("Authenticating password")

        if password != self.__password:
            logging.warning(f"Password Mismatch[{password} != {self.__password}] | Raised PermissionError")
            raise PermissionError("Access Denied [Incorrect Password]")
        logging.info("Password Matched | Returning Salary")
        return self._salary


    def set_salary(self, value, password=None):
        logging.debug("Trying to Set Salary")
        logging.debug("Authenticating password")

        if password != self.__password:
            logging.warning(f"Password Mismatch[{password} != {self.__password}] | Raised PermissionError")
            raise NotImplementedError("Access Denied [Incorrect Password]")
        logging.info("Password Matched | Validating Input")

        is_valid, data = self.vl.validate_integer(value)
        if not is_valid:
            logging.warning(f"Invalid input [{data}]| Raised NotImplementedError")
            raise NotImplementedError(data)

        logging.info("Input Validated | Setting Salary")
        self._salary += data

    def calculate_bonus(self):
        logging.info("Returning calculated bonus")
        return 0.5 * len(self.programming_languages)

    def add_salary(self, new_salary, password=None):
        logging.debug("Trying to Add Salary")
        logging.debug("Authenticating password")

        if password is None:
            logging.warning(f"No Password Entered | NotImplementedError")
            raise PermissionError ("Access Denied [Enter Password]")
        bonus = self.calculate_bonus()
        self.set_salary(bonus * new_salary, password=password)
        logging.info("\n")

    def compare_salaries(self, other, password, other_password):
        logging.debug(f"Trying to Compare Salaries for class :{self.__class__.__name__}")
        logging.debug("Trying to Get Salaries")

        if isinstance(other, (Manager, Developer)):
            my_salary = self.get_salary(password=password)
            other_salary = other.get_salary(password=other_password)
            logging.info("Salary Compared | Returning Results")
            return my_salary < other_salary

        logging.warning("Invalid Instance| NotImplemented Returned")
        return NotImplemented



class ValidationLayer:
    def validate_non_empty_string(self, value):
        logging.info("Validating if: Input is Empty")
        return (False, "Value is empty") if len(str(value)) == 0 else (True, value)

    def validate_integer(self, value):
        logging.info("Validating if: Input is an Integer")
        is_valid, data = self.validate_non_empty_string(value)
        if is_valid:
            return (False, "Value is not a Digit") if not str(int(data)).isdigit() else (True, data)
        return is_valid, data


@total_ordering
class Department:
    def __init__(self, name):
        self.name = name
        self.emps = {}

    def set_emp(self, emp):
        logging.info(f"Adding Employee Object to Dict(self.emps) in class: {self.__class__.__name__}\n")
        self.emps[emp.employee_id] = emp

    def get_emp(self, emp):
        logging.debug(f"Returning Employee Object to Dict(self.emps) in class: {self.__class__.__name__}\n")
        return self.emps.get(emp.employee_id)

    def test_run(self):
        logging.info("Test Running |Returning values in Dict(self.emps)")
        return "|\n".join(repr(v) for v in self.emps.values())

    def compare_salary_with_auth(self, emp_1, emp_2, password, other_password):
        logging.info("Trying to call objects method(.compare_salaries)| Comparing object Salaries\n")
        return self.get_emp(emp_1).compare_salaries(self.get_emp(emp_2), password, other_password)

    def __str__(self):
        logging.info(f"Returning str for class:{self.__class__.__name__}\n")
        return f"{self.name}, {self.emps}"

    def __repr__(self):
        logging.info(f"Returning repr for class:{self.__class__.__name__}| values in Dict(self.emps)\n")
        return f"Department(Department Name = {self.name}\nEmployees = {self.test_run()})"

    def __len__(self):
        logging.info("Returning Length of Dict(self.emps)\n")
        return len(self.emps)

    def __contains__(self, item):
        logging.info(f"Returning True if item in Dict(self.emps)\n")
        return item in self.emps

    def __iter__(self):
        logging.info(f"Returning Iterator for Dict(self.emps)\n")
        return iter(self.emps.values())

    def __eq__(self, other):
        logging.debug("Trying to compare Classes")
        if isinstance(other, Department):
            logging.info("Returning True if self.Class == other.Class\n")
            return self.name == other.name

        logging.warning("Invalid Instance | NotImplemented Raised\n")
        return NotImplemented

    def __lt__(self, other):
        logging.debug("Trying to compare Classes\n")
        if isinstance(other, Department):
            logging.info("Returning True| class compared\n")
            return self.name < other.name

        logging.warning("Invalid Instance | NotImplemented Raised\n")
        return NotImplemented



"""Testing Cases from Json File(Assignments)"""

if __name__ == "__main__":
    """Create different employee types"""

    dp = Department("Engineering")
    fake = Faker()
    languages = ['Python', 'Java', 'JavaScript', 'C++', 'Ruby', 'Go', 'Rust']
    while len(dp.emps) < 100:
        dp.set_emp(Developer(fake.name(), fake.email(),
                             random.randint(100, 1000),
                             random.randint(3000, 5000),
                             set(fake.random_element(elements=languages) for _ in range(random.randint(1, 5))),
                             fake.password()))

        dp.set_emp(Manager(fake.name(), fake.email(),
                           random.randint(100, 1000),
                           random.randint(3000, 5000),
                           random.randint(5, 20),
                           fake.password()))
    print(repr(dp)) #different employee types created and stored | called by repr

    """Testing inheritance & polymorphism and also Validating encapsulation (private attributes)"""

    dv_1 = Developer("John",
                     "john@example.com",
                     "123",
                     5000,
                     ["Python", "Java", "C++"],
                     "password"
                     )


    mg_1 = Manager("lisa",
                   "lisa@example.com",
                   "456",
                   5000, #Assuming both have same salary in their account
                   5,
                   "password1"
                   )

    dv_1.add_salary(1000, "password")
    mg_1.add_salary(1000, "password1")

    print(f"${dv_1.get_salary(password="password"):.2f}") #both have a calculate bonus method (output: $6500.00)
    print(f"${mg_1.get_salary(password="password1"):.2f}") #but implement it differently (output: $5500.00)
    #This shows inheritance & polymorphism
    #it also shows Validating encapsulation as you would need a password to access salary

    """Test magic methods (sorting, comparison, iteration)"""
    dv_2 = Developer("pam",
                     "pam@example.com",
                     "132",
                     5000,
                     ["Python", "Java", "C++"],
                     "password2"
                     )
    dp.set_emp(mg_1)
    dp.set_emp(dv_1)
    dp.set_emp(dv_2)

    #comparison was set using both an authentication and direct feature
    dp1 = dp.compare_salary_with_auth(dv_2, mg_1,
                                      "password2",
                                      "password1")
    dp2 = dp.get_emp(dv_1) < dp.get_emp(mg_1)
    dp3 = dp.get_emp(dv_1) > dp.get_emp(mg_1)
    print(dp1) #output(True)
    print(dp2) #output(False)
    print(dp3) #output(True)

    #iteration can also be used
    for x in dp:
        print(x)

    #finally sorting is also applicable
    emps = [dv_1, dv_2, mg_1]
    emps.sort()
    for emp in emps:
        print(emp)



