import re
from django.shortcuts import render
from django.http import HttpResponse

bank = r'([BIDV]{4}(?= [+|-]))|([VietinBank]{10}(?=:))|([Agribank]{8}(?=:))|([TPBank]{6}(?=\):))|((?<=VND\. )[Ref]{3})'

rAccountNumber = [r'([0-9]{14})(?= tai)', r'([0-9]{12})(?=[\|]GD:)'
                  , r'([0-9]{13})(?=[-|+|thay doi])', r'[x]{4}[0-9]{7}', r'([0-9]{13})(?=:)']

rIn = [r'([\+|-])([0-9]+[,])+([0-9]+)', r'([\+|-])([0-9]+)'
       , r'([\+|-])([0-9]+[,])+([0-9]+)', r'([\+|-])([0-9]+)', r'([\+|-])([0-9]+[,])+([0-9]+)']

rTime = [r'[0-9]{2}[:][0-9]{2}', r'[0-9]{2}[:][0-9]{2}([:][0-9]{2})?', r'[0-9]{2}[:][0-9]{2}([:][0-9]{2})?'
         , r'[0-9]{2}[:][0-9]{2}([:][0-9]{2})?', r'[0-9]{2}[:][0-9]{2}([:][0-9]{2})?']

rDate = [r'[0-9]{2}[\/|-][0-9]{2}[\/|-][0-9]{2,4}', r'[0-9]{2}[\/|-][0-9]{2}[\/|-][0-9]{2,4}'
         , r'[0-9]{2}[\/|-][0-9]{2}[\/|-][0-9]{2,4}', r'[0-9]{2}[\/|-][0-9]{2}[\/|-][0-9]{2,4}', r'[0-9]{2}[\/|-][0-9]{2}[\/|-][0-9]{2,4}']

rContent = [r'(?<=ND:)(.*)', r'(?<=ND:)(.*)', r'(?<=Ref).*', r'(?<=ND:)(.*)', r'(?<=[\(])(.*)(?=\))']

rBalance = [r'(([0-9]+[,])+([0-9]+))(?=VND[\.|;])', r'(([0-9]+[,])+([0-9]+))(?=VND\|ND:)'
            , r'(([0-9]+[,])+([0-9]+))(?=VND[\.])', r'(([0-9]+[,])+([0-9]+))(?= VND)', r'(([0-9]+[,])+([0-9]+))(?=VND[\.])']

service = r'((?<=(tai|TAI))ATM)|(ATM(?=.))|(Topup|TOP-UP)|(MOMO(?=.)|(POS))'

result = {'Bank':'', 'TK':'', 'Time':'', 'Amount':'','Currency':'', 'Content':'', 'Service':''}

def MessageBank(message, i):
    a = re.search(rAccountNumber[i], message)
    if a:
        result['TK'] = a.group()

    I = re.search(rIn[i], message)
    if I:
        result['Amount'] = I.group()

    t = re.search(rTime[i], message)
    if t:
        result['Time'] = t.group()

    d = re.search(rDate[i], message)
    if d:
        result['Time'] = result['Time'] +' ' + d.group()

    c = re.search(rContent[i], message)
    if c:
        result['Content'] = c.group()
        s = re.search(service, c.group())
        if s:
            if s.group() == 'ATM': result['Service'] = 'giao dich rut tien tu ATM'
            elif s.group() == 'Topup' or 'TOP_UP': result['Service'] = 'giao dich tra tien dien thoai'
            elif s.group() == 'MOMO': result['Service'] = 'giao dich nap tien vaoo vi dien tu momo'
            elif s.group == 'POS': result['Service'] = 'dung the mua hang'
        else: result['Service'] = 'chua xac dinh giao dich'

    b = re.search(rBalance[i], message)
    if b:
        result['Currency'] = b.group() + 'VND'

def index(request):
    return render(request, 'sms/index.html')

def results(request):
    messag = request.POST.get('message', False)
    message = str(messag)
    print(messag)
    print(message)
    #message = dict.get('message', ' ')
    i = -1;
    m = re.search(bank, message)

    if m:
        if m.group() == 'BIDV':
            i = 0
            result['Bank'] = 'BIDV'
        elif m.group() == 'VietinBank':
            i = 1
            result['Bank'] = 'VietinBank'
            #print('i = ', i)
        elif m.group() == 'Ref':
            i = 2
            result['Bank'] = 'Vietcombank'
            #print('i = ', i)
        elif m.group() == 'TPBank':
            i = 3
            result['Bank'] = 'TPBank'
        elif m.group() == 'Agribank':
            i = 4
            result['Bank'] = 'Agribank'
    MessageBank(message, i)
    list = [message, result['Bank'], result['TK'], result['Time'], result['Amount'], result['Currency'], result['Content'], result['Service']]
    content = {
        'list':list,
    }
    for k in result.keys():
        result[k] = ' '
    return render(request,'sms/results.html', content)
