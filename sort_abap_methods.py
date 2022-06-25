import re, os.path as path;

def readFileLines(fileName):
    fileHandler = open(fileName, "r");
    fileContent = fileHandler.read();
    fileHandler.flush();
    fileHandler.close();

    return fileContent.splitlines();
# ENDDEF


#TODO Consider sections
#TODO Check line breaks at ENDCLASS.
def extractMethod(fileLines):
    # Extract method names
    newFileContentList = [];
    methodName = '';
    methodType = '';
    methodIndex = -1;
    methodNames = [];
    methodDefs = [];
    methodImps = None;
    isClassDef = False;
    isClassImp = False;
    isMethodDef = False;
    isMethodImp = False;

    for i, line in enumerate(fileLines):
        if i > 0:
            line = "\n" + line;
        #ENDIF

        if re.search('ENDCLASS', line):
            isClassDef = False;
            isClassImp = False;
            if methodImps == None:
                methodImps = ['' for y in range(len(methodNames))];
            # ENDIF
        #ENDIF

        if isClassDef == True:
            methodNames, methodName, methodType, isMethodDef, methodDefs, newFileContentList = detMethodDef(
                line, methodNames, methodName, methodType, isMethodDef, methodDefs, newFileContentList);
        elif isClassImp == True:
            isMethodImp, methodIndex, methodImps, newFileContentList = detMethodImp(
                line, methodNames, isMethodImp, methodIndex, methodImps, newFileContentList);
        else:
            newFileContentList.append(line);
        # ENDIF

        if re.search('CLASS[\s\S]*DEFINITION', line):
            isClassDef = True;
        elif re.search('CLASS[\s\S]*IMPLEMENTATION', line):
            isClassImp = True;
        # ENDIF
    # ENDFOR

    methods = [[0 for x in range(3)] for y in range(len(methodNames))];
    for i, methodName in enumerate(methodNames):
        methods[i][0] = methodName;
        methods[i][1] = methodDefs[i];
        methods[i][2] = methodImps[i];
    # ENDFOR

    methods = sorted(methods, key=lambda m: m[0]);
    return methods, newFileContentList;

# ENDDEF


def detMethodDef(line, methodNames, methodName, methodType, isMethodDef, methodDefs, newFileContentList):
    if re.search('METHODS', line):
        isMethodDef = True;
        methodName = '';
        result = re.search('METHODS:?\s+(\w+)', line);
        if result != None:
            methodName = result.group(1);
            methodNames.append(methodName);
        # ENDIF
        if re.search('CLASS-METHODS', line):
            methodType = 'CLASS-METHODS';
        elif re.search('METHODS', line):
            methodType = 'METHODS';
        # ENDIF
    elif isMethodDef == True and methodName == '':
        result = re.search('\s*(\w+)', line);
        if result != None:
            methodName = result.group(1);
            methodNames.append(methodName);
        # ENDIF
    # ENDIF

    methodIndex = len(methodNames) - 1;

    if isMethodDef == True:
        try:
            methodDefs[methodIndex];
        except IndexError:
            methodDefs.append('');
        # ENDTRY
        methodDefs[methodIndex] += line;
    # ENDIF

    isEndOfDef = False;
    if isMethodDef == True and re.search(',', line):
        isEndOfDef = True;
        methodDefs[methodIndex] = methodDefs[methodIndex].replace(",", ".");
    elif isMethodDef == True and re.search('.*\.+', line):
        isEndOfDef = True;
        isMethodDef = False;
    # ENDIF

    if isEndOfDef == True:
        if not re.search('METHODS', methodDefs[methodIndex]):
            result = re.search('\w', methodDefs[methodIndex]);
            startIndex = result.start();
            methodDefs[methodIndex] = methodDefs[methodIndex][:startIndex] + \
                methodType + ' ' + methodDefs[methodIndex][startIndex:];
        # ENDIF
        methodName = '';
        isEndOfDef = False;
        newFileContentList.append(methodDefs[methodIndex]);
    elif isMethodDef == False:
        newFileContentList.append(line);
    # ENDIF

    return methodNames, methodName, methodType, isMethodDef, methodDefs, newFileContentList;
# ENDDEF


def detMethodImp(line, methodNames, isMethodImp, methodIndex, methodImps, newFileContentList):
    # Check if method implementation
    result = re.search('^\s*METHOD\s+(\w+)', line);
    if result != None:
        isMethodImp = True;
    # ENDIF

    # Determine method index
    if result != None:
        methodIndex = -1;
        for i, methodName in enumerate(methodNames):
            if methodName == result.group(1):
                methodIndex = i;
                break;
            # ENDIF
        # ENDFOR
    # ENDIF

    if methodIndex > -1 and isMethodImp == True:
        methodImps[methodIndex] += line;
    # ENDIF

    if isMethodImp == True and re.search('ENDMETHOD', line):
        isMethodImp = False;
        newFileContentList.append(methodImps[methodIndex]);
    elif isMethodImp == False:
        newFileContentList.append(line);        
    # ENDIF

    return isMethodImp, methodIndex, methodImps, newFileContentList;
# ENDDEF


def convMethodDefinitions(methods):
    for method in methods:
        if re.search('CLASS-METHODS', method[1]):
            methodType = 'CLASS-METHODS';
        elif re.search('METHODS', method[1]):
            methodType = 'METHODS';
        # ENDIF

        if not re.search('METHODS', method[1]):
            result = re.search('\w', method[1]);
            startIndex = result.start();
            method[1] = method[1][:startIndex] + \
                methodType + ' ' + method[1][startIndex:];
        # ENDIF
    # ENDFOR
    return methods;
# ENDDEF


def createNewFileContent(newFileContentList, methods):
    newFileContent = '';
    methodIndex = -1;

    for line in newFileContentList:
        # if methodIndex > 0:
        #     newFileContent += "\n";
        # # ENDIF

        if methodIndex + 1 == len(methods):
            methodIndex = 0;
        #ENDIF

        if re.search('METHODS', line):
            methodIndex += 1;
            newFileContent += methods[methodIndex][1];
        elif re.search('^\s*METHOD', line):
            methodIndex += 1;
            newFileContent += methods[methodIndex][2];
        else:
            newFileContent += line;
        # ENDIF

    # ENDFOR

    print(newFileContent);
    return newFileContent;

# ENDDEF


def writeNewFileContent(fileName, newFileContent):
    fileHandler = open(fileName + "_sorted", "w");
    fileHandler.write(newFileContent);
    fileHandler.flush();
    fileHandler.close();
# ENDDEF


print('Dateiname:');
fileName = '';
while fileName == '' or not path.exists(fileName):
    fileName = input();
# ENDWHILE

fileLines = readFileLines(fileName);
methods, newFileContentList = extractMethod(fileLines);
newFileContent = createNewFileContent(newFileContentList, methods);
writeNewFileContent(fileName, newFileContent);