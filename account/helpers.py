from .models import Role
from .constant import ROLE

def load_role():
    for role in ROLE:
        Role.objects.get_or_create(
            role=role,
            defaults={
                "role":role
            }
        )