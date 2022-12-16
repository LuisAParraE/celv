# celv

## What is celv?

celv is a persistent data structure that emulates how git functions. It is our second project on Algorithm Design I.

## How it works?

We first map a local folder on our system (This only charges the names on ram memory for usage, it doesn't affect the actual file or folder), to create a persistent tree with the names of the folders and files. Then we map it into our 2 local clases **Directory** and **File**, yeah a really unique names, and begin to construct our tree in a recursive way. After that you can navigate the tree and interact with it, on the local repl created for it.

## Requirements

- Python 3+
- Free Time to test

## How to use It.

Just run the command:

```console
python celv.py
```

or

```console
python3 celv.py
```

Then the program will start and you can begin to interact with it. You can write `help` on the repl and it will display the available commands you can use, with a simple example format. You should first use `celv_importar(<Pc path>)` with a path you want to create a new tree. From then you can use `celv_iniciar()` if you want to create the persisten tree. After thar, you cam move through folders with `ir()`. For more info, use `help` command.

## Modules Used

### Safelock.py

**Safelock.py** on Resources Folder just contain Safelock Class, used to save data that has change on the node or that affect it on one way or another. It contains the mutable attributes of **file** and **directory**.

### DirectoryAndFile

Here we can find two clases, **file** and **directory**, in addition to **safelock** this 3 classes are basically our core information storage. Directory has the unique attibute of _children_ this is a list that contains all elements that this directory is pointin towards, this element can be other directories or files. File has the unique atribute of _content_ this attribute contains as her name sais, just a string simulating context in the file. Both of them aren't actual data in your pc, so destroying it or changing it won't affect your actual files.

### TreeFilesFunctions

This file Contains all the Brain of the system. It has all the functions this program needs to work.

## Implementation

-

## Last Words

- Thanks to Professor [Monascal](https://github.com/rmonascal) for this great Course.
