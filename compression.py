def compress(text, limit):

    probabilities = [] # list that contains dictionaries -> chars, probalilities & used in combining them
    branch_source = {} # dictionary that contains keys:values -> name of merging node: dictionary having the 1st & 2nd probs in order
    originalCode_table = {} # dictionary that contains keys:values -> chars: original code
    symCode_table = {} # dictionary that contains keys:values -> chars: binary code


    # counting each char & calculating its prob
    for x in text:

        # if it's already calculated and added to the list, skip
        if x in (probability["char"] for probability in probabilities):
            continue

        else:
            count = text.count(x)
            prob = count / len(text)
            probabilities.append({"char": x, "prob": prob})


    # building original codes table
    num = len(probabilities)
    original_bits = max(1, (num-1).bit_length())  # representing in how many bits based on how many chars, n-1 -> 0 to 5 if 6 symbols

    # building it with first presence OR alphabetical
    # for i in range(num):
    #     x = probabilities[i]["char"]
    #     org_code = format(i, f"0{original_bits}b")
    #     originalCode_table[x] = org_code

    chars = sorted(p["char"] for p in probabilities)
    for i in range(len(chars)):
        x = chars[i]
        org_code = format(i, f"0{original_bits}b")
        originalCode_table[x] = org_code


    # building sybmol codes table

    # 1) getting "others" probability
    i = 0
    total = 0 

    while i < len(probabilities):
        prob = probabilities[i]["prob"]
        if prob <= limit:
            total += prob
            probabilities.pop(i)  # keeping the index, bec after deleting -> the next char becomes at the same index
        else:
            i +=1  # incrementing only if nothing is removed

    if total != 0:
        probabilities.append({"char": "others" , "prob": total})

    probabilities.sort(key=lambda p: p["prob"], reverse=True)  # arrange probs descendingly


    # 2) combining each last two probilities & saving them in branch_source 
    i = 1
    while len(probabilities) > 1: # bec. if one item, all combinations between symbols are done
       
        summ = probabilities[-1]["prob"] + probabilities[-2]["prob"]  # last + previous "greater"
        branch_source[f"merge{i}"] = {"first":probabilities[-2]["char"], "second":probabilities[-1]["char"]}

        probabilities.pop()
        probabilities.pop()

        # sorting way in case of tie: same first order OR the newest
        # probabilities.append({"char": f"merge{i}", "prob": summ})
        # probabilities.sort(key=lambda p: p["prob"], reverse=True)
        pos = 0
        while pos < len(probabilities) and round(probabilities[pos]["prob"], 9) > round(summ, 9):
            pos += 1
        probabilities.insert(pos, {"char": f"merge{i}", "prob": summ})

        i += 1


    # 3) assigning the binary codes
    symCode_table = {probabilities[0]["char"]: ""}  # start with the last merge name remained in probabilities list ex: "merge4": ""

    for name in reversed(list(branch_source)):
        code = symCode_table[name]  # getting the code assigned to that merge name, use it to build the next code
        del symCode_table[name]     # delete it bec. it's a merged name not a real char
        symCode_table[branch_source[name]["first"]] = code + "0"   # ex: others+b+c : 0
        symCode_table[branch_source[name]["second"]] = code + "1"  # ex: a : 1

    # if the text has only one char -> so, there's no merging process, then make it's code = 0
    if len(symCode_table) == 1:
        for key in symCode_table:
            symCode_table[key] = "0"


    # applying compression
    compressed = ""

    for x in text:
        if x in symCode_table:
            compressed += symCode_table[x]
        else:
            compressed += symCode_table["others"]
            compressed += originalCode_table[x]


    # reverse the two tables for decompression
    symDecode_table = {}
    for char, code in symCode_table.items():
        symDecode_table[code] = char

    originalDecode_table = {}
    for char, code in originalCode_table.items():
        originalDecode_table[code] = char

    return compressed, symDecode_table, originalDecode_table, original_bits