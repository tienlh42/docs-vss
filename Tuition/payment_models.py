from django.db.models import (  # type: ignore
    CharField,
    JSONField,
    BooleanField,
    TextField,
    DateField,
    DateTimeField,
    IntegerField,
    BigIntegerField,
    CASCADE,
    ForeignKey,
    DecimalField,
)
from app.models import BaseModel
from django.utils.translation import gettext_lazy as _  # type: ignore
from django.db.models import TextChoices  # type: ignore


class GroupOrderStatus(TextChoices):
    CREATED = "created", _("The order has been created but not confirmed")
    REQUESTED = "requested", _("The order has been requested for processing")
    PROCESSING = "processing", _("Processed and prepared for shipment")
    CONFIRMED = "confirmed", _("Confirmed and is awaiting payment")
    CANCELLED = "cancelled", _("The order has been canceled for some other reason")
    SUCCESS = "success", _("Fully processed and the transaction is complete")


class OrderStatus(TextChoices):
    CREATED = "created", _("The order has been created but not confirmed")
    REQUESTED = "requested", _("The order has been requested for processing")
    PROCESSING = "processing", _("Processed and prepared for shipment")
    CONFIRMED = "confirmed", _("Confirmed and is awaiting payment")
    CANCELLED = "cancelled", _("The order has been canceled for some other reason")
    PENDING_PAYMENT = "pending_payment", _("Payment is pending or being processed")
    FAILED = "failed", _("The order has been the transaction has failed")
    SUCCESS = "success", _("Fully processed and the transaction is complete")


class TransactionStatus(TextChoices):
    CREATED = "created", _("created")
    PROCESSING = "processing", _("processing")
    FAILED = "failed", _("failed")
    CANCELLED = "cancelled", _("cancelled")
    PENDING = "pending", _("pending")
    SUCCESS = "success", _("success")


class PaymentMethod(TextChoices):
    CASH = "cash", _("cash")
    BANK_TRANSFER = "bank_transfer", _("bank_transfer")
    QR_CODE = "qr_code", _("qr_code")
    POS = "pos", _("pos")
    CREDIT_ONLINE = "credit_online", _("credit_online")
    PAYMENT_GATE = "payment_gateway", _("payment_gateway")
    GUARANTEE = "guarantee", _("guarantee")


class OrderType(TextChoices):
    FEE = "fee", _("fee")
    SHOP = "shop", _("shop")


class ProductType(TextChoices):
    FEE = "fee", _("fee")
    SHOP = "shop", _("shop")


class SpecialPay(TextChoices):
    NORMAL = "normal", _("normal")
    QR_CODE = "qr_code", _("qr_code")
    GUARANTEE = "guarantee", _("guarantee")
    

class brand_code(TextChoices):
    GALAXY = "galaxy", _("galaxy")
    HDBANK = "hdbank", _("hdbank")


# PAYMENT MODEL
class GroupOrder(BaseModel):
    lead_id = CharField(max_length=100)
    person_guardian_id = IntegerField()
    group_order_info = JSONField(null=True, blank=True)
    callback_info = JSONField(null=True, blank=True)
    bank_status_code = CharField(max_length=100, null=True, blank=True)
    request_time = CharField(max_length=100, null=True, blank=True)


class Order(BaseModel):
    title = CharField(max_length=255, null=True, blank=True)
    order_type = CharField(
        max_length=20, choices=OrderType.choices, default=OrderType.FEE
    )

    lead_id = CharField(max_length=100, null=True, blank=True)
    order_type = CharField(
        max_length=20, choices=OrderType.choices, default=OrderType.FEE
    )

    person_id = IntegerField(null=True, blank=True)
    student_id = IntegerField(null=True, blank=True)
    campus_id = IntegerField(null=True, blank=True)

    reason_of_promotion = TextField(null=True, blank=True)

    discount_amount = DecimalField(
        max_digits=14, decimal_places=2, default=0, null=True, blank=True
    )
    total_amount = DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    special_pay = CharField(
        max_length=20, choices=SpecialPay.choices, default=SpecialPay.NORMAL
    )
    multiple_year_contract = BooleanField(default=False, null=True, blank=True)

    note = TextField(null=True, blank=True)
    order_status = CharField(
        max_length=30, choices=OrderStatus.choices, default=OrderStatus.CREATED
    )
    due_date = DateField(null=True, blank=True)

    # Long term contract
    is_split = BooleanField(default=False)


class OrderPaymentCode(BaseModel):
    order = ForeignKey("Order", on_delete=CASCADE, related_name="order_payment_code")
    payment_code = CharField(max_length=255, null=True, blank=True)
    brand_code = CharField(max_length=20, null=True, blank=True, choices=brand_code.choices)

class OrderItem(BaseModel):
    order = ForeignKey("Order", on_delete=CASCADE, related_name="order_item")

    product_id = IntegerField(null=True, blank=True)
    product_type = CharField(
        max_length=20, choices=ProductType.choices, default=ProductType.FEE
    )
    external_product_info = JSONField(null=True, blank=True)

    price = DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    quantity = IntegerField(default=1, blank=True)
    discount_amount = DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    total_amount = DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)


class QRCode(BaseModel):
    order = ForeignKey("Order", on_delete=CASCADE, related_name="order_qr_code")
    bill_id = CharField(max_length=100, null=True, blank=True)
    qr_code = CharField(max_length=100, null=True, blank=True)
    expired = DateTimeField(null=True, blank=True)


class Transaction(BaseModel):
    order = ForeignKey("Order", on_delete=CASCADE, related_name="order_transaction")
    transaction_id = CharField(max_length=200, null=True, blank=True)
    order_info = JSONField(null=True, blank=True)
    payment_info = JSONField(null=True, blank=True)

    total_amount = IntegerField(null=True, blank=True)

    payment_date = DateField(null=True, blank=True)
    payment_method = CharField(
        max_length=30, choices=PaymentMethod.choices, null=True, blank=True
    )
    payment_partner = CharField(max_length=30, null=True, blank=True)
    payment_collect_by = CharField(null=True, blank=True)

    transaction_status = CharField(
        max_length=30,
        choices=TransactionStatus.choices,
        default=TransactionStatus.CREATED,
    )

    # Long term contract
    percentage = IntegerField(null=True, blank=True)
    due_order = DateField(null=True, blank=True)
    amount = DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    @property
    def payment_method_name(self):
        return self.payment_method.replace("_", " ").title()

    @property
    def payment_partner_name(self):
        return (
            self.payment_partner.replace("_", " ").title()
            if self.payment_partner
            else ""
        )


class Receipt(BaseModel):
    order = ForeignKey("Order", on_delete=CASCADE, related_name="order_receipt")
    transaction_id = CharField(max_length=200, null=True, blank=True)
    file_path = CharField(max_length=255, null=True, blank=True)
    file_url = CharField(max_length=255, null=True, blank=True)


class Quote(BaseModel):
    guardian_id = IntegerField(null=True, blank=True)
    student_id = IntegerField()
    quote_domain = CharField(max_length=500, null=True, blank=True)
    quote_expiration_date = DateField(null=True, blank=True)
    quote_title = CharField(max_length=500, null=True, blank=True)
    quote_link = CharField(max_length=500)
    quote_number = CharField(max_length=500, null=True, blank=True)
    quote_amount = IntegerField(null=True, blank=True)
    quote_hs_id = CharField(max_length=500)
    is_created = BooleanField(default=False)
    quote_sign_status = CharField(max_length=500, null=True, blank=True)
    quote_status = CharField(max_length=500)


class ActivityLog(BaseModel):
    order_id = BigIntegerField()
    action = CharField(max_length=255)
    note = TextField()
    old_data = TextField(null=True, blank=True)


# PAYMENT CONFIGURATION
class CampusAccount(BaseModel):
    campus_code = CharField(max_length=255)
    campus_name = CharField(max_length=255)
    galaxy_partner_code = CharField(max_length=255, null=True, blank=True)
    hd_bank_partner_code = CharField(max_length=255, null=True, blank=True)
    is_default = BooleanField(default=False)

    account_name = CharField(max_length=255, null=True, blank=True)
    account_number = CharField(max_length=255, null=True, blank=True)
    bank_name = CharField(max_length=255, null=True, blank=True)
    bank_branch = CharField(max_length=255, null=True, blank=True)
