in1='1100000000110000010'
in2="100000000"
in3='100000000000100'
in4='1100000000110000010'
in5='1101001'
exp1='+-000-+0+-+-+00000-'
exp2='+000+-0-+'
exp3='+000+-0-+000-00'
exp4='+-000-+0+-+-00000+0'
exp5='+-0+00-'

inputsValues = [in1,in2,in3,in4,in5]
expectedValues=[exp1,exp2,exp3,exp4,exp5]

def encode(s):
    # find the length of the string 
    size = len(s)
    # flags 
    wasLow = True
    inASequence=False
    toIgnore=0
    # return value 
    result =""
    for i in range(size) : 
        if (int(s[i]) == 1): 
            if (wasLow):
                #this time should be high 
                result+="+"
                wasLow=False
            else: 
                #It was not low, so this time it should be low
                result+="-"
                wasLow=True 
        elif(int(s[i]) == 0 ): 
            # check if there are enough numbers in a range of 8
            # if we are in a sequence, then 8 rounds have been applied, continue
            if (inASequence and toIgnore>0): 
                toIgnore-=1
                continue 
            else : 
                # check the length
                # print(i)
                if (  (i+7) > size  ): 
                    result+="0"
                else : 
                    # check how many of them are zero 
                    next8 = s[i:(i+8)]
                    # if the eight of them are 0
                    if (next8.count('0') == 8): 
                        # Apply the corresponding sequence
                        inASequence=True
                        toIgnore=7
                        # if the previous was low 
                        if (wasLow): 
                            # apply the sequence for negative
                            result+="000-+0+-"
                            wasLow=True
                        else : 
                            # apply the sequence for positive 
                            result+="000+-0-+"
                            wasLow=False
                    else : 
                        # simply add 0
                        result+="0"  
        else: 
            # invalid value 
            print("Invalid value detected")
    # print(result)
    return result
    
def test(): 
    for i in range(5): 
        print("======  ")
        print(i)
        if (  encode(inputsValues[i]) == expectedValues[i] ):
            print ("ok")
        else: 
            print("not ok")

test()