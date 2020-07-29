import os
import shutil
import subprocess


def initTruffleProject(path):
    print("Starting to Create Truffle Project")
    path = path + '\\truffle\\'
    try:
        os.mkdir(path + 'truffle-project')
    except OSError:
        print("Creation of the Directory %struffle-project failed" % path)
    else:
        print("✓ Successfully Created the Directory %struffle-project " % path)

    init_out = open(path + "out.txt", "w")
    os.chdir(path + 'truffle-project')

    subprocess.call("truffle init", shell=True, stdout=init_out)
    init_out.close()
    init_out = open(path + "out.txt", "r")
    init_done = False
    for line in init_out:
        if 'successful' in line:
            init_done = True
            print("✓ Creating Truffle Project was Done Successfully")
            init_out.close()
            break
    if not init_done:
        print("⨉ Creating Truffle Project has Problems, Check out.txt for Errors")
    init_out.close()
    return init_done


def compileTruffleProject(is_first, path):
    if not is_first:
        print("Starting to Compile Truffle Project")

    path = path + '\\truffle\\'
    compile_out = open(path + "out.txt", "w")
    os.chdir(path + '\\truffle-project')
    subprocess.call("truffle compile", shell=True, stdout=compile_out)
    compile_out.close()
    compile_out = open(path + "out.txt", "r")
    compile_done = False
    for line in compile_out:
        if 'successfully' in line:
            compile_done = True
            compile_out.close()
            break
    if compile_done:
        print("✓ Project Compiled successfully")
    else:
        print("⨉ Compiling Project has Problems, Check out.txt for Errors")
    return compile_done


def createMutants(path):
    try:
        os.mkdir(path + '\\truffle\\mutants')
    except OSError:
        print("Creation of the Directory %s\\truffle\\mutants failed" % path)
    else:
        print("✓ Successfully Created the Directory %s\\truffle\\mutants " % path)
    shutil.copyfile(path + '\\contract\\contract.sol', path + '\\truffle\\mutants\\contract.sol')
    create_mutants = open(path + "out.txt", "w")
    os.chdir(path + '\\truffle\\mutants')
    print("Starting to Create Mutants, This may Take a While")
    subprocess.call("mutate contract.sol --noCheck", shell=True, stdout=create_mutants)
    print("✓ Creating Mutants was Successful")
    create_mutants.close()
    os.remove(path + '\\truffle\\mutants\\contract.sol')


def runTestOnMainContract(path):
    shutil.rmtree(path + '\\truffle\\truffle-project')
    init_done = initTruffleProject(path)
    if init_done:
        shutil.copyfile(path + '\\contract\\tempContract.sol', path + '\\truffle\\truffle-project\\contracts'
                                                                      '\\contract.sol')
        shutil.copyfile(path + '\\test\\testTemp2.js', path + '\\truffle\\truffle-project\\test\\test.js')
        try:
            os.mkdir(path + '\\test-out')
        except OSError:
            print("⨉ Error Creating Directory")
        os.chdir(path + '\\truffle\\truffle-project')
        compile_done = compileTruffleProject(False, path)
        if compile_done:
            print("Running Tests on Smart Contract")
            test_out = open(path + "\\test-out\\test-out.txt", "w")
            subprocess.call("truffle test", shell=True, stdout=test_out)
    else:
        print("⨉ There was a Problem Initialing Truffle Project")


def runTestOnMutants(path):
    temp_path = path + '\\truffle\\changed-mutants'
    try:
        os.mkdir(path + '\\truffle\\working-directory')
    except OSError:
        print("⨉ Error Creating Directory")

    for filename in os.listdir(temp_path):
        if filename.endswith(".sol"):
            print("***************************")
            print("Running Tests on", filename)
            try:
                os.mkdir(path + '\\truffle\\working-directory\\' + filename[:-4])
            except OSError:
                print("⨉ Error Creating Directory")
            init_done = initMuTruffleProject(path, filename)
            if init_done:
                shutil.copyfile(path + '\\truffle\\changed-mutants\\' + filename,
                                path + '\\truffle\\working-directory\\' + filename[:-4] + '\\contracts'
                                                                                          '\\contract.sol')
                shutil.copyfile(path + '\\truffle\\mutants-tests\\' + filename[:-4] + '.test.js',
                                path + '\\truffle\\working-directory\\' + filename[:-4] + '\\test\\test.js')

                compile_done = compileMuTruffleProject(False, path + '\\truffle\\working-directory\\' + filename[:-4],
                                                       filename)
                if compile_done:
                    print("Running Tests on Smart Contract")
                    test_out = open(path + "\\test-out\\" + filename[:-4] + "-test-out.txt", "w")
                    subprocess.call("truffle test", shell=True, stdout=test_out)
            else:
                print("⨉ There was a Problem Initialing Truffle Project")
            continue
        else:
            continue


def initMuTruffleProject(path, filename):
    print("Starting to Create Truffle Project")

    init_out = open(path + '\\truffle\\working-directory\\' + filename[:-4] + "\\out.txt", "w")
    os.chdir(path + '\\truffle\\working-directory\\' + filename[:-4])

    subprocess.call("truffle init", shell=True, stdout=init_out)
    init_out.close()
    init_out = open(path + '\\truffle\\working-directory\\' + filename[:-4] + "\\out.txt", "r")
    init_done = False
    for line in init_out:
        if 'successful' in line:
            init_done = True
            print("✓ Creating Truffle Project was Done Successfully")
            init_out.close()
            break
    if not init_done:
        print("⨉ Creating Truffle Project has Problems, Check out.txt for Errors")
    init_out.close()
    return init_done


def compileMuTruffleProject(is_first, path, filename):
    if not is_first:
        print("Starting to Compile Truffle Project")
    compile_out = open(path + "\\out.txt", "w")
    os.chdir(path)
    subprocess.call("truffle compile", shell=True, stdout=compile_out)
    compile_out.close()
    compile_out = open(path + "\\out.txt", "r")
    compile_done = False
    for line in compile_out:
        if 'successfully' in line:
            compile_done = True
            compile_out.close()
            break
    if compile_done:
        print("✓ Project Compiled successfully")
    else:
        print("⨉ Compiling Project has Problems, Check out.txt for Errors")
    return compile_done
