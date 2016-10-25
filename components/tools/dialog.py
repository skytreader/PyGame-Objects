from components.framework_exceptions import MalformedDialogException

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

        if sections and ("START" in sections.keys() or "END" in sections.keys()):
            raise MalformedDialogException("Special START/END sections must not be specified.")

        self.sections = sections
        self.start = start

    def __str__(self):
        aggregate = []

        if self.start:
            aggregate.append("[START]\n%s" % self.start)
        else:
            aggregate.append("[START]\n")

        for section in self.sections.keys():
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
