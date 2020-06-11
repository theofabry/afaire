from rest_framework import serializers

from tasks.models import Task, TaskTag


class TaskTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTag
        fields = ['id', 'name', 'task_set']
        read_only_fields = ['task_set']

    def create(self, validated_data):
        tag = TaskTag.objects.create(user=self.context['request'].user, **validated_data)

        return tag


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'content', 'due_date', 'status', 'tags']
        extra_kwargs = {'tags': {'required': False}}

    def create(self, validated_data):
        task = Task.objects.create(user=self.context['request'].user, **validated_data)

        return task

    def validate_tags(self, value):
        for tag in value:
            if tag.user != self.instance.user:
                raise serializers.ValidationError('This tag is not owned by the user.')

        return value


class TaskDetailSerializer(TaskSerializer):
    tags = TaskTagSerializer(many=True)


class TaskExportSerializer(TaskSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'content': instance.content,
            'due_date': instance.due_date,
            'status': Task.STATUS_CHOICES[instance.status][1],
            'tags': instance.tags,
        }
