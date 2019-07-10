# -*- coding: utf-8 -*-
from __future__ import unicode_literals



class LeasingUserInfoSerializer(ModelSerializer):

    class Meta:
        model = LeasingUser
        exclude = ['password']


class LeasingSignupSerializer(ModelSerializer):
    token = SerializerMethodField()

    def get_token(self, instance):
        return Token.objects.get(user=instance).key

    class Meta:
        model =  LeasingClient
        exclude = ('last_login',
                   'is_active',
                   'is_staff',
                   'is_admin',
                   'date_joined')


class UserLoginSerializer(ModelSerializer):

    class Meta:
        model = LeasingUser
        exclude = ('id', 'last_login', 'first_name',
                   'last_name', 'is_active', 'is_staff',
                   'is_admin', 'date_joined', 'email')


class ClientSettingModelSerializer(ModelSerializer):

    class Meta:
        model = ClientSetting
        fields = "__all__"


class DoucmentUploadModelSerializer(ModelSerializer):

    class Meta:
        model = DocumentUpload
        exclude = ('upload_datetime',)
        extra_kwargs = {
            'client': {
                'default': CreateOnlyDefault(
                    CurrentUserDefault()
                ),
            }
        }


class LeasingClientInviteTokenModelSerializer(ModelSerializer):

    class Meta:
        model = LeasingClientInviteToken
        fields = '__all__'


class KeyTextSerializer(ModelSerializer):

    class Meta:
        model = KeyText
        fields = '__all__'


class DescriptionSerializer(ModelSerializer):

    class Meta:
        model = Description
        fields = '__all__'


class LegalPositionModelSerializer(WritableNestedModelSerializer):
    text = KeyTextSerializer(many=True)
    clause_name = DescriptionSerializer(many=True)

    class Meta:
        model = LegalPosition
        fields = "__all__"
        extra_kwargs = {
            'client': {
                'default': CreateOnlyDefault(
                    CurrentUserDefault()
                ),
            }
        }

    def create(self, validated_data):
        # print("validated_data is {}", validated_data)
        if validated_data['text'] and validated_data['clause_name']:
            key_text =  KeyTextSerializer(data=validated_data['text'], many=True)
            Description =  DescriptionSerializer(data=validated_data['clause_name'], many=True)
            if key_text.is_valid() and Description.is_valid():
                key_text.save()
                Description.save()
                print("\n\n______key_text_data is_____ ", key_text.data , '\n\n')
                validated_data = dict(validated_data)
                validated_data.pop('text', None)
                validated_data.pop('clause_name', None)
                legal_position =  LegalPosition.objects.create(**validated_data)
                key_text_id_array = [dict(x)['id'] for x in key_text.data]
                description_id_array = [dict(x)['id'] for x in Description.data]
                print("key text id array is", key_text_id_array)
                legal_position.text.add(*key_text_id_array)
                legal_position.clause_name.add(*description_id_array)
                return legal_position
            else:
                raise ValidationError(key_text.errors)
            return LegalPosition.objects.create(**validated_data)


class ReasonSerializer(ModelSerializer):

    class Meta:
        model = LegalPosition
        fields = ('clause_name', 'reason', 'action', 'text')


class TextSearchSerializer(ModelSerializer):
    text = SerializerMethodField()

    def get_text(self, instance):
        return instance.content

    class Meta:
        model = KeyText
        fields = ('text', )


class ExportResultSerializer(ModelSerializer):

    class Meta:
        model = ExportResult
        fields = '__all__'


class ForgotLoginSerializer(ModelSerializer):

    class Meta:
        model = LeasingUser
        fields = '__all__'
