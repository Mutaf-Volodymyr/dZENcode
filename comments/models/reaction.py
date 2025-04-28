from django.contrib.auth import get_user_model
from django.db import models

from base.model import BaseModel

User = get_user_model()


class Reaction(BaseModel):
    class ReactionTypes(models.IntegerChoices):
        LIKE = 1, 'like'
        DISLIKE = -1, 'dislike'
        NEUTRAL = 0, 'neutral'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE)
    reaction = models.IntegerField(choices=ReactionTypes.choices)


    def __str__(self):
        return f'{self.user.username} - {self.comment.id} - {self.reaction}'

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('user', 'comment')
