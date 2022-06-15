import re;

print('Dateiname:');
fileName = input();

fileHandler = open(fileName, "r+");
fileContent = fileHandler.read();
fileLines = fileContent.splitlines();

methodDefinition = False;

# TODO: Regex doesn't consider long lists of methods after just one METHODS keyword
for methodName in re.finditer('METHODS:?\s+(\w+)(?:[\s\w\/!=>()]+)(?:,\s*(\w+))*', fileContent):
    entry = methodName.group(1);
    print(entry);
    entry = methodName.group(2);
    if entry != None:
        print(entry);

# for line in fileLines:
#     if.re

#     if re.match('^[\t\s]*CLASS-METHODS:?[\s\t]+.*$', line):
#         methodDefinition = True;
#         print(line);
#     elif methodDefinition == True and re.match('^.*[,.]+$', line):
#         methodDefinition = False;
#         print(line);

    

#TODO
# - Extract method names from definition (consider CLASS-METHODS also comma-separated)
# - Sort method names

# regexBeginOfMethod = '^[\s\t]*METHOD\s{1}\w+\.$';
# regexEndOfMethod = '^[\s\t]*ENDMETHOD\.$';

# newFileContent = '';
# startMethodSorting = False;
# beginOfMethod = False;
# endOfMethod = False;

# for line in fileLines:
    
#     if re.match(regexBeginOfMethod, line):
#         startMethodSorting = True;
#         beginOfMethod = True;
#         methodContent = '';
#     elif re.match(regexEndOfMethod):
#         endOfMethod = True;
#     #ENDIF

#     if startMethodSorting == False:
#         newFileContent += line;
#         continue;
#     else:
#         methodContent += line;
#     #ENDIF

#     if endOfMethod == True:
#         newFileContent += methodContent;
#         print('New method:\n' + methodContent);
#     ##ENDIF

# #ENDFOR

# print(newFileContent);
# fileHandler.write(newFileContent);

#fileHandler.close();
#fileHandler.flush();