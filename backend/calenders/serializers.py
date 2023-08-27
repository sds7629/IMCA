from rest_framework import serializers
from .models import Calendar, Memo


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = "__all__"


class DotInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = (
            "pk",
            "selected_date",
        )


class DetailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        exclude = ("owner",)