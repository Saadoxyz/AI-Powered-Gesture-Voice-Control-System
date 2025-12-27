"""
UI Styling Module - Premium Modern Design with Glassmorphism
"""


class AppStyles:
    """Premium application styling with modern glassmorphism effects"""
    
    # Spacing values
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
    }
    
    # Border radius
    RADIUS = {
        'sm': 8,
        'md': 12,
        'lg': 16,
        'xl': 20,
    }
    
    # Premium Color Palette - Modern Dark Theme
    COLORS = {
        # Primary colors - Modern gradient
        'primary': '#7c3aed',           # Purple
        'primary_hover': '#6d28d9',
        'secondary': '#06b6d4',         # Cyan
        'accent': '#14b8a6',            # Teal
        
        # Status colors - Vibrant
        'success': '#10b981',           # Emerald
        'warning': '#f59e0b',           # Amber
        'danger': '#ef4444',            # Red
        'info': '#0ea5e9',              # Sky Blue
        
        # Backgrounds - Premium dark
        'bg_main': '#0f172a',           # Very dark blue
        'bg_card': '#1e293b',           # Dark card
        'bg_hover': '#334155',          # Hover state
        'bg_secondary': '#1a2c40',      # Secondary dark
        
        # Text - Excellent contrast
        'text_primary': '#f8fafc',      # Almost white
        'text_secondary': '#cbd5e1',    # Light gray
        'text_muted': '#94a3b8',        # Muted gray
        
        # Borders & Dividers
        'border': '#475569',
        'border_active': '#7c3aed',
        'border_light': '#334155',
        
        # Special
        'gradient_start': '#7c3aed',
        'gradient_end': '#06b6d4',
        'gradient_alt_start': '#0ea5e9',
        'gradient_alt_end': '#06b6d4',
    }
    
    @classmethod
    def get_main_window_style(cls):
        """Main window with gradient background"""
        return f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0e27, stop:1 #1a1f3a);
            }}
            QWidget {{
                background: transparent;
                color: {cls.COLORS['text_primary']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """
    
    @classmethod
    def get_card_style(cls):
        """Modern card with glassmorphism"""
        return f"""
            QFrame {{
                background: rgba(26, 31, 58, 0.7);
                border: 1px solid rgba(99, 102, 241, 0.3);
                border-radius: 16px;
                padding: 20px;
            }}
        """
    
    @classmethod
    def get_button_primary(cls):
        """Primary action button"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {cls.COLORS['primary']}, stop:1 {cls.COLORS['secondary']});
                color: white;
                border: none;
                border-radius: 12px;
                padding: 14px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {cls.COLORS['primary_hover']}, stop:1 {cls.COLORS['secondary']});
            }}
            QPushButton:pressed {{
                background: {cls.COLORS['primary_hover']};
            }}
            QPushButton:disabled {{
                background: {cls.COLORS['bg_hover']};
                color: {cls.COLORS['text_muted']};
            }}
        """
    
    @classmethod
    def get_button_success(cls):
        """Success button"""
        return f"""
            QPushButton {{
                background: {cls.COLORS['success']};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 14px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background: #059669;
            }}
            QPushButton:pressed {{
                background: #047857;
            }}
            QPushButton:disabled {{
                background: {cls.COLORS['bg_hover']};
                color: {cls.COLORS['text_muted']};
            }}
        """
    
    @classmethod
    def get_button_danger(cls):
        """Danger button"""
        return f"""
            QPushButton {{
                background: {cls.COLORS['danger']};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 14px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background: #dc2626;
            }}
            QPushButton:pressed {{
                background: #b91c1c;
            }}
        """
    
    @classmethod
    def get_button_mode(cls, is_active=False):
        """Mode selection button"""
        if is_active:
            return f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {cls.COLORS['primary']}, stop:1 {cls.COLORS['secondary']});
                    color: white;
                    border: 2px solid {cls.COLORS['primary']};
                    border-radius: 10px;
                    padding: 12px;
                    font-size: 13px;
                    font-weight: 600;
                    min-height: 40px;
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background: {cls.COLORS['bg_card']};
                    color: {cls.COLORS['text_secondary']};
                    border: 2px solid {cls.COLORS['border']};
                    border-radius: 10px;
                    padding: 12px;
                    font-size: 13px;
                    font-weight: 600;
                    min-height: 40px;
                }}
                QPushButton:hover {{
                    border-color: {cls.COLORS['primary']};
                    color: {cls.COLORS['text_primary']};
                    background: {cls.COLORS['bg_hover']};
                }}
            """
    
    @classmethod
    def get_label_header(cls):
        """Large header text"""
        return f"""
            QLabel {{
                color: {cls.COLORS['text_primary']};
                font-size: 28px;
                font-weight: 700;
                background: transparent;
            }}
        """
    
    @classmethod
    def get_label_title(cls):
        """Section title"""
        return f"""
            QLabel {{
                color: {cls.COLORS['text_primary']};
                font-size: 16px;
                font-weight: 700;
                background: transparent;
            }}
        """
    
    @classmethod
    def get_label_normal(cls):
        """Normal text"""
        return f"""
            QLabel {{
                color: {cls.COLORS['text_primary']};
                font-size: 13px;
                background: transparent;
            }}
        """
    
    @classmethod
    def get_label_secondary(cls):
        """Secondary text"""
        return f"""
            QLabel {{
                color: {cls.COLORS['text_secondary']};
                font-size: 12px;
                background: transparent;
            }}
        """
    
    @classmethod
    def get_status_online(cls):
        """Online status indicator"""
        return f"""
            QLabel {{
                background: {cls.COLORS['success']};
                color: white;
                border-radius: 14px;
                padding: 6px 16px;
                font-size: 12px;
                font-weight: 600;
            }}
        """
    
    @classmethod
    def get_status_offline(cls):
        """Offline status indicator"""
        return f"""
            QLabel {{
                background: {cls.COLORS['bg_hover']};
                color: {cls.COLORS['text_muted']};
                border-radius: 14px;
                padding: 6px 16px;
                font-size: 12px;
                font-weight: 600;
            }}
        """
    
    @classmethod
    def get_video_widget(cls):
        """Video display area"""
        return f"""
            QLabel {{
                background: {cls.COLORS['bg_main']};
                border: 2px solid rgba(99, 102, 241, 0.3);
                border-radius: 16px;
            }}
        """
    
    @classmethod
    def get_stat_card(cls):
        """Statistics card"""
        return f"""
            QFrame {{
                background: rgba(99, 102, 241, 0.1);
                border: 1px solid rgba(99, 102, 241, 0.3);
                border-radius: 12px;
                padding: 16px;
            }}
        """
    
    @classmethod
    def get_text_edit(cls):
        """Text edit / log area"""
        return f"""
            QTextEdit {{
                background: {cls.COLORS['bg_main']};
                color: {cls.COLORS['text_primary']};
                border: 1px solid {cls.COLORS['border']};
                border-radius: 12px;
                padding: 12px;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 8px;
            }}
            QScrollBar::handle:vertical {{
                background: {cls.COLORS['border']};
                border-radius: 4px;
            }}
        """
    
    @classmethod
    def get_scroll_area(cls):
        """Scroll area styling"""
        return f"""
            QScrollArea {{
                background: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 8px;
            }}
            QScrollBar::handle:vertical {{
                background: {cls.COLORS['border']};
                border-radius: 4px;
            }}
        """
    
    @classmethod
    def get_gesture_display(cls):
        """Large gesture name display"""
        return f"""
            QLabel {{
                color: {cls.COLORS['primary']};
                font-size: 32px;
                font-weight: 700;
                background: transparent;
            }}
        """