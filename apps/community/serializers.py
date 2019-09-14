from .models import Articles, Message, MessageRecipient, InteractedArticle
from rest_framework.serializers import ModelSerializer


class ArticlesSerializer(ModelSerializer):
    class Meta:
        model = Articles
        field = '__all__'


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        field = '__all__'


class MessageRecipientSerializer(ModelSerializer):
    class Meta:
        model = MessageRecipient
        field = '__all__'


class InteractedArticleSerializer(ModelSerializer):
    class Meta:
        model = InteractedArticle
        field = '__all__'