from BOOL_FA import FA_boolean

FAChecker = FA_boolean()
try:
    #FAChecker.checkBoolStatement("(not kontol()) and jembod()") # <- ganti isi string kalo mo tes
    FAChecker.checkComparisonStatement("(12*-34) != (6 * - 5 // 9)")
except Exception as e:
    print(e)
else:
    print("Success")