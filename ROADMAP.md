### https://pymotw.com/2/cmd/

- complete_ to get list of fw IP addresses ir names
- last_output = '' self.last_output
- Commands from sys.argv
    import sys
    if len(sys.argv) > 1:
        InteractiveOrCommandLine().onecmd(' '.join(sys.argv[1:]))
    else:
        InteractiveOrCommandLine().cmdloop()