"""
Basic Framebuffer Graphics Test for ST7701 Display
Simple graphics without LVGL - pure MicroPython
"""

import machine
import time
import math
from machine import Pin, SPI, I2C

# Display configuration
DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 480

# Pin configuration 
PINS = {
    'backlight': 38,
    'cs': 39,
    'sck': 48,
    'mosi': 47,
    'de': 18,
    'vsync': 17,
    'hsync': 16,
    'pclk': 21,
    'r': [11, 12, 13, 14, 0],
    'g': [8, 20, 3, 46, 9, 10],
    'b': [4, 5, 6, 7, 15],
}

class RGB565Color:
    """RGB565 color utilities"""
    BLACK = 0x0000
    WHITE = 0xFFFF
    RED = 0xF800
    GREEN = 0x07E0
    BLUE = 0x001F
    YELLOW = 0xFFE0
    CYAN = 0x07FF
    MAGENTA = 0xF81F
    
    @staticmethod
    def rgb(r, g, b):
        """Convert RGB888 to RGB565"""
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

class SimpleFrameBuffer:
    """Basic framebuffer for ST7701 display"""
    
    def __init__(self, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT):
        self.width = width
        self.height = height
        
        # Initialize hardware
        self.init_hardware()
        
        # Create framebuffer (16-bit RGB565)
        self.buffer_size = width * height * 2  # 2 bytes per pixel
        self.buffer = bytearray(self.buffer_size)
        
        print(f"Framebuffer initialized: {width}x{height} ({self.buffer_size} bytes)")
    
    def init_hardware(self):
        """Initialize display hardware"""
        
        # Backlight
        self.backlight = Pin(PINS['backlight'], Pin.OUT)
        self.backlight.on()
        
        # SPI for commands
        self.spi = SPI(2,
                      baudrate=20000000,
                      sck=Pin(PINS['sck']),
                      mosi=Pin(PINS['mosi']))
        
        self.cs = Pin(PINS['cs'], Pin.OUT)
        self.cs.on()
        
        # RGB control signals
        self.de = Pin(PINS['de'], Pin.OUT)
        self.vsync = Pin(PINS['vsync'], Pin.OUT)
        self.hsync = Pin(PINS['hsync'], Pin.OUT)
        self.pclk = Pin(PINS['pclk'], Pin.OUT)
        
        # Initialize display controller
        self.init_st7701()
    
    def init_st7701(self):
        """Initialize ST7701 display controller"""
        
        def send_cmd(cmd, data=None):
            self.cs.off()
            self.spi.write(bytes([cmd]))
            if data:
                self.spi.write(bytes(data))
            self.cs.on()
        
        # Basic initialization sequence
        send_cmd(0x01)  # Software reset
        time.sleep_ms(150)
        
        send_cmd(0x11)  # Sleep out
        time.sleep_ms(150)
        
        # Interface pixel format: 16-bit/pixel
        send_cmd(0x3A, [0x55])
        
        # Memory access control
        send_cmd(0x36, [0x00])
        
        # Column address set
        send_cmd(0x2A, [0x00, 0x00, 0x01, 0xDF])  # 0-479
        
        # Page address set  
        send_cmd(0x2B, [0x00, 0x00, 0x01, 0xDF])  # 0-479
        
        # Display on
        send_cmd(0x29)
        time.sleep_ms(50)
        
        print("ST7701 initialized")
    
    def set_pixel(self, x, y, color):
        """Set a single pixel in the framebuffer"""
        if 0 <= x < self.width and 0 <= y < self.height:
            pos = (y * self.width + x) * 2
            self.buffer[pos] = (color >> 8) & 0xFF     # High byte
            self.buffer[pos + 1] = color & 0xFF        # Low byte
    
    def get_pixel(self, x, y):
        """Get pixel color from framebuffer"""
        if 0 <= x < self.width and 0 <= y < self.height:
            pos = (y * self.width + x) * 2
            return (self.buffer[pos] << 8) | self.buffer[pos + 1]
        return 0
    
    def fill(self, color):
        """Fill entire framebuffer with color"""
        high_byte = (color >> 8) & 0xFF
        low_byte = color & 0xFF
        
        for i in range(0, self.buffer_size, 2):
            self.buffer[i] = high_byte
            self.buffer[i + 1] = low_byte
    
    def fill_rect(self, x, y, w, h, color):
        """Fill rectangle with color"""
        for py in range(y, min(y + h, self.height)):
            for px in range(x, min(x + w, self.width)):
                self.set_pixel(px, py, color)
    
    def draw_line(self, x0, y0, x1, y1, color):
        """Draw line using Bresenham's algorithm"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            self.set_pixel(x0, y0, color)
            
            if x0 == x1 and y0 == y1:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
    
    def draw_circle(self, cx, cy, r, color):
        """Draw circle outline"""
        x = r
        y = 0
        err = 0
        
        while x >= y:
            self.set_pixel(cx + x, cy + y, color)
            self.set_pixel(cx + y, cy + x, color)
            self.set_pixel(cx - y, cy + x, color)
            self.set_pixel(cx - x, cy + y, color)
            self.set_pixel(cx - x, cy - y, color)
            self.set_pixel(cx - y, cy - x, color)
            self.set_pixel(cx + y, cy - x, color)
            self.set_pixel(cx + x, cy - y, color)
            
            if err <= 0:
                y += 1
                err += 2 * y + 1
            
            if err > 0:
                x -= 1
                err -= 2 * x + 1
    
    def draw_text(self, x, y, text, color, size=1):
        """Draw simple text (basic 8x8 font)"""
        # Simple 8x8 bitmap font for basic characters
        font_8x8 = {
            'A': [0x3C, 0x66, 0x66, 0x7E, 0x66, 0x66, 0x66, 0x00],
            'B': [0x7C, 0x66, 0x66, 0x7C, 0x66, 0x66, 0x7C, 0x00],
            'C': [0x3C, 0x66, 0x60, 0x60, 0x60, 0x66, 0x3C, 0x00],
            'D': [0x78, 0x6C, 0x66, 0x66, 0x66, 0x6C, 0x78, 0x00],
            'E': [0x7E, 0x60, 0x60, 0x7C, 0x60, 0x60, 0x7E, 0x00],
            'H': [0x66, 0x66, 0x66, 0x7E, 0x66, 0x66, 0x66, 0x00],
            'L': [0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x7E, 0x00],
            'O': [0x3C, 0x66, 0x66, 0x66, 0x66, 0x66, 0x3C, 0x00],
            'T': [0x7E, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x00],
            ' ': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        }
        
        char_x = x
        for char in text.upper():
            if char in font_8x8:
                bitmap = font_8x8[char]
                for row in range(8):
                    byte = bitmap[row]
                    for col in range(8):
                        if byte & (0x80 >> col):
                            for sy in range(size):
                                for sx in range(size):
                                    self.set_pixel(char_x + col * size + sx, 
                                                 y + row * size + sy, color)
            char_x += 8 * size
    
    def update_display(self):
        """Send framebuffer to display (simplified)"""
        # In a real implementation, this would send the framebuffer data
        # to the display via the RGB interface or DMA
        print("Framebuffer update (simplified)")
        
        # For demonstration, just toggle some control signals
        self.vsync.off()
        time.sleep_us(10)
        self.vsync.on()

class GraphicsTest:
    """Graphics demonstration"""
    
    def __init__(self):
        self.fb = SimpleFrameBuffer()
        self.colors = [
            RGB565Color.RED, RGB565Color.GREEN, RGB565Color.BLUE,
            RGB565Color.YELLOW, RGB565Color.CYAN, RGB565Color.MAGENTA,
            RGB565Color.WHITE
        ]
    
    def test_basic_shapes(self):
        """Test basic shape drawing"""
        print("\n--- Testing Basic Shapes ---")
        
        # Clear screen
        self.fb.fill(RGB565Color.BLACK)
        
        # Draw rectangles
        self.fb.fill_rect(50, 50, 100, 80, RGB565Color.RED)
        self.fb.fill_rect(200, 50, 100, 80, RGB565Color.GREEN)
        self.fb.fill_rect(350, 50, 100, 80, RGB565Color.BLUE)
        
        # Draw lines
        self.fb.draw_line(0, 200, 479, 200, RGB565Color.WHITE)
        self.fb.draw_line(240, 0, 240, 479, RGB565Color.WHITE)
        
        # Draw circles
        self.fb.draw_circle(120, 300, 50, RGB565Color.YELLOW)
        self.fb.draw_circle(240, 300, 70, RGB565Color.CYAN)
        self.fb.draw_circle(360, 300, 60, RGB565Color.MAGENTA)
        
        self.fb.update_display()
        print("✓ Basic shapes drawn")
    
    def test_text_display(self):
        """Test text rendering"""
        print("\n--- Testing Text Display ---")
        
        self.fb.fill(RGB565Color.BLACK)
        
        # Draw text at different sizes
        self.fb.draw_text(50, 50, "HELLO", RGB565Color.WHITE, 2)
        self.fb.draw_text(50, 100, "ESP32", RGB565Color.GREEN, 3)
        self.fb.draw_text(50, 200, "ST7701", RGB565Color.BLUE, 2)
        self.fb.draw_text(50, 250, "DISPLAY", RGB565Color.YELLOW, 1)
        
        self.fb.update_display()
        print("✓ Text displayed")
    
    def test_color_gradient(self):
        """Test color gradient"""
        print("\n--- Testing Color Gradient ---")
        
        # Create horizontal color gradient
        for x in range(self.fb.width):
            r = int((x / self.fb.width) * 31)  # 5-bit red
            color = RGB565Color.rgb(r * 8, 0, 0)  # Scale to 8-bit for conversion
            
            for y in range(100):
                self.fb.set_pixel(x, y + 100, color)
        
        # Create vertical gradient
        for y in range(200, 400):
            g = int(((y - 200) / 200) * 63)  # 6-bit green
            color = RGB565Color.rgb(0, g * 4, 0)  # Scale to 8-bit
            
            for x in range(200):
                self.fb.set_pixel(x + 140, y, color)
        
        self.fb.update_display()
        print("✓ Color gradient created")
    
    def test_animation(self):
        """Test simple animation"""
        print("\n--- Testing Animation ---")
        
        center_x, center_y = 240, 240
        
        for frame in range(30):
            self.fb.fill(RGB565Color.BLACK)
            
            # Rotating circles
            angle = frame * 12  # degrees
            rad = math.radians(angle)
            
            # Calculate positions for orbiting circles
            for i, color in enumerate(self.colors):
                orbit_angle = rad + (i * math.pi / 3)
                x = center_x + int(80 * math.cos(orbit_angle))
                y = center_y + int(80 * math.sin(orbit_angle))
                
                self.fb.draw_circle(x, y, 20, color)
            
            # Center circle
            self.fb.draw_circle(center_x, center_y, 30, RGB565Color.WHITE)
            
            self.fb.update_display()
            time.sleep_ms(100)
        
        print("✓ Animation completed")
    
    def run_all_tests(self):
        """Run all graphics tests"""
        print("="*60)
        print("ST7701 Framebuffer Graphics Test")
        print("No LVGL - Pure MicroPython Implementation")
        print("="*60)
        
        tests = [
            ("Basic Shapes", self.test_basic_shapes),
            ("Text Display", self.test_text_display),
            ("Color Gradient", self.test_color_gradient),
            ("Animation", self.test_animation),
        ]
        
        for test_name, test_func in tests:
            try:
                test_func()
                time.sleep(2)  # Pause between tests
                print(f"✓ {test_name} test completed")
            except Exception as e:
                print(f"✗ {test_name} test failed: {e}")
        
        print("\n" + "="*60)
        print("Graphics test sequence completed!")
        print("="*60)

def main():
    """Main test function"""
    test = GraphicsTest()
    test.run_all_tests()

if __name__ == "__main__":
    main()