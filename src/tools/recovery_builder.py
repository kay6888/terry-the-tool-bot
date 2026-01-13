"""
Recovery Builder - Advanced TWRP & Orange Fox Recovery Building Tool

Expert-level recovery building system with comprehensive device support,
automated building, and artifact management.
"""

import os
import sys
import subprocess
import json
import logging
import shutil
import hashlib
import requests
import tarfile
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecoveryType(Enum):
    TWRP = "twrp"
    ORANGE_FOX = "orange_fox"
    CUSTOM = "custom"

class BuildStatus(Enum):
    PENDING = "pending"
    BUILDING = "building"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class DeviceInfo:
    codename: str
    brand: str
    model: str
    arch: str
    platform: str
    android_version: str
    maintainer: str = ""
    
@dataclass
class BuildConfig:
    device_info: DeviceInfo
    recovery_type: RecoveryType
    twrp_version: str = "3.7.0_12"
    orange_fox_version: str = "12.1"
    enable_a2dp: bool = True
    enable_compression: bool = True
    enable_keystore: bool = True
    custom_patches: Union[List[str], None] = None
    
    def __post_init__(self):
        if self.custom_patches is None:
            self.custom_patches = []

@dataclass
class BuildArtifact:
    device_codename: str
    recovery_type: RecoveryType
    build_time: datetime
    file_path: Path
    file_size: int
    sha256_hash: str
    build_log_path: Path
    status: BuildStatus
    build_config: BuildConfig

class RecoveryBuilder:
    """Advanced Recovery Building System"""
    
    def __init__(self, workspace_dir: Optional[Path] = None):
        self.workspace_dir = workspace_dir or Path.home() / ".terry_toolbot" / "recovery_builder"
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup subdirectories
        self.setup_directories()
        
        # Initialize device database
        self.device_database = self.load_device_database()
        
        # Build tracking
        self.current_builds = {}
        self.build_history = []
        
        logger.info(f"Recovery Builder initialized with workspace: {self.workspace_dir}")
    
    def setup_directories(self) -> None:
        """Create organized directory structure"""
        dirs = [
            "sources/twrp",
            "sources/orange_fox", 
            "sources/device_trees",
            "builds/twrp",
            "builds/orange_fox",
            "tools",
            "logs",
            "cache",
            "artifacts"
        ]
        
        for dir_path in dirs:
            (self.workspace_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    def load_device_database(self) -> Dict[str, DeviceInfo]:
        """Load comprehensive device database"""
        default_devices = {
            # Xiaomi Devices
            "beryllium": DeviceInfo("beryllium", "Xiaomi", "Poco F1", "arm64", "sdm845", "10"),
            "begonia": DeviceInfo("begonia", "Xiaomi", "Redmi Note 8 Pro", "arm64", "mt6768", "10"),
            "sweet": DeviceInfo("sweet", "Xiaomi", "Redmi Note 10 Pro", "arm64", "sdm732g", "11"),
            "lmi": DeviceInfo("lmi", "Xiaomi", "POCO F2 Pro", "arm64", "sdm865", "11"),
            
            # Samsung Devices
            "star2lte": DeviceInfo("star2lte", "Samsung", "S9+", "arm64", "exynos9810", "10"),
            "beyond2lte": DeviceInfo("beyond2lte", "Samsung", "S10+", "arm64", "exynos9820", "11"),
            
            # OnePlus Devices
            "guacamole": DeviceInfo("guacamole", "OnePlus", "7 Pro", "arm64", "sdm855", "11"),
            "hotdog": DeviceInfo("hotdog", "OnePlus", "7T Pro", "arm64", "sdm855+", "11"),
            
            # Google Devices
            "sunfish": DeviceInfo("sunfish", "Google", "Pixel 4a", "arm64", "sdm765g", "12"),
            "redfin": DeviceInfo("redfin", "Google", "Pixel 5", "arm64", "sdm765g", "12"),
            "bluejay": DeviceInfo("bluejay", "Google", "Pixel 6a", "arm64", "gs101", "13"),
            
            # ASUS Devices  
            "I01WD": DeviceInfo("I01WD", "ASUS", "ROG Phone 3", "arm64", "sdm865+", "11"),
            
            # Realme Devices
            "RMX2061": DeviceInfo("RMX2061", "Realme", "6 Pro", "arm64", "sdm720g", "11"),
            "RMX1971": DeviceInfo("RMX1971", "Realme", "5 Pro", "arm64", "sdm712", "10")
        }
        
        device_db_file = self.workspace_dir / "device_database.json"
        if device_db_file.exists():
            try:
                with open(device_db_file, 'r') as f:
                    data = json.load(f)
                    return {k: DeviceInfo(**v) for k, v in data.items()}
            except Exception as e:
                logger.warning(f"Failed to load device database: {e}")
        
        # Save default database
        self.save_device_database(default_devices)
        return default_devices
    
    def save_device_database(self, devices: Dict[str, DeviceInfo]) -> None:
        """Save device database to file"""
        device_db_file = self.workspace_dir / "device_database.json"
        data = {k: vars(v) for k, v in devices.items()}
        with open(device_db_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def setup_build_environment(self) -> bool:
        """Setup complete build environment"""
        logger.info("Setting up build environment...")
        
        try:
            # Check for required tools
            required_tools = ["git", "make", "gcc", "python3", "zip", "unzip"]
            missing_tools = []
            
            for tool in required_tools:
                if not shutil.which(tool):
                    missing_tools.append(tool)
            
            if missing_tools:
                logger.error(f"Missing required tools: {missing_tools}")
                return False
            
            # Setup Android build environment
            if not self.setup_android_build_env():
                logger.error("Failed to setup Android build environment")
                return False
            
            # Clone TWRP source
            if not self.clone_twrp_source():
                logger.error("Failed to clone TWRP source")
                return False
            
            # Clone Orange Fox source
            if not self.clone_orange_fox_source():
                logger.error("Failed to clone Orange Fox source")
                return False
            
            # Setup device trees
            if not self.setup_common_device_trees():
                logger.error("Failed to setup device trees")
                return False
            
            logger.info("Build environment setup complete")
            return True
            
        except Exception as e:
            logger.error(f"Build environment setup failed: {e}")
            return False
    
    def setup_android_build_env(self) -> bool:
        """Setup Android build environment"""
        try:
            # Create build environment
            build_env_file = self.workspace_dir / "build_env.sh"
            build_env_content = '''#!/bin/bash
# Android Build Environment Setup for Recovery Builder

export ANDROID_HOME=$HOME/Android/Sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

# Build tools
export ARCH=arm64
export SUBARCH=arm64
export CROSS_COMPILE=aarch64-linux-android-
export CC=clang
export CLANG_TRIPLE=aarch64-linux-gnu-

# Optimization flags
export USE_CLANG_PLATFORM_BUILD=true
export CLANG_VERSION=11
export ALLOW_MISSING_DEPENDENCIES=true
export LC_ALL=C

echo "Android build environment configured"
'''
            
            with open(build_env_file, 'w') as f:
                f.write(build_env_content)
            
            build_env_file.chmod(0o755)
            
            # Source environment
            result = subprocess.run(f"source {build_env_file}", shell=True, 
                                  capture_output=True, text=True)
            
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Failed to setup Android build env: {e}")
            return False
    
    def clone_twrp_source(self) -> bool:
        """Clone TWRP source code"""
        twrp_dir = self.workspace_dir / "sources" / "twrp"
        
        try:
            if twrp_dir.exists():
                logger.info("TWRP source already exists, updating...")
                result = subprocess.run(
                    ["git", "pull"],
                    cwd=twrp_dir,
                    capture_output=True,
                    text=True
                )
            else:
                logger.info("Cloning TWRP source...")
                result = subprocess.run([
                    "git", "clone", 
                    "https://github.com/minimal-manifest-twrp/platform_manifest.git",
                    str(twrp_dir)
                ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("TWRP source cloned/updated successfully")
                return True
            else:
                logger.error(f"TWRP clone failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to clone TWRP source: {e}")
            return False
    
    def clone_orange_fox_source(self) -> bool:
        """Clone Orange Fox source code"""
        orange_fox_dir = self.workspace_dir / "sources" / "orange_fox"
        
        try:
            if orange_fox_dir.exists():
                logger.info("Orange Fox source already exists, updating...")
                result = subprocess.run(
                    ["git", "pull"],
                    cwd=orange_fox_dir,
                    capture_output=True,
                    text=True
                )
            else:
                logger.info("Cloning Orange Fox source...")
                result = subprocess.run([
                    "git", "clone", 
                    "https://gitlab.com/OrangeFox/manifest.git",
                    str(orange_fox_dir)
                ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Orange Fox source cloned/updated successfully")
                return True
            else:
                logger.error(f"Orange Fox clone failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to clone Orange Fox source: {e}")
            return False
    
    def setup_common_device_trees(self) -> bool:
        """Setup common device trees"""
        device_trees_dir = self.workspace_dir / "sources" / "device_trees"
        
        try:
            # Create device tree repos for common devices
            device_repos = {
                "beryllium": "https://github.com/TWRP-Team/device_xiaomi_beryllium",
                "begonia": "https://github.com/TWRP-Team/device_xiaomi_begonia", 
                "guacamole": "https://github.com/TWRP-Team/device_oneplus_guacamole",
                "redfin": "https://github.com/TWRP-Team/device_google_redfin"
            }
            
            for codename, repo_url in device_repos.items():
                device_dir = device_trees_dir / f"device_{codename}"
                
                if device_dir.exists():
                    logger.info(f"Device tree for {codename} exists, updating...")
                    subprocess.run(["git", "pull"], cwd=device_dir, capture_output=True)
                else:
                    logger.info(f"Cloning device tree for {codename}...")
                    subprocess.run([
                        "git", "clone", repo_url, str(device_dir)
                    ], capture_output=True)
            
            logger.info("Common device trees setup complete")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup device trees: {e}")
            return False
    
    def check_device_compatibility(self, device_codename: str) -> Tuple[bool, str]:
        """Check if device is supported"""
        if device_codename not in self.device_database:
            return False, f"Device {device_codename} not found in database"
        
        device_info = self.device_database[device_codename]
        
        # Check for device tree
        device_tree_path = self.workspace_dir / "sources" / "device_trees" / f"device_{device_codename}"
        if not device_tree_path.exists():
            return False, f"No device tree found for {device_codename}"
        
        # Check kernel sources
        kernel_sources_path = device_tree_path / "kernel"
        if not kernel_sources_path.exists():
            return False, f"Kernel sources not found for {device_codename}"
        
        return True, f"Device {device_codename} is compatible"
    
    def build_recovery(self, build_config: BuildConfig) -> BuildArtifact:
        """Build recovery with given configuration"""
        device_codename = build_config.device_info.codename
        build_id = f"{build_config.recovery_type.value}_{device_codename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"Starting build {build_id}")
        
        # Check compatibility
        compatible, message = self.check_device_compatibility(device_codename)
        if not compatible:
            logger.error(f"Build failed: {message}")
            return self.create_failed_artifact(build_config, build_id, message)
        
        # Create build directory
        build_dir = self.workspace_dir / "builds" / build_config.recovery_type.value / device_codename / build_id
        build_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup build log
        log_file = build_dir / "build.log"
        
        try:
            # Update current builds
            self.current_builds[build_id] = {
                'config': build_config,
                'start_time': datetime.now(),
                'status': BuildStatus.BUILDING
            }
            
            if build_config.recovery_type == RecoveryType.TWRP:
                artifact = self.build_twrp(build_config, build_dir, log_file)
            elif build_config.recovery_type == RecoveryType.ORANGE_FOX:
                artifact = self.build_orange_fox(build_config, build_dir, log_file)
            else:
                raise ValueError(f"Unsupported recovery type: {build_config.recovery_type}")
            
            # Update build history
            self.build_history.append(artifact)
            self.current_builds[build_id]['status'] = artifact.status
            
            logger.info(f"Build {build_id} completed with status: {artifact.status}")
            return artifact
            
        except Exception as e:
            logger.error(f"Build {build_id} failed: {e}")
            failed_artifact = self.create_failed_artifact(build_config, build_id, str(e))
            self.build_history.append(failed_artifact)
            self.current_builds[build_id]['status'] = BuildStatus.FAILED
            return failed_artifact
    
    def build_twrp(self, build_config: BuildConfig, build_dir: Path, log_file: Path) -> BuildArtifact:
        """Build TWRP recovery"""
        device_codename = build_config.device_info.codename
        twrp_source_dir = self.workspace_dir / "sources" / "twrp"
        device_tree_dir = self.workspace_dir / "sources" / "device_trees" / f"device_{device_codename}"
        
        try:
            with open(log_file, 'w') as log:
                log.write(f"Starting TWRP build for {device_codename}\\n")
                log.write(f"Build time: {datetime.now()}\\n")
                log.write(f"TWRP version: {build_config.twrp_version}\\n\\n")
            
            # Setup build environment
            env_vars = os.environ.copy()
            env_vars.update({
                'ANDROID_BUILD_TOP': str(twrp_source_dir),
                'OUT_DIR': str(build_dir / "out"),
                'DEVICE': device_codename,
                'TWRP_VERSION': build_config.twrp_version
            })
            
            # Run build commands
            build_commands = [
                f"cd {twrp_source_dir}",
                f"source {self.workspace_dir}/build_env.sh",
                f"repo init -u https://github.com/minimal-manifest-twrp/platform_manifest.git -b twrp-{build_config.twrp_version}",
                "repo sync",
                f"export DEVICE={device_codename}",
                f"mka recoveryimage"
            ]
            
            full_command = " && ".join(build_commands)
            
            with open(log_file, 'a') as log:
                result = subprocess.run(
                    full_command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    env=env_vars
                )
                
                log.write(f"Build command: {full_command}\\n")
                log.write(f"Return code: {result.returncode}\\n")
                log.write(f"STDOUT:\\n{result.stdout}\\n")
                log.write(f"STDERR:\\n{result.stderr}\\n")
            
            # Check build results
            recovery_image = build_dir / "out" / "product" / device_codename / "recovery.img"
            
            if recovery_image.exists():
                # Create artifact
                artifact_path = self.workspace_dir / "artifacts" / f"twrp_{device_codename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.img"
                shutil.copy2(recovery_image, artifact_path)
                
                # Calculate hash
                sha256_hash = self.calculate_file_hash(artifact_path)
                
                artifact = BuildArtifact(
                    device_codename=device_codename,
                    recovery_type=RecoveryType.TWRP,
                    build_time=datetime.now(),
                    file_path=artifact_path,
                    file_size=artifact_path.stat().st_size,
                    sha256_hash=sha256_hash,
                    build_log_path=log_file,
                    status=BuildStatus.SUCCESS,
                    build_config=build_config
                )
                
                # Copy build log to artifacts
                log_artifact_path = self.workspace_dir / "artifacts" / f"twrp_{device_codename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_build.log"
                shutil.copy2(log_file, log_artifact_path)
                
                with open(log_file, 'a') as log:
                    log.write(f"\\nBuild SUCCESS: {artifact_path}\\n")
                    log.write(f"File size: {artifact.file_size} bytes\\n")
                    log.write(f"SHA256: {sha256_hash}\\n")
                
                return artifact
            else:
                error_msg = f"Recovery image not found at {recovery_image}"
                with open(log_file, 'a') as log:
                    log.write(f"\\nBuild FAILED: {error_msg}\\n")
                
                return self.create_failed_artifact(build_config, f"twrp_{device_codename}", error_msg)
                
        except Exception as e:
            error_msg = f"TWRP build error: {str(e)}"
            with open(log_file, 'a') as log:
                log.write(f"\\nBuild EXCEPTION: {error_msg}\\n")
            
            return self.create_failed_artifact(build_config, f"twrp_{device_codename}", error_msg)
    
    def build_orange_fox(self, build_config: BuildConfig, build_dir: Path, log_file: Path) -> BuildArtifact:
        """Build Orange Fox recovery"""
        device_codename = build_config.device_info.codename
        orange_fox_source_dir = self.workspace_dir / "sources" / "orange_fox"
        device_tree_dir = self.workspace_dir / "sources" / "device_trees" / f"device_{device_codename}"
        
        try:
            with open(log_file, 'w') as log:
                log.write(f"Starting Orange Fox build for {device_codename}\\n")
                log.write(f"Build time: {datetime.now()}\\n")
                log.write(f"Orange Fox version: {build_config.orange_fox_version}\\n\\n")
            
            # Setup build environment
            env_vars = os.environ.copy()
            env_vars.update({
                'ANDROID_BUILD_TOP': str(orange_fox_source_dir),
                'OUT_DIR': str(build_dir / "out"),
                'DEVICE': device_codename,
                'FOX_VERSION': build_config.orange_fox_version,
                'FOX_BUILD_TYPE': 'Unofficial',
                'OF_MAINTAINER': 'Terry-Recovery-Builder'
            })
            
            # Orange Fox specific build commands
            build_commands = [
                f"cd {orange_fox_source_dir}",
                f"source {self.workspace_dir}/build_env.sh",
                "repo init -u https://gitlab.com/OrangeFox/manifest.git -b fox_{build_config.orange_fox_version}",
                "repo sync",
                f"export DEVICE={device_codename}",
                f"export OF_DISABLE_RECOVERY_MEDIA=1",  # Disable recovery media for smaller builds
                f"export OF_USE_TWRP_SHELL=1",  # Use TWRP shell
                f"mka recoveryimage"
            ]
            
            full_command = " && ".join(build_commands)
            
            with open(log_file, 'a') as log:
                result = subprocess.run(
                    full_command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    env=env_vars
                )
                
                log.write(f"Build command: {full_command}\\n")
                log.write(f"Return code: {result.returncode}\\n")
                log.write(f"STDOUT:\\n{result.stdout}\\n")
                log.write(f"STDERR:\\n{result.stderr}\\n")
            
            # Check build results
            recovery_image = build_dir / "out" / "product" / device_codename / "recovery.img"
            
            if recovery_image.exists():
                # Create artifact
                artifact_path = self.workspace_dir / "artifacts" / f"orange_fox_{device_codename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.img"
                shutil.copy2(recovery_image, artifact_path)
                
                # Calculate hash
                sha256_hash = self.calculate_file_hash(artifact_path)
                
                artifact = BuildArtifact(
                    device_codename=device_codename,
                    recovery_type=RecoveryType.ORANGE_FOX,
                    build_time=datetime.now(),
                    file_path=artifact_path,
                    file_size=artifact_path.stat().st_size,
                    sha256_hash=sha256_hash,
                    build_log_path=log_file,
                    status=BuildStatus.SUCCESS,
                    build_config=build_config
                )
                
                # Copy build log to artifacts
                log_artifact_path = self.workspace_dir / "artifacts" / f"orange_fox_{device_codename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_build.log"
                shutil.copy2(log_file, log_artifact_path)
                
                with open(log_file, 'a') as log:
                    log.write(f"\\nBuild SUCCESS: {artifact_path}\\n")
                    log.write(f"File size: {artifact.file_size} bytes\\n")
                    log.write(f"SHA256: {sha256_hash}\\n")
                
                return artifact
            else:
                error_msg = f"Recovery image not found at {recovery_image}"
                with open(log_file, 'a') as log:
                    log.write(f"\\nBuild FAILED: {error_msg}\\n")
                
                return self.create_failed_artifact(build_config, f"orange_fox_{device_codename}", error_msg)
                
        except Exception as e:
            error_msg = f"Orange Fox build error: {str(e)}"
            with open(log_file, 'a') as log:
                log.write(f"\\nBuild EXCEPTION: {error_msg}\\n")
            
            return self.create_failed_artifact(build_config, f"orange_fox_{device_codename}", error_msg)
    
    def create_failed_artifact(self, build_config: BuildConfig, build_id: str, error_message: str) -> BuildArtifact:
        """Create a failed build artifact"""
        return BuildArtifact(
            device_codename=build_config.device_info.codename,
            recovery_type=build_config.recovery_type,
            build_time=datetime.now(),
            file_path=Path(""),
            file_size=0,
            sha256_hash="",
            build_log_path=self.workspace_dir / "logs" / f"{build_id}_failed.log",
            status=BuildStatus.FAILED,
            build_config=build_config
        )
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def get_supported_devices(self) -> List[str]:
        """Get list of supported devices"""
        return list(self.device_database.keys())
    
    def get_build_history(self) -> List[BuildArtifact]:
        """Get build history"""
        return self.build_history
    
    def get_current_builds(self) -> Dict[str, Dict]:
        """Get current builds"""
        return self.current_builds
    
    def get_artifacts_directory(self) -> Path:
        """Get artifacts directory path"""
        return self.workspace_dir / "artifacts"
    
    def save_build_report(self, artifacts: List[BuildArtifact]) -> Path:
        """Save comprehensive build report"""
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "total_builds": len(artifacts),
            "successful_builds": len([a for a in artifacts if a.status == BuildStatus.SUCCESS]),
            "failed_builds": len([a for a in artifacts if a.status == BuildStatus.FAILED]),
            "builds": []
        }
        
        for artifact in artifacts:
            build_data = {
                "device_codename": artifact.device_codename,
                "recovery_type": artifact.recovery_type.value,
                "build_time": artifact.build_time.isoformat(),
                "status": artifact.status.value,
                "file_size": artifact.file_size,
                "sha256_hash": artifact.sha256_hash,
                "file_path": str(artifact.file_path),
                "build_log_path": str(artifact.build_log_path),
                "build_config": {
                    "twrp_version": artifact.build_config.twrp_version,
                    "orange_fox_version": artifact.build_config.orange_fox_version,
                    "enable_a2dp": artifact.build_config.enable_a2dp,
                    "enable_compression": artifact.build_config.enable_compression,
                    "enable_keystore": artifact.build_config.enable_keystore
                }
            }
            report_data["builds"].append(build_data)
        
        report_file = self.workspace_dir / "artifacts" / f"build_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return report_file

# Main interface for integration
def main():
    """Main interface for recovery builder"""
    builder = RecoveryBuilder()
    
    print("🔧 Terry Recovery Builder - Expert System")
    print("=" * 50)
    
    # Setup environment if needed
    if not builder.setup_build_environment():
        print("❌ Failed to setup build environment")
        return
    
    # Show supported devices
    devices = builder.get_supported_devices()
    print(f"✅ Supported devices: {len(devices)}")
    for device in devices:
        device_info = builder.device_database[device]
        print(f"   • {device} - {device_info.brand} {device_info.model}")
    
    # Example build for demonstration
    print("\\n🚀 Starting example build...")
    device = "beryllium"  # Poco F1
    if device in devices:
        build_config = BuildConfig(
            device_info=builder.device_database[device],
            recovery_type=RecoveryType.TWRP,
            twrp_version="3.7.0_12"
        )
        
        artifact = builder.build_recovery(build_config)
        
        if artifact.status == BuildStatus.SUCCESS:
            print(f"✅ Build successful: {artifact.file_path}")
            print(f"   Size: {artifact.file_size:,} bytes")
            print(f"   SHA256: {artifact.sha256_hash}")
        else:
            print(f"❌ Build failed")
    
    # Save build report
    if builder.build_history:
        report_file = builder.save_build_report(builder.build_history)
        print(f"📊 Build report saved: {report_file}")

if __name__ == "__main__":
    main()