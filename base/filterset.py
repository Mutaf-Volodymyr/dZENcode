from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django_filters import rest_framework as filters


class BaseFilter(filters.FilterSet):
    LOOKUP_MAPPING = {
        models.CharField: ["exact", "icontains", "istartswith", "iendswith"],
        models.TextField: ["exact", "icontains"],
        models.IntegerField: ["exact", "gte", "lte"],
        models.FloatField: ["exact", "gte", "lte"],
        models.DecimalField: ["exact", "gte", "lte"],
        models.DateField: ["exact", "gte", "lte"],
        models.DateTimeField: ["exact", "gte", "lte"],
        models.PositiveIntegerField: ["exact", "gte", "lte"],
    }

    FILTER_OVERRIDES = {
        models.ImageField: {
            "filter_class": filters.CharFilter,
        },
    }

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        class_meta = getattr(cls, "Meta", None)

        if not class_meta:
            return

        if not hasattr(class_meta, "filter_overrides"):
            class_meta.filter_overrides = BaseFilter.FILTER_OVERRIDES

    @classmethod
    def get_fields(cls):
        fields = super().get_fields()
        model = cls._meta.model

        for field in fields.keys():
            try:
                model_field = model._meta.get_field(field)
                lookup = cls.LOOKUP_MAPPING.get(type(model_field), fields[field])
                fields[field] = lookup
            except FieldDoesNotExist:
                continue

        return fields
