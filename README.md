### what

This CLI has a dual purpose:

1. As an evaluator, to design new coding challenges. Initialize it in a new directory and it will ask for:
    1. the boilerplate (e.g. `flask-api`) you want to use to design it
    2. the boilerplates (e.g. `flask-api` or `express-api`) candidates are allowed to use to solve it

2. As a candidate, to switch out the boilerplate you want to use to solve a coding challenge.
    * It will show you a list of files that will be added/deleted before continuing.
    * If you want to keep certain files, consider doing a `git add file-to-keep.txt` and `git stash` before running it.


### develop

To run locally

```sh
make
```

To install locally

```sh
make install

# use it in a new directory
mkdir foo
cd foo
ot
```
