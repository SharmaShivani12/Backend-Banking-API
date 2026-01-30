from fastapi import HTTPException, status


# Generic RBAC role checker
def require_role(user, *allowed_roles):
    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: insufficient permissions"
        )


# Specific helper for customers accessing only their own accounts
def require_owner_or_staff(user, account_customer_id):
    # staff bypass
    if user.role in ("admin", "employee"):
        return

    # customer accessing own account
    if user.role == "customer" and user.id == account_customer_id:
        return

    raise HTTPException(status.HTTP_403_FORBIDDEN, "Access denied")
