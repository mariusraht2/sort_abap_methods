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
            print(line);
            methodName = '';
            result = re.search('METHODS:?\s+(\w+)', line);
            if result != None:
                methodName = result.group(1);
                methodNames.append(methodName);
        elif methodDefinition == True and re.search('.*\.+', line):
            methodDefinition = False;
            methodName = '';
            print(line);
        elif methodDefinition == True and methodName == '':
            result = re.search('\s*(\w+)', line);
            if result != None:
                methodName = result.group(1);
                methodNames.append(methodName);
        # ENDIF
        
        if re.search('ENDCLASS', line):
            break;
        #ENDIF
        
        if methodDefinition == True and re.search('.*,', line):
            print(line);
            methodName = '';
        #ENDIF
        
    #ENDFOR

    methodNames = sorted(methodNames);
    print(methodNames);
    return methodNames;

#ENDDEF
    
def createNewFileContent(fileLines, methodNames):
    methodContent = '';
    newFileContentList = [];
    isMethod = False;
    
    for line in fileLines:        
        result = re.search('METHOD\s+(\w+)', line);
        if result != None:
            isMethod = True;
            methodName = result.group(1);
        
        # Content either belongs to file in general or to specific methods
        if isMethod == True:
            methodContent += line;
        else:
            newFileContentList.append(line);
        #ENDIF
                
        if re.search('ENDMETHOD', line):
            isMethod = False; 
            newFileContentList.append(methodContent);
            methodContent = '';
        #ENDIF
        
    #ENDFOR

    print(newFileContentList);
    
    newFileContent = '';
    for line in newFileContentList:
        if not re.search('METHOD/s+(/w+)\s*\.', line):
            newFileContent += line;
        else:
            newFileContent += methodContent[methodNameIndex];                
            methodNameIndex += 1;
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
fileName = input();

fileLines = readFileLines(fileName);
methodNames = extractMethodNames(fileLines);
newFileContent = createNewFileContent(fileLines, methodNames);
# writeNewFileContent(fileName, newFileContent);