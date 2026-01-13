# 📁 Where Terry's Built Custom Recoveries Are Saved

## Complete File Structure

All recovery builds from Terry's Recovery Builder are organized in a structured workspace at:

```
~/.terry_toolbot/recovery_builder/
```

## 🎯 Final Recovery Files Location

**Primary Artifacts Directory:**
```
~/.terry_toolbot/recovery_builder/artifacts/
```

This is where all **completed recovery files** are saved.

## 📱 Built Recovery File Types

### TWRP Recoveries
```
~/.terry_toolbot/recovery_builder/artifacts/twrp_[device]_[timestamp].img
```
- **Format**: `twrp_beryllium_20240113_103045.img`
- **Type**: Flashable recovery image
- **Size**: Typically 20-50 MB

### Orange Fox Recoveries  
```
~/.terry_toolbot/recovery_builder/artifacts/orange_fox_[device]_[timestamp].img
```
- **Format**: `orange_fox_guacamole_20240113_103045.img`
- **Type**: Flashable recovery image
- **Size**: Typically 15-40 MB

## 📋 Supporting Files

### Build Logs
```
~/.terry_toolbot/recovery_builder/artifacts/twrp_[device]_[timestamp]_build.log
~/.terry_toolbot/recovery_builder/artifacts/orange_fox_[device]_[timestamp]_build.log
```

### Flashable ZIP Files
```
~/.terry_toolbot/recovery_builder/artifacts/twrp_[device]_[timestamp].zip
~/.terry_toolbot/recovery_builder/artifacts/orange_fox_[device]_[timestamp].zip
```

### Build Reports
```
~/.terry_toolbot/recovery_builder/artifacts/build_report_[timestamp].json
```

## 🌳 Roomservice.xml Files

**Roomservice Directory:**
```
~/.terry_toolbot/recovery_builder/roomservice/
```

**Format:**
```
~/.terry_toolbot/recovery_builder/roomservice/roomservice_[device].xml
```

## 🗂️ Complete Directory Structure

```
~/.terry_toolbot/recovery_builder/
├── 📁 sources/                    # Source code repositories
│   ├── 📁 twrp/                # TWRP source code
│   ├── 📁 orange_fox/           # Orange Fox source code
│   ├── 📁 device_trees/         # Default device trees
│   └── 📁 custom_trees/         # Custom device trees
├── 📁 builds/                     # Temporary build directories
│   ├── 📁 twrp/                # TWRP build outputs
│   ├── 📁 orange_fox/           # Orange Fox build outputs
│   └── 📁 custom/               # Custom device build outputs
├── 📁 artifacts/ ⭐             # FINAL RECOVERY FILES HERE!
│   ├── 📄 twrp_beryllium_20240113_103045.img
│   ├── 📄 twrp_beryllium_20240113_103045_build.log
│   ├── 📄 orange_fox_guacamole_20240113_103045.img
│   ├── 📄 orange_fox_guacamole_20240113_103045_build.log
│   └── 📊 build_report_20240113_103045.json
├── 📁 roomservice/                 # Roomservice.xml files
│   └── 📄 roomservice_beryllium.xml
├── 📁 logs/                       # Build system logs
├── 📁 cache/                      # Download cache
└── 📁 tools/                      # Build tools and scripts
```

## 🔍 Quick Access Commands

```bash
# Navigate to artifacts directory
cd ~/.terry_toolbot/recovery_builder/artifacts/

# List all recovery images
ls -la *.img

# List all flashable ZIPs
ls -la *.zip

# List all build logs
ls -la *.log

# List roomservice files
cd ~/.terry_toolbot/recovery_builder/roomservice/
ls -la *.xml
```

## 📱 Example Built Recovery Paths

### TWRP for Xiaomi Poco F1 (beryllium)
```
~/.terry_toolbot/recovery_builder/artifacts/twrp_beryllium_20240113_103045.img
```

### Orange Fox for OnePlus 7 Pro (guacamole)
```
~/.terry_toolbot/recovery_builder/artifacts/orange_fox_guacamole_20240113_103045.img
```

### Build Log for Poco F1
```
~/.terry_toolbot/recovery_builder/artifacts/twrp_beryllium_20240113_103045_build.log
```

## 🔐 Security Features

- **SHA256 Checksums**: Every recovery file has a calculated checksum
- **Build Metadata**: JSON reports contain complete build information
- **Timestamp Tracking**: Unique timestamps prevent file overwrites
- **Organized Structure**: Logical directory organization prevents confusion

## 🚀 Flashing Built Recoveries

Once recovered files are built in the artifacts directory:

```bash
# Flash with ADB
adb sideload ~/.terry_toolbot/recovery_builder/artifacts/twrp_beryllium_20240113_103045.img

# Or copy to device storage and flash via custom recovery
cp ~/.terry_toolbot/recovery_builder/artifacts/orange_fox_guacamole_20240113_103045.img /sdcard/
```

## 📊 File Naming Convention

**Pattern**: `{recovery_type}_{device_codename}_{timestamp}.{extension}`

**Timestamp Format**: `YYYYMMDD_HHMMSS`
- Example: `20240113_103045` = January 13, 2024 at 10:30:45

**Examples**:
- `twrp_beryllium_20240113_103045.img`
- `orange_fox_lavender_20240113_103045.zip`
- `twrp_beryllium_20240113_103045_build.log`

## 💡 Pro Tips

1. **Check File Size**: Recovery images should be 15-50 MB
2. **Verify Checksum**: Use SHA256 to verify file integrity
3. **Review Build Logs**: Check logs for any warnings or errors
4. **Monitor Artifacts**: Keep an eye on the artifacts directory
5. **Backup Roomservice**: Save roomservice.xml files for future builds

---

🎯 **Bottom Line**: All your custom built recoveries are saved to:
```
~/.terry_toolbot/recovery_builder/artifacts/
```

This is where you'll find your finished TWRP and Orange Fox recovery files ready for flashing!