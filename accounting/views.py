from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Account_names, Journal, Entities
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Sum, Q
from datetime import datetime


@login_required(login_url='login')
def index(request):
    if request.method == 'POST' and 'new_entity_name' in request.POST:
        new_entity_name = request.POST.get('new_entity_name')
        if Entities.objects.filter(entity_name=new_entity_name).exists():
            return HttpResponse('Entity name already exist')
        else:
            new_ety = Entities.objects.create(
                entity_name=new_entity_name)
            new_ety.save()
            messages.info(request,'Entity Added Successfully')
            return redirect('index')

    context={
        'entities':Entities.objects.only('entity_name').all(),
    }
    return render(request, 'index.html', context)


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        # terms = request.POST.getlist('terms')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'usrname taken')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email, first_name=name)
            user.save()


            return redirect('index')

    return render(request, 'pages-register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'index.html')
        else:
            messages.info(request, 'invalid credentials')

    return redirect('index')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def add_transaction(request,entity_name):
    accounts_list = Account_names.objects.filter(entity__entity_name=entity_name)
    # print(request, '',)
    if request.method == 'POST' and 'account_add_btn' in request.POST:

        new_ac_name = request.POST.get('new_ac_name')
        if Account_names.objects.filter(Q(ac_name=new_ac_name) & Q(entity__entity_name=entity_name)).exists():
            return HttpResponse('Account name already exist')
        else:
            is_loan_ac = request.POST.get('is_loan_ac')
           
            ety=Entities.objects.get(entity_name=entity_name)
            new_ac = Account_names.objects.create(
                ac_name=new_ac_name, is_loan_ac=is_loan_ac,entity=ety)
            new_ac.save()
            messages.info(request,'Account added successfully')
            # print(entity_name)
            # context={
            #     'entity_name':entity_name,
            #     'entities':Entities.objects.only('entity_name').all()
            # }
            # print(context['entity_name'])
            # return redirect('add transaction',context)

    elif request.method == 'POST' and "transaction_btn2" in request.POST:

        date = request.POST.get('date')
        r_v_number = request.POST.get('r_v_number')
        r_v_number = None if r_v_number == '' else r_v_number
        item = request.POST.get('item')
        item = None if item == '' else item
        account = Account_names.objects.get(
            ac_name=request.POST.get('account'))
        debit = request.POST.get('debit')
        credit = request.POST.get('credit')
        if debit == '' and credit != '':
            debit = None
            credit = int(credit)
        elif debit != '' and credit == '':
            debit = int(debit)
            credit = None
        else:
            return HttpResponse('Check Debit or Credit')
        
        ety=Entities.objects.get(entity_name=entity_name)
        journal_obj = Journal.objects.create(
            date=date, r_v_number=r_v_number, item=item, account=account, debit=debit, credit=credit, entity=ety
        )
        journal_obj.save()
        messages.info(request,'Transaction added Successfully')
    # else:
    #     print('if failed')
    # # print(request.POST)

    context = {
        'account_names': accounts_list,
        'entity_name':entity_name,
        'entities':Entities.objects.only('entity_name').all(),
    }

    return render(request, 'add_transaction.html', context)


@login_required(login_url='login')
def journal_view(request,entity_name):
    print(entity_name)
    if request.method == 'POST' and request.POST.get('from_date') != '' and request.POST.get('to_date') != '':
        print('date ok')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        journals = Journal.objects.filter(Q(date__range=[from_date, to_date]) & Q(entity__entity_name=entity_name))
        
        total_debit = sum([i.debit for i in journals if i.debit != None])
        total_credit = sum([i.credit for i in journals if i.credit != None])
        
        context={
            'journals': journals,
            'from_date': datetime.strptime(from_date, '%Y-%m-%d').strftime('%d-%b-%Y'),
            'to_date': datetime.strptime(to_date, '%Y-%m-%d').strftime('%d-%b-%Y'),
            'entity_name':entity_name,
            'entities':Entities.objects.only('entity_name').all(),
            'total_debit':total_debit,
            'total_credit':total_credit,
            }
        return render(request, 'journal.html',context)
        
    journals = Journal.objects.filter(entity__entity_name=entity_name)
    
    
    total_debit = sum([i.debit for i in journals if i.debit != None])
    total_credit = sum([i.credit for i in journals if i.credit != None])
    print(total_credit,total_debit)
    context={
        'journals': journals,
        'entity_name':entity_name,
        'entities':Entities.objects.only('entity_name').all(),
        'total_debit':total_debit,
        'total_credit':total_credit,
        }
    
    return render(request, 'journal.html', context)


@login_required(login_url='login')
def balance_sheet(request,entity_name):
    if request.method == 'POST' and request.POST.get('from_date') != '' and request.POST.get('to_date') != '':

        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        # Taking Non-loan account transactions details...
        acs_1 = Journal.objects.filter(Q(account__is_loan_ac=False) & Q(date__range=[from_date, to_date]) & Q(entity__entity_name=entity_name)).order_by().values_list('account__ac_name').distinct()
        balance_sheet_1 = []

        for i in acs_1:
            debit_1 = Journal.objects.filter(Q(account__ac_name=i[0]) & Q(account__is_loan_ac=False) & Q(entity__entity_name=entity_name)).aggregate(Sum('debit'))['debit__sum']
            credit_1 = Journal.objects.filter(Q(account__ac_name=i[0]) & Q(account__is_loan_ac=False) & Q(entity__entity_name=entity_name)).aggregate(Sum('credit'))['credit__sum']
            debit_1=debit_1 if debit_1 != None else 0
            credit_1=credit_1 if credit_1 != None else 0
            balance_1 = int(credit_1)-int(debit_1)

            balance_sheet_1.append({
                'ac_name': i[0],
                'debit': debit_1,
                'credit': credit_1,
                'balance': balance_1,
            })

        # Taking loan account transactions details...
        acs_2 = Journal.objects.filter(Q(account__is_loan_ac=True) & Q(date__range=[from_date, to_date]) & Q(entity__entity_name=entity_name)).order_by().values_list('account__ac_name').distinct()
        balance_sheet_2 = []

        for i in acs_2:
            debit_2 = Journal.objects.filter(Q(account__ac_name=i[0]) & Q(account__is_loan_ac=True) & Q(entity__entity_name=entity_name) & Q(date__range=[from_date, to_date])).aggregate(Sum('debit'))['debit__sum'],
            credit_2 = Journal.objects.filter(Q(account__ac_name=i[0]) & Q(account__is_loan_ac=True) & Q(entity__entity_name=entity_name) & Q(date__range=[from_date, to_date])).aggregate(Sum('credit'))['credit__sum'],
            debit_2=debit_2[0] if debit_2[0] != None else 0
            credit_2=credit_2[0] if credit_2[0] != None else 0
            
            balance_2 = int(credit_2)-int(debit_2)

            balance_sheet_2.append({
                'ac_name': i[0],
                'debit':  debit_2,
                'credit': credit_2,
                'balance': balance_2,
            })

        total_debit_1 = sum([i['debit'] for i in balance_sheet_1 if i['debit'] != None])
        total_credit_1 = sum([i['credit'] for i in balance_sheet_1 if i['credit'] != None])
        # total_debit_1 = total_debit_1 if total_debit_1 != None else 0
        # total_credit_1 = total_credit_1 if total_credit_1 != None else 0
        
        total_balance_1 = int(total_credit_1)-int(total_debit_1)

        total_debit_2 = sum([i['debit'] for i in balance_sheet_2 if i['debit'] != None])
        total_credit_2 = sum([i['credit'] for i in balance_sheet_2 if i['credit'] != None])
        # total_debit_1 = total_debit_1 if total_debit_1 != None else 0
        # total_credit_1 = total_credit_1 if total_credit_1 != None else 0
        
        total_balance_2 = int(total_credit_2)-int(total_debit_2)

        context = {
            'balance_sheet_1': balance_sheet_1,
            'total_debit_1': total_debit_1,
            'total_credit_1': total_credit_1,
            'total_balance_1': total_balance_1,

            'balance_sheet_2': balance_sheet_2,
            'total_debit_2': total_debit_2,
            'total_credit_2': total_credit_2,
            'total_balance_2': total_balance_2,

            'from_date': datetime.strptime(from_date, '%Y-%m-%d').strftime('%d-%b-%Y'),
            'to_date': datetime.strptime(to_date, '%Y-%m-%d').strftime('%d-%b-%Y'),
            
            'entity_name':entity_name,
            'entities':Entities.objects.only('entity_name').all()
        }
        return render(request, 'balance_sheet.html', context)
    


# taking full balance sheet without date range when first visit to balance sheet view

    # Taking Non-loan account transactions details...
    acs_1 = Journal.objects.filter(Q(account__is_loan_ac=False) & Q(entity__entity_name=entity_name)).order_by().values_list('account__ac_name').distinct()
    balance_sheet_1 = []

    for i in acs_1:
        debit_1 = Journal.objects.filter(Q(account__ac_name=i[0]) & Q(account__is_loan_ac=False) & Q(entity__entity_name=entity_name)).aggregate(Sum('debit'))['debit__sum']
        credit_1 = Journal.objects.filter(Q(account__ac_name=i[0]) & Q(account__is_loan_ac=False) & Q(entity__entity_name=entity_name)).aggregate(Sum('credit'))['credit__sum']
        debit_1=debit_1 if debit_1 != None else 0
        credit_1=credit_1 if credit_1 != None else 0
        balance_1 = int(credit_1)-int(debit_1)

        balance_sheet_1.append({
            'ac_name': i[0],
            'debit': debit_1,
            'credit': credit_1,
            'balance': balance_1,
        })

    # Taking loan account transactions details...
    acs_2 = Journal.objects.filter(Q(account__is_loan_ac=True) & Q(entity__entity_name=entity_name)).order_by().values_list('account__ac_name').distinct()
    balance_sheet_2 = []

    for i in acs_2:
        debit_2 = Journal.objects.filter(Q(account__ac_name=i[0]) & Q(account__is_loan_ac=True) & Q(entity__entity_name=entity_name)).aggregate(Sum('debit'))['debit__sum'],
        credit_2 = Journal.objects.filter(Q(account__ac_name=i[0]) & Q(account__is_loan_ac=True) & Q(entity__entity_name=entity_name)).aggregate(Sum('credit'))['credit__sum'],
        debit_2=debit_2[0] if debit_2[0] != None else 0
        credit_2=credit_2[0] if credit_2[0] != None else 0
        
        balance_2 = int(credit_2)-int(debit_2)

        balance_sheet_2.append({
            'ac_name': i[0],
            'debit':  debit_2,
            'credit': credit_2,
            'balance': balance_2,
        })

    total_debit_1 = sum([i['debit'] for i in balance_sheet_1 if i['debit'] != None])
    total_credit_1 = sum([i['credit'] for i in balance_sheet_1 if i['credit'] != None])
    # total_debit_1 = total_debit_1 if total_debit_1 != None else 0
    # total_credit_1 = total_credit_1 if total_credit_1 != None else 0
    
    total_balance_1 = int(total_credit_1)-int(total_debit_1)

    total_debit_2 = sum([i['debit'] for i in balance_sheet_2 if i['debit'] != None])
    total_credit_2 = sum([i['credit'] for i in balance_sheet_2 if i['credit'] != None])
    # total_debit_1 = total_debit_1 if total_debit_1 != None else 0
    # total_credit_1 = total_credit_1 if total_credit_1 != None else 0
    
    total_balance_2 = int(total_credit_2)-int(total_debit_2)

    context = {
        'balance_sheet_1': balance_sheet_1,
        'total_debit_1': total_debit_1,
        'total_credit_1': total_credit_1,
        'total_balance_1': total_balance_1,

        'balance_sheet_2': balance_sheet_2,
        'total_debit_2': total_debit_2,
        'total_credit_2': total_credit_2,
        'total_balance_2': total_balance_2,

        # 'from_date': datetime.strptime(from_date, '%Y-%m-%d').strftime('%d-%b-%Y'),
        # 'to_date': datetime.strptime(to_date, '%Y-%m-%d').strftime('%d-%b-%Y'),
        
        'entity_name':entity_name,
        'entities':Entities.objects.only('entity_name').all()
    }
    
    
    # context={
    #     'entity_name':entity_name,
    #     'entities':Entities.objects.only('entity_name').all(),
    # }
    return render(request, 'balance_sheet.html',context)






@login_required(login_url='login')
def edit_transaction(request,pk):
    transaction = Journal.objects.get(id=pk)
    entity_name = transaction.entity.entity_name
    if request.method == 'POST' and "edit_transaction_btn" in request.POST:
        
        date = request.POST.get('date')
        r_v_number = request.POST.get('r_v_number')
        r_v_number = None if r_v_number == '' else r_v_number
        item = request.POST.get('item')
        item = None if item == '' else item
        account = Account_names.objects.get(
            ac_name=request.POST.get('account'))
        debit = request.POST.get('debit')
        credit = request.POST.get('credit')
        if debit == '' and credit != '':
            debit = None
            credit = int(credit)
        elif debit != '' and credit == '':
            debit = int(debit)
            credit = None
        else:
            return HttpResponse('Check Debit or Credit')
        
        ety = Entities.objects.get(entity_name=entity_name)
        Journal.objects.filter(id=pk).update(
            date=date, r_v_number=r_v_number, item=item, account=account, debit=debit, credit=credit, entity=ety
        )
        # journal_obj.save()
        messages.info(request,'Transaction Updated Successfully')
        # context={
        #     'entity_name':ety,
        #     'entities':Entities.objects.only('entity_name').all(),
        #     }
        return redirect('journal',entity_name=str(ety))

    context = {
        'entity_name':entity_name,
        'transaction':transaction,
        'account_names':Account_names.objects.only('ac_name').filter(entity__entity_name=entity_name),
        'entities':Entities.objects.only('entity_name').all(),
    }

    return render(request, 'edit_transaction.html', context)

