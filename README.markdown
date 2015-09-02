# Pelita demo player module

## Notes on writing

* Please use Python 3
* Numpy is pre-installed on the tournament machine; everything else must be negotiated
* Please use relative imports inside your module
* You may need to set the PYTHONPATH to point to the main pelita directory

## Files

### team/

The main module which contains all your team’s code. Please use relative imports from inside the module.

### team/__init__.py

Builds the final teams and exports the factory methods. When using the module on the command line, such as in

    pelitagame ../path/to/module/team

the method named `factory` is automatically called. Different methods can be specified with a colon

    pelitagame ../path/to/module/team:other_factory

### team/demo_player.py

Contains the code for a simple `DrunkPlayer`.

### team/utils/helper.py

This could be a good place for global utility functions (but feel free to add more files for this, if needed)

### team/utils/__init__.py

Needed to export the helper file.

### test/test_drunk_player.py

Simple unittest for your player. Note the relative imports. You can run tests using nosetests or py.test, which automatically executes all tests in the `test/` directory.

    $ nosetests test/
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.025s
    
    OK


