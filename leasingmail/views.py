# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound 
from leasingforgotpassword.models import LeasingResetPassword
from leasingauth.models import LeasingUser
# Create your views here.

def ResetPassword(request, id):
    
    if request.method=="GET":
        try:
            q1= LeasingResetPassword.objects.values_list('client').get(hash=id, active=True)
            # return render(request,'password_recovery.html',{'id':q1[0],'hash':id})
            return render(request,'ResetPassword.html',{'id':q1[0],'hash':id})
        except Exception as e:
            return HttpResponseNotFound('not found')

    elif request.method == "POST":

        password = request.POST['password']
        conf_password = request.POST['conf_password']
        user_id = request.POST['user_id']
        hash_id= request.POST['hash_id']
        
        if password == conf_password:
            try:
                q1 = LeasingUser.objects.get(id=user_id)
                q1.set_password(password)
                q1.save()
                
                query_updat_activity = LeasingResetPassword.objects.get(hash=hash_id)
                query_updat_activity.active=False
                query_updat_activity.save()
                
                return HttpResponse('password reset done')
            except Exception as e:
                print(e)
                return HttpResponse('user not found')
        else:
            return HttpResponse('password did not match' )
