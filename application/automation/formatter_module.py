def formatter(number):
    numberFormatted = ""; 
    for i in str(number):
        if (i == '.'):
            numberFormatted += ','
        else:
            numberFormatted+= i
    dadaVuelta = numberFormatted[::-1]
    print(dadaVuelta)
    
    passedComma = False
    count = 0 
    realNumber = ""
    numbersBeforeComma = ""
    print(realNumber)
    for i in dadaVuelta: 
        if (passedComma):   
            count += 1 
            if (count % 3 == 0): 
                realNumber += i + '.'
            else: 
                realNumber += i
        else: 
            if (i == ','):
                passedComma = True
            else: 
                numbersBeforeComma += i 
    print(realNumber)
    return realNumber[::-1] + ',' + numbersBeforeComma[::-1] 

if __name__ == "__main__":
    print(formatter(0.00))