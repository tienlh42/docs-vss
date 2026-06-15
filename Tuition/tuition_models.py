from django.db.models import (  # type: ignore
    CharField,
    BooleanField,
    ForeignKey,
    IntegerField,
    FloatField,
    DateField,
    SlugField,
    BigIntegerField,
    DecimalField,
    CASCADE,
    TextChoices,
    UniqueConstraint,
    Q,
    Sum,
)
from django.db.models.fields.json import JSONField  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore
from rest_framework.exceptions import ValidationError  # type: ignore
from app.models import BaseModel


class Fee(BaseModel):
    en_name = CharField(max_length=255, unique=True)
    vi_name = CharField(max_length=255, unique=True)
    en_unit = CharField(max_length=255)
    vi_unit = CharField(max_length=255)
    feetype = ForeignKey("FeeType", blank=True, null=True, on_delete=CASCADE)

    is_compulsory = BooleanField(default=False)
    is_term = BooleanField(default=False)
    is_quantity = BooleanField(default=False)


class FeeDate(BaseModel):
    fee = ForeignKey(
        "Fee", blank=True, null=True, on_delete=CASCADE, related_name="fee_dates"
    )
    due_date = DateField(blank=True, null=True)
    maturity_date = DateField(blank=True, null=True)
    enrollment_year = IntegerField(blank=True, null=True)


class FeeGroup(BaseModel):
    fee = ForeignKey("Fee", blank=True, null=True, on_delete=CASCADE)
    price = FloatField(blank=True, default=0)
    is_edit = BooleanField(default=False)

    grade_level = IntegerField(blank=True, null=True)

    campus_id = IntegerField(blank=True, null=True)
    school_id = IntegerField(blank=True, null=True)
    program = CharField(max_length=20, blank=True, null=True)
    year = IntegerField(blank=True, null=True)

    hub_product_id = BigIntegerField(blank=True, null=True)


class Term(BaseModel):
    campus_id = IntegerField(null=True, blank=True)

    en_name = CharField(max_length=255, null=True)
    vi_name = CharField(max_length=255, null=True)
    percent = IntegerField(blank=True, default=0)

    base_due_date = DateField(blank=True, null=True)
    base_maturity_date = DateField(blank=True, null=True)

    base_from_date = DateField(blank=True, null=True)
    base_to_date = DateField(blank=True, null=True)

    unit = CharField(
        choices=[("term", "term"), ("semester", "semester"), ("year", "year")],
        max_length=10,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):

        if self.campus_id is not None:
            total_percent = (
                Term.objects.filter(
                    campus_id=self.campus_id, unit=self.unit, deleted=False
                )
                .exclude(id=self.id)
                .aggregate(total=Sum("percent"))["total"]
                or 0
            )

            total_percent += self.percent

            if total_percent > 100:
                raise ValidationError(
                    _(
                        "Total percent of this campus_id and unit must be less than or equal to 100."
                    )
                )

        super().save(*args, **kwargs)


class Discount(BaseModel):
    slug = SlugField(max_length=255, blank=True, null=True)
    en_name = CharField(max_length=255, blank=True, null=True)
    vi_name = CharField(max_length=255, blank=True, null=True)
    percent = IntegerField(blank=True, default=0)
    amount = IntegerField(blank=True, default=0)
    note = CharField(max_length=255, blank=True, null=True)


class StudentFeeGroup(BaseModel):
    student_id = BigIntegerField(blank=True, null=True)

    term = ForeignKey("Term", blank=True, null=True, on_delete=CASCADE)
    fee_group = ForeignKey("FeeGroup", blank=True, null=True, on_delete=CASCADE)
    grade_level = IntegerField(blank=True, null=True)

    price = DecimalField(max_digits=20, decimal_places=0, blank=True, null=True)
    quantity = IntegerField(default=1, blank=True)

    note = CharField(max_length=255, blank=True, null=True)
    year = IntegerField(
        blank=True, null=True
    )  # year is the year in which the student pays the tuition to attend school.
    reference_year = IntegerField(
        blank=True, null=True
    )  # reference_year is the fee reference year.
    due_date = DateField(
        blank=True, null=True
    )  # due_date is the date by which the school is required to receive the fee.
    maturity_date = DateField(
        blank=True, null=True
    )  # maturity_date is the date that the guardian has to pay the fee

    discount = ForeignKey("Discount", blank=True, null=True, on_delete=CASCADE)

    discount_amount = DecimalField(
        max_digits=20, decimal_places=0, null=True, blank=True
    )
    total_amount = DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)

    is_active = BooleanField(default=True)


class FeeType(BaseModel):
    vi_name = CharField(max_length=500, null=True, blank=True)
    en_name = CharField(max_length=500, null=True, blank=True)
    type = CharField(max_length=500, null=True, blank=True)
    order = IntegerField(null=True, blank=True)


## Service Subscription: bus, breakfast
class RouteType(TextChoices):
    MORNING_ONLY = "morning_only", _("1 chiều/1 way (morning only)")
    AFTERNOON_ONLY = "afternoon_only", _("1 chiều/1 way (afternoon only)")
    TWO_WAYS = "two_ways", _("to and from school")


class ServiceType(TextChoices):
    BREAKFAST = "breakfast", _("breakfast")
    BUS = "bus", _("bus")


class ServiceStatus(TextChoices):
    ACTIVE = "active", _("active")
    CANCEL = "cancel", _("cancel")
    EXPIRED = "expired", _("expired")
    PENDING = "pending", _("pending")
    INACTIVE = "inactive", _("inactive")


class ServiceSubscription(BaseModel):

    student_id = IntegerField()
    student_uuid = CharField(max_length=255, null=True, blank=True)

    service_usage_year = IntegerField(null=True, blank=True)
    from_date = DateField(blank=True, null=True)
    to_date = DateField(blank=True, null=True)
    term = ForeignKey("Term", blank=True, null=True, on_delete=CASCADE)

    status = CharField(
        max_length=25,
        choices=ServiceStatus.choices,
        default="active",
    )

    service_type = CharField(
        max_length=25, choices=ServiceType.choices, null=True, blank=True
    )
    service_info = JSONField(null=True, blank=True)
    service_fee = IntegerField(
        blank=True, null=True
    )  # service_fee is the fee for the service subscription

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["student_id", "from_date", "to_date", "service_type"],
                condition=Q(deleted=False),
                name="unique_student_service_subscription",
            )
        ]
