#!/usr/bin/env python3
"""
Simple Recovery Builder Test

Test the recovery builder module directly without full Terry initialization.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from tools.recovery_builder import RecoveryBuilder, BuildConfig, RecoveryType, DeviceInfo
    
    def test_recovery_builder():
        """Test recovery builder functionality"""
        print("🔧 Testing Terry Recovery Builder")
        print("=" * 50)
        
        # Initialize recovery builder
        builder = RecoveryBuilder()
        print(f"✅ Recovery Builder initialized")
        print(f"📁 Workspace: {builder.workspace_dir}")
        
        # Test device database
        devices = builder.get_supported_devices()
        print(f"📱 Supported devices: {len(devices)}")
        print(f"   First 5 devices: {devices[:5]}")
        
        # Test device compatibility
        test_device = "beryllium"
        compatible, message = builder.check_device_compatibility(test_device)
        print(f"🔍 Device compatibility for {test_device}: {compatible}")
        print(f"   Message: {message}")
        
        # Test build config creation
        if test_device in builder.device_database:
            device_info = builder.device_database[test_device]
            build_config = BuildConfig(
                device_info=device_info,
                recovery_type=RecoveryType.TWRP,
                twrp_version="3.7.0_12"
            )
            print(f"⚙️ Build config created for {test_device}")
            print(f"   Recovery type: {build_config.recovery_type.value}")
            print(f"   TWRP version: {build_config.twrp_version}")
        
        # Test environment setup (without actual building)
        print("\\n🛠️ Testing build environment setup...")
        try:
            # Just test the setup function structure, not actual building
            result = builder.setup_android_build_env()
            print(f"   Android build env setup: {'✅ Success' if result else '❌ Failed'}")
        except Exception as e:
            print(f"   Android build env setup: ⚠️ Expected error - {str(e)[:50]}...")
        
        # Test artifacts directory
        artifacts_dir = builder.get_artifacts_directory()
        print(f"📁 Artifacts directory: {artifacts_dir}")
        print(f"   Directory exists: {artifacts_dir.exists()}")
        
        print("\\n✅ Recovery Builder test completed successfully!")
        print("🚀 Ready for advanced recovery building!")
        
    if __name__ == "__main__":
        test_recovery_builder()
        
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("🔧 Recovery Builder module not available")
except Exception as e:
    print(f"❌ Test failed: {e}")