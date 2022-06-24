import re;

def readFileLines(fileName): 
    fileHandler = open(fileName, "r");
    fileContent = fileHandler.read();
    fileHandler.flush();
    fileHandler.close();
    
    return fileContent.splitlines();
#ENDDEF

def extractMethodNames(fileLines):
    # Extract method names
    methodName = '';
    methodIndex = -1;
    methodNames = [];
    methodDefs = [];
    methodImps = None;
    isClassDef = False;
    isClassImp = False;
    isMethodDef = False;
    isMethodImp = False;

    for line in fileLines:

        if re.search('CLASS[\s\S]*DEFINITION', line):
            isClassDef = True;
        elif re.search('ENDCLASS', line):
            isClassDef = False;
            isClassImp = False;
            if methodImps == None:
                methodImps = ['' for y in range(len(methodNames))];
            #ENDIF
        elif re.search('CLASS[\s\S]*IMPLEMENTATION', line):
            isClassImp = True;
        #ENDIF

        if isClassDef == True:
            methodName, methodNames, isMethodDef, methodDefs = detMethodDef(line, methodName, methodNames, isMethodDef, methodDefs);
        elif isClassImp == True:
            isMethodImp, methodIndex, methodImps = detMethodImp(line, methodNames, isMethodImp, methodIndex, methodImps);
        #ENDIF

    #ENDFOR

    methods = [[0 for x in range(3)] for y in range(len(methodNames))];
    for i, methodName in enumerate(methodNames):
        methods[i][0] = methodName;
        methods[i][1] = methodDefs[i];
        methods[i][2] = methodImps[i];
    #ENDFOR

    methods = sorted(methods, key=lambda m:m[0]);
    return methods;

#ENDDEF

def detMethodDef(line, methodName, methodNames, isMethodDef, methodDefs):
    if re.search('METHODS:?', line):
        isMethodDef = True;
        methodName = '';
        result = re.search('METHODS:?\s+(\w+)', line);  
        if result != None:
            methodName = result.group(1);
            methodNames.append(methodName);
    elif isMethodDef == True and methodName == '':
        result = re.search('\s*(\w+)', line);
        if result != None:
            methodName = result.group(1);
            methodNames.append(methodName);
        #ENDIF
    # ENDIF
    
    if isMethodDef == True:
        try:
            methodDefs[len(methodNames)-1];
        except IndexError:
             methodDefs.append('');
        #ENDTRY

        if methodDefs[len(methodNames)-1] != '':
            methodDefs[len(methodNames)-1] += "\n";
        #ENDIF
        methodDefs[len(methodNames)-1] += line;
    #ENDIF

    if isMethodDef == True and re.search(',', line):
        methodName = '';
    elif isMethodDef == True and re.search('.*\.+', line):
        isMethodDef = False;
        methodName = '';
    #ENDIF

    return methodName, methodNames, isMethodDef, methodDefs;
#ENDDEF

def detMethodImp(line, methodNames, isMethodImp, methodIndex, methodImps):
    # Check if method implementation
    result = re.search('^\s*METHOD\s+(\w+)', line);
    if result != None:
        isMethodImp = True;
    #ENDIF

    # Determine method index
    if result != None:
        methodIndex = -1;
        for i, methodName in enumerate(methodNames):
            if methodName == result.group(1):
                methodIndex = i;
                break;
            #ENDIF
        #ENDFOR
    #ENDIF

    if methodIndex > -1 and isMethodImp == True:
        methodImps[methodIndex] += line;
    #ENDIF
    
    if isMethodImp == True and re.search('ENDMETHOD', line):
        isMethodImp = False;
    #ENDIF

    return isMethodImp, methodIndex, methodImps;
#ENDDEF

def convMethodDefinitions(methods):
    for method in methods:
        if re.search('CLASS-METHODS', method[1]):
            methodType = 'CLASS-METHODS';
        elif re.search('METHODS', method[1]):
            methodType = 'METHODS';
        #ENDIF

        if re.search(',', method[1]):
            method[1] = method[1].replace(",",".");
        #ENDIF

        if not re.search('METHODS', method[1]):
            result = re.search('\w', method[1]);
            startIndex = result.start();
            method[1] = method[1][:startIndex] + methodType + ' ' + method[1][startIndex:];
        #ENDIF
    #ENDFOR
    return methods;
#ENDDEF

def createNewFileContent(fileLines, methods):
    newFileContentList = [];    
    newFileContent  = '';
    methodIndex = -1;

    for line in newFileContentList:
        if methodIndex > 0:
            newFileContent += "\n";
        #ENDIF

        if re.search('METHODS:?\s+(\w+)', line):
            newFileContent += methods[methodIndex][1];
        elif re.search('METHOD\s+(\w+)', line):
            newFileContent += methods[methodIndex][2];
        else:
            newFileContent += line;
        #ENDIF
        
    #ENDFOR
    
    print(newFileContent);
        
#ENDDEF    
    
def writeNewFileContent(fileName, newFileContent):
    fileHandler = open(fileName, "w");
    fileHandler.write(newFileContent);
    fileHandler.flush();
    fileHandler.close();
#ENDDEF

print('Dateiname:');
fileName = '';
while fileName == '':
    fileName = input();
#ENDWHILE

fileLines = readFileLines(fileName);
methods = extractMethodNames(fileLines);
methods = convMethodDefinitions(methods);
# newFileContent = createNewFileContent(fileLines, methods);
# writeNewFileContent(fileName, newFileContent);