from AbstractClass import abstractStatement, abstractArithmeticExpression


class program:

    def __init__(self, block):
        self.block = block

    def execute(self):
        self.block.execute()


class Block:

    def __init__(self):
        self.state = []
        self.size = 0

    def add(self, statement):
        assert statement is not None
        self.state.append(statement)
        self.size = self.size + 1

    def execute(self):
        # noinspection PyTypeChecker
        for i in range(0, self.size):

            self.state[i].evaluate()



diction = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12,
           'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'y': 23, 'x': 24,
           'z': 25, 'A': 26, 'B': 27, 'C': 28, 'D': 29, 'E': 30, 'F': 31, 'G': 32, 'H': 33, 'I': 34, 'J': 35, 'K': 36,
           'L': 37, 'M': 38, 'N': 39, 'O': 40, 'P': 41, 'Q': 42, 'R': 43, 'S': 44, 'T': 45, 'U': 46, 'V': 47, 'W': 48,
           'X': 49, 'Y': 50, 'Z': 51}

class Memory:

    def __init__(self):
        self.memory = [None] * 52

    def read(self, ch):

        return self.memory[diction[ch]]

    def write(self, ch, entry):
        self.memory[diction[ch]] = entry



mem = Memory()


class booleanExpression:

    def __init__(self, rational, expression_1, expression_2):
        assert rational is not None
        assert expression_1 is not None
        assert expression_2 is not None
        self.rational = rational
        self.expression_1 = expression_1
        self.expression_2 = expression_2

    def evaluate(self):
        boolean = False
        if self.rational == "LE_TOK":
            boolean = self.expression_1.evaluate() <= self.expression_2.evaluate()
        elif self.rational == "LT_TOK":
            boolean = self.expression_1.evaluate() < self.expression_2.evaluate()
        elif self.rational == "EQ_TOK":
            boolean = self.expression_1.evaluate() == self.expression_2.evaluate()
        elif self.rational == "NE_TOK":
            boolean = self.expression_1.evaluate() != self.expression_2.evaluate()
        elif self.rational == "GE_TOK":
            boolean = self.expression_1.evaluate() >= self.expression_2.evaluate()
        elif self.rational == "GT_TOK":
            boolean = self.expression_1.evaluate() > self.expression_2.evaluate()
        else:
            print("Invalid rational operator")
        return boolean


class ID(abstractArithmeticExpression):

    def __init__(self, ch):
        assert ch.isalpha()
        self.ch = ch
        super(ID, self).__init__()

    def getCh(self):
        return self.ch

    def evaluate(self):
        return mem.read(self.ch)


class binaryExpression(abstractArithmeticExpression):

    def __init__(self, operator, expression_1, expression_2):
        assert operator is not None
        assert expression_1 is not None
        assert expression_2 is not None
        self.operator = operator
        self.expression_1 = expression_1
        self.expression_2 = expression_2
        super(binaryExpression, self).__init__()

    def evaluate(self):
        value = 0
        if self.operator == "ADD_OP":
            value = self.expression_1.evaluate() + self.expression_2.evaluate()
        elif self.operator == "SUB_OP":
            value = self.expression_1.evaluate() - self.expression_2.evaluate()
        elif self.operator == "MUL_OP":
            value = self.expression_1.evaluate() * self.expression_2.evaluate()
        elif self.operator is "DIV_OP":
            value = self.expression_1.evaluate() / self.expression_2.evaluate()

        return value


class literalInteger(abstractArithmeticExpression):

    def __init__(self, number):
        self.number = number
        super(literalInteger, self).__init__()

    def evaluate(self):
        return self.number


class assignStatement(abstractStatement):

    def __init__(self, ch, expression):
        assert ch is not None
        assert expression is not None
        self.ch = ch
        self.expression = expression
        super(assignStatement, self).__init__()

    def evaluate(self):
        mem.write(self.ch.getCh(), self.expression.evaluate())


class ifStatement(abstractStatement):

    def __init__(self, expression, block_1, block_2):
        assert expression is not None
        assert block_1 is not None
        assert block_2 is not None
        self.expression = expression
        self.block_1 = block_1
        self.block_2 = block_2
        super(ifStatement, self).__init__()

    def evaluate(self):
        if self.expression.evaluate():
            self.block_1.execute()
        else:
            self.block_2.execute()


class printStatement(abstractStatement):

    def __init__(self, expression):
        assert expression is not None
        self.expression = expression

        super(printStatement, self).__init__()

    def evaluate(self):
        #f = open("Interpreter_test_4.txt", "w+")
        #f.write(str(self.expression.evaluate()))
        #f.close()
        print(self.expression.evaluate())


class repeatStatement(abstractStatement):

    def __init__(self, expression, block):
        assert expression is not None
        assert block is not None
        self.expression = expression
        self.block = block
        super(repeatStatement, self).__init__()

    def evaluate(self):

        while True:
            self.block.execute()
            if not self.expression.evaluate():
                break


class whileStatement(abstractStatement):

    def __init__(self, expression, block):
        assert expression is not None
        assert block is not None
        self.expression = expression
        self.block = block
        super(whileStatement, self).__init__()

    def evaluate(self):
        while self.expression.evaluate():
            self.block.execute()

