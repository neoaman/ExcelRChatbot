from datetime import datetime
import datetime as dt


def courseduration(course):
    duration = {'Data Science': '5 months', 'Data Analyst': '2 months',
                'Master in Data Science': '12 months','AI':"12 months","PMP":"6 months","Tableau":"1 month"}

    speech = '{} course duration is about {}'.format(course, duration[course])
    return {
        "fulfillmentText": speech,
    }

def appointmentset(args):

    
    """ For Location of Appointment_______________ """
    avilloc = ['Bengaluru', 'Pune', 'Hyderabad', 'Mumbai']
    if args[0] not in avilloc:
        s2 = "There is no ExcelR Branch at {} . ".format(args[0])
        args[0] = 'Bengaluru'
    else:
        s2 =""
    
    """ Final Post """
    speech = s2+'One of Our Sales person from , Excelr {} for {} Course will contact you very soon. Are You Ok with it ?'.format(args[0], args[1])
    
    return args,{
        "fulfillmentText": speech,
    }

def coursefees(*args):
    """ Course fees in Dictonary format """
    duration = {'Data Science': '46000/-', 'Data Analyst': '30000/-',
                'Master in Data Science': '120000/-','AI':"70000/-","PMP":"40000/-","Tableau":"Free with all courses except PMP"}
    speech = '{} Course is {}'.format(args[0], duration[args[0]])
    return {
        "fulfillmentText": speech,
    }

    



