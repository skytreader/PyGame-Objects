# -*- coding: utf-8 -*-

from components.framework_exceptions import MalformedDialogException
from components.tools.dialog import BranchingDialog, BranchingDialogParser, DialogSection

import unittest

class DialogParserTests(unittest.TestCase):
    
    def setUp(self):
        self.sample_dialog = """[START]
Cooper, Fletcher, Miller and Smith live on December 17, 2, 12, 4, 5, …, we want
to the expression metastatement calls the factor and number 5 and returns the
factor metastatement. Then the middle.

lolwat, u_ok, sorrySayThatAgain

[lolwat]
Mr. P.: Now I know them

Norwegian lives in Hanoi where V[i,w] is driven by the term -> factor
metastatement, which identifies the factor metastatement. The next to the
expression, even between the exercise in the expression, evaluates them, and
combines them into a solution. The parser is driven by a higher floor adjacent
to a function that recognizes that the term metastatement, which recognizes
factors.

kfine, u_ok, sorrySayThatAgain

[u_ok]
Edouard Lucas, whom we have a computer to do all of a known as the expression,
evaluates an infix arithmetic expression. When you are welcome to read or run a
suggested solution, or to post your own solution or to post your own solution or
leave it, this variant of the interest of 23. Parentheses may change the order
of.

The Spaniard owns the

lolwat, sorrySayThatAgain, END

[sorrySayThatAgain]
Cooper's. Where does not live on different beverages and placing it back to the
factor metastatement looks for a suggested solution, or to read or to post your
own different pets, drink different pets, drink different beverages and smoke
different brands of

The driver passes the input stream and ) are finished, you are to evaluate an
arithmetic expression, evaluates them, and combines them into a solution. The
parser that identifies each element of the first i ≤ n, where n is the first
tower to the ith object. The program that calculates the sequence of moves is
often with some kind of the most fundamental operations in computing is to the
second. To move four rings and towers were placed on top or the remainder of
moves. When you are finished, you are finished, you are of different national
extractions, own different pets, drink different beverages and smoke different
brands of

kfine, END

[kfine]
Then the expression metastatement, which returns 3 giving a parser that
determines the expression metastatement of the result of an apartment house
that recognizes terms. Then, since the metastatement is complete, so it or leave
it, this puzzle to the third, then move a ring from one tower to the term
metastatement, which returns 3 to the expression metastatement is satisfied
because the term metastatement, which calls the factor | term /

Milk is drunk in the metastatement for expressions expects a term, that function
that recognizes the number is and integer consisting of either the top of a
floor adjacent to Cooper's. Where does not live on either 0 or to post your own
solution or run a factor, and Mr. P. engage in the

END"""
        
        self.start_section = DialogSection(
            prompt="Cooper, Fletcher, Miller and Smith live on December 17, 2, 12, 4, 5, …, we want to the expression metastatement calls the factor and number 5 and returns the factor metastatement. Then the middle.",
            reply=None,
            cont=["lolwat", "u_ok", "sorrySayThatAgain"]
        )
        self.lolwat = DialogSection(
            prompt="Mr. P.: Now I know them",
            reply="Norwegian lives in Hanoi where V[i,w] is driven by the term -> factor metastatement, which identifies the factor metastatement. The next to the expression, even between the exercise in the expression, evaluates them, and combines them into a solution. The parser is driven by a higher floor adjacent to a function that recognizes that the term metastatement, which recognizes factors.",
            cont=["kfine", "u_ok", "sorrySayThatAgain"]
        )
        self.u_ok = DialogSection(
            prompt="Edouard Lucas, whom we have a computer to do all of a known as the expression, evaluates an infix arithmetic expression. When you are welcome to read or run a suggested solution, or to post your own solution or to post your own solution or leave it, this variant of the interest of 23. Parentheses may change the order of.",
            reply="The Spaniard owns the",
            cont=["lolwat", "sorrySayThatAgain", "END"]
        )
        self.sorrySayThatAgain = DialogSection(
            prompt="Cooper's. Where does not live on different beverages and placing it back to the factor metastatement looks for a suggested solution, or to read or to post your own different pets, drink different pets, drink different beverages and smoke different brands of",
            reply="The driver passes the input stream and ) are finished, you are to evaluate an arithmetic expression, evaluates them, and combines them into a solution. The parser that identifies each element of the first i ≤ n, where n is the first tower to the ith object. The program that calculates the sequence of moves is often with some kind of the most fundamental operations in computing is to the second. To move four rings and towers were placed on top or the remainder of moves. When you are finished, you are finished, you are of different national extractions, own different pets, drink different beverages and smoke different brands of",
            cont=["kfine", "END"]
        )
        self.kfine = DialogSection(
            prompt="Then the expression metastatement, which returns 3 giving a parser that determines the expression metastatement of the result of an apartment house that recognizes terms. Then, since the metastatement is complete, so it or leave it, this puzzle to the third, then move a ring from one tower to the term metastatement, which returns 3 to the expression metastatement is satisfied because the term metastatement, which calls the factor | term /",
            reply="Milk is drunk in the metastatement for expressions expects a term, that function that recognizes the number is and integer consisting of either the top of a floor adjacent to Cooper's. Where does not live on either 0 or to post your own solution or run a factor, and Mr. P. engage in the",
            cont=["END"]
        )

        sections = {}
        sections["lolwat"] = self.lolwat
        sections["kfine"] = self.kfine
        sections["u_ok"] = self.u_ok
        sections["sorrySayThatAgain"] = self.sorrySayThatAgain

        self.branching_dialog = BranchingDialog(sections, self.start_section)

    def test_eq(self):
        sections = {}
        sections["lolwat"] = self.lolwat
        sections["kfine"] = self.kfine
        sections["u_ok"] = self.u_ok
        sections["sorrySayThatAgain"] = self.sorrySayThatAgain
        bd = BranchingDialog(sections, self.start_section)

        self.assertEqual(self.branching_dialog, bd)

    def test_parsing(self):
        parser = BranchingDialogParser()
        self.assertEqual(self.branching_dialog, parser.parse(self.sample_dialog))

    def test_regexes(self):
        self.assertTrue(BranchingDialogParser.EMPTY_LINE.match(""))
        self.assertTrue(BranchingDialogParser.EMPTY_LINE.match(" "))
        self.assertTrue(BranchingDialogParser.EMPTY_LINE.match("\t"))
        self.assertFalse(BranchingDialogParser.EMPTY_LINE.match("__"))

        self.assertTrue(BranchingDialogParser.SECTION_DECLARATION.match("[START]"))
        self.assertTrue(BranchingDialogParser.SECTION_DECLARATION.match("[spam]"))
        self.assertTrue(BranchingDialogParser.SECTION_DECLARATION.match("[a12_-bb.ae]"))
        self.assertFalse(BranchingDialogParser.SECTION_DECLARATION.match("[new section]"))
        self.assertFalse(BranchingDialogParser.SECTION_DECLARATION.match("newsection"))
        self.assertFalse(BranchingDialogParser.SECTION_DECLARATION.match("[spam,]"))

        self.assertTrue(BranchingDialogParser.LABEL_LIST.match("something"))
        self.assertTrue(BranchingDialogParser.LABEL_LIST.match("spam1, spam2"))
        self.assertTrue(BranchingDialogParser.LABEL_LIST.match("spam2,spam2"))
        self.assertTrue(BranchingDialogParser.LABEL_LIST.match("spam1,    spam2"))
        self.assertTrue(BranchingDialogParser.LABEL_LIST.match("spam1,\tspam2"))
        self.assertFalse(BranchingDialogParser.LABEL_LIST.match("spam1 spam2"))
        
        self.assertTrue(BranchingDialogParser.LABEL_LIST.match("lolwat, u_ok, sorrySayThatAgain"))

class BranchingDialogTests(unittest.TestCase):
    
    def setUp(self):
        self.simple_dialog = """[START]
hi

hello, yay, END

[yay]

yay

awesome

END

[hello]

hello

um

yay, END"""
        self.simple_startless = """[START]

hello, yay, END

[yay]

yay

awesome

END

[hello]

hello

um

yay, END"""
        
        self.start = DialogSection(prompt="hi", reply=None, cont=["hello", "yay", "END"])
        self.startless = DialogSection(prompt=None, reply=None, cont=["hello", "yay", "END"])
        self.hello = DialogSection(prompt="hello", reply="um", cont=["yay", "END"])
        self.yay = DialogSection(prompt="yay", reply="awesome", cont=["END"])

    def test_construction_exceptions(self):
        with self.assertRaises(MalformedDialogException):
            spam_start = DialogSection(prompt="hi", reply="hello", cont="END")
            BranchingDialog(None, spam_start)

        with self.assertRaises(MalformedDialogException):
            spam_start = DialogSection(prompt="abc", reply="def", cont="END")
            sections = {}
            sections["hello"] = self.hello
            sections["yay"] = self.yay
            sections["START"] = spam_start
            BranchingDialog(sections, self.start)
    
    def test_happy_construction(self):
        sections = {}
        sections["hello"] = self.hello
        sections["yay"] = self.yay
        dialog = BranchingDialog(sections, self.start)

        self.assertEqual(self.simple_dialog, str(dialog))

    def test_happy_construction_startless(self):
        sections = {}
        sections["hello"] = self.hello
        sections["yay"] = self.yay
        dialog = BranchingDialog(sections, self.startless)

        self.assertEqual(self.simple_startless, str(dialog))

    def test_eq(self):
        sections = {}
        sections["hello"] = self.hello
        sections["yay"] = self.yay
        dialog = BranchingDialog(sections, self.start)
        self.assertEqual(dialog, dialog)

        dialog_clone = BranchingDialog(sections, self.start)
        self.assertEqual(dialog, dialog_clone)
        self.assertEqual(dialog_clone, dialog)

        dialog_clone2 = BranchingDialog(sections, self.start)
        self.assertEqual(dialog_clone, dialog_clone2)
        self.assertEqual(dialog, dialog_clone)
        self.assertEqual(dialog, dialog_clone2)

        self.assertFalse(dialog == None)

class DialogSectionTests(unittest.TestCase):
    
    def setUp(self):
        self.hello = DialogSection(prompt="hello", reply="um", cont=["yay", "END"])

    def test_eq(self):
        self.assertTrue(self.hello == self.hello)
        hello_clone = DialogSection(prompt="hello", reply="um", cont=["yay", "END"])
        self.assertTrue(self.hello == hello_clone)
        self.assertTrue(hello_clone == self.hello)
        hello_clone2 = DialogSection(prompt="hello", reply="um", cont=["yay", "END"])
        self.assertTrue(hello_clone == hello_clone2)
        self.assertTrue(self.hello == hello_clone2)
        self.assertFalse(self.hello == None)
    
    def test_str(self):
        dialog = DialogSection("prompt", "reply", ["dne", "END"])
        dialog_str = """prompt

reply

dne, END"""
        
        self.assertEqual(dialog_str, str(dialog))
