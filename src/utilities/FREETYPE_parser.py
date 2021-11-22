from CYKcheck import CYKCHECKCLASS
from CNF import CNF_Freetype
from FA_varchecker import varNameChecker
from LOOP_FA_function import FA_function_HELPER


class freetypeParser:
    # buat def,class,try,raise,return,pass, di sini
    
    def checkDefClass(self, string):
        # def class di sini
        keyWords = ["def", "class"]
        # cek colon
        if (string[-1] != ":"):
            raise Exception(["Colon sign missing"])
        if string.count(":") > 1:
            raise Exception(["Too many colon signs"])
        #cek apakah bener depannya keyword
        
        arr = (' '.join(string.split())).split(' ')
        if ":" in arr[-1] and arr[-1] != ":":
            arr[-1] = arr[-1][:-1]
            arr.append(":")

        #print(arr)
        if (arr[0] not in keyWords):
            raise Exception(["Missing def/class keyword"])

        func = (' '.join(arr[1:-1]))
        #print(func)
        
        varFunChecker = varNameChecker()
        if "(" in func:
            if ")" not in func:
                raise Exception(["Missing ')'"])
            else:
                funcName = func[:func.find('(')]
                funcName = funcName.strip()
                #print(funcName)
                if(func.find('(')+1 != func.find(')')):
                    arguments = func[func.find('(')+1:-1]
                    arguments = arguments.split(',')
                    for i in range(len(arguments)):
                        arguments[i]= arguments[i].strip()
                else:
                    arguments = []
                #print(arguments)
                    
                for i in range(len(arguments)):
                    try:
                        varFunChecker.check(arguments[i])
                    except Exception as e:
                        raise(e)
                    else:
                        arguments[i] = "VAR"
        
                #print(arguments)
        else:
            funcName = func
            arguments = []
        try: 
            varFunChecker.check(funcName)
        except Exception as e:
            raise(e)
        else:
            funcName = "FUNNAME"
                        
        word = [arr[0],funcName]
        word.extend(arguments)
        word.append(arr[-1])
        cyk = CYKCHECKCLASS()
        defClassRule = CNF_Freetype()
        if cyk.check(defClassRule.getDefClass(), word):
            return True
        else:
            raise Exception(["Incompatible grammar!"])
    
    def checkPassReturnRaise(self,string):
        funcallCheck = FA_function_HELPER()
        word = (' '.join(string.split())).split(' ')
        if(word[0] == "return"):
            if (len(word) == 1):
                raise Exception(["return to monke"])
            else:
                statement = ' '.join(word[1:])
                bool = FA_function_HELPER()
                try:
                    bool.checkBool(statement)
                except Exception as e:
                    try:
                        bool.checkComparison(statement)
                    except Exception as e:
                        if type(statement) == type(""):
                            statement = "STATEMENT"
                        else:
                            statement = "INVALID"
                    else:
                        statement = "STATEMENT"
                else:
                    statement = "STATEMENT"
            word = [word[0],statement]

        elif (word[0] == "raise"):
            exception = ' '.join(word[1:])
            if len(exception) < 9:
                raise Exception(["No Exception"])
            else:
                if exception[:9] != "Exception":
                    raise Exception(["No Exception"])
                else:
                    try:
                        funcallCheck.checkfuncall(exception)
                    except Exception as e:
                        raise(e)
                    else:
                        exception = "EXCEPTION"
                        word = [word[0],exception]
                    
        cyk = CYKCHECKCLASS()
        passReturnRule = CNF_Freetype()
        if cyk.check(passReturnRule.getPassReturnRaise(),word):
            return True
        else:
            raise Exception(["Incompatible grammar!"])
        