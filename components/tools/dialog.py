from components.framework_exceptions import MalformedDialogException

import re

class DialogSection(object): 
    def __init__(self, prompt, reply, cont):
        """
        Where prompt and reply are dialog strings while cont is a list of strings.
        """
        self.prompt = prompt
        self.reply = reply
        self.cont = cont

    def __enum_cont(self):
        return ", ".join(self.cont)

    def __str__(self):
        # All these conditionals are necssary to handle the START section
        if self.reply:
            return "\n\n".join((self.prompt, self.reply, self.__enum_cont()))
        elif self.prompt:
            return "\n\n".join((self.prompt, self.__enum_cont()))
        else:
            return "\n%s" % self.__enum_cont()

    def __eq__(self, other):
        try:
            return (self.prompt == other.prompt and self.reply == other.reply and
              frozenset(self.cont) == frozenset(other.cont))
        except:
            return False

    def __hash__(self):
        return hash((self.prompt, self.reply, frozenset(self.cont)))

class BranchingDialog(object):
    
    def __init__(self, sections, start):
        """
        sections - dictionary of labels to sections. The labels START and END
        should not be used. May be empty or None.
        start - the special START section.
        """
        if start.reply is not None:
            raise MalformedDialogException("The START section's reply should be None.")

        if sections and ("START" in list(sections.keys()) or "END" in list(sections.keys())):
            raise MalformedDialogException("Special START/END sections must not be specified.")

        end_found = "END" in start.cont

        if not end_found and sections:
            for label in list(sections.keys()):
                if "END" in sections[label].cont:
                    end_found = True
                    break

        if not end_found:
            raise MalformedDialogException("No section leads to END.")

        self.sections = sections
        self.start = start

    def __str__(self):
        aggregate = []

        if self.start:
            aggregate.append("[START]\n%s" % self.start)
        else:
            aggregate.append("[START]\n")

        for section in list(self.sections.keys()):
            aggregate.append("[%s]" % section)
            aggregate.append(str(self.sections[section]))

        return "\n\n".join(aggregate)

    def __eq__(self, other):
        try:
            return self.sections == other.sections and self.start == other.start
        except:
            return False

    def __hash__(self):
        return hash((self.sections, self.start))

class BranchingDialogParser(object):
    
    EMPTY_LINE = re.compile(r"^\s*$")
    __LABEL_RE = r"[a-zA-Z_\.\-0-9]+"
    SECTION_DECLARATION = re.compile(r"^\[%s\]$" % __LABEL_RE)
    LABEL_LIST = re.compile(r"^%s(,\s*%s)*$" % (__LABEL_RE, __LABEL_RE))
    
    def parse(self, dialog):
        return self.__parse(dialog.split("\n"))

    def __parse(self, lstring):
        self.__lineno = 0
        l = 0
        def eat_empty_lines():
            while self.__lineno < len(lstring) and BranchingDialogParser.EMPTY_LINE.match(lstring[self.__lineno]):
                self.__lineno += 1

        def get_section(normal=True):
            """
            Assumes that the line pointed to by `lineno` is the start of a
            section.
            """
            eat_empty_lines()
            if BranchingDialogParser.SECTION_DECLARATION.match(lstring[self.__lineno]):
                label = lstring[self.__lineno][1:-1]
                self.__lineno += 1
                eat_empty_lines()

                option = []
                while not BranchingDialogParser.EMPTY_LINE.match(lstring[self.__lineno]):
                    option.append(lstring[self.__lineno])
                    self.__lineno += 1
                option_s = " ".join(option)
                eat_empty_lines()

                reply_s = None
                if normal:
                    reply = []
                    while not BranchingDialogParser.EMPTY_LINE.match(lstring[self.__lineno]):
                        reply.append(lstring[self.__lineno])
                        self.__lineno += 1
                    reply_s = " ".join(reply) if reply else None
                    eat_empty_lines()

                if BranchingDialogParser.LABEL_LIST.match(lstring[self.__lineno]):
                    labels = lstring[self.__lineno].split(r",\s*")
                    labels = re.split(r",\s*", lstring[self.__lineno])
                    self.__lineno += 1
                    return (label, DialogSection(prompt=option_s, reply=reply_s, cont=labels))
                else:
                    raise MalformedDialogException("Failed to parse: expected label list, got: %s" % lstring[self.__lineno])
            else:
                raise MalformedDialogException("Failed to parse: expected section declaration, got: %s" % lstring[self.__lineno])

        sections = {}
        start = get_section(False)[1]

        while self.__lineno < len(lstring):
            _section = get_section()
            sections[_section[0]] = _section[1]

        return BranchingDialog(sections, start)
