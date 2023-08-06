# Yet Another Option Parser

A simple and light library that handle both command line parsing
and config file reading.

The only thing you have to do, is to describe (throught a YAML resource /
config file) all options and parameters your main function expects.

This way, you only describe what to do, and not how to do it.

Every is done under the hood ; a simple call to the library handle :

  - application banner and help screen printing
  - command line parsing
  - building of dictionnary that hold configuration (flags, options and parameters values)
  - parsing optional config file that will override default values
  - etc.

Please be warned, that the library is in pre-alpha stage (for a short time),
until full documentation will be written : so package don't contains all
source files yet.

## Installation

Via pip :
```sh
pip install yaop
```

Or wheel :
```sh
pip install https://pypi.python.org/packages/<not yet>/yaop-0.1.whl
```

Or setuptools :
```sh
easy_install https://pypi.python.org/packages/<not yet>/yaop-0.1.egg
```

Or :
```sh
easy_install https://pypi.python.org/packages/14/1b/f1c7696e27e993c94f1ede69f48a3a71b8b00fd24cd490d86b5d2924b63c/yaop-0.1.tar.gz#md5=74ecf214cc2b7bff99476afcd005a2c3
```

Or via source code, available at github :
[https://github.com/Aygos/yaop.git](https://github.com/Aygos/yaop.git).

Or via direct download :

```sh
curl https://github.com/Aygos/yaop/archive/master.zip
```

And follow common `setup.py` and `setuptools` build and installation procedures.

## Usage

First you need to instruct your main script to instanciate a `cmdline`
instance object, and execute it to call your application entry point (function
`main()` by default). For example your `my_app.py` could look like :

```python
#!/usr/bin/python

"""My first application using library 'cmdline' to automate command line options handling and config file parsing."""

from yaop import cmdline

if __name__ == '__main__':
    def main(cmdline):
        print '- processed command line is :'
        print cmdline
    
    cfg = cmdline()
    cfg.run()
```

Note that `main()` global function will be automatically called from inside
`cfg.run()`.

Second you need to create a file containing the meta-description of all
the command line options (and parameters) that your application expects.
This file must be in `YAML` format (because it's sensibly clearer than `JSON`) :

Sample of a near minimal meta-description file `my_app.yml` :

```yaml
# --- meta-description of the application
app:
  name: my_app
  desc: My first application using yaop library
  version: '1.0'
  date: May 2016
# --- here comes pure options (with flags, order doesn't matter)
opts:
  help:
    action: help()
    desc: print this help screen
  opt_flag:
    flag: -f
    type: bool
    desc: a flag switch
  opt_str:
    flag: -s
    default: a string
    desc: optional string option
  opt_int:
    flag: -i
    default: 123
    desc: optional integer option
# --- here comes pure parameters (no flags, order is meaningfull)
params:
  param_str_not_opt:
    default: another string
    desc: a (not optional) string parameter
  param_int:
    default: 456
    optional: true
```

Additionnaly you could, if you wish, override default values in a
`config.yml` config file :

```yaml
opt_flag: false
opt_str: modified string
opt_int: 321
# param_str_not_opt: # default value is kept untouched ('another string')
param_int: 789
```

Parameters differs from options, in the way that they represents all remaining
command line arguments after the last option flag. So, by definition, they
will never have any command line flag associated with them.

Finaly, a typical python test session, could be :

```sh
bash> ./my_app

usage : my_app [ -<option> ... ] <param_str_not_opt> <param_int>

options :
  -h | --help         : print this help screen
  -f | --opt_flag     : a flag switch
  -s | --opt_str      : optional string option
  -i | --opt_int      : optional integer option
  <param_str_not_opt> : a (not optional) string parameter
  <param_int>         : param_int


<< ERROR : missing argument variable [param_str_not_opt] on command line >>```
```

`param_str_not_opt` is not optional, so :

```sh
bash> ./my_app.py "another modified string"

my_app - My first application using yaop library
v1.0 - May 2016 - from & by C.B.

- processed command line is :
cmdline([('help', False),
         ('opt_flag', False),
         ('opt_str', 'modified string'),
         ('opt_int', 321),
         ('param_str_not_opt', 'another modified string'),
         ('param_int', 789)])
```

And testing additionals options, gives :

```sh
bash> ./my_app.py -f -i 007 "another modified string"

my_app - My first application using yaop library
v1.0 - May 2016 - from & by C.B.

- processed command line is :
cmdline([('help', False),
         ('opt_flag', True),
         ('opt_str', 'modified string'),
         ('opt_int', 7),
         ('param_str_not_opt', 'another modified string'),
         ('param_int', 789)])
```

## Documentation

User and reference manuals : [documentation](manual.html).

## Credits

Designed, coded, developped, tested and documented by Aygos - May 2016.

## License

This creation is provided according terms of the Licence Creative Commons
BY-NC-ND - Attribution - Non-commercial - No Derivates Works - 4.0 - International.

Please contact me by [e-mail](mailto:cyrilb01@sfr.fr) if you wish to propose new feature, submit bug
report or do derivates works.
