# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny, IsAdminUser)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from leasingauth.models import (LeasingUser,
                                LeasingClient,
                                LeasingClientInviteToken)
from leasingapi.models import (ClientSetting,
                               DocumentUpload,
                               LegalPosition,
                               ExportResult, KeyText)
from leasingapi.serializers import (LeasingUserInfoSerializer,
                                    UserLoginSerializer,
                                    LeasingSignupSerializer,
                                    ClientSettingModelSerializer,
                                    DoucmentUploadModelSerializer,
                                    LeasingClientInviteTokenModelSerializer,
                                    LegalPositionModelSerializer,
                                    ReasonSerializer,
                                    TextSearchSerializer,
                                    ExportResultSerializer,
                                    ForgotLoginSerializer)
from leasingmail.models import EmailQueue, EmailLog
from leasingforgotpassword.models import LeasingResetPassword
from django.shortcuts import (get_object_or_404, _get_queryset)
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
# from leasingai.ai.clause_analyze import (main, clean, create_table)
from leasingai.ai.clause_analyze import (main, create_table)
from leasingai.ai.classify_clause import matching_rate
from django.core.files import File
from django.conf import settings
import json
from docx import Document
from docx.shared import Inches
import pdb
from django.db.models import Q
from django.conf import settings
from leasingapi.models import _create_short_hash
from leasingai.helpers.checkup import execute_NLP_backend
#############################
# HELPER FUNCTION BEGINS HERE
#############################


def get_client_or_401(klass, *args, **kwargs):
    """
    Use get() to return an object, or raise a PermissionDenied exception if the object
    does not exist.
    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_401() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise PermissionDenied('No %s matches the given query.' % queryset.model._meta.object_name)


#################################
# API VIEWSET CLASSES BEGINS HERE
#################################


class LoginViewSet(ModelViewSet):
    """
    API model viewset used to login
    using API and receive an Authentication token
    in response
    """

    queryset = LeasingUser.objects.none()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['post', 'option', 'head']

    def create(self, request, *args, **kwargs):
        print("request.post is", request.data)
        username = request.data.get('username').lower()
        password = request.data.get('password')
        auth = authenticate(username=username, password=password)
        if auth is not None:
            user = LeasingUser.objects.get(username=username)
            if not Token.objects.filter(user=user).exists():
                Token.objects.create(user=user)
                token = Token.objects.get(user=user).key
            else:
                token = Token.objects.get(user=user).key
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'token': None},
                            status=status.HTTP_401_UNAUTHORIZED)


class LogoutViewSet(ModelViewSet):
    """
    API model viewset used to logout
    using API. This endpoint will remove the
    """
    queryset = LeasingUser.objects.none()
    serializer_class = UserLoginSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', 'options', 'head']

    def list(self, request, *args, **kwargs):
        if Token.objects.filter(user=request.user).exists():
            Token.objects.get(user=request.user).delete()
            return Response({'status': 'Token Removed From Database'},
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'No token to remove already logged out'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SignUpViewSet(ModelViewSet):
    """
    API model viewset used to logout
    using API. This endpoint will remove the
    """
    queryset = LeasingUser.objects.none()
    serializer_class = LeasingSignupSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['post', 'option', 'head']

    def create(self, request, *args, **kwargs):
        print(request.data)
        token = request.data.get('invite_token', None)
        if token is not None:
            try:
                validate_token = LeasingClientInviteToken.objects.get(
                    invite_token=token)
                print(request.data)
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    user.set_password(request.data.get('password',None))
                    user.save()
                    validate_token.client = user
                    validate_token.save()
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
            except LeasingClientInviteToken.DoesNotExist:
                return Response({'error': {'invite_token': ["Invite token is not valid", ]}}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No invite token provided'}, status=status.HTTP_400_BAD_REQUEST)


class LeasingUserInfoViewSet(ModelViewSet):
    """
    API endpoint to get the info of the logedin
    LeasingClient
    """
    queryset = LeasingUser.objects.none()
    serializer_class = LeasingUserInfoSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', 'option', 'head']

    def get_queryset(self):
        try:
            user_id = self.kwargs['pk']
            return LeasingUser.objects.filter(id=user_id)
        except KeyError:
            return LeasingUser.objects.filter(id=self.request.user.id)


class ClientSettingModelViewSet(ModelViewSet):
    """
    ModelViewSet used for client settings and 
    it can accept all available HTTP methods 
    """

    queryset = ClientSetting.objects.none()
    serializer_class = ClientSettingModelSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        try:
            id = self.kwargs['pk']
            client_setting = ClientSetting.objects.get(id=id)
            return ClientSetting.objects.filter(id=client_setting.id)
        except KeyError:
            try:
                return ClientSetting.objects.filter(id=LeasingClient.objects.get(id=self.request.user.id).client_settings.order_by('id').last().id)
            except ObjectDoesNotExist:
                return self.queryset
        except ObjectDoesNotExist:
            return self.queryset

    def perform_create(self, serializer):
        print("\n perform_create is called on settings \n")

    def create(self, request, *args, **kwargs):
        request_data = dict(request.data)
        print("___ request.data without client is _____", request_data)
        request_data['client'] = request.user.leasingclient
        print("_____ request data after adding client is ___", request_data)
        context = {'request': self.request}
        serializer = self.serializer_class(data=request_data,
                                           context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentUploadModelViewSet(ModelViewSet):
    """
    ModelViewset used to upload the doucment 
    that are submited by clients . It accept all of HTTP methods 
    """
    queryset = DocumentUpload.objects.all()
    serializer_class = DoucmentUploadModelSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        print("perform_create is called for document upload")
        serializer.save(client=LeasingClient.objects.get(id=self.request.user.id))


class LeasingClientInviteTokenModelViewSet(ModelViewSet):
    """
    model viewset class  used to show all
    inivite tokens but only to admins
    """
    queryset = LeasingClientInviteToken.objects.all()
    serializer_class = LeasingClientInviteTokenModelSerializer
    permission_classes = [IsAdminUser, ]


class LegalPositionModelViewSet(ModelViewSet):
    """
    ModelViewSet used to provide  the complete 
    access to user's legal positions
    """

    queryset = LegalPosition.objects.none()
    serializer_class = LegalPositionModelSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        try:
            user = LeasingClient.objects.get(id=self.request.user.id)
            return LegalPosition.objects.filter(client=user)
        except LeasingClient.DoesNotExist:
            return LegalPosition.objects.none()

    def perform_create(self, serializer):
        print("\n __perform_create has been called on legalpositions __\n")
        serializer.save(client=LeasingClient.objects.get(id=self.request.user.id))

    def create(self, request, *args, **kwargs):
        request_data = request.data
        print("request data is ", request_data)
        context = {'request': self.request}
        serializer = self.serializer_class(data=request_data,
                                           many=True,
                                           context=context)
        if serializer.is_valid():
            # condition when serializers have validated the mode
            print(" Serializer is Valid ")
            serializer.save()
            export_results=[]
            document_id = serializer.data[0]['document']
            for data in json.loads(json.dumps(serializer.data)):
                print("LegalPositionSerializer_data is", data)
                temp_exported_results = {
                    "id": "",
                    "action": "",
                    "agree": "",
                    "clause_no": "",
                    "clausename": "",
                    "index": '',
                    "keep": '',
                    "reason": ""
                }
                temp_exported_results["significance_data"] = json.loads(execute_NLP_backend(document_id, data['id']))
                export_results.append(temp_exported_results)
                return Response(export_results, status=status.HTTP_200_OK)  # check response is 200 not 201 since we haven't saved anything to exported results
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LegalTableReasonViewSet(ModelViewSet):
    """
    ModelViewSet used to provide the
    reason view
    """

    queryset = LegalPosition.objects.none()
    serializer_class = ReasonSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return LegalPosition.objects.all().distinct('clause_name')


class TextSearchViewSet(ModelViewSet):
    """
    model viewset that accept  : reason, : clause_name  as query_parameters 
    and return a list of key text associated with them,  In case if these two
    queury parameters are not provided, This viewset  will return empty list 
    and event in case of 'No match found' an empty list will be returned
    """

    queryset = LegalPosition.objects.all()
    serializer_class = TextSearchSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'option', 'head']

    def list(self, request, *args, **kwargs):
        data = request.query_params
        print("data in the request is %s %s" % (request.query_params.get('reason', None),
                                                request.query_params.get('clause_name', None)))
        if((request.query_params.get('clause_name', None) is not None) and (request.query_params.get('reason', None) is not None)):
            key_texts = KeyText.objects.filter(legal_positions__clause_name__text__icontains=data['clause_name'],
                                                     legal_positions__reason__icontains=data['reason']).distinct('content')
            return Response(self.serializer_class(key_texts, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response(list(), status=status.HTTP_200_OK)


class ForgotLoginViewSet(ModelViewSet):

    queryset = LeasingUser.objects.all()
    serializer_class = ForgotLoginSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['post', 'option', 'head']

    def create(self, request, *args, **kwargs):
        request_data = dict(request.data)
        username = request_data['username']
        try:
            q1 = LeasingUser.objects.get(Q(username = username) | Q(email=username))
            subject = 'reset your password'
            body = 'this is a autogenerated mail to reset you password'
            query_reset_password =  LeasingResetPassword.objects.filter(client=q1, active=True)
            if query_reset_password:
                print('LeasingResetPassword exist')
                try:
                    query_check_email_queue = EmailQueue.objects.get(reset_password = query_reset_password)
                    print('mail is in email queue')
                    return Response('Please wait mail was send to your email', status=status.HTTP_200_OK)
                except Exception as e:
                    query_check_email_log = EmailLog.objects.filter(reset_password=query_reset_password)
                    if query_check_email_log:
                        print('mail is in email log')
                        print('resend email')
                    else:
                        print('email is not in queue and log')
            else:
                query_create_reset_password = LeasingResetPassword.objects.create(client=q1, hash=_create_short_hash())
                EmailQueue.objects.create(subject = subject, body = body, to_email=q1.email, from_email=settings.DEFAULT_FROM_EMAIL, reset_password=query_create_reset_password)
                print('new password rest created and added in email queue')

            return Response(self.serializer_class(q1, many=False).data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response('user not found %s'%(e), status=status.HTTP_404_NOT_FOUND)
