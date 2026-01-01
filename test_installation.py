"""
Installation Test Script

Run this to verify your Meme Content Studio installation is working correctly.
"""

import sys
from pathlib import Path


def test_python_version():
    """Test Python version"""
    print("Testing Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (need 3.9+)")
        return False


def test_imports():
    """Test required imports"""
    print("\nTesting required packages:")

    packages = {
        "anthropic": "Anthropic Claude API",
        "PIL": "Pillow (image processing)",
        "dotenv": "python-dotenv",
        "typer": "Typer (CLI)",
        "rich": "Rich (terminal UI)"
    }

    all_good = True
    for package, name in packages.items():
        try:
            if package == "PIL":
                from PIL import Image
            elif package == "dotenv":
                import dotenv
            else:
                __import__(package)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            all_good = False

    return all_good


def test_directories():
    """Test directory structure"""
    print("\nTesting directory structure:")

    required_dirs = [
        "app",
        "prompts",
        "tones",
        "angles",
        "meme_library",
        "assets",
        "output"
    ]

    all_good = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - MISSING")
            all_good = False

    return all_good


def test_prompt_files():
    """Test prompt files"""
    print("\nTesting prompt files:")

    required_prompts = [
        "prompts/content_creator.txt",
        "prompts/humanizer.txt",
        "prompts/meme_analyzer.txt",
        "prompts/caption_writer.txt"
    ]

    all_good = True
    for prompt_file in required_prompts:
        prompt_path = Path(prompt_file)
        if prompt_path.exists():
            print(f"  ✓ {prompt_file}")
        else:
            print(f"  ✗ {prompt_file} - MISSING")
            all_good = False

    return all_good


def test_env_file():
    """Test .env file"""
    print("\nTesting environment configuration:")

    env_path = Path(".env")
    if not env_path.exists():
        print("  ✗ .env file not found")
        print("    → Copy .env.example to .env and add your API key")
        return False

    print("  ✓ .env file exists")

    # Try to load it
    try:
        from dotenv import load_dotenv
        import os

        load_dotenv()

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key and api_key != "your_api_key_here":
            print(f"  ✓ ANTHROPIC_API_KEY is set")
            return True
        else:
            print("  ✗ ANTHROPIC_API_KEY not set or still placeholder")
            print("    → Edit .env and add your real API key")
            return False

    except Exception as e:
        print(f"  ✗ Error loading .env: {e}")
        return False


def test_modules():
    """Test app modules can be imported"""
    print("\nTesting app modules:")

    modules = [
        "app.config",
        "app.rewriter",
        "app.humanizer",
        "app.meme_matcher",
        "app.caption_generator",
        "app.slide_generator"
    ]

    all_good = True
    for module in modules:
        try:
            __import__(module)
            module_name = module.split('.')[1]
            print(f"  ✓ {module_name}")
        except Exception as e:
            module_name = module.split('.')[1]
            print(f"  ✗ {module_name} - {str(e)}")
            all_good = False

    return all_good


def test_cli():
    """Test CLI is accessible"""
    print("\nTesting CLI:")

    try:
        from app.main import app
        print("  ✓ CLI module loaded")
        return True
    except Exception as e:
        print(f"  ✗ CLI module failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Meme Content Studio - Installation Test")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Python Version", test_python_version()))
    results.append(("Required Packages", test_imports()))
    results.append(("Directory Structure", test_directories()))
    results.append(("Prompt Files", test_prompt_files()))
    results.append(("Environment Config", test_env_file()))
    results.append(("App Modules", test_modules()))
    results.append(("CLI", test_cli()))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status:8} {test_name}")

    print("=" * 60)

    if passed == total:
        print(f"\n🎉 All tests passed! ({passed}/{total})")
        print("\nYou're ready to create content!")
        print("\nNext steps:")
        print("  1. Read QUICK_START.md for usage examples")
        print("  2. Try: python -m app.main list-tones")
        print("  3. Create your first carousel!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed ({passed}/{total} passed)")
        print("\nPlease fix the issues above before continuing.")
        print("\nCommon fixes:")
        print("  • Missing packages: pip install -r requirements.txt")
        print("  • Missing .env: cp .env.example .env (then edit)")
        print("  • Missing directories: Check PROJECT_OVERVIEW.md")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
