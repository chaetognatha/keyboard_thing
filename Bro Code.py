lst=[["a", "b", "c"], ["d", "e", "f"], ["g","h"]]
check="a"
print ["{} {}".format(index1,index2) for index1,value1 in enumerate(lst) for (index2,value2) in enumerate(value1) if value2==check]