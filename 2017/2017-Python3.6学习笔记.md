---
title: Python 3.6 学习笔记
subtitle: p3note
date: 2017-10-25 10:21:00
tags: Python
---

<!--# Python 3.6 学习笔记-->

# IDE

Coding with [Atom](http://atom.io/).

Coding with Sublime Text3

I used PyCharm.

# Function

Catching exception with `try...except...`

```
try:
	...
except:
	...
```

# String

A string is a sequence.

`len()` to get length of string.

* `ord` char to ASCII
* `chr` ASCII to char


### String slices

```
>>> s = 'Monty Python'
>>> print(s[0:5])
Monty
>>> print(s[6:12])
Python
```

* omit the first index means that it starts at begining of the string.
* omit the second index means that the slice goes to the end of the string.
* if first index is greater than or equal to the second index, the result is empty string.

I guess it work like that :

```
s[A,B]
if(A<0)A=0
if(B>length)B=length
if(A>B)A=B
if(B<A)B=A
return s->subString(A,B)
```

### Strings are imutable

The best you can do is create a new string that is a variation on the original.


### The `in` operator

```
>>> 'a' in 'banana'
True
>>> 'seed' in 'banana'
False
```

### `string` methods

More documents at [https://docs.python.org/3.5/library/stdtypes.html#string-methods](https://docs.python.org/3.5/library/stdtypes.html#string-methods)

`dir()` to show all functions of type

```
['capitalize', 'casefold', 'center', 'count', 'encode',
'endswith', 'expandtabs', 'find', 'format', 'format_map',
'index', 'isalnum', 'isalpha', 'isdecimal', 'isdigit',
'isidentifier', 'islower', 'isnumeric', 'isprintable',
'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower',
'lstrip', 'maketrans', 'partition', 'replace', 'rfind',
'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip',
'split', 'splitlines', 'startswith', 'strip', 'swapcase',
'title', 'translate', 'upper', 'zfill']
```

`strip()` remove white space (spaces, tabs newlines) from the beginning and endof a string.

### Format operator

When applied to integers , `%` is a modulus operator, but when first operand is a string, `%` is the format operator.

```
>>> camels = 42
>>> '%d' % camels
'42'
```

A format sequence can appear anywhere in the string, so you can embed a value in a sentence:

```
>>> camels = 42
>>> 'I have spotted %d camels.' % camels
'I have spotted 42 camels.'
```

The second argument also can be a tuple:

```
>>> 'In %d years I have spotted %g %s.' % (3, 0.1, 'camels')
'In 3 years I have spotted 0.1 camels.'
```


# Files

### Persistence

#### Opening files

```
open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
    Open file and return a stream.  Raise IOError upon failure.
    
    file is either a text or byte string giving the name (and the path
    if the file isn't in the current working directory) of the file to
    be opened or an integer file descriptor of the file to be
    wrapped. (If a file descriptor is given, it is closed when the
    returned I/O object is closed, unless closefd is set to False.)
    
    mode is an optional string that specifies the mode in which the file
    is opened. It defaults to 'r' which means open for reading in text
    mode.  Other common values are 'w' for writing (truncating the file if
    it already exists), 'x' for creating and writing to a new file, and
    'a' for appending (which on some Unix systems, means that all writes
    append to the end of the file regardless of the current seek position).
    In text mode, if encoding is not specified the encoding used is platform
    dependent: locale.getpreferredencoding(False) is called to get the
    current locale encoding. (For reading and writing raw bytes use binary
    mode and leave encoding unspecified.) The available modes are:
    
    ========= ===============================================================
    Character Meaning
    --------- ---------------------------------------------------------------
    'r'       open for reading (default)
    'w'       open for writing, truncating the file first
    'x'       create a new file and open it for writing
    'a'       open for writing, appending to the end of the file if it exists
    'b'       binary mode
    't'       text mode (default)
    '+'       open a disk file for updating (reading and writing)
    'U'       universal newline mode (deprecated)
    ========= ===============================================================
```

### Searching through a files

* use str.startwidth:

```
fhand = open('mbox-short.txt')
count = 0
for line in fhand:
    if line.startswith('From:'):
        print(line)
```

* use str.find:

```
fhand = open('mbox-short.txt')
for line in fhand:
    line = line.rstrip()
    if line.find('@uct.ac.za') == -1: continue
    print(line)
```

### Writing files

* open with mode `w`, If the file already exists, opening it in write mode `clears out the old data and starts fresh`, so be careful! If the file doesn't exist, a new one is created.
* `write` method does't add the newline automatically.
* using `close` to make sure the last bit of data is phsically written to the disk.

### Debugging

* use `repr` to display string whitch contain whitespace/tabs/newlines.

If there are whitespace/tabs/newlines charactor in a string, it's hard to read, because of it's invisable. Use built-in function `repr` can help:

```
>>> print(repr(s))
'1 2\t 3\n 4'
```

# Lists

* List is a sequence
* A list whitin another list is nested.
* A list the contains no elements is clled an empty list, use `[]` to create one.
* **Lists are mutable**
* If you try to read or write an element that does not exist, you get an `IndexError`.
* **If an index has a negative value, it counts backward from the end of the list.**
* A for loop over an empty list never executes the body.


### List operations

* The `+` operator concatenates lists
* The `*` operator repeats a list a given number of time

### List slices

```
>>> t = ['a', 'b', 'c', 'd', 'e', 'f']
>>> t[1:3]
>>> t[:4]
>>> t[3:]
>>> t[:] #return all
```

A slice operator on the left side of an assignment can update multiple elements:

```
>>> t = ['a', 'b', 'c', 'd', 'e', 'f']
>>> t[1:3] = ['x', 'y']
>>> print(t)
['a', 'x', 'y', 'd', 'e', 'f']
```

### List methods

* `append` adds a new elements to the end of a list
* `extend` takes a list as an argument and appends all of the elements
* `sort` arranges the elements of the list from low to hight
* `pop(index=None)` remove object at index and return the object removed.
* `del` delete the element without return. `del t[1]`,`del t[1:3]`.
* `remove(value)` remove the element you want to remove(but not the index).return`None`
* 
* Most list methods are void; they modify the list and return `None`. If you accidentally write `t = t.sort()`, you will be disappointed with the result.

### Lists and functions

```
>>> nums = [3, 41, 12, 9, 74, 15]
>>> print(len(nums))
6
>>> print(max(nums))
74
>>> print(min(nums))
3
>>> print(sum(nums))
154
>>> print(sum(nums)/len(nums))
25
```

* `sum()` function only works when the list elements are numbers. `max() len()` etc.


### Lists and strings

A string is a sequence of characters and a list is a sequence of values, but a list of characters is not the same as a string. 

* Conver string to list use `list` or `split`
* Conver list to string use `join()->List`

### Parsing lines

* `split` method is very effective when faced with the problem that reading lines of file and extract what we want.

### Objects and values

```
>>> a = 'banana'
>>> b = 'banana'
>>> a is b
True

>>> a = [1, 2, 3]
>>> b = [1, 2, 3]
>>> a is b
False
```

Aliasing:

```
>>> a = [1, 2, 3]
>>> b = a
>>> b is a
True
>>> b[0] = 17
>>> print(a)
[17, 2, 3]
```

### List arguments

* `append` method modifies a list, but the `+` operator creates a new list
* slices operator creates a new list, haven't effect on the original list

### Debugging

###### 1 Don't forget that most list methods modify the argument and return None.

```
word = word.strip()    # WRONG!
t.append([x])          # WRONG!
t = t.append(x)        # WRONG!
t + [x]                # WRONG!
t = t + x              # WRONG!
```

###### 2 Pick an idiom and stick with it.

```
t.append(x)
t = t + [x]
```

###### 3 Make coples to avoid aliasing.

If you want to use a method like sort that modifies the argument, but you need to keep the original list as well, you can make a copy.

```
orig = t[:]
t.sort()
```

or use the built-in function `sorted` 

```
>>> A = list("123456789")
>>> A = list("9234567890")
>>> B = sorted(A)
>>> A
['9', '2', '3', '4', '5', '6', '7', '8', '9', '0']
>>> B
['0', '2', '3', '4', '5', '6', '7', '8', '9', '9']

```

###### 4 Lists, `split`, and files


# Dictionaries

The dictionary is similary with JSON and Objc and Swift

* `len` return the number of key-value pairs.
* `in` only check the key.
* Dictionary as a set of counters
* `get` method return a key-value pair. If key doesn't exist return 0.

# Tuples

Tuples like a list but it's **immutable**.

```
>>> t = 'a', 'b', 'c', 'd', 'e'
>>> t = ('a', 'b', 'c', 'd', 'e') # Should do
>>> t = tuple('lupins')
>>> print(t)
('l', 'u', 'p', 'i', 'n', 's')
```

**Without the comma Python treats ('a') as an expression with a string in parentheses that evaluates to a string:**

```
>>> t2 = ('a')
>>> type(t2)
<type 'str'>
```


Most list operators also work on tuples. 

```
>>> t = ('a', 'b', 'c', 'd', 'e')
>>> print(t[0])
'a'

>>> print(t[1:3])
('b', 'c')

>>> t = ('A',) + t[1:]
>>> print(t)
('A', 'b', 'c', 'd', 'e')
```

### Comparing tuples

Python starts by comparing the first element from each sequence.

```
>>> (0, 1, 2) < (0, 3, 4)
True
>>> (0, 1, 2000000) < (0, 3, 4)
True
```
* So it can use to sort element

```
txt = 'but soft what light in yonder window breaks'
words = txt.split()
t = list()
for word in words:
    t.append((len(word), word))

t.sort(reverse=True)

res = list()
for length, word in t:
    res.append(word)

print(res)

['yonder', 'window', 'breaks', 'light', 'what',
'soft', 'but', 'in']
```

### Tuple assignment

```
listA = ["aaa", "bbb"]
(a,b) = listA
print(a)
aaa
print(b)
bbb
```


A particularly clever application of tuple assignment allows us to swap the values of two variables in a single statement:

```
>>> a, b = b, a
```


* right must be list or tuple, and the number of element must equal the left's.


### Dictionaries and tuples

* dictionary's `items` method return tuple (key,value)

### Using tuples as keys in dictionaries

```
directory[last,first] = number
```

```
for last, first in directory:
    print(first, last, directory[last,first])
```

