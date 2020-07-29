from src.contract.functions import *
from src.test.functions import *


def checkMutants(path, lineNum, contract_name):
    print("Start Changing Mutants and Creating Test Nets for Mutants, This May Take a While")
    temp_path = path + '\\truffle\\mutants'
    try:
        os.mkdir(path + '\\truffle\\changed-mutants')
    except OSError:
        print("Error Creating Directory")
    try:
        os.mkdir(path + '\\truffle\\mutants-tests')
    except OSError:
        print("Error Creating Directory")
    try:
        os.mkdir(path + '\\truffle\\mutants-tests-temp')
    except OSError:
        print("Error Creating Directory")

    for filename in os.listdir(temp_path):
        if filename.endswith(".sol"):
            variables = checkMutantsVariables(path, lineNum, filename)
            generateTest(path, filename, variables, contract_name)
            continue
        else:
            continue
    shutil.rmtree(path + '\\truffle\\mutants-tests-temp')
    print("Done Modifying Mutants and Test Nets")


def insertMutantsTestName(current_path, filename):
    global main_name
    testFile = open(current_path + '\\test\\test.js', 'r')
    testFileTemp = open(current_path + '\\truffle\\mutants-tests-temp\\' + filename[:-4] + '.test.js', 'w')
    for line in testFile:
        if 'describe(' in line:
            testFileTemp.write(line)
            if len(line.split('\'')) > 1:
                main_name = line.split('\'')[1]
            else:
                main_name = line.split('\"')[1]
        elif 'it(' in line:
            name = line.split('\"')
            if len(name) > 1:
                testFileTemp.write(
                    line + 'console.log(\'##########\');\nconsole.log("TestName:' + main_name + '#' + name[
                        1] + '");\nconsole.log(\'##########\');')
            else:
                name = line.split('\"')
                testFileTemp.write(line + 'console.log(\'##########\');console.log("TestName:' + main_name + name[
                    1] + '");\nconsole.log(\'##########\');')
        else:
            testFileTemp.write(line)
    testFile.close()
    testFileTemp.close()


def insertMutantTestsBalances(current_path, variables, contract_name, filename):
    testFile = open(current_path + '\\truffle\\mutants-tests-temp\\' + filename[:-4] + '.test.js', 'r')
    testFileTemp = open(current_path + '\\truffle\\mutants-tests\\' + filename[:-4] + '.test.js', 'w')
    check = []
    start = False
    for line in testFile:
        if 'it(' in line:
            start = True
        if start:
            if '{' in line:
                check.append('{')
            if '}' in line:
                check = check[:-1]
        if len(check) == 0 and start:
            start = False
            accountPrint = "console.log('**********');\n"
            accountPrint += "for (i = 0; i < accounts.length; i++){ \nlet balance = await web3.eth.getBalance(" \
                            "accounts[i]);\nconsole.log(\"accounts \", i, balance);\n}\n"
            accountPrint += varPrint(variables, contract_name)
            accountPrint += "console.log('**********');\n"
            testFileTemp.write(accountPrint + line)
        else:
            testFileTemp.write(line)
    testFile.close()
    testFileTemp.close()


def generateTest(path, filename, vars, contract_name):
    insertMutantsTestName(path, filename)
    insertMutantTestsBalances(path, vars, contract_name, filename)


def checkMutantsVariables(current_path, line_num, file_name):
    types = readTypes(current_path)
    contract = open(current_path + '\\truffle\\mutants\\' + file_name, 'r')
    var_lines = findVariableLines(types, contract)
    var_type = extractVarAndType(var_lines)
    contract.close()
    contract = open(current_path + '\\truffle\\mutants\\' + file_name, 'r')
    tempContract = open(current_path + '\\truffle\\changed-mutants\\' + file_name, 'w')
    insertVarPrintInContract(tempContract, contract, var_type, line_num)
    contract.close()
    tempContract.close()
    return var_type


def extractNeededData(path, filename, failed):
    test_output = open(path + '\\test-out\\' + filename, 'r')
    output = failed
    is_data = False
    for line in test_output:
        if 'TestName:' in line:
            output += line
            continue
        if '**********' in line:
            is_data = not is_data
            continue
        if is_data:
            output += line
    test_output.close()
    test_output = open(path + '\\test-out\\' + filename, 'w')
    test_output.write(output)


def checkPassedOrFailedTests(path, filename):
    test_output = open(path + '\\test-out\\' + filename, 'r')
    output = ""
    count = 0
    for line in test_output:
        if 'failing' in line:
            count = line.strip().split()[1]
            break
        else:
            continue
    index = 0
    is_failed = False
    counter = 0
    if int(count) > 0:
        for line in test_output:
            if 'Contract:' in line:
                is_failed = not is_failed
                index += 1
                continue
            if is_failed:
                if index == 1:
                    output += "FailedTest:" + line.strip() + '#'
                    index += 1
                elif index == 2:
                    output += line.strip().split(':')[0] + '\n'
                    index = 0
                    is_failed = False
                    counter += 1

            if count == counter:
                break
    print(filename + output)
    return output


def extractTestOutputs(path):
    print("Extracting Tests Outputs")
    for filename in os.listdir(path + '\\test-out'):
        if filename.endswith(".txt"):
            failed = checkPassedOrFailedTests(path, filename)
            extractNeededData(path, filename, failed)
    shutil.rmtree(path + '\\truffle\\working-directory')
