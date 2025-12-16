#!/usr/bin/env python3
"""
MASTER REFACTORING SCRIPT
Execute all refactoring steps in sequence
"""

import os
import sys

def run_step(step_num, script_name, description):
    """Run a refactoring step"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {description}")
    print(f"{'='*60}")
    
    try:
        exec(open(script_name).read())
        print(f"✓ Step {step_num} completed successfully!")
        return True
    except Exception as e:
        print(f"✗ Error in step {step_num}: {e}")
        return False

def main():
    """Execute all refactoring steps"""
    print("="*60)
    print("ALBUMMAN PROJECT - COMPLETE REFACTORING")
    print("="*60)
    
    steps = [
        (1, 'refactor_step1.py', 'Create directory structure'),
        (2, 'refactor_step2_models.py', 'Extract models'),
        (3, 'refactor_step3_services.py', 'Extract services'),
        (4, 'refactor_step4_utils.py', 'Create utilities'),
        (5, 'refactor_step5_config.py', 'Create configuration'),
        (6, 'refactor_step6a_routes.py', 'Create routes (part 1)'),
        (7, 'refactor_step6b_upload.py', 'Create upload routes'),
    ]
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    success_count = 0
    for step_num, script, desc in steps:
        if run_step(step_num, script, desc):
            success_count += 1
        else:
            print(f"\n⚠ Stopping at step {step_num}")
            break
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {success_count}/{len(steps)} steps completed")
    print(f"{'='*60}")
    
    if success_count == len(steps):
        print("\n✓ Phase 1 of refactoring complete!")
        print("\nNext: Create remaining route files and templates manually,")
        print("or run individual step scripts.")
    
    return success_count == len(steps)

if __name__ == '__main__':
    sys.exit(0 if main() else 1)
