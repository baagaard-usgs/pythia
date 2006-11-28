#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


class CommandlineParser(object):


    def parse(self, root, argv=None):
        if argv is None:
            import sys
            argv = sys.argv[1:]

        self._parse(argv, root)

        return


    def __init__(self):
        self.actions = {
            'help': ['?', 'h'],
            'complete': ['c'],
            }
        self.assignment = '='
        self.prefixes = ['--', '-']
        self.separator = '.'

        self.action = None
        self.argv = []
        self.processed = []
        self.unprocessed = []

        import pyre.parsing.locators
        self.locator = pyre.parsing.locators.commandLine()

        import journal
        self._debug = journal.debug("pyre.commandline")

        return


    def _parse(self, argv, root):
        self.action = None
        self.argv = argv
        self.processed = []
        self.unprocessed = []

        while self.argv:
            arg = self.argv.pop(0)
            
            self._debug.line("processing '%s'" % arg)

            # is this an option
            candidate = self._filterNonOptionArgument(arg)
            if candidate is None:
                continue

            candidate = self._filterAction(candidate)
            if candidate is None:
                continue

            lhs, rhs = self._parseArgument(candidate)
            
            # store this option
            self._processArgument(lhs, rhs, root)
            
        self._debug.log()

        return


    def _filterNonOptionArgument(self, arg):
        for prefix in self.prefixes:
            if arg.startswith(prefix):
                self._debug.line("    prefix: '%s starts with '%s'" % (arg, prefix))
                candidate = arg[len(prefix):]
                return candidate
        else:
            # prefix matching failed; leave this argument alone
            self._debug.line("    prefix: '%s' is not an option" % arg)
        self.processed.append(arg)
        return None


    def _parseArgument(self, candidate):
        self._debug.line("    prefix: arg='%s' after prefix stripping" % candidate)

        # check for assignment
        tokens = candidate.split(self.assignment)
        self._debug.line("    tokens: %s" % `candidate`)

        # dangling =
        if len(tokens) > 1 and not tokens[1]:
            self._debug.log("tokens: bad expression: %s" % candidate)
            raise CommandlineParser.CommandlineException("bad expression: '%s': no rhs" % candidate)

        # lhs, rhs
        lhs = tokens[0]
        if len(tokens) > 1:
            rhs = tokens[1]
        else:
            rhs = "true"
        self._debug.line("    tokens: key={%s}, value={%s}" % (lhs,  rhs))

        return lhs, rhs


    def _filterAction(self, candidate):
        for action, args in self.actions.iteritems():
            if candidate in args:
                self.action = action
                self.unprocessed.extend(self.argv)
                self.argv = []
                return None
        return candidate


    def _processArgument(self, key, value, root):
        separator = self.separator
        fields = key.split(separator)
        self._debug.line("    sub: fields=%s" % fields)

        children = []
        for level, field in enumerate(fields):
            if field[0] == '[' and field[-1] == ']':
                candidates = field[1:-1].split(',')
            else:
                candidates = [field]
            self._debug.line("    sub: [%02d] candidates=%s" % (level, candidates))
            children.append(candidates)

        self._storeValue(root, children, value)

        return


    def _storeValue(self, node, children, value):
        self._debug.line("    set: children=%s" % children)
        if len(children) == 1:
            for key in children[0]:
                key = key.strip()
                self._debug.line("    option: setting '%s'='%s'" % (key, value))
                node.setProperty(key, value, self.locator)
            return

        for key in children[0]:
            self._debug.line("    sub: processing '%s'" % key)
            self._storeValue(node.getNode(key), children[1:], value)

        return


    # the class used for reporting errors
    class CommandlineException(Exception):


        def __init__(self, msg):
            self._msg = msg
            return


        def __str__(self):
            return self._msg
            

# version
__id__ = "$Id: CommandlineParser.py,v 1.2 2005/03/10 06:04:50 aivazis Exp $"

#  End of file 
