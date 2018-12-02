The package distributions is supposed to get a needed distribution function of files by their size
according parameters that are set.
The central module of this package is dist.py which implements selection the distribution function
using 'form' parameter.

Modules:
linear_decay.py - constructs distribution kind of f(x)=A*x+B, where A<0, B>0
exp_decay.py - distribution kind of f(x) = A*exp(-alpha*x)-C, where A, alpha, C > 0
user_distribution.py - builds the function according user data, which loaded to file 'user_distribution_example'