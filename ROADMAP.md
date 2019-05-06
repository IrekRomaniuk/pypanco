### [Doc](https://pymotw.com/2/cmd/)

- Autocompletion *complete_* to get list of fw IP addresses or names or tags
- *last_output* = '' *self.last_output* for jobid
- Commands from sys.argv
    ```
    import sys
    if len(sys.argv) > 1:
        InteractiveOrCommandLine().onecmd(' '.join(sys.argv[1:]))
    else:
        InteractiveOrCommandLine().cmdloop()
    ```    