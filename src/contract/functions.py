def readTypes(current_path):
    types = []
    typesFile = open(current_path + '\\contract\\types.txt', 'r')
    for line in typesFile:
        if line:
            if '\n' in line:
                types.append(line[:-1])
            else:
                types.append(line)
    return types


def findVariableLines(types: [], contract):
    variables_lines = []
    check1 = []
    check2 = []
    for line in contract:
        if 'contract' in line:
            continue
        if '[]' in line:
            continue
        if '{' in line:
            check1.append('{')
        if '}' in line:
            check1 = check1[:-1]
        if not len(check1) == 0:
            continue

        if '(' in line:
            check2.append('(')
        if ')' in line:
            check2 = check2[:-1]
        if not len(check2) == 0:
            continue

        if '//' in line:
            continue
        if 'function' in line:
            continue
        for typ in types:
            line = line.strip()
            if typ in line:
                if '\n' in line:
                    variables_lines.append(line[:-1])
                else:
                    variables_lines.append(line)
                break

    return variables_lines


def extractVarAndType(var_lines):
    vars = []
    for line in var_lines:
        index = line.find('=')
        if index != -1:
            line = line[:index]
        if ';' in line:
            line = line[:-1]
        if line.find('constant') != -1:
            line = line.replace('constant', '')
        if line.find('public') != -1:
            line = line.replace('public', '')
        if line.find('private') != -1:
            line = line.replace('private', '')
        vars.append(line.split())
    for var in vars:
        if len(var) == 3:
            temp = [var[0] + ' ' + var[1], var[2]]
            vars = [temp if var2 == var else var2 for var2 in vars]
    return vars


def insertVarPrintInContract(tempContract, contract, var_types, line_count):
    index = 0
    for line in contract:
        if index != line_count - 2:
            tempContract.write(line)
        else:
            count = 0
            for type_var in var_types:
                if len(type_var) < 2:
                    continue
                else:
                    type = type_var[0]
                    var = type_var[1]
                if type == 'string':
                    tempContract.write(
                        'function printVariables' + str(count) + '() public view returns(' + type + ' memory n){\n')
                    tempContract.write('return ' + var + ' ;\n')
                    tempContract.write('}\n')
                    count += 1
                else:
                    tempContract.write(
                        'function printVariables' + str(count) + '() public view returns(' + type + ' n){\n')
                    tempContract.write('return ' + var + ' ;\n')
                    tempContract.write('}\n')
                    count += 1


        index += 1


def checkVariables(current_path, line_num):
    types = readTypes(current_path)
    contract = open(current_path + '\\contract\\contract.sol', 'r')
    var_lines = findVariableLines(types, contract)
    var_type = extractVarAndType(var_lines)
    contract.close()
    contract = open(current_path + '\\contract\\contract.sol', 'r')
    tempContract = open(current_path + '\\contract\\tempContract.sol', 'w')
    insertVarPrintInContract(tempContract, contract, var_type, line_num)
    return var_type


def extractFunctionLines(contract):
    check = []
    functions = []
    func = []
    in_func = False
    for line in contract:
        if '//' in line:
            continue
        if line == '\n':
            continue
        if 'function' in line:
            in_func = True

        if in_func:
            func.append(line.strip())
            if '}' in line:
                check = check[:-1]
            if '{' in line:
                check.append('{')

            if len(check) == 0:
                in_func = False
                functions.append(func)
                func = []
    return functions


def checkFunctions(current_path):
    contract = open(current_path + '\\contract\\contract.sol', 'r')
    functionLines = extractFunctionLines(contract)
    contract.close()
