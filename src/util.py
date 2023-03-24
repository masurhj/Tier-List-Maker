def arrayToPrettyString(array):
    result = ""
    for item in array:
        result += item + ","
    return result[0:len(result)-1]