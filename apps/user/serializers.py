from .models import User, UserProfile, AgentGroup, Agent, LoginRecord, VerifyCode
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        field = '__all__'


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        field = '__all__'


class AgentGroupSerializer(ModelSerializer):
    class Meta:
        model = AgentGroup
        field = '__all__'


class AgentSerializer(ModelSerializer):
    class Meta:
        model = Agent
        field = '__all__'


class LoginRecordSerializer(ModelSerializer):
    class Meta:
        model = LoginRecord
        field = '__all__'


class VerifyCodeSerializer(ModelSerializer):
    class Meta:
        model = VerifyCode
        field = '__all__'
