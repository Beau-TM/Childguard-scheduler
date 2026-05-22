import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from childguard.models import User, Teacher


def create_demo_data():
    print("Creating demo users and teachers...")

    # Admin
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            password='admin123',
            first_name='Systeembeheerder',
            role='admin',
            first_login=False,
        )
        print("  ✓ admin created")

    # Director
    if not User.objects.filter(username='directie').exists():
        u = User.objects.create_user(
            username='directie',
            password='directie123',
            first_name='Directie',
            role='director',
            first_login=False,
        )
        print("  ✓ directie created")

    # Teachers
    demo_teachers = [
        ('teacher1', 'Anna Janssens', 100),
        ('teacher2', 'Pieter De Vries', 80),
        ('teacher3', 'Sophie Peeters', 50),
    ]

    for username, name, work_pct in demo_teachers:
        if not User.objects.filter(username=username).exists():
            u = User.objects.create_user(
                username=username,
                password='teacher123',
                first_name=name,
                role='teacher',
                first_login=True,
            )
            t = Teacher.objects.create(
                user=u,
                name=name,
                work_percentage=work_pct,
                is_available=True,
            )
            print(f"  ✓ {username} / teacher '{name}' created")

    print("\nDemo data ready!")
    print("\nLogin credentials:")
    print("  admin      / admin123     (Systeembeheerder)")
    print("  directie   / directie123  (Directie)")
    print("  teacher1   / teacher123   (Anna Janssens)")
    print("  teacher2   / teacher123   (Pieter De Vries)")
    print("  teacher3   / teacher123   (Sophie Peeters)")


if __name__ == '__main__':
    create_demo_data()
