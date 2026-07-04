"""Table Generator - Creates styled subscription table layout"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class TableGenerator:
    """Generates subscription table layout with custom styling"""
    
    # Colors based on the design in photo_2026-07-04_23-44-22.jpg
    COLORS = {
        'background': '#1a1a2e',      # Dark blue-black
        'header': '#16213e',           # Darker blue
        'text_primary': '#eaeaea',     # Light gray
        'text_secondary': '#a0a0a0',   # Medium gray
        'button': '#e94560',           # Red accent
        'button_hover': '#d63447',     # Darker red
        'border': '#2a2a4e',           # Dark blue border
    }
    
    def __init__(self):
        self.colors = self.COLORS
    
    def generate_table_xml(self, subscription_link: str, title: str, branding: str) -> str:
        """Generate table XML layout"""
        
        xml = f'''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:background="{self.COLORS['background']}"
    android:padding="16dp">

    <!-- Header -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:background="{self.COLORS['header']}"
        android:padding="20dp"
        android:gravity="center">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="{title}"
            android:textSize="24sp"
            android:textColor="{self.COLORS['text_primary']}"
            android:textStyle="bold"
            android:gravity="center"
            android:layout_marginBottom="8dp" />

        <View
            android:layout_width="60dp"
            android:layout_height="3dp"
            android:background="{self.COLORS['button']}" />

    </LinearLayout>

    <!-- Table Content -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:layout_marginTop="12dp">

        <!-- Row 1 -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:background="{self.COLORS['border']}"
            android:padding="12dp">

            <TextView
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="Сборка"
                android:textColor="{self.COLORS['text_secondary']}"
                android:textSize="13sp" />

            <TextView
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="Статус"
                android:textColor="{self.COLORS['text_secondary']}"
                android:textSize="13sp"
                android:gravity="end" />

        </LinearLayout>

        <!-- Row 2 -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:background="{self.COLORS['background']}"
            android:padding="12dp">

            <TextView
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="{branding}"
                android:textColor="{self.COLORS['text_primary']}"
                android:textSize="14sp"
                android:textStyle="bold" />

            <TextView
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="✓ Активна"
                android:textColor="#4CAF50"
                android:textSize="14sp"
                android:textStyle="bold"
                android:gravity="end" />

        </LinearLayout>

    </LinearLayout>

    <!-- Subscription Button -->
    <Button
        android:id="@+id/btn_subscribe"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:layout_marginTop="16dp"
        android:text="📲 Подписаться"
        android:textColor="{self.COLORS['text_primary']}"
        android:textSize="16sp"
        android:textStyle="bold"
        android:background="{self.COLORS['button']}"
        android:tag="{subscription_link}" />

</LinearLayout>
'''
        return xml
    
    def generate_table_java(self, subscription_link: str, title: str, branding: str) -> str:
        """Generate Java code snippet for table initialization"""
        
        java_code = f'''
// Subscribe Table Initialization
public void initSubscriptionTable(ViewGroup container) {{
    LinearLayout tableLayout = new LinearLayout(this);
    tableLayout.setOrientation(LinearLayout.VERTICAL);
    tableLayout.setBackgroundColor(Color.parseColor("{self.COLORS['background']}"));
    tableLayout.setPadding(16, 16, 16, 16);

    // Header
    LinearLayout header = new LinearLayout(this);
    header.setOrientation(LinearLayout.VERTICAL);
    header.setBackgroundColor(Color.parseColor("{self.COLORS['header']}"));
    header.setPadding(20, 20, 20, 20);
    header.setGravity(Gravity.CENTER);

    TextView title = new TextView(this);
    title.setText("{title}");
    title.setTextSize(24);
    title.setTextColor(Color.parseColor("{self.COLORS['text_primary']}"));
    title.setTypeface(null, android.graphics.Typeface.BOLD);
    title.setGravity(Gravity.CENTER);
    header.addView(title);

    tableLayout.addView(header);

    // Subscribe Button
    Button subscribeBtn = new Button(this);
    subscribeBtn.setText("📲 Подписаться");
    subscribeBtn.setTextColor(Color.parseColor("{self.COLORS['text_primary']}"));
    subscribeBtn.setBackgroundColor(Color.parseColor("{self.COLORS['button']}"));
    subscribeBtn.setOnClickListener(v -> {{
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.setData(Uri.parse("{subscription_link}"));
        startActivity(intent);
    }});

    LinearLayout.LayoutParams btnParams = new LinearLayout.LayoutParams(
        LinearLayout.LayoutParams.MATCH_PARENT,
        48
    );
    btnParams.setMargins(0, 16, 0, 0);
    tableLayout.addView(subscribeBtn, btnParams);

    container.addView(tableLayout);
}}
'''
        return java_code
    
    def get_color_resources(self) -> str:
        """Generate colors.xml resource file"""
        
        xml = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Theme Colors -->
    <color name="table_background">#1a1a2e</color>
    <color name="table_header">#16213e</color>
    <color name="table_text_primary">#eaeaea</color>
    <color name="table_text_secondary">#a0a0a0</color>
    <color name="table_button">#e94560</color>
    <color name="table_button_hover">#d63447</color>
    <color name="table_border">#2a2a4e</color>
    <color name="table_status_active">#4CAF50</color>
</resources>
'''
        return xml
