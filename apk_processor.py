"""APK Processing Module - Embeds subscription table into APK files"""

import os
import shutil
import logging
import subprocess
import zipfile
from pathlib import Path
from datetime import datetime
from xml.dom import minidom

from config import config
from table_generator import TableGenerator
from smali_modifier import SmaliModifier

logger = logging.getLogger(__name__)


class APKProcessor:
    """Main APK processing class"""
    
    def __init__(self):
        self.apktool = config.APKTOOL_PATH
        self.work_dir = Path(config.WORK_DIR)
        self.output_dir = Path(config.OUTPUT_DIR)
        self.table_gen = TableGenerator()
        self.smali_mod = SmaliModifier()
        
    async def process_apk(self, input_path: str, subscription_link: str, 
                         title: str, branding: str) -> str:
        """
        Process APK file:
        1. Decompile with apktool
        2. Modify smali files with table
        3. Add subscription link
        4. Recompile APK
        5. Sign APK
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"APK file not found: {input_path}")
        
        # Create unique work directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        work_apk_dir = self.work_dir / f"apk_{timestamp}"
        work_apk_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Step 1: Decompile APK
            logger.info(f"Decompiling {input_path.name}...")
            decompile_dir = work_apk_dir / "decompiled"
            self._decompile_apk(input_path, decompile_dir)
            
            # Step 2: Modify smali files with table
            logger.info("Modifying smali files...")
            self._inject_table(decompile_dir, subscription_link, title, branding)
            
            # Step 3: Generate new resources if needed
            self._update_resources(decompile_dir, title)
            
            # Step 4: Recompile APK
            logger.info("Recompiling APK...")
            unsigned_apk = work_apk_dir / "unsigned.apk"
            self._recompile_apk(decompile_dir, unsigned_apk)
            
            # Step 5: Sign APK
            logger.info("Signing APK...")
            output_apk = self.output_dir / f"{input_path.stem}_modified_{timestamp}.apk"
            self._sign_apk(unsigned_apk, output_apk)
            
            logger.info(f"Successfully processed: {output_apk}")
            return str(output_apk)
            
        except Exception as e:
            logger.error(f"Error processing APK: {e}")
            raise
        
        finally:
            # Cleanup work directory
            if work_apk_dir.exists():
                shutil.rmtree(work_apk_dir, ignore_errors=True)
    
    def _decompile_apk(self, apk_path: Path, output_dir: Path):
        """Decompile APK using apktool"""
        cmd = [
            self.apktool, "d", "-f", "-r",
            str(apk_path),
            "-o", str(output_dir)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"apktool decompile failed: {result.stderr}")
    
    def _inject_table(self, decompile_dir: Path, subscription_link: str, 
                     title: str, branding: str):
        """Inject subscription table into smali files"""
        # Find MainActivity or main activity
        smali_dir = decompile_dir / "smali"
        
        if not smali_dir.exists():
            # Try different smali directory names
            for d in decompile_dir.iterdir():
                if d.is_dir() and d.name.startswith("smali"):
                    smali_dir = d
                    break
        
        # Find main activity file
        main_activity = self._find_main_activity(smali_dir)
        
        if main_activity:
            # Modify the activity
            self.smali_mod.inject_subscription_table(
                main_activity,
                subscription_link=subscription_link,
                title=title,
                branding=branding
            )
            logger.info(f"Injected table into {main_activity}")
        else:
            logger.warning("Main activity not found")
    
    def _find_main_activity(self, smali_dir: Path) -> Path:
        """Find main activity smali file"""
        manifest_path = smali_dir.parent / "AndroidManifest.xml"
        
        if manifest_path.exists():
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Look for MAIN action
                    if 'android.intent.action.MAIN' in content:
                        # Parse package and activity name
                        import re
                        package_match = re.search(r'package="([^"]+)"', content)
                        activity_match = re.search(
                            r'<activity[^>]+android:name="([^"]+)"[^>]*>.*?'
                            r'<action android:name="android.intent.action.MAIN"',
                            content,
                            re.DOTALL
                        )
                        
                        if package_match and activity_match:
                            package = package_match.group(1)
                            activity = activity_match.group(1)
                            
                            # Convert to path
                            if activity.startswith('.'):
                                activity = package + activity
                            
                            activity_path = activity.replace('.', '/')
                            smali_file = smali_dir / f"{activity_path}.smali"
                            
                            if smali_file.exists():
                                return smali_file
            except Exception as e:
                logger.warning(f"Error parsing manifest: {e}")
        
        # Fallback: find any MainActivity.smali
        for smali_file in smali_dir.rglob("MainActivity.smali"):
            return smali_file
        
        # Fallback: find any *Activity.smali in root package
        for smali_file in smali_dir.glob("**/MainActivity.smali"):
            return smali_file
        
        return None
    
    def _update_resources(self, decompile_dir: Path, title: str):
        """Update resource files (strings, colors, etc.)"""
        res_dir = decompile_dir / "res"
        
        if not res_dir.exists():
            return
        
        # Update strings.xml
        for strings_file in res_dir.rglob("strings.xml"):
            try:
                self._update_strings_xml(strings_file, title)
            except Exception as e:
                logger.warning(f"Error updating {strings_file}: {e}")
    
    def _update_strings_xml(self, strings_file: Path, title: str):
        """Update strings.xml with new title"""
        try:
            dom = minidom.parse(str(strings_file))
            
            # Add custom strings if needed
            root = dom.documentElement
            
            # Check if title string exists
            title_found = False
            for elem in root.getElementsByTagName('string'):
                if elem.getAttribute('name') in ['app_name', 'title']:
                    elem.firstChild.nodeValue = title
                    title_found = True
            
            # Save
            with open(strings_file, 'w', encoding='utf-8') as f:
                dom.writexml(f, encoding='utf-8')
                
        except Exception as e:
            logger.warning(f"Could not modify strings.xml: {e}")
    
    def _recompile_apk(self, decompile_dir: Path, output_apk: Path):
        """Recompile APK using apktool"""
        cmd = [
            self.apktool, "b",
            str(decompile_dir),
            "-o", str(output_apk)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"apktool build failed: {result.stderr}")
    
    def _sign_apk(self, unsigned_apk: Path, signed_apk: Path):
        """Sign APK with debug key"""
        # For production, you'd use a proper keystore
        # This uses the default debug key
        
        cmd = [
            "jarsigner",
            "-verbose",
            "-sigalg", "SHA1withRSA",
            "-digestalg", "SHA1",
            "-keystore", str(self._get_debug_keystore()),
            "-storepass", "android",
            "-keypass", "android",
            str(unsigned_apk),
            "androiddebugkey"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # Try alternative: use zipalign
            self._zipalign_apk(unsigned_apk, signed_apk)
            return
        
        # Align with zipalign
        self._zipalign_apk(unsigned_apk, signed_apk)
    
    def _zipalign_apk(self, input_apk: Path, output_apk: Path):
        """Align APK with zipalign"""
        cmd = [
            "zipalign",
            "-v", "4",
            str(input_apk),
            str(output_apk)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # If zipalign fails, just copy
            shutil.copy(input_apk, output_apk)
    
    def _get_debug_keystore(self) -> Path:
        """Get path to debug keystore"""
        keystore = Path.home() / ".android" / "debug.keystore"
        return keystore
