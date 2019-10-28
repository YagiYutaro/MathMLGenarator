import xml.etree.ElementTree as et
import xml.dom.minidom as md

dic_operator = {'+':0,'-':0,'*':1,'/':2,'=':-2,'(':-3,'^':3,'exp':4,'minus':4}

def is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

def brackets(stack):
    for i,char in enumerate(reversed(stack)):
        if char == "(":
            return len(stack)-(i+1)

def checkFunction(operand,stack_operator):
    if operand=="-":
        stack_operator.append("munis")
        operand=""
    elif operand=="exp":
        stack_operator.append("exp")
        operand=""
    return operand

def makeRPN(exp):
    stack_operator = []
    operand = ""
    result = []
    str_exp = list(exp)
    for char in str_exp:
        if char == "(":
            operand = checkFunction(operand,stack_operator)
            stack_operator.append(char)
        elif char == ")":
            if len(operand) != 0:
                result.append(operand)
                operand = ""
            bracket_point = brackets(stack_operator)
            result.extend(reversed(stack_operator[bracket_point+1:]))
            stack_operator = stack_operator[:bracket_point]
        elif char == "-" and len(operand)==0:
            stack_operator.append("minus")
            operand = ""
        elif char in list(dic_operator.keys()):
            if len(operand) != 0:
                result.append(operand)
                operand = ""
            if len(stack_operator) != 0:
                while dic_operator[char] <= dic_operator[stack_operator[-1]]:
                    result.append(stack_operator.pop())
                    if len(stack_operator) == 0:
                        break
            stack_operator.append(char)
        else:
            operand += char
    if len(operand) != 0:
        result.append(operand)
    while len(stack_operator) > 0:
        result.append(stack_operator.pop())
    return result

def makeMathML(factor):
    txt = ""
    if factor == "+":
        txt += "<plus/>\n"
    elif factor == "*":
        txt += "<times/>\n"
    elif factor == "-":
        txt += "<minus/>\n"
    elif factor == "/":
        txt += "<divide/>\n"
    elif factor == "=":
        txt += "<eq/>\n"
    elif factor == "^":
        txt += "<power/>\n"
    elif factor == "exp":
        txt += "<exp/>\n"
    elif factor == "minus":
        txt += "<minus/>\n"
    elif is_num(factor):
        txt += "<cn>"+factor+"</cn>\n"
    else:
        txt += "<ci>"+factor+"</ci>\n"
    return txt

def makeTree(lst_RPN):
    stack = []
    lst = []
    minus = ""
    for factor in lst_RPN:
        if factor in dic_operator.keys():
            if factor=="exp" or factor=="minus":
                txt = makeMathML(factor)
                txt += "<apply>\n"
                txt += stack.pop()
                txt += "</apply>\n"
                stack.append(txt)
            else:
                txt = makeMathML(factor)
                pre = stack.pop()
                back = stack.pop()
                txt += "<apply>\n"
                txt += back
                txt += "</apply>\n"
                txt += "<apply>\n"
                txt += pre
                txt += "</apply>\n"
                stack.append(txt)
        else:
            stack.append(minus+makeMathML(factor))
            minus = ""
        #print(stack)
    return stack[0]
#数式部生成
with open("input_exp.txt") as f: #元数式読み込み
    vec_exp = [s.strip() for s in f.readlines()]
mathML = "<math>\n"
set_var = set()
for exp in vec_exp:
    mathML += "<apply>\n"
    exp = exp.replace(' ','')
    RPN = makeRPN(exp)
    mathML += makeTree(RPN)
    mathML += "</apply>\n"
    #変数リスト作成
    lst_var = [var for var in RPN if not var in list(dic_operator.keys())]
    lst_var = [var for var in lst_var if not is_num(var)]
    set_var |= set(lst_var)
mathML += "</math>\n"
#変数宣言部生成
variableML = ""
with open("input_initialvalue.txt") as f: #元数式読み込み
    vec_value = [s.strip() for s in f.readlines()]
    for value in vec_value:
        seq = value.split("=")
        variableML += '<variable name="'+seq[0]+'" initial_value="'+seq[1]+'"/>\n'
        set_var.remove(seq[0])
componentName = "Main"
with open("test.cellml", mode='w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<component name="'+componentName+'">\n')
    f.write(variableML)
    for var in list(set_var):
        f.write('<variable name="'+var+'"/>\n')
    f.write(mathML)
    f.write("</component>")
""" #debug
#exp = "y=10+20*30-40+50"
#exp = "Epac2=cAMPtot/(0.02+cAMPtot)"
#alphap=1/(8.23*exp(-(Vm)/6.5)+1.03*exp(-(Vm)/500))
#exp = "alphaq=1/(1142857*exp(-(-Vm+VshiftKDr)/10)+10857*exp(-(-Vm+VshiftKDr)/3000))"
exp = "alphaq=1/(1142857*exp(-(-Vm+VshiftKDr)/10)+10857*exp(-(-Vm+VshiftKDr)/3000))"
exp = exp.replace(' ','')
RPN = makeRPN(exp)
print(RPN)
mathML = "<math>\n<apply>\n"
mathML += makeTree2(RPN)
mathML += "</apply>\n</math>\n"
with open("test.xml", mode='w') as f:
    f.write(mathML)
"""
