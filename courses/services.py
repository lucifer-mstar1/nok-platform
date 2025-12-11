from decimal import Decimal
from wallet.models import Transaction
from .models import Enrollment
from django.db import transaction as db_transaction

PLATFORM_COMMISSION = Decimal("0.10")  # 10%
ENROLL_XP_REWARD = 50  # xp for buying a part

def purchase_course_part(student, part):
    if student.role != "student":
        raise ValueError("Only students can purchase course parts")

    student_wallet = student.wallet
    teacher = part.course.teacher
    teacher_wallet = teacher.wallet

    price_z = part.price_z
    if student_wallet.balance_z < price_z:
        raise ValueError("Not enough Z coins")

    commission_z = (price_z * PLATFORM_COMMISSION).quantize(Decimal("0.01"))
    teacher_z = price_z - commission_z

    with db_transaction.atomic():
        student_wallet.spend_z(price_z)
        Transaction.objects.create(
            user=student,
            wallet=student_wallet,
            type="course_purchase",
            amount_z=-price_z,
            description=f"Purchase {part}",
        )

        teacher_wallet.credit_z(teacher_z)
        Transaction.objects.create(
            user=teacher,
            wallet=teacher_wallet,
            type="course_purchase",
            amount_z=teacher_z,
            description=f"Earned from {student.username} for {part}",
        )

        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            part=part,
            defaults={"is_trial": False, "progress_percent": 0},
        )

        # reward XP for commitment
        from accounts.models import User  # local import
        student.xp += ENROLL_XP_REWARD
        student.save()

    return enrollment
