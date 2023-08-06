PyTaskmaster
============

Simple way to create build script on python.

Features
--------

  - CLI tool for launch task
  - Config manager on JSON files
  - Generator for configuration headers

Usage
-----

Create `master.py` in project folder or use `master -t` for create template
`master.py`.

See `master -h` for more information.

For zsh users
-------------

.. code:: shell

          _master() {
              typeset -A opt_args

              __get_tasks() {
                  file="master.py"
                  if [ -n "${opt_args[-f]}" ];
                  then
                      eval file="${opt_args[-f]}"
                  fi
                  if [ -n "${opt_args[--file]}" ];
                  then
                      eval file="${opt_args[--file]}"
                  fi
                  tasks_command="ls $file 2>/dev/null 1>/dev/null && master -f \"${file}\" -s"
                  eval ${tasks_command} 2>/dev/null | grep '^  [a-zA-Z]' | while read -r a b; do echo $a$b | sed 's/^[\ \t]* \([a-zA-Z]\)/\1/g' | sed 's/[\ \t]*--\(.*\)/:\1/g'; done;
              }

              __tasks() {
                  local -a tasks
                  tasks=(${(fo)"$(__get_tasks)"})
                  _describe 'tasks' tasks
              }

              _arguments '(-h --help)'{-h,--help}'[show this help message and exit]' \
                         '(-s --show-tasks)'{-s,--show-tasks}'[show all tasks from master file]' \
                         '(-f --file)'{-f,--file}'[use custom FILE for run tasks]:file:_files' \
                         '(-t --template)'{-t,--template}'[create `master.py` from template]' \
                         '1::tasks:__tasks' \
                         '2::files:_files'
          }

          compdef _master master

Source code
-----------

You can access the source code at: https://github.com/Plambir/pytaskmaster

Release History
---------------

1.1.0 (2015-05-18)
------------------

  - Add CLI script
  - Refactoring `pytaskmaster` module

1.0.0 (2015-03-15)
------------------

First working version


