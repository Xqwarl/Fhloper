"""Smali Modifier - Modifies smali bytecode to inject subscription table"""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class SmaliModifier:
    """Modifies smali files to inject subscription table functionality"""
    
    def inject_subscription_table(self, smali_file: Path, subscription_link: str, 
                                 title: str, branding: str):
        """Inject subscription table into main activity smali file"""
        
        try:
            with open(smali_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add import statements
            content = self._add_imports(content)
            
            # Inject table initialization method
            content = self._inject_table_method(content, subscription_link, title, branding)
            
            # Hook into onCreate or onResume
            content = self._hook_lifecycle(content)
            
            with open(smali_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Successfully modified {smali_file.name}")
            
        except Exception as e:
            logger.error(f"Error modifying smali file: {e}")
            raise
    
    def _add_imports(self, content: str) -> str:
        """Add necessary imports to smali file"""
        
        imports = [
            "android/widget/LinearLayout",
            "android/widget/Button",
            "android/widget/TextView",
            "android/view/ViewGroup",
            "android/content/Intent",
            "android/net/Uri",
            "android/graphics/Color",
            "android/view/Gravity",
        ]
        
        for imp in imports:
            import_line = f"L{imp};"
            if import_line not in content:
                # Add before .class definition
                content = content.replace(
                    ".class ",
                    f"# Injected imports\n# {import_line}\n.class ",
                    1
                )
        
        return content
    
    def _inject_table_method(self, content: str, subscription_link: str, 
                            title: str, branding: str) -> str:
        """Inject table initialization method into smali"""
        
        # Escape special characters for smali format
        link_escaped = subscription_link.replace('/', '\\/')
        title_escaped = title.replace('"', '\\"')
        branding_escaped = branding.replace('"', '\\"')
        
        table_method = f'''
# Subscription Table Method
.method public initSubscriptionTable(Landroid/view/ViewGroup;)V
    .registers 5
    .param p1, "container"    # Landroid/view/ViewGroup;

    new-instance v0, Landroid/widget/LinearLayout;
    invoke-direct {{v0, p0}}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V
    
    const/0 v1, 0x1
    invoke-virtual {{v0, v1}}, Landroid/widget/LinearLayout;->setOrientation(I)V
    
    const v2, -0x252526
    invoke-virtual {{v0, v2}}, Landroid/widget/LinearLayout;->setBackgroundColor(I)V

    # Create header
    new-instance v3, Landroid/widget/LinearLayout;
    invoke-direct {{v3, p0}}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V
    invoke-virtual {{v3, v1}}, Landroid/widget/LinearLayout;->setOrientation(I)V
    invoke-virtual {{v3, v2}}, Landroid/widget/LinearLayout;->setBackgroundColor(I)V

    # Create title TextView
    new-instance v4, Landroid/widget/TextView;
    invoke-direct {{v4, p0}}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V
    const-string v2, "{title_escaped}"
    invoke-virtual {{v4, v2}}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V
    const/high16 v2, 0x41c00000
    invoke-virtual {{v4, v2}}, Landroid/widget/TextView;->setTextSize(F)V
    const v2, -0x151516
    invoke-virtual {{v4, v2}}, Landroid/widget/TextView;->setTextColor(I)V

    invoke-virtual {{v3, v4}}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V
    invoke-virtual {{v0, v3}}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    # Create subscribe button
    new-instance v2, Landroid/widget/Button;
    invoke-direct {{v2, p0}}, Landroid/widget/Button;-><init>(Landroid/content/Context;)V
    const-string v3, "📲 Подписаться"
    invoke-virtual {{v2, v3}}, Landroid/widget/Button;->setText(Ljava/lang/CharSequence;)V
    const v3, -0x16baa
    invoke-virtual {{v2, v3}}, Landroid/widget/Button;->setBackgroundColor(I)V
    
    # Store link as tag for click listener
    const-string v3, "{link_escaped}"
    invoke-virtual {{v2, v3}}, Landroid/widget/Button;->setTag(Ljava/lang/Object;)V

    invoke-virtual {{p1, v0}}, Landroid/view/ViewGroup;->addView(Landroid/view/View;)V

    return-void
.end method
'''
        
        # Find the end of class and insert method before it
        if ".end class" in content:
            content = content.replace(
                ".end class",
                f"{table_method}\n.end class",
                1
            )
        
        return content
    
    def _hook_lifecycle(self, content: str) -> str:
        """Hook into onCreate or onResume to initialize table"""
        
        # Look for onCreate method
        if ".method protected onCreate" in content:
            # Find the invoke-super line and add our initialization after
            content = re.sub(
                r'(invoke-super.*?onCreate)',
                r'\1\n    # Initialize subscription table\n    const/4 v0, 0x0\n    # Table initialization would go here',
                content,
                count=1
            )
        
        return content
    
    def modify_smali_from_zip(self, zip_path: Path, subscription_link: str,
                             title: str, branding: str) -> bytes:
        """Modify smali files from extracted zip (from smali12.zip)"""
        
        import zipfile
        import io
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Read all smali files
                modified_files = {}
                
                for file_info in zip_ref.filelist:
                    if file_info.filename.endswith('.smali'):
                        content = zip_ref.read(file_info.filename).decode('utf-8')
                        
                        # Apply modifications
                        content = self._patch_smali_content(
                            content,
                            subscription_link,
                            title,
                            branding
                        )
                        
                        modified_files[file_info.filename] = content
                
                # Create new zip with modified files
                output = io.BytesIO()
                with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as output_zip:
                    for file_info in zip_ref.filelist:
                        if file_info.filename in modified_files:
                            output_zip.writestr(
                                file_info.filename,
                                modified_files[file_info.filename].encode('utf-8')
                            )
                        else:
                            output_zip.writestr(
                                file_info.filename,
                                zip_ref.read(file_info.filename)
                            )
                
                return output.getvalue()
        
        except Exception as e:
            logger.error(f"Error modifying smali zip: {e}")
            raise
    
    def _patch_smali_content(self, content: str, subscription_link: str,
                            title: str, branding: str) -> str:
        """Apply patches to smali content"""
        
        # Replace placeholder values
        content = content.replace('PLACEHOLDER_LINK', subscription_link)
        content = content.replace('PLACEHOLDER_TITLE', title)
        content = content.replace('PLACEHOLDER_BRANDING', branding)
        content = content.replace('PLACEHOLDER_IZIAPK', '@ApkVzlomers')
        
        # Remove icon references (empty string replacement)
        content = re.sub(r'drawable/ic_.*?[,;)]', '', content)
        
        return content
