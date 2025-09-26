from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from django.core.management import call_command
import sys

User = get_user_model()

class Command(BaseCommand):
    help = 'Check database status and fix common issues'
    
    def handle(self, *args, **options):
        self.stdout.write("🔍 CHECKING DATABASE STATUS")
        self.stdout.write("=" * 50)
        
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                self.stdout.write(
                    self.style.SUCCESS("✅ Database connection: OK")
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Database connection failed: {e}")
            )
            return
        
        # Check migrations
        try:
            call_command('showmigrations', '--list', verbosity=0)
            self.stdout.write(
                self.style.SUCCESS("✅ Migrations: Accessible")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Migrations check failed: {e}")
            )
        
        # Check if there are unapplied migrations
        try:
            from django.db.migrations.executor import MigrationExecutor
            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            
            if plan:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Unapplied migrations found: {len(plan)}")
                )
                for migration, backwards in plan:
                    self.stdout.write(f"  - {migration}")
                
                # Apply migrations
                self.stdout.write("🔧 Applying migrations...")
                call_command('migrate', verbosity=1)
            else:
                self.stdout.write(
                    self.style.SUCCESS("✅ All migrations applied")
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Migration check failed: {e}")
            )
        
        # Check User model
        try:
            user_count = User.objects.count()
            self.stdout.write(
                self.style.SUCCESS(f"✅ User model accessible. Users in DB: {user_count}")
            )
            
            if user_count == 0:
                self.stdout.write(
                    self.style.WARNING("⚠️  No users found. You may need to create an admin user.")
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ User model check failed: {e}")
            )
        
        # Check table existence
        try:
            table_names = connection.introspection.table_names()
            important_tables = [
                'administration_user',
                'auth_permission',
                'django_content_type',
                'django_migrations'
            ]
            
            missing_tables = [table for table in important_tables if table not in table_names]
            
            if missing_tables:
                self.stdout.write(
                    self.style.ERROR(f"❌ Missing tables: {missing_tables}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS("✅ All important tables exist")
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Table check failed: {e}")
            )
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("🏁 DATABASE CHECK COMPLETE")