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

This file Contains all the Brain of the system. It has all the functions this program needs to work. We will talk later on implementation how is the logic of this function. All the behavior of the functions are made here, the most common functions you will find here:

- create new file or directory
- delete file or directory
- write content on files
- read content from files

Also this file contains two more classes **history** and **celvId**. The second one is used for maintain the information, for this purpose it has a collection of all the roots generated for the tree, a version counter for keep track of version generation, a collection of changes made on the tree(a collection of history types), Id for the tree. And then we have history that has the information related of every change made on the tree.

## Implementation

- To differenciate normal trees from persistent trees, at the use of `celv_iniciar()` we create a new celvId that has all the information of the persistent tree, this makes easier to manage different persistent trees. We have all the celvIds objects in a global array inside **treeFilesFunctions.py**. Aside from that for every element in the persisten tree will have its celv atribute set to `TRUE` to make it easy to find if the element is part of a persistent tree or not, and the attribute celvIndex will have as value the ID of the correspondent `celvIds` Id.

- For every change on the tree (write, add or delete) we need to verify constantly if the safelock of the node is empty or not, and verify the version we are using. If the safelock exist, we proceed with the information inside it only if the version of the safe is less or equal than the version we are in. If not we use the base information of the node.

- A problem that was found was the reference to same object using python. Because python doesn't let you the handling of the pointers in a direct way, is needed to create new empty arrays, and then fill it with the elements this takes more time but is the solution founded on this repo, to maintain the references to the same objects, if we just re-assing the list, in the case of the directory the childrens, it will reach some conflict if you just want to manintain the information. Example:

we do the following to keep the same element reference, but change the "wrapper" of the elements:

```console
children = [x,y,z]

newChildrens = []

for element in children:
    newChildren.append(element)
```

-

## Last Words

- Thanks to Professor [Monascal](https://github.com/rmonascal) for this great Course.
