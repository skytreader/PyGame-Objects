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
        return "\n\n".join((self.prompt, self.reply, self.__enum_cont()))

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
