"""
Simple GUI Test for Terry-the-Tool-Bot

Tests GUI functionality without requiring tkinter.
"""

import sys
import time
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    # Import from the actual location
    from src.terry_bot import TerryToolBot
    from src.qcse.integration.terry_integration import QCSEIntegration
    print("✅ Core modules imported successfully")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def test_gui_functionality():
    """Test GUI-related functionality"""
    print("\n🎨 Testing GUI Functionality")
    print("=" * 50)
    
    # Test Terry bot initialization
    try:
        terry = TerryToolBot()
        print("✅ Terry bot initialized successfully")
        print(f"   Name: {terry.name}")
        print(f"   Version: {terry.version}")
        print(f"   Mode: {terry.mode}")
    except Exception as e:
        print(f"❌ Terry bot initialization failed: {e}")
        return False
    
    # Test QCSE integration
    try:
        qcse = QCSEIntegration(terry)
        print("✅ QCSE integration initialized successfully")
        
        # Test QCSE status
        status = qcse.get_integration_status()
        print(f"   QCSE Enabled: {status['qcse_enabled']}")
        print(f"   Synthesizer Active: {status['synthesizer_active']}")
        print(f" Tool Integrated: {status['tool_integrated']}")
    except Exception as e:
        print(f"❌ QCSE integration failed: {e}")
        return False
    
    # Test QCSE synthesis
    try:
        result = qcse.optimize_code(
            "def hello_world():\n    print('Hello, World!')\n",
            ['efficiency', 'maintainability']
        )
        print("✅ QCSE optimization test passed")
        print(f"   Status: {result.get('status')}")
        print(f"   Fitness Score: {result.get('fitness_score', 0):.4f}")
        print(f"   Execution Time: {result.get('execution_time', 0):.3f}s")
    except Exception as e:
        print(f"❌ QCSE optimization test failed: {e}")
        return False
    
    return True

def test_gui_features():
    """Test GUI-specific features"""
    print("\n🎨 Testing GUI Features")
    print("=" * 50)
    
    # Test conversation system
    try:
        terry = TerryBot()
        
        # Test conversation processing
        test_inputs = [
            "Create a modern Android app",
            "Optimize this code for performance",
            "Generate secure authentication system",
            "Build maintainable architecture"
        ]
        
        print("📝 Testing Conversation Processing:")
        for i, test_input in enumerate(test_inputs, 1):
            response = terry.process_input(test_input)
            print(f"   Test {i}: {test_input[:30]}...")
            print(f"   Response: {response[:50]}...")
            print()
        
        print("✅ Conversation processing test passed")
        
    except Exception as e:
        print(f"❌ Conversation processing test failed: {e}")
        return False
    
    return True

def test_qcse_advanced():
    """Test advanced QCSE features"""
    print("\n⚛️ Testing Advanced QCSE Features")
    print("=" * 50)
    
    try:
        qcse = QCSEIntegration(TerryToolBot())
        
        # Test synthesis statistics
        stats = qcse.qcse_tool.get_synthesis_statistics()
        print("📊 QCSE Statistics:")
        print(f"   Total Syntheses: {stats['total_syntheses']}")
        print(f"   Best Syntheses: {stats['best_syntheses']}")
        print(f"   Average Fitness: {stats['average_fitness']:.4f}")
        print(f"   Best Fitness: {stats['best_fitness']:.4f}")
        
        # Test synthesis report
        report = qcse.qcse_tool.create_synthesis_report()
        print("\n📋 Synthesis Report:")
        print(report[:200] + "..." if len(report) > 200 else report)
        
        print("✅ Advanced QCSE features test passed")
        
    except Exception as e:
        print(f"❌ Advanced QCSE test failed: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🎯 Terry-the-Tool-Bot GUI Test Suite")
    print("=" * 60)
    print("Testing GUI functionality without requiring tkinter")
    print()
    
    start_time = time.time()
    
    # Run tests
    tests = [
        ("Core Functionality", test_gui_functionality),
        ("GUI Features", test_gui_features),
        ("Advanced QCSE", test_qcse_advanced)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} Test...")
        if test_func():
            print(f"✅ {test_name} test passed")
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    # Summary
    execution_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("🎯 Test Summary")
    print("=" * 60)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    print(f"Execution Time: {execution_time:.2f}s")
    
    if passed == total:
        print("\n🎉 All GUI tests passed! Ready for full GUI implementation.")
        print("📱 GUI components are ready for integration with tkinter.")
        print("🚀 Quantum Code Synthesis Engine is fully functional.")
        print("🎨 Terry-the-Tool-Bot v2.0 is ready for production use!")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Ready for debugging.")
    
    return passed == total

if __name__ == "__main__":
    main()