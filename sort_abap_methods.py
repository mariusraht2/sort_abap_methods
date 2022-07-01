import re, os.path as path;

def readFileLines(fileName):
    fileHandler = open(fileName, "r");
    fileContent = fileHandler.read();
    fileHandler.flush();
    fileHandler.close();

    return fileContent.splitlines();
# ENDDEF

#TODO Consider sections in definition part
def extractMethod(fileLines):
    # Extract method names
    newFileContentList = [];
    methodName = '';
    methodType = '';
    methodIndex = -1;
    methods = [];
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
        #ENDIF

        if isClassDef == True:
            methods, methodName, methodType, isMethodDef, newFileContentList = detMethodDef(
                line, methods, methodName, methodType, isMethodDef, newFileContentList);
        elif isClassImp == True:
            methods, isMethodImp, methodIndex, newFileContentList = detMethodImp(
                line, methods, isMethodImp, methodIndex, newFileContentList);
        else:
            newFileContentList.append(line);
        # ENDIF

        if re.search('CLASS[\s\S]*DEFINITION', line):
            isClassDef = True;
        elif re.search('CLASS[\s\S]*IMPLEMENTATION', line):
            isClassImp = True;
        # ENDIF
    # ENDFOR

    methods = sorted(methods, key=lambda m: m[0]);
    return methods, newFileContentList;

# ENDDEF


def detMethodDef(line, methods, methodName, methodType, isMethodDef, newFileContentList):   
    if re.search('METHODS', line):
        isMethodDef = True;
        methods.append(['','','','']);
        methodName = '';
        result = re.search('METHODS:?\s+(\w+)', line);
        if result != None:
            methodName = result.group(1);
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
        # ENDIF
    # ENDIF

    methodIndex = len(methods) - 1;

    if isMethodDef == True:
        methods[methodIndex][1] += line;
    # ENDIF

    if methodName != '' and methods[methodIndex][0] == '':
        methods[methodIndex][0] = methodName;
    #ENDIF

    isEndOfDef = False;
    if isMethodDef == True and re.search(',', line):
        isEndOfDef = True;
        methods[methodIndex][1] = methods[methodIndex][1].replace(",", ".");
        methods.append(['','','','']);
    elif isMethodDef == True and re.search('.*\.+', line):
        isEndOfDef = True;
        isMethodDef = False;
    # ENDIF

    if isEndOfDef == True:
        if not re.search('METHODS', methods[methodIndex][1]):
            result = re.search('\w', methods[methodIndex][1]);
            startIndex = result.start();
            methods[methodIndex][1] = methods[methodIndex][1][:startIndex] + \
                methodType + ' ' + methods[methodIndex][1][startIndex:];
        # ENDIF
        methodName = '';
        isEndOfDef = False;
        newFileContentList.append(methods[methodIndex][1]);
    elif isMethodDef == False:
        newFileContentList.append(line);
    # ENDIF

    return methods, methodName, methodType, isMethodDef, newFileContentList;
# ENDDEF


def detMethodImp(line, methods, isMethodImp, methodIndex, newFileContentList):
    # Check if method implementation
    result = re.search('^\s*METHOD\s+(\w+)', line);
    if result != None:
        isMethodImp = True;
    # ENDIF

    # Determine method index
    if result != None:
        methodIndex = -1;
        for i, method in enumerate(methods):
            if method[0] == result.group(1):
                methodIndex = i;
                break;
            # ENDIF
        # ENDFOR
    # ENDIF

    if methodIndex > -1 and isMethodImp == True:
        methods[methodIndex][2] += line;
    # ENDIF

    if isMethodImp == True and re.search('ENDMETHOD', line):
        isMethodImp = False;
        newFileContentList.append(methods[methodIndex][2]);
    elif isMethodImp == False:
        newFileContentList.append(line);        
    # ENDIF

    return methods, isMethodImp, methodIndex, newFileContentList;
# ENDDEF


def createNewFileContent(newFileContentList, methods):
    newFileContent = '';
    methodIndex = 0;

    for line in newFileContentList:
        if re.search('METHODS', line):
            newFileContent += methods[methodIndex][1];
            methodIndex += 1;
        elif re.search('^\s*METHOD', line):
            newFileContent += methods[methodIndex][2];
            methodIndex += 1;
        else:
            newFileContent += line;
        # ENDIF

        if methodIndex == len(methods):
            methodIndex = 0;
        #ENDIF
    # ENDFOR

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