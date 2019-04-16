from QueryModule import *
#from SearchModule import *
import ast

searchDict = None

def form():
    filterDict = obtainFilterDictMT()
    conversionDict = obtainConversionDict()

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
    form_rows.append(TR("",INPUT(_type="submit",_value="Search")))
    form = FORM(TABLE(*form_rows))
    
    if form.process().accepted:
        global searchDict
        searchDict = form.vars
        session.flash = 'form accepted'
        redirect(URL('result'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'

    
    return dict(form=form,searchDict=form.vars)


def result():
    print('Redirect worked:')
    print(searchDict)
    return(dict(form=searchDict))
