import pathlib

from src.contract.functions import *
from src.test.functions import *
from src.truffle.commands import *
from src.truffle.functions import *

if __name__ == "__main__":
    contract_name = 'kingoftheetherthrone'
    currentPath = str(pathlib.Path().absolute())
    contract = open(currentPath + '\\contract\\contract.sol', 'r')
    lineNum = 0
    for line in contract:
        lineNum += 1
    contract.close()

    init_done = initTruffleProject(currentPath)
    is_first = True
    if init_done:
        print("Starting to Compile Contract")
        shutil.copyfile(currentPath + '\\contract\\contract.sol', currentPath + '\\truffle\\truffle-project'
                                                                  '\\contracts\\contract.sol')
        compile_done = compileTruffleProject(is_first,currentPath)
        is_first = False
    if compile_done:
        print("Creating Mutants")
        createMutants(currentPath)

    variables = checkVariables(currentPath, lineNum)
    checkTestNet(currentPath, variables)

    runTestOnMainContract(currentPath)

    mu_variables = checkMutants(currentPath, lineNum, contract_name)
    runTestOnMutants(currentPath)
    extractTestOutputs(currentPath)


    selected = selectTests(currentPath)
    selected_tests = open(currentPath + '\\selected-tests.txt', 'w')
    if not type(selected) == type(None):
        for i in selected:
            selected_tests.write(i + '\n')
    selected_tests.close()
    print("✓ Done Selecting Tests, Selected Test Cases can be Seen in selected-tests.txt")