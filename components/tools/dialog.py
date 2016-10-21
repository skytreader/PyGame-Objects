class DialogSection(object):
    
    def __init__(self, prompt, reply, cont):
        self.prompt = prompt
        self.reply = reply
        self.cont = cont

    def __str__(self):
        return "\n\n".join((self.prompt, self.reply, self.cont))

class BranchingDialog(object):
    
    def __init__(self, sections, start):
        self.sections = sections
        self.start = start

    def __str__(self):
        aggregate = []

        if self.start:
            aggregate.append("START:%s" % self.start)
        else:
            aggregate.append("START:")

        for section in self.sections.keys():
            aggregate.append("[%s]" % section)
            aggregate.append(str(self.sections[section]))

        return "\n\n".join(aggregate)
