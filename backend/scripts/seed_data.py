# ==========================================
# 2. backend/scripts/seed_data.py
# ==========================================
#!/usr/bin/env python3
"""
MediaLab Platform - Data Seeding Script
Universidad Galileo MediaLab Platform

Seeds initial data for available modules.
Currently supports:
- Security (permissions and roles)
"""

import sys
import os
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal

# Import available seeders
from app.modules.security.seeds import SecuritySeeder


class MasterSeeder:
    """Master seeder that coordinates all available module seeders"""
    
    def __init__(self, db: Session):
        self.db = db
        self.available_seeders = {
            'security': SecuritySeeder(db),
        }
    
    def seed_all(self, reset: bool = False, verbose: bool = True):
        """Seed all available modules"""
        if verbose:
            print("🌱 Starting MediaLab Platform Data Seeding")
            print("=" * 50)
        
        # Only seed available modules
        available_modules = ['security']
        
        try:
            for module_name in available_modules:
                if verbose:
                    print(f"\n📦 Seeding {module_name.upper()} module...")
                
                seeder = self.available_seeders[module_name]
                
                if reset:
                    seeder.reset_data()
                
                seeder.seed_all()
                
                if verbose:
                    stats = seeder.get_stats()
                    print(f"✅ {module_name.upper()} completed: {stats}")
            
            self.db.commit()
            
            if verbose:
                print("\n" + "=" * 50)
                print("🎉 All available modules seeded successfully!")
                self._print_summary()
                
        except Exception as e:
            self.db.rollback()
            print(f"❌ Error during seeding: {e}")
            raise
    
    def seed_module(self, module_name: str, reset: bool = False, verbose: bool = True):
        """Seed specific module"""
        if module_name not in self.available_seeders:
            available = ', '.join(self.available_seeders.keys())
            raise ValueError(f"Module '{module_name}' not available. Available modules: {available}")
        
        if verbose:
            print(f"🌱 Seeding {module_name.upper()} module...")
        
        try:
            seeder = self.available_seeders[module_name]
            
            if reset:
                seeder.reset_data()
            
            seeder.seed_all()
            self.db.commit()
            
            if verbose:
                stats = seeder.get_stats()
                print(f"✅ {module_name.upper()} completed: {stats}")
                
        except Exception as e:
            self.db.rollback()
            print(f"❌ Error seeding {module_name}: {e}")
            raise
    
    def reset_all(self):
        """Reset all available data (DANGEROUS - use only in development)"""
        print("🔄 Resetting ALL available data...")
        
        # Reset in reverse order (only security for now)
        reset_order = ['security']
        
        for module_name in reset_order:
            print(f"🗑️  Resetting {module_name}...")
            self.available_seeders[module_name].reset_data()
        
        self.db.commit()
        print("✅ All data reset completed")
    
    def list_modules(self):
        """List available modules"""
        print("📋 Available modules for seeding:")
        for module_name in self.available_seeders.keys():
            print(f"  - {module_name}")
    
    def _print_summary(self):
        """Print seeding summary"""
        print("\n📊 SEEDING SUMMARY:")
        for module_name, seeder in self.available_seeders.items():
            stats = seeder.get_stats()
            print(f"  {module_name.capitalize()}: {stats}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="MediaLab Platform Data Seeding Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/seed_data.py                    # Seed all available modules
  python scripts/seed_data.py --reset            # Reset and seed all
  python scripts/seed_data.py --module security  # Seed only security
  python scripts/seed_data.py --list             # List available modules
  python scripts/seed_data.py --reset-all        # Reset all data only
        """
    )
    
    parser.add_argument(
        '--module', '-m',
        help='Seed specific module only'
    )
    
    parser.add_argument(
        '--reset', '-r',
        action='store_true',
        help='Reset module data before seeding'
    )
    
    parser.add_argument(
        '--reset-all',
        action='store_true',
        help='Reset all data without seeding (DANGEROUS)'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available modules'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Minimal output'
    )
    
    parser.add_argument(
        '--environment', '-e',
        choices=['development', 'staging', 'production'],
        default='development',
        help='Target environment (affects safety checks)'
    )
    
    args = parser.parse_args()
    
    # Safety check for production
    if args.environment == 'production' and (args.reset or args.reset_all):
        print("❌ Cannot reset data in production environment!")
        sys.exit(1)
    
    # Connect to database
    db = SessionLocal()
    
    try:
        seeder = MasterSeeder(db)
        verbose = not args.quiet
        
        if args.list:
            seeder.list_modules()
        elif args.reset_all:
            seeder.reset_all()
        elif args.module:
            seeder.seed_module(args.module, reset=args.reset, verbose=verbose)
        else:
            seeder.seed_all(reset=args.reset, verbose=verbose)
            
    except KeyboardInterrupt:
        print("\n⚠️ Seeding interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
