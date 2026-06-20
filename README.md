# Employee Management System
*A password-protected payroll system I built to really understand encapsulation, inheritance, and polymorphism in Python.*

## What this is

So this is one of the bigger projects from my Python learning journey, and it's the one I'm probably most proud of so far.

The premise: a system for managing employees (Developers and Managers in this case), their info, salaries, and bonuses. Nothing groundbreaking on the surface. What I actually cared about was building it the way a real system would need to work, not just a script that technically runs.

## Why I built it this way

- **Salaries are locked behind passwords.** Not "private by convention," actually gated. You can't read or change someone's salary without authenticating first — get the password wrong and you get a `PermissionError`, no exceptions.
- **Printing an object is safe by default.** If you print an employee, their password and salary automatically show as hidden. I didn't want accidental leaks just from debugging with a `print()` statement.
- **Everything gets logged.** Every salary check, every raise, every failed password attempt, it's all written to a rotating log file. A real audit trail, the kind an actual payroll system would need.
- **Managers and Developers calculate bonuses completely differently.** team size for one, number of programming languages for the other. But you call the exact same method, `calculate_bonus()`, on either one. That's polymorphism actually doing something useful, not just for learning.
- **I used `Faker` to generate 100 fake employees** to stress-test the system at a slightly more realistic scale instead of just testing with two or three hardcoded people.

## What it's demonstrating

- Abstract base classes: you can't create a generic "Employee," only a concrete Developer or Manager
- Operator overloading (`@total_ordering`): so employees can be sorted and compared directly
- A reusable `ValidationLayer`: class instead of scattering validation checks everywhere (A nod at the DVOU architecture)
- Custom `__repr__` / `__str__` methods that respect privacy instead of just dumping every attribute

## Stress Note

- Getting the password-gated salary logic and the redacted `__repr__` to behave consistently across two different employee types, took a few (i mean a lot evn with Claudes help) passes before it actually clicked.

## What I'd change later on

- Real password hashing instead of plain string comparison
- Pull the logging setup into its own module instead of having it at the top of the file

## Running it

```bash
pip install -r requirements.txt
python main.py
```

This generates 100 fake employees, runs through raises and salary checks (passwords required), pits two employees against each other in a salary comparison, then sorts and iterates over the department using the operators above.

Check `Enterprise_Employee_Management_System.log` afterward to see the full trail of what happened.