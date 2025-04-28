from django_filters import OrderingFilter
from django_filters import rest_framework as filters
from base.filterset import BaseFilter
from comments.models import Comment


class AssessmentFilter(BaseFilter):
    ordering = OrderingFilter(
        fields=(
            ("id", "id"),
            ("user__username", "user__username"),
            ("user__email", "user__email"),
            ("rating", "rating"),
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        )
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "rating",
            "created_at",
            "updated_at",
        ]

    search = filters.CharFilter(
        field_name="text", lookup_expr="icontains", required=False
    )