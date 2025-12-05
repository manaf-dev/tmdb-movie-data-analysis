import importlib
import sys

# List of test modules
test_modules = [
    "src.tests.test_data_quality",
    "src.tests.test_analysis",
    "src.tests.test_extractors",
]


def run_tests():
    failed = []
    passed = []

    for module_name in test_modules:
        try:
            module = importlib.import_module(module_name)

            # Run all test_* functions
            for func_name in dir(module):
                if func_name.startswith("test_"):
                    test_func = getattr(module, func_name)
                    try:
                        test_func()
                        print(f"{module_name}::{func_name}")
                        passed.append(f"{module_name}::{func_name}")
                    except AssertionError as e:
                        print(f"{module_name}::{func_name} - {e}")
                        failed.append(f"{module_name}::{func_name}")
                    except Exception as e:
                        print(f"{module_name}::{func_name} - ERROR: {e}")
                        failed.append(f"{module_name}::{func_name}")
        except Exception as e:
            print(f"Failed to load {module_name}: {e}")
            failed.append(module_name)

    print(f"\n{'Test Results':=^40}")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("\nFailed tests:")
        for test in failed:
            print(f"  - {test}")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
