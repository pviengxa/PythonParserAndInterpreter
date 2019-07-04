from ClassWillHelpParse import assignStatement, binaryExpression, Block, booleanExpression, ID, ifStatement, literalInteger, \
    Memory, printStatement, program, repeatStatement, whileStatement
from AbstractClass import abstractStatement

readme = open("/Users/testuser/Downloads/Parser/TokenList4", "r")
token = readme.read().split("\n")


class ParserException(Exception):
    def __init__(self, errorMessage):
        super().__init__(errorMessage)


class Token:
    def __init__(self, tokenType, lexeme, row, colume):
        self.tokenType = tokenType
        self.row = row
        self.colume = colume
        self.lexeme = lexeme

    def getTokenType(self):
        return self.tokenType

    def getRow(self):
        return self.row

    def getColume(self):
        return self.colume

    def getLexeme(self):
        return self.lexeme;

    def setTokenType(self, tokenType):
        self.tokenType = tokenType

    def setRow(self, row):
        self.row = row

    def setColume(self, colume):
        self.colume = colume

    def setLexeme(self, lexeme):
        self.lexeme = lexeme

tokenList = []
for tok in token:
    if tok == "":
        break
    elif tok.split(" ")[0] == "Test":
        print("Begin Test", tok.split(" ")[1])
    else:
        tokenList.append(Token(tok.split(" ")[0], tok.split(" ")[1], tok.split(" ")[2], tok.split(" ")[3]))

def parsingProgram():
    try:
        testToken = tokenList.pop(0)
        overloadEqual(testToken, "FUNCTION_TOK")
        #print("<program> → function id ( ) <block> end")
        functionName = loadID()
        testToken = tokenList.pop(0)
        overloadEqual(testToken, "LEFT_PAREN_TOK")
        testToken = tokenList.pop(0)
        overloadEqual(testToken, "RIGHT_PAREN_TOK")
        block = loadBlock()
        testToken = tokenList.pop(0)
        overloadEqual(testToken, "END_TOK")
        testToken = tokenList.pop(0)
        if not testToken.getTokenType() == "EOS_TOK":
            raise ParserException("There are extra Tokens and should not be scan")
        return block
    except ParserException as e:
        print(e)



def overloadEqual(testToken, token):
    assert testToken is not None
    assert token is not None
    try:
        if testToken.getTokenType() != token:
            raise ParserException("There an error at row "+testToken.getRow()+" and colume "+testToken.getColume()+
                                  ". Excepted "+token+" got "+testToken.getTokenType()+".")
    except ParserException as e:
        print(e)

def loadBlock():
    #print("<block> → <statement> | <statement><Block>")
    block = Block()
    lookAheadToken = tokenList[0]
    while statementIsValid(lookAheadToken.getTokenType()):
        statement = loadStatements(lookAheadToken.getTokenType())
        block.add(statement)
        lookAheadToken = tokenList[0]
    return block

def loadStatements(lookAHeadToken):
    #print("<statement> → <if_statement> | <assignment_statement> | <while_statement> | <print_statement> | <repeat_statement> ")
    try:
        x = abstractStatement
        if lookAHeadToken == "ID_TOK":
            #print("<statement → <assignment statement>")
            x = loadAssignStatement()
        elif lookAHeadToken == "IF_TOK":
            #print("<statement → <if_statement>")
            x = loadIfStatement()
        elif lookAHeadToken == "WHILE_TOK":
            #print("<statement → <while_statementt>")
            x = loadWhileStatement()
        elif lookAHeadToken == "PRINT_TOK":
            #print("<statement → <print_statement>")
            x = loadPrintStatement()
        elif lookAHeadToken == "REPEAT_TOK":
            #print("<statement → <repeat_statement>")
            x = loadRepeatStatement()
        else:
            raise ParserException("Invalid Statement Initiation")
        return x
    except ParserException as e:
        print(e)

def statementIsValid(token):
    assert token is not None

    return token == "ID_TOK" \
           or token == "IF_TOK" \
           or token == "WHILE_TOK" \
           or token == "PRINT_TOK" \
           or token == "REPEAT_TOK"


def loadID():
    try:
        testToken = tokenList.pop(0)
        if not testToken.getLexeme().isalpha():
            raise ParserException(testToken.getLexeme()+" is not a character")
        else:
            overloadEqual(testToken, "ID_TOK")
            #print("<id> →", testToken.getLexeme())
            return ID(testToken.getLexeme())
    except ParserException as e:
        print(e)

def loadInteger():
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "LITERAL_INTEGER_TOK")
    #print("<literal_integer> →", int(testToken.getLexeme()))
    value = literalInteger(int(testToken.getLexeme()))
    return value

def loadRelationalOperator():
    #print("<relative_op> → le_operator | lt_operator | ge_operator | gt_operator | eq_operator | ne_operator")
    try:
        testToken = tokenList.pop(0)
        if testToken.getTokenType() == "LE_TOK":
            #print("<ralative_op> → le_operator")
            return "LE_TOK"
        elif testToken.getTokenType() == "LT_TOK":
            #print("<ralative_op> → lt_operator")
            return "LT_TOK"
        elif testToken.getTokenType() == "EQ_TOK":
            #print("<ralative_op> → eq_operator")
            return "EQ_TOK"
        elif testToken.getTokenType() == "NE_TOK":
            #print("<ralative_op> → ne_operator")
            return "NE_TOK"
        elif testToken.getTokenType() == "GE_TOK":
            #print("<ralative_op> → ge_operator")
            return "GE_TOK"
        elif testToken.getTokenType() == "GT_TOK":
            #print("<ralative_op> → gt_operator")
            return "GT_TOK"
        else:
            raise ParserException("Error at row "+testToken.getRow()+" and colume "+testToken.getColume()+
                                  ". Expected LE_TOK, LT_TOK, EQ_TOK, NE_TOK, GE_TOK, or GT_TOK; recieved: "+testToken.getLexeme())

    except ParserException as e:
        print(e)

def loadArithmeticExpression():
    #print(" <arithmetic_expression> → <id> | <literal_integer> | <arithmetic_op> <arithmetic_expression> <arithmetic_expression>")
    headsUp = tokenList[0]
    if headsUp.getTokenType() == "ID_TOK":
        return loadID()
    elif headsUp.getTokenType() == "LITERAL_INTEGER_TOK":
        return loadInteger()
    else:
        return loadBinaryExpression()


def loadAssignStatement():
    #print("<assignment_statement> → id <assignment_operator> <arithmetic_expression>")
    id = loadID()
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "ASSIGN_TOK")
    expression = loadArithmeticExpression()
    return assignStatement(id, expression)

def loadIfStatement():
    #print("<if_statement> → if <boolean_expression> then <block> else <block> end")
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "IF_TOK")
    boolean = loadBooleanExpression()
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "THEN_TOK")
    block_1 = loadBlock()
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "ELSE_TOK")
    block_2 = loadBlock()
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "END_TOK")
    return ifStatement(boolean, block_1, block_2)

def loadPrintStatement():
    #print("<print_statement> → print ( <arithmetic_expression> )")
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "PRINT_TOK")
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "LEFT_PAREN_TOK")
    expression = loadArithmeticExpression()
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "RIGHT_PAREN_TOK")
    return printStatement(expression)

def loadRepeatStatement():
    #print("<repeat_statement> → repeat <block> until <boolean_expression>")
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "REPEAT_TOK")
    block = loadBlock()
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "UNTIL_TOK")
    boolean = loadBooleanExpression()
    return repeatStatement(boolean, block)

def loadWhileStatement():
    #print("<while_statement> → while <boolean_expression> do <block> end")
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "WHILE_TOK")
    boolean = loadBooleanExpression()
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "DO_TOK")
    block = loadBlock()
    testToken = tokenList.pop(0)
    overloadEqual(testToken, "END_TOK")
    return whileStatement(boolean, block)


def loadBinaryExpression():
    #print("<arithmetic_op> <arithmetic_expression> <arithmetic_expression>")
    operator = loadArithmeticOperator()
    expression_1 = loadArithmeticExpression()
    expression_2 = loadArithmeticExpression()
    return binaryExpression(operator, expression_1, expression_2)

def loadArithmeticOperator():
    #print("<arithmetic_op> → add_operator | sub_operator | mul_operator | div_operator")
    try:
        testToken = tokenList.pop(0)
        if testToken.getTokenType() == "ADD_TOK":
            #print("<arithmetic_op> → add_operator")
            return "ADD_OP"
        elif testToken.getTokenType() == "SUB_TOK":
            #print("<arithmetic_op> → sub_operator")
            return "SUB_OP"
        elif testToken.getTokenType() == "MUL_TOK":
            #print("<arithmetic_op> → mul_operator")
            return "MUL_OP"
        elif testToken.getTokenType() == "DIV_TOK":
            #print("<arithmetic_op> → div_operator")
            return "DIV_OP"
        else:
            raise ParserException("Error at row "+testToken.getRow()+" and colume "+testToken.getColume()+". Expected "
                                  " ADD_TOK, SUB_TOK, MUL_TOK, DIV_TOK, recieve "+testToken.getTokenType()+".")
    except ParserException as e:
        print(e)

def loadBooleanExpression():
    #print("<boolean_expression> → <relative_op> <arithmetic_expression> <arithmetic_expression>")
    rational = loadRelationalOperator()
    expression_1 = loadArithmeticExpression()
    expression_2 = loadArithmeticExpression()
    return booleanExpression(rational, expression_1, expression_2)


p = program(parsingProgram())
p.execute()



#for tok in tokenList:
 #   print(tok.getTokenType(), "and lexeme:", tok.getLexeme())
