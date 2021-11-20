from ARITH_helper import arithHelper
from CNF_general import CNF_Boolean
from CYKCHECKER_general import CYKCHECKCLASS
from LOOP_FA_function import FA_VALIDFUNVARNAMEC, FA_function_HELPER
class FA_boolean:
    #the exceptions are still ambiguous because im confused
    #ini buat and/not/or
    def checkBoolStatement(self, str):
        word = []
        buffer = ""
        length = len(str)
        for i in range(0, length):
            if (str[i] == " "):
                word.append(buffer)
                buffer = ""
            else:
                buffer += str[i]
        if (buffer != ""):
            word.append(buffer)
        word = list(filter(lambda a: a != "", word))
        
        openingBracketCount = 0
        closingBracketCount = 0
        # asumsi kasusnya masih nerima True/False dulu
        for i in range(len(word)):
            '''
            if ("not" in word[i]):
                if ("True" in word[i] or "False" in word[i]):
                    raise Exception("'not' should be separated")
                elif word[i + 1] == "and" or word[i + 1] == "or":
                    if (len(word[i]) == 3):
                        raise Exception("'not' should be followed by a constant/variable")
                    else:
                        arr = [x for x in word[i]]
                        varFlag = False
                        j = 0
                        while (not varFlag and j < len(arr)):
                            print(arr[j])
                            if (arr[j].isnumeric()):
                                varFlag = True
                            j += 1
                        if varFlag == False:
                            raise Exception("'not' should be followed by a constant/variable")
            '''
            
            if ("(" in word[i]):
                if ("and" in word[i] or "or" in word[i]):
                    raise Exception("'and/or' operator should not have an opening bracket")
                else:
                    openingBracketCount += word[i].count("(")
            if (")" in word[i]):
                if ("and" in word[i] or "or" in word[i] or "not" in word[i]):
                    raise Exception("'and/or/not' operator should not have a closing bracket")
                else:
                    closingBracketCount += word[i].count(")")
        
        funVarCheck = FA_VALIDFUNVARNAMEC()
        funcNameCheck = FA_function_HELPER()
        
        for i in range(len(word)):
            if word[i][0] == "(": word[i] = word[i][1:]
            if word[i][-1] == ")" and word[i][-2] != "(": word[i] = word[i][:-1]
        print(word)
        arr = ["not", "and", "or", "True", "False"]
        for i in range(len(word)):
            if word[i] not in arr:
                if word[i].isdigit():
                    word[i] = "VAR"
                else:
                    try:
                        funcNameCheck.checkfuncall(word[i])
                    except Exception as e:
                        raise e
                    else:
                        word[i] = "FUNCALL"

        if openingBracketCount != closingBracketCount:
            raise Exception("open bracket detected but no close bracket")
        for i in range(len(word)):
            if "(" in word[i]:
                word[i] = word[i].replace("(", "")
            if ")" in word[i]:
                word[i] = word[i].replace(")", "")
        
        CYKChecker = CYKCHECKCLASS()
        CNF = CNF_Boolean()
        boolRule = CNF.getBooleanRule()
        if CYKChecker.check(boolRule, word):
            return True
        else:
            raise Exception("Grammar incompatible!")

    def checkComparisonStatement(self, str):
        comparisonOps = ["<", "<=", ">", ">=", "==", "!="]
        opsCount = 0;
        for i in range(len(comparisonOps)):
            if (comparisonOps[i] in str):
                opsCount += 1
                word = str.split(comparisonOps[i])
        if (opsCount > 1):
            raise Exception("More than one comparison operator detected")

        #cek arithmetic
        instArith = arithHelper()
        for i in range(len(word)):
            instArith.checkArithStatement(word[i].replace(" ", ""))