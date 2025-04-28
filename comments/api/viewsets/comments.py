from django.db import transaction
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from comments.api.filters import AssessmentFilter
from comments.api.permissions import OwnerOrReadOnly
from comments.models import Comment, Reaction
from comments.api.serializers import (
    CommentListSerializer,
    CommentDetailUpdateSerializer,
    CommentCreateDeleteSerializer,
)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [OwnerOrReadOnly]
    filterset_class = AssessmentFilter


    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer
        if self.action == 'create':
            return CommentCreateDeleteSerializer
        return CommentDetailUpdateSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Comment.objects.filter(parent=None)
        return Comment.objects.all()

    def _update_rating(self, comment):
        reactions = Reaction.objects.filter(comment=comment)
        total = reactions.aggregate(total=Sum('reaction'))['total'] or 0
        comment.rating = total
        comment.save(update_fields=['rating'])

    def _set_reaction(self, user, reaction_type):
        comment = self.get_object()
        with transaction.atomic():
            reaction, created = Reaction.objects.get_or_create(
                user=user,
                comment=comment,
                defaults={'reaction': reaction_type}
            )
            if not created:
                reaction.reaction = reaction_type
                reaction.save(update_fields=['reaction'])

            self._update_rating(comment)

        return Response({'status': 'reaction set'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        return self._set_reaction(request.user, Reaction.ReactionTypes.LIKE)

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        return self._set_reaction(request.user, Reaction.ReactionTypes.DISLIKE)

    @action(detail=True, methods=['post'])
    def neutral(self, request, pk=None):
        return self._set_reaction(request.user, Reaction.ReactionTypes.NEUTRAL)
