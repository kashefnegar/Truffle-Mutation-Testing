import os
import shutil
import subprocess


def insertTestName(current_path):
    global main_name
    testFile = open(current_path + '\\test\\test.js', 'r')
    testFileTemp = open(current_path + '\\test\\testTemp.js', 'w')
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


def insertBalances(current_path, variables, contract_name):
    testFile = open(current_path + '\\test\\testTemp.js', 'r')
    testFileTemp = open(current_path + '\\test\\testTemp2.js', 'w')
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


def varPrint(variables, contract_name):
    index = 0
    var_print = ""
    for _ in variables:
        var_print += "let temp" + str(index) + " = await " + contract_name + ".printVariables" + str(
            index) + "();\nawait console.log(temp" + str(index) + ");\n "
        index += 1
    return var_print


def checkTestNet(current_path, variables):
    contract_name = "kingoftheetherthrone"
    insertTestName(current_path)
    insertBalances(current_path, variables, contract_name)


def getFailedTests(path, filename):
    failed = []
    main_test = open(path + '\\test-out\\' + filename, 'r')
    out = ""
    for line in main_test:
        if 'FailedTest:' in line:
            failed.append(line.split(':')[1][:-1])
        else:
            out += line
    main_test.close()
    main_test = open(path + '\\test-out\\' + filename, 'w')
    main_test.write(out)
    main_test.close()
    return failed


def compareFiles(path, temp_file_name):
    main_file = open(path + '\\test-out.txt', 'r')
    temp_file = open(path + '\\' + temp_file_name, 'r')
    main_line_num = 0
    temp_line_num = 0
    main_file_lines = []
    temp_file_lines = []
    for line in main_file:
        main_file_lines.append(line)
        main_line_num += 1
    for line in temp_file:
        temp_file_lines.append(line)
        temp_line_num += 1

    if not temp_line_num == main_line_num:
        return
    tests = []
    test_name = ""
    for i in range(main_line_num):
        if 'TestName:' in main_file_lines[i]:
            test_name = main_file_lines[i].split(':')[1][:-1]
        if not main_file_lines[i] == temp_file_lines[i]:
            tests.append(test_name)
    main_file.close()
    temp_file.close()
    return tests


def selectTests(path):
    print("Selecting Test Cases\n")
    print("Selecting Test Cases Failed on Main Contract\n")
    main_failed = getFailedTests(path, 'test-out.txt')
    selected_tests = main_failed
    print("Selecting Test Cases by Comparing Tests Results\n")
    for filename in os.listdir(path + '\\test-out'):
        if filename == 'test-out.txt':
            continue
        else:
            failed = getFailedTests(path, filename)
            for test in failed:
                if test not in main_failed:
                    selected_tests.append(test)

    for filename in os.listdir(path + '\\test-out'):
        if not filename == 'test-out.txt':
            selected = compareFiles(path + '\\test-out', filename)
            if not type(selected) == type(None):
                for i in selected:
                    if i not in selected_tests:
                        selected_tests.append(i)

    return selected_tests
