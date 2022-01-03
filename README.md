# task
1) The Single-responsibility principle (SRP): “A class should have one, and only one, reason to change” In other words, every component of your code (in general a class, but also a function) should have one and only one responsibility. As a consequence of that, there should be only a reason to change it. Too often you see a piece of code that takes care of an entire process all at once. I.e., A function that loads data, modifies and, plots them, all before returning its result.
import numpy as np

def math_operations(list_):
    # Compute Average
    print(f"the mean is {np.mean(list_)}")
    # Compute Max
    print(f"the max is {np.max(list_)}") 

math_operations(list_ = [1,2,3,4,5])

#after_SRP:

def get_mean(list_):
    '''Compute Mean'''
    print(f"the mean is {np.mean(list_)}") 

def get_max(list_):
    '''Compute Max'''
    print(f"the max is {np.max(list_)}") 

def main(list_): 
    # Compute Average
    get_mean(list_)
    # Compute Max
    get_max(list_)

main([1,2,3,4,5])

Now, you would only have one single reason to change each function connected with “main”.
The result of this simple action is that now:1)It is easier to localize errors. Any error in execution will point out to a smaller section of your code, accelerating your debug phase.
2)Any part of the code is reusable in other section of your code.
3)Moreover and, often overlooked, is that it is easier to create testing for each function of your code. Side note on testing: You should write tests before you actually write the script. But, this is often ignored in favour of creating some nice result to be shown to the stakeholders instead.


2) The Open–closed principle (OCP):“Software entities … should be open for extension but closed for modification”.In other words: You should not need to modify the code you have already written to accommodate new functionality, but simply add what you now need.This does not mean that you cannot change your code when the code premises needs to be modified, but that if you need to add new functions similar to the one present, you should not require to change other parts of the code.To clarify this point let’s refer to the example we saw earlier. If we wanted to add new functionality, for example, compute the median, we should have created a new method function and add its invocation to “main”. That would have added an extension but also modified the main.
We can solve this by turning all the functions we wrote into subclasses of a class. In this case, I have created an abstract class called “Operations” with an abstract method “get_operation”. (Abstract classes are generally an advanced topic. If you don’t know what an abstract class is, you can run the following code even without).
Now, all the old functions, now classes are called by the __subclasses__() method. That will find all classes inheriting from Operations and operate the function “operations” that is present in all sub-classes.
import numpy as np
from abc import ABC, abstractmethod

class Operations(ABC):
    '''Operations'''
    @abstractmethod
    def operation():
        pass

class Mean(Operations):
    '''Compute Max'''
    def operation(list_):
        print(f"The mean is {np.mean(list_)}") 

class Max(Operations):
    '''Compute Max'''
    def operation(list_):
        print(f"The max is {np.max(list_)}") 

class Main:
    '''Main'''
    @abstractmethod
    def get_operations(list_):
        # __subclasses__ will found all classes inheriting from Operations
        for operation in Operations.__subclasses__():
            operation.operation(list_)


if __name__ == "__main__":
    Main.get_operations([1,2,3,4,5])
If now we want to add a new operation e.g.: median, we will only need to add a class “Median” inheriting from the class “Operations”. The newly formed sub-class will be immediately picked up by __subclasses__() and no modification in any other part of the code needs to happen.
The result is a very flexible class, that requires minimum time to be maintained.

3)The Liskov substitution principle (LSP):“Functions that use pointers or references to base classes must be able to use objects of derived classes without knowing it”.
Alternatively, this can be expressed as “Derived classes must be substitutable for their base classes”.
In (maybe) simpler words, if a subclass redefines a function also present in the parent class, a client-user should not be noticing any difference in behaviour, and it is a substitute for the base class.For example, if you are using a function and your colleague change the base class, you should not notice any difference in the function that you are using.

The Interface Segregation Principle (ISP):“Many client-specific interfaces are better than one general-purpose interface”
In the contest of classes, an interface is considered, all the methods and properties “exposed”, thus, everything that a user can interact with that belongs to that class.
In this sense, the IS principles tell us that a class should only have the interface needed (SRP) and avoid methods that won’t work or that have no reason to be part of that class.This problem arises, primarily, when, a subclass inherits methods from a base class that it does not need.
import numpy as np
from abc import ABC, abstractmethod

class Mammals(ABC):
    @abstractmethod
    def swim() -> bool:
        print("Can Swim") 

    @abstractmethod
    def walk() -> bool:
        print("Can Walk") 

class Human(Mammals):
    def swim():
        return print("Humans can swim") 

    def walk():
        return print("Humans can walk") 

class Whale(Mammals):
    def swim():
        return print("Whales can swim") 
For this example, we have got the abstract class “Mammals” that has two abstract methods: “walk” and “swim”. These two elements will belong to the sub-class “Human”, whereas only “swim” will belong to the subclass “Whale”.And indeed, if we run this code we could have:
Human.swim()
Human.walk()

Whale.swim()
Whale.walk()

# Humans can swim
# Humans can walk
# Whales can swim
# Can Walk
The sub-class whale can still invoke the method “walk” but it shouldn’t, and we must avoid it.
The way suggested by ISP is to create more client-specific interfaces rather than one general-purpose interface. So, our code example becomes:
from abc import ABC, abstractmethod

class Walker(ABC):
  @abstractmethod
  def walk() -> bool:
    return print("Can Walk") 

class Swimmer(ABC):
  @abstractmethod
  def swim() -> bool:
    return print("Can Swim") 

class Human(Walker, Swimmer):
  def walk():
    return print("Humans can walk") 
  def swim():
    return print("Humans can swim") 

class Whale(Swimmer):
  def swim():
    return print("Whales can swim") 

if __name__ == "__main__":
  Human.walk()
  Human.swim()

  Whale.swim()
  Whale.walk()

# Humans can walk
# Humans can swim
# Whales can swim
This principle is closely connected with the other ones and specifically, it tells us to keep the content of a subclass clean from elements of no use to that subclass. This has the final aim to keep our classes clean and minimise mistakes.
The Dependency Inversion Principle (DIP):“Abstractions should not depend on details. Details should depend on abstraction. High-level modules should not depend on low-level modules. Both should depend on abstractions”So, that abstractions (e.g., the interface, as seen above) should not be dependent on low-level methods but both should depend on a third interface.To better explain this concept, I prefer to think of a sort of information flow.
Imagine that you have a program that takes in input a specific set of info (a file, a format, etc) and you wrote a script to process it.
What would happen if that info were subject to changes?
You would have to rewrite your script and adjust the new format. Losing the retro compatibility with the older files.
However, you could solve this by creating a third abstraction that takes the info as input and passes it to the others.
This is basically what an API is also, used for.
