#Import for abstract syntax tree
import ast
from pathlib import Path
#List of identifiers found here https://docs.python.org/3/library/ast.html#abstract-grammar
from pprint import pprint

#Function that returns all the Identifiers in the ast tree
def getIdentifiers(ast_code):
    root = ast_code

    #Gets the child node of the current node and sees if it's an indentifier and yields it if it is
    for node in ast.walk(root):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            yield node.id
        elif isinstance(node, ast.Attribute):
            yield node.attr
        elif isinstance(node, ast.FunctionDef):
            yield node.name
        elif isinstance(node, ast.AsyncFunctionDef):
            yield node.name
        elif isinstance(node, ast.ClassDef):
            yield node.name
        elif isinstance(node, ast.ImportFrom):
            yield node.module
        elif isinstance(node, ast.Global):
            yield node.names
        elif isinstance(node, ast.Nonlocal):
            yield node.names
        elif isinstance(node, ast.excepthandler):
            yield node.name
        elif isinstance(node, ast.arg):
            yield node.arg
        elif isinstance(node, ast.keyword):
            yield node.arg
        elif isinstance(node, ast.alias):
            yield node.name

#Function that checks if a string of length 13 exists
def length13Check(words):
    return [word for word in words if len(word) == 13]

#Gets the max depth of the control structure
def depthAst(root, depth, maxDepth):
    for child in ast.iter_child_nodes(root):
        #Checks if a control stucture exists at the current node, if it does add one to the depth and move one node down the tree
        if isinstance(child, ast.If) or isinstance(child, ast.For) or isinstance(child, ast.While) or isinstance(child, ast.With) or isinstance(child, ast.AsyncFor) or isinstance(child, ast.AsyncWith):
            depth = depth + 1
            maxDepth = depthAst(child, depth, maxDepth)
            if maxDepth < depth:
                maxDepth = depth
            #Recursion to help travel the list
            depth = depth - 1
    return maxDepth

def main(pythonFile):
    #Places the text of the .py code being tested into a string so the ast.parse can read it
    code = Path(pythonFile).read_text()
    code_ast = ast.parse(code)

    #List of the identifiers within the program
    identifierList = list(getIdentifiers(code_ast))

    #List of length 13 identifiers in the program
    identifierListLength13 = length13Check(identifierList)

    #Prints the .py filename
    print(pythonFile)

    #States if there are identifiers of size 13 within the program and if it there are they are listed
    if not identifierListLength13:
        print("No identifiers of length 13 exist")
    else:
        print(str(len(identifierListLength13)) + " identifier(s) of length 13 exist: " + str(identifierListLength13))

    #States if the Maximum control structure nesting is below, equal to or above 4 and what the max depth is
    maxDepth = depthAst(code_ast, 0, 0)
    if maxDepth < 4:
        print("Maximum control structure nesting is below 4. The max nesting is: " + str(maxDepth))
    else:
        print("Maximum control structure nesting is above or equal to 4. The max nesting is: " + str(maxDepth))



main("Test1.py")
main("Test2.py")
main("Test3.py")
main("Test4.py")
main("Test5.py")
main("Test6.py")
main("Test7.py")