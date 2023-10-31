from rest_framework import serializers

from django.contrib.auth.models import Group
from front_sidebar.models import LayoutSidebar


class SidebarSerializer(serializers.ModelSerializer):
    #parent_path = serializers.IntegerField(required=False)
    parent_path = serializers.PrimaryKeyRelatedField(
        queryset=LayoutSidebar.objects.all(), required=False)
    auth_group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False)

    class Meta:
        model = LayoutSidebar
        fields = '__all__'

    def create(self, validated_data):
        value = LayoutSidebar.objects.create(**validated_data)
        return value



