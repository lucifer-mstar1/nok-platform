from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import Transaction
from .services import withdraw_z_to_uzs, handle_first_zcoin_purchase

@login_required
def wallet_view(request):
    wallet = request.user.wallet
    transactions = wallet.transactions.order_by("-created_at")[:50]

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "deposit":
            amount = Decimal(request.POST.get("amount_uzs", "0") or "0")
            if amount <= 0:
                messages.error(request, "Amount must be positive.")
            else:
                wallet.deposit_uzs(amount)
                Transaction.objects.create(
                    user=request.user,
                    wallet=wallet,
                    type="deposit",
                    amount_uzs=amount,
                    description="Manual deposit (simulate HUMO/Uzcard/Visa)",
                )
                messages.success(request, "Balance topped up (simulation).")
            return redirect("wallet:wallet")

        if action == "convert":
            uzs_amount = Decimal(request.POST.get("convert_uzs", "0") or "0")
            try:
                z = wallet.convert_uzs_to_z(uzs_amount)
            except ValueError as e:
                messages.error(request, str(e))
            else:
                Transaction.objects.create(
                    user=request.user,
                    wallet=wallet,
                    type="convert_to_z",
                    amount_uzs=-uzs_amount,
                    amount_z=z,
                    description="Converted to Z coins",
                )
                handle_first_zcoin_purchase(request.user, z)
                messages.success(request, f"Converted to {z} Z.")
            return redirect("wallet:wallet")

        if action == "withdraw":
            z_amount = Decimal(request.POST.get("withdraw_z", "0") or "0")
            try:
                net, fee = withdraw_z_to_uzs(request.user, z_amount)
            except ValueError as e:
                messages.error(request, str(e))
            else:
                messages.success(request, f"Withdrew {net} UZS (fee {fee}). (Simulation)")
            return redirect("wallet:wallet")

    return render(request, "wallet/wallet.html", {"wallet": wallet, "transactions": transactions})
