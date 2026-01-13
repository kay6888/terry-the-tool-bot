"""
Android Builder Tool for Terry-the-Tool-Bot

Creates complete Android projects with modern architecture and best practices.
"""

import os
import shutil
from typing import Dict, Any, Optional
from pathlib import Path
import json
import time
from .base_tool import BaseTool
import logging

logger = logging.getLogger(__name__)

class AndroidBuilderTool(BaseTool):
    """Android project builder tool"""
    
    def __init__(self):
        super().__init__(
            name="android_builder",
            version="2.1",
            description="Creates complete Android projects with proper structure"
        )
        
        # Android project templates
        self.templates = {
            'basic': self._get_basic_template(),
            'mvvm': self._get_mvvm_template(),
            'compose': self._get_compose_template(),
            'kmp': self._get_kmp_template()
        }
        
        # Supported features
        self.features = [
            'material_design',
            'viewbinding',
            'livedata',
            'coroutines',
            'room_database',
            'dagger_hilt',
            'navigation_component',
            'recyclerview',
            'retrofit',
            'work_manager'
        ]
    
    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Android project creation"""
        start_time = time.time()
        
        try:
            # Extract project requirements
            project_config = self._extract_project_config(user_input, context)
            
            # Validate configuration
            if not self._validate_project_config(project_config):
                return self._format_response(
                    status='error',
                    message='Invalid project configuration',
                    execution_time=time.time() - start_time
                )
            
            # Create project structure
            project_path = self._create_project_structure(project_config)
            
            # Generate project files
            generated_files = self._generate_android_files(project_config, project_path)
            
            # Setup Gradle and dependencies
            self._setup_gradle(project_config, project_path)
            
            # Create README
            self._create_readme(project_config, project_path)
            
            result_data = {
                'project_name': project_config['name'],
                'package_name': project_config['package_name'],
                'app_type': project_config['app_type'],
                'location': str(project_path),
                'files_created': generated_files,
                'features': project_config['features']
            }
            
            logger.info(f"Created Android project: {project_config['name']}")
            
            return self._format_response(
                status='success',
                message=f'Successfully created Android project: {project_config["name"]}',
                data=result_data,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Android project creation failed: {str(e)}")
            return self._format_response(
                status='error',
                message=f'Project creation failed: {str(e)}',
                execution_time=time.time() - start_time
            )
    
    def validate_input(self, user_input: str) -> bool:
        """Validate if input is suitable for Android building"""
        android_keywords = [
            'android', 'app', 'kotlin', 'java', 'studio', 'gradle',
            'create', 'build', 'project', 'activity', 'fragment',
            'material', 'viewmodel', 'livedata', 'dagger', 'hilt'
        ]
        
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in android_keywords)
    
    def _extract_project_config(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract project configuration from user input"""
        import re
        
        # Default configuration
        config = {
            'name': self._extract_project_name(user_input),
            'package_name': self._extract_package_name(user_input),
            'app_type': self._detect_app_type(user_input),
            'min_sdk': 24,
            'target_sdk': 34,
            'compile_sdk': 34,
            'features': self._extract_features(user_input),
            'template': 'basic'
        }
        
        # Override with context if available
        if 'project_preferences' in context:
            config.update(context['project_preferences'])
        
        return config
    
    def _extract_project_name(self, user_input: str) -> str:
        """Extract project name from user input"""
        patterns = [
            r'create (?:an? )?android (?:app|project) (?:called|named) "?([^"\s]+)"?',
            r'build (?:an? )?android (?:app|project) "?([^"\s]+)"?',
            r'project "?([^"\s]+)"?',
            r'app "?([^"\s]+)"?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                return self._sanitize_project_name(name)
        
        return 'MyAndroidApp'
    
    def _sanitize_project_name(self, name: str) -> str:
        """Sanitize project name for file system"""
        # Remove invalid characters
        import re
        name = re.sub(r'[^a-zA-Z0-9_]', '', name)
        
        # Ensure it doesn't start with number
        if name and name[0].isdigit():
            name = 'App' + name
            
        return name.capitalize()
    
    def _extract_package_name(self, user_input: str) -> str:
        """Extract package name from user input"""
        patterns = [
            r'package "?([^"\s]+)"?',
            r'com\. "?([^"\s]+)"?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                package = match.group(1).strip()
                return self._validate_package_name(package)
        
        # Derive from project name
        project_name = self._extract_project_name(user_input)
        return f"com.terry.{project_name.lower()}"
    
    def _validate_package_name(self, package: str) -> str:
        """Validate and fix package name format"""
        # Remove invalid characters
        import re
        package = re.sub(r'[^a-zA-Z0-9_.]', '', package)
        
        # Ensure reverse domain name format
        parts = package.split('.')
        if len(parts) < 2:
            return f"com.terry.{package}"
        
        # Fix common issues
        parts = [part.lower() for part in parts if part]
        return '.'.join(parts)
    
    def _detect_app_type(self, user_input: str) -> str:
        """Detect app type from user input"""
        user_input_lower = user_input.lower()
        
        if any(keyword in user_input_lower for keyword in ['game', 'gaming']):
            return 'game'
        elif any(keyword in user_input_lower for keyword in ['camera', 'photo', 'video']):
            return 'camera'
        elif any(keyword in user_input_lower for keyword in ['music', 'audio', 'player']):
            return 'music'
        elif any(keyword in user_input_lower for keyword in ['chat', 'messaging', 'social']):
            return 'social'
        elif any(keyword in user_input_lower for keyword in ['ecommerce', 'shop', 'store']):
            return 'ecommerce'
        else:
            return 'general'
    
    def _extract_features(self, user_input: str) -> list:
        """Extract desired features from user input"""
        user_input_lower = user_input.lower()
        detected_features = []
        
        feature_mapping = {
            'material design': ['material', 'mdc', 'design'],
            'viewbinding': ['viewbinding', 'binding'],
            'livedata': ['livedata', 'viewmodel', 'observable'],
            'coroutines': ['coroutine', 'async'],
            'room database': ['room', 'database', 'dao'],
            'dagger hilt': ['dagger', 'hilt', 'di', 'injection'],
            'navigation': ['navigation', 'nav'],
            'recyclerview': ['recycler', 'list', 'adapter'],
            'retrofit': ['retrofit', 'network', 'api'],
            'work manager': ['work', 'manager', 'background']
        }
        
        for feature, keywords in feature_mapping.items():
            if any(keyword in user_input_lower for keyword in keywords):
                detected_features.append(feature)
        
        return detected_features if detected_features else ['material_design', 'viewbinding']
    
    def _create_project_structure(self, config: Dict[str, Any]) -> Path:
        """Create Android project directory structure"""
        base_dir = Path(context.get('projects_dir', Path.home() / 'TerryProjects'))
        project_dir = base_dir / config['name']
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Create standard directories
        directories = [
            'app/src/main/java/com/terry/' + config['name'].lower(),
            'app/src/main/res/values',
            'app/src/main/res/layout',
            'app/src/main/res/drawable',
            'app/src/main/res/mipmap-hdpi',
            'app/src/main/res/mipmap-mdpi',
            'app/src/main/res/mipmap-xhdpi',
            'app/src/main/res/mipmap-xxhdpi',
            'app/src/main/res/mipmap-xxxhdpi',
            'gradle/wrapper',
            '.idea'
        ]
        
        for directory in directories:
            (project_dir / directory).mkdir(parents=True, exist_ok=True)
        
        return project_dir
    
    def _generate_android_files(self, config: Dict[str, Any], project_path: Path) -> list:
        """Generate Android project files"""
        generated_files = []
        
        # Select template
        template = self.templates.get(config.get('template', 'basic'), self.templates['basic'])
        
        # Generate main activity
        main_activity = template['MainActivity'].format(
            package_name=config['package_name'],
            class_name=config['name']
        )
        activity_path = project_path / f"app/src/main/java/com/terry/{config['name'].lower()}/MainActivity.java"
        with open(activity_path, 'w') as f:
            f.write(main_activity)
        generated_files.append(str(activity_path))
        
        # Generate layout
        layout_xml = template['activity_main']
        layout_path = project_path / "app/src/main/res/layout/activity_main.xml"
        with open(layout_path, 'w') as f:
            f.write(layout_xml)
        generated_files.append(str(layout_path))
        
        # Generate strings
        strings_xml = template['strings']
        strings_path = project_path / "app/src/main/res/values/strings.xml"
        with open(strings_path, 'w') as f:
            f.write(strings_xml.format(app_name=config['name']))
        generated_files.append(str(strings_path))
        
        # Generate Gradle files
        settings_gradle = template['settings_gradle']
        build_gradle = template['build_gradle'].format(
            package_name=config['package_name'],
            min_sdk=config['min_sdk'],
            target_sdk=config['target_sdk'],
            compile_sdk=config['compile_sdk']
        )
        
        with open(project_path / "settings.gradle.kts", 'w') as f:
            f.write(settings_gradle)
        generated_files.append(str(project_path / "settings.gradle.kts"))
        
        with open(project_path / "build.gradle.kts", 'w') as f:
            f.write(build_gradle)
        generated_files.append(str(project_path / "build.gradle.kts"))
        
        return generated_files
    
    def _setup_gradle(self, config: Dict[str, Any], project_path: Path) -> None:
        """Setup Gradle wrapper and configuration"""
        # Create gradle wrapper
        gradle_dir = project_path / 'gradle'
        gradle_dir.mkdir(exist_ok=True)
        
        # Gradle wrapper properties
        gradle_properties = """
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.5-bin.zip
zipStoreBase=GRADLE_USER_HOME
"""
        
        with open(gradle_dir / 'gradle-wrapper.properties', 'w') as f:
            f.write(gradle_properties)
    
    def _create_readme(self, config: Dict[str, Any], project_path: Path) -> None:
        """Create README.md for the project"""
        readme_content = f"""# {config['name']}

An Android application created by Terry-the-Tool-Bot.

## Project Information

- **Package Name**: {config['package_name']}
- **App Type**: {config['app_type']}
- **Minimum SDK**: {config['min_sdk']}
- **Target SDK**: {config['target_sdk']}
- **Features**: {', '.join(config['features'])}

## Getting Started

1. Open this project in Android Studio
2. Sync Gradle dependencies
3. Run the application on an emulator or device

## Features

{self._format_features(config['features'])}

## File Structure

```
{self._get_project_structure(config['name'])}
```

## Build Instructions

```bash
./gradlew assembleDebug
./gradlew assembleRelease
```

---

*Generated by Terry-the-Tool-Bot v2.0 - Advanced AI Coding Assistant*
"""
        
        with open(project_path / 'README.md', 'w') as f:
            f.write(readme_content)
    
    def _format_features(self, features: list) -> str:
        """Format features for README"""
        feature_descriptions = {
            'material_design': 'Material Design components',
            'viewbinding': 'View Binding for type-safe view references',
            'livedata': 'LiveData for observable data',
            'coroutines': 'Kotlin Coroutines for async operations',
            'room_database': 'Room persistence library',
            'dagger_hilt': 'Dependency injection',
            'navigation': 'Navigation Component',
            'recyclerview': 'RecyclerView for lists',
            'retrofit': 'Retrofit for network operations',
            'work_manager': 'WorkManager for background tasks'
        }
        
        formatted = []
        for feature in features:
            desc = feature_descriptions.get(feature, feature)
            formatted.append(f"- **{feature.replace('_', ' ').title()}**: {desc}")
        
        return '\n'.join(formatted) if formatted else '- Modern Android development'
    
    def _get_project_structure(self, project_name: str) -> str:
        """Get formatted project structure for README"""
        return f"""{project_name}/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/com/terry/{project_name.lower()}/
│   │       └── MainActivity.java
│   └── res/
│       ├── layout/
│       │   └── activity_main.xml
│       ├── values/
│       │   └── strings.xml
│       └── drawable/
│           └── ic_launcher.xml
├── gradle/
│   └── wrapper/
├── build.gradle.kts
├── settings.gradle.kts
└── README.md"""
    
    def _validate_project_config(self, config: Dict[str, Any]) -> bool:
        """Validate project configuration"""
        required_fields = ['name', 'package_name', 'app_type']
        
        for field in required_fields:
            if not config.get(field):
                logger.error(f"Missing required field: {field}")
                return False
        
        # Validate package name format
        package = config['package_name']
        if not package.count('.') >= 2:
            logger.error(f"Invalid package name format: {package}")
            return False
        
        return True
    
    def _get_basic_template(self) -> Dict[str, str]:
        """Get basic Android project template"""
        return {
            'MainActivity': '''package {package_name};

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;
import android.widget.Button;
import android.widget.TextView;
import android.view.View;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        TextView textView = findViewById(R.id.textView);
        Button button = findViewById(R.id.button);
        
        button.setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                textView.setText("Hello from {class_name}!");
            }}
        }});
    }}
}}''',
            'activity_main': '''<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Welcome to {app_name}!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Me!"
        android:layout_marginTop="32dp"
        app:layout_constraintTop_toBottomOf="@id/textView"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>''',
            'strings': '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{app_name}</string>
</resources>''',
            'settings_gradle': '''
// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    compileSdk 34
    defaultConfig {{
        applicationId "{package_name}"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
        
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }}
    
    buildFeatures {{
        viewBinding true
        dataBinding true
    }}
    
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }}
    
    kotlinOptions {{
        jvmTarget = '17'
    }}
    
    dependencies {{
        implementation 'androidx.core:core-ktx:1.12.0'
        implementation 'androidx.appcompat:appcompat:1.6.1'
        implementation 'com.google.android.material:material:1.10.0'
        implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
        implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.2'
        implementation 'androidx.lifecycle:lifecycle-livedata-ktx:2.6.2'
        
        testImplementation 'junit:junit:4.13.2'
        androidTestImplementation 'androidx.test.ext:junit:1.1.5'
        androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
    }}
}}'''
        }
    
    def _get_mvvm_template(self) -> Dict[str, str]:
        """Get MVVM template with LiveData and ViewModel"""
        # Implementation would include MVVM architecture
        return self._get_basic_template()
    
    def _get_compose_template(self) -> Dict[str, str]:
        """Get Jetpack Compose template"""
        # Implementation would include Jetpack Compose
        return self._get_basic_template()
    
    def _get_kmp_template(self) -> Dict[str, str]:
        """Get Kotlin Multiplatform template"""
        # Implementation would include KMP structure
        return self._get_basic_template()