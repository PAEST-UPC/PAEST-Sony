from QueryModule import *
#from SearchModule import *
import ast


def form():
    filterDict = obtainFilterDictMT()
    conversionDict = obtainConversionDict()
    #filterDict = ast.literal_eval(open(r"C:\Users\Ruben\Documents\Universidad\4B\PAE\test\filt.txt", "r").read())
    #conversionDict = ast.literal_eval(open(r"C:\Users\Ruben\Documents\Universidad\4B\PAE\test\conv.txt", "r").read())

    form_rows = []
    for (tableName, filterName) in filterDict:
        values = ['']
        for tupled_value in filterDict[(tableName,filterName)]:
            for value in tupled_value:
                if (tableName,filterName,value) in conversionDict:
                    values.append(conversionDict[(tableName,filterName,value)])
                else:
                    values.append(value)

        form_rows.append(TR(filterName,SELECT(values,_name=(tableName,filterName))))
    form_rows.append( TR("",INPUT(_type="submit",_value="Search")))
    form = FORM(TABLE(*form_rows))
    
    print(request.vars)
    
    return dict(form=form,searchDict=form.vars)
