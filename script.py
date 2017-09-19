import os
import locale

# TODO
# - solve problem when 1.398,00 gets badly split
# -

locale.setlocale(locale.LC_ALL, 'de_DE')

statementsPath = "statements/"
csvSeparator = ';'

categories = { 1 : 'groceries', 2 : 'cash', 3 : 'fun', 4 : 'apartment', 5 : 'transport'}

def calculateBalanceForMonth(monthString):
    mainStatementPath = statementsPath + monthString + ".csv"
    creditcardStatementPath = statementsPath + monthString + "cc.csv"

    mainIncome, mainExpenses, mainCategories = parseStatementFile(mainStatementPath)
    ccIncome, ccExpenses, ccCategories = parseStatementFile(creditcardStatementPath)
    income = mainIncome + ccIncome
    expense = mainExpenses + ccExpenses
    print("------------------------------------")
    print("Income = " + str(income))
    print("Expenses = " + str(expense))
    print("Balance = " + str(income + expense))
    print("------------------------------------")
    print("Categories:")
    for cat in range(1,6):
        print(categories[cat] + ": " + str(mainCategories[cat] + ccCategories[cat]))

    f = open('results/' + monthString + '.txt', 'w')
    f.write('Income = ' + str(income) + '\n')
    f.write('Expense = ' + str(expense) + '\n')
    f.write('Balance = ' + str(income + expense) + '\n')
    f.write('--------------------------------------------\n')
    for cat in range(1,6):
        f.write(categories[cat] + ": " + str(mainCategories[cat] + ccCategories[cat]) + '\n')
        
def parseStatementFile(filePath):
    #fileFullPath = filename + "august2017.csv"
    #print("loading statements: " + fileFullPath)
    print("Parsing file..." + filePath)

    monthlyIncome = []
    monthlyExpenses = []
    categoryExpenses = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    f = open(filePath, "r")
    
    firstLine = f.readline()
    headers = firstLine.split(csvSeparator)
    amountIndex = -1
    for i, header in enumerate(headers):
        #print(header)
        if "Amount" in header:
            amountIndex = i

    if amountIndex == -1:
        print("error")
        return
    
    #for line in file.lines:
    for line in f:
        tokens = line.split(csvSeparator)
        amount = tokens[amountIndex]
        descrip = tokens[amountIndex + 1].rstrip()

        #skip kredit card items
        if ('Kreditkarte' in descrip) or ('Ihre Zahlung' in descrip): 
            continue
        
        if isIncome(amount):
            monthlyIncome.append(parseAmountToNumber(amount))
        else:
            monthlyExpenses.append(parseAmountToNumber(amount))
            category = getCategoryOfItem(amount, descrip)
            categoryExpenses[category] += parseAmountToNumber(amount)

    return sum(monthlyIncome), sum(monthlyExpenses), categoryExpenses

def parseAmountToNumber(numberStr):
    numberStr = numberStr.replace('.', '')
    number = locale.atof(numberStr)
    return number

def parseAndSum(amounts):
    sumAmount = 0
    for number in amounts:
        number = number.replace('.', '')
        amountNumber = locale.atof(number)
        sumAmount += amountNumber
    return sumAmount
    
def isIncome(amount):
    if '-' in amount:
        return False
    else:
        return True
        
def getCategoryOfItem(amount, descrip):
    descrip = descrip.upper()
    if ("SPAR" in descrip) or ("BILLA" in descrip) or ("HOFER" in descrip) or ("MERKUR" in descrip) or ("LIDL" in descrip) or ("BIPA" in descrip) or ("ALBERT" in descrip):
        return 1

    if "AUSZAHLUNG" in descrip:
        return 2

    if "NETFLIX" in descrip:
        return 3
    
    if ("MARCHFELDSTRASSE" in descrip) or ("MESSTECHNIK" in descrip) or ("UPC" in descrip):
        return 4
    
    if ("WIENER LINIEN" in descrip) or ("WR. LINIEN" in descrip) or ("T-MOBILE" in descrip) or ("ZLUTY.CZ" in descrip) or ("CD.CZ" in descrip):
        return 5 # transportation and communication

    return int(getCategoryFromUser(amount, descrip))
    #return 2
        
def getCategoryFromUser(amount, descrip):
    print("-------------------------------------------------------------------------")
    print(amount)
    print(descrip)
    print("-------------------------------------------------------------------------")
    print("Categorize this item:")
    print("(1) groceries, (2) cash, (3) fun, (4) apartment, (5) transport")
    cat = input("Category: ")
    return cat

def checkFolderForStatements():
    for (dirpath, dirnames, filenames) in os.walk(statementsPath):
        print(filenames)
    

#checkFolderForStatements()
#parseStatementFile(statementsPath)
calculateBalanceForMonth("may2017")
calculateBalanceForMonth("june2017")
calculateBalanceForMonth("july2017")
calculateBalanceForMonth("august2017")
