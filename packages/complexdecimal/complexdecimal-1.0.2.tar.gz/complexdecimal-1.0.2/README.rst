ComplexDecimal
=======================

A project designed to extend python's Decimal library to the complex numbers.
This project comes with support for many complex number functions.

----

Basic usage:
```json
from complexdecimal import ComplexDecimal

a = ComplexDecimal(10) #Creates a ComplexDecimal = 10+0i
b = ComplexDecimal("3",Decimal(5)) #Creates a ComplexDecimal = 3+5i

print a+b #13+5i
print a.log10() #1
```

More functions can be found on the wiki at
https://github.com/Bowserinator/ComplexDecimal/wiki

