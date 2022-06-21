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
    methodNames = [];
    methodDefinition = False;

    for line in fileLines:       
        if re.search('METHODS:?', line):
            methodDefinition = True;
            methodName = '';
            result = re.search('METHODS:?\s+(\w+)', line);
            if result != None:
                methodName = result.group(1);
                methodNames.append(methodName);
        elif methodDefinition == True and re.search('.*\.+', line):
            methodDefinition = False;
            methodName = '';
        elif methodDefinition == True and methodName == '':
            result = re.search('\s*(\w+)', line);
            if result != None:
                methodName = result.group(1);
                methodNames.append(methodName);
            #ENDIF
        # ENDIF
        
        if re.search('ENDCLASS', line):
            break;
        #ENDIF
        
        if methodDefinition == True and re.search('.*,', line):
            methodName = '';
        #ENDIF
        
    #ENDFOR

    methods = [[0 for x in range(3)] for y in range(len(methodNames))];
    for i, methodName in enumerate(methodNames):
        methods[i][0] = methodName;
    #ENDFOR

    methods = sorted(methods, key=lambda m:m[0]);
    return methods;

#ENDDEF
    
def createNewFileContent(fileLines, methods):
    newFileContentList = [];
    isMethodDef = False;
    isMethodImp = False;

    for line in fileLines:

        i = 0;
        for i in range(2):
            if i == 1:
                # Check if method definition
                result = re.search('METHODS:?\s+(\w+)', line);
            elif i == 2:
                # Check if method implementation
                result = re.search('METHOD\s+(\w+)', line);
            #ENDIF

            if result != None:
                if i == 1:
                    isMethodDef = True;
                elif i == 2:
                    isMethodImp = True;
                #ENDIF
            #ENDIF
        #ENDFOR

        # Determine method index
        if result != None:
            methodIndex = -1;
            for i, method in enumerate(methods):
                if method[i][0] == result.group(1):
                    methodIndex = i;
                    break;
                #ENDIF
            #ENDFOR
        #ENDIF

        if methodIndex > -1:
            if isMethodDef == True:
                method[methodIndex][1] += "\n";
            elif isMethodImp == True:
                method[methodIndex][2] += "\n";
        #ENDIF

        # Content either belongs to file in general or to specific methods
        if methodIndex > -1:
            if isMethodDef == True:
                method[methodIndex][1] += line;
            elif isMethodImp == True:
                method[methodIndex][2] += line;
        else:
            newFileContentList.append(line);
        #ENDIF
        
        if isMethodDef == True and re.search('\.', line):
            newFileContentList.append(method[methodIndex][1]);
            isMethodDef = False;

        elif isMethodImp == True and re.search('ENDMETHOD', line):
            newFileContentList.append(method[methodIndex][2]);
            isMethodImp = False;
        #ENDIF
        
    #ENDFOR
    
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
newFileContent = createNewFileContent(fileLines, methods);
# writeNewFileContent(fileName, newFileContent);