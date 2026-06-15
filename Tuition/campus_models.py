# Create your models here.
from django.utils.translation import gettext_lazy as _ # type: ignore

from django.db.models import ( # type: ignore
    ForeignKey,
    CharField,
    IntegerField,
    TextChoices,
    BooleanField,
    CASCADE,
    OneToOneField,
    UniqueConstraint, 
    Q
)
from app.models import BaseModel


class CampusType(TextChoices):
    SCHOOL = "school", _("school")
    CENTER = "center", _("center")


class Campus(BaseModel):
    from app.enum import type_list

    code = CharField(max_length=120, null=True, blank=True)
    number = IntegerField(null=True, blank=True)
    name = CharField(max_length=120, null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)
    type = CharField(
        choices=CampusType.choices, max_length=20, default=CampusType.SCHOOL
    )
    priority_order = IntegerField(blank=True, null=True)


class School(BaseModel):
    campus = ForeignKey(
        "Campus", related_name="campus", blank=True, null=True, on_delete=CASCADE
    )
    name = CharField(max_length=120, null=True, blank=True)
    campus_number = IntegerField(null=True, blank=True)
    grade_group = CharField(max_length=120, null=True, blank=True)
    ps_school_id = IntegerField(null=True, blank=True)
    priority_order = IntegerField(blank=True, null=True)


class GradeLevel(BaseModel):
    name = CharField(max_length=255, null=True, blank=True)
    level = IntegerField(null=True, blank=True)


class Class(BaseModel):
    school = ForeignKey(
        "School", related_name="school", blank=True, null=True, on_delete=CASCADE
    )
    grade_level = ForeignKey("GradeLevel", blank=True, null=True, on_delete=CASCADE)
    class_name = CharField(max_length=255, null=True, blank=True)
    class_number = IntegerField(blank=True, null=True)
    home_room = CharField(max_length=255, null=True, blank=True)
    priority_order = IntegerField(blank=True, null=True)
    
    
    
class CampusInfo(BaseModel):
    
    campus = OneToOneField("Campus", related_name="infos", blank=True, null=True, on_delete=CASCADE, unique= True)
    vi_name = CharField(max_length=120, null=True, blank=True)
    en_name = CharField(max_length=120, null=True, blank=True)
    vi_sort_name = CharField(max_length=120, null=True, blank=True)
    en_sort_name = CharField(max_length=120, null=True, blank=True)
    vi_license = CharField(max_length=500, null=True, blank=True)
    en_license = CharField(max_length=500, null=True, blank=True)
    vi_permit = CharField(max_length=500, null=True, blank=True)
    en_permit = CharField(max_length=500, null=True, blank=True)
    representative = CharField(max_length=255, null=True, blank=True)
    vi_job_title = CharField(max_length=255, null=True, blank=True)
    en_job_title = CharField(max_length=255, null=True, blank=True)
    phone = CharField(max_length=20, null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)
    # vi_establishment = CharField(max_length=255, null=True, blank=True)
    # en_establishment = CharField(max_length=255, null=True, blank=True)
    # investor info
    investor_vi_name = CharField(max_length=255, null=True, blank=True)
    investor_en_name = CharField(max_length=255, null=True, blank=True)
    investor_vi_license = CharField(max_length=255, null=True, blank=True)
    investor_en_license = CharField(max_length=255, null=True, blank=True)
    investor_vi_permit = CharField(max_length=255, null=True, blank=True)
    investor_en_permit = CharField(max_length=255, null=True, blank=True)
    investor_address = CharField(max_length=255, null=True, blank=True)
    
    
    
class CampusPaymentInfo(BaseModel):
    
    campus = ForeignKey( "Campus", related_name="payment_infos", blank=True, null=True, on_delete=CASCADE)
    bank_holder = CharField(max_length=255, null=True, blank=True)
    bank_account = CharField(max_length=255, null=True, blank=True)
    bank_name = CharField(max_length=255, null=True, blank=True)
    bank_branch = CharField(max_length=255, null=True, blank=True)
    default = BooleanField(default=False)
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['bank_account','campus'],
                condition=Q(deleted=False),
                name='unique_bank_account_campus'
            )
        ]
    
    
            
    
