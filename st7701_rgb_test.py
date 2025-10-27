"""
ST7701 RGB Interface Test - Proper RGB Parallel Display Driver
This script properly drives the RGB parallel interface of the ST7701
"""

import machine
import time
from machine import Pin, SPI, PWM, Timer
import gc

# Pin configuration for ESP32-S3-4848S040
class ST7701Config:
    # Display control
    BL = 38          # Backlight
    CS = 39          # SPI Chip Select  
    SCK = 48         # SPI Clock
    MOSI = 47        # SPI Data
    
    # RGB Parallel Interface
    DE = 18          # Data Enable
    VSYNC = 17       # Vertical Sync
    HSYNC = 16       # Horizontal Sync  
    PCLK = 21        # Pixel Clock
    
    # RGB Data Lines
    R = [11, 12, 13, 14, 0]      # R0-R4 (5 bits)
    G = [8, 20, 3, 46, 9, 10]    # G0-G5 (6 bits) 
    B = [4, 5, 6, 7, 15]         # B0-B4 (5 bits)
    
    # Display specs
    WIDTH = 480
    HEIGHT = 480

class ST7701Driver:
    def __init__(self):
        self.config = ST7701Config()
        self.width = self.config.WIDTH
        self.height = self.config.HEIGHT
        
        print("Initializing ST7701 RGB Display Driver...")
        
        # Initialize hardware components
        self.init_backlight()
        self.init_spi()
        self.init_rgb_pins()
        self.init_control_pins()
        
        # Initialize display controller
        self.init_display_controller()
        
        print("ST7701 driver initialized successfully")
    
    def init_backlight(self):
        """Initialize backlight with PWM control"""
        self.backlight = PWM(Pin(self.config.BL))
        self.backlight.freq(1000)  # 1kHz PWM
        self.set_brightness(100)   # Full brightness
        print("✓ Backlight initialized")
    
    def set_brightness(self, percent):
        """Set backlight brightness (0-100%)"""
        duty = int(1023 * percent / 100)
        self.backlight.duty(duty)
    
    def init_spi(self):
        """Initialize SPI for display commands"""
        self.spi = SPI(2,
                      baudrate=10000000,
                      polarity=0,
                      phase=0,
                      sck=Pin(self.config.SCK),
                      mosi=Pin(self.config.MOSI))
        
        self.cs = Pin(self.config.CS, Pin.OUT)
        self.cs.on()  # Deselect
        print("✓ SPI initialized")
    
    def init_rgb_pins(self):
        """Initialize RGB data pins"""
        self.rgb_r = [Pin(p, Pin.OUT) for p in self.config.R]
        self.rgb_g = [Pin(p, Pin.OUT) for p in self.config.G] 
        self.rgb_b = [Pin(p, Pin.OUT) for p in self.config.B]
        
        # Initialize all RGB pins to 0
        for pin in self.rgb_r + self.rgb_g + self.rgb_b:
            pin.off()
        
        print("✓ RGB data pins initialized")
    
    def init_control_pins(self):
        """Initialize RGB control signals"""
        self.de = Pin(self.config.DE, Pin.OUT)
        self.vsync = Pin(self.config.VSYNC, Pin.OUT)
        self.hsync = Pin(self.config.HSYNC, Pin.OUT)
        self.pclk = Pin(self.config.PCLK, Pin.OUT)
        
        # Set initial states
        self.de.off()
        self.vsync.on()    # Active low
        self.hsync.on()    # Active low
        self.pclk.off()
        
        print("✓ Control signals initialized")
    
    def send_spi_cmd(self, cmd, data=None):
        """Send command to ST7701 via SPI"""
        self.cs.off()
        self.spi.write(bytes([cmd]))
        if data:
            self.spi.write(bytes(data))
        self.cs.on()
        time.sleep_us(10)
    
    def init_display_controller(self):
        """Initialize ST7701 display controller"""
        print("Initializing ST7701 controller...")
        
        # Hardware reset sequence
        time.sleep_ms(10)
        
        # ST7701 initialization commands
        init_sequence = [
            # Software reset
            (0x01, None, 120),
            
            # Sleep out  
            (0x11, None, 120),
            
            # Interface pixel format (16-bit RGB565)
            (0x3A, [0x55], 10),
            
            # Memory access control
            (0x36, [0x00], 10),
            
            # Display inversion off
            (0x20, None, 10),
            
            # Normal display mode
            (0x13, None, 10),
            
            # Display on
            (0x29, None, 50),
        ]
        
        for cmd_data in init_sequence:
            cmd, data, delay = cmd_data
            self.send_spi_cmd(cmd, data)
            if delay:
                time.sleep_ms(delay)
        
        print("✓ ST7701 controller initialized")
    
    def set_rgb_pixel(self, r5, g6, b5):
        """Set RGB pins for one pixel (5-6-5 bit format)"""
        # Set red bits (5 bits: R4-R0)
        for i in range(5):
            self.rgb_r[i].value((r5 >> i) & 1)
        
        # Set green bits (6 bits: G5-G0)  
        for i in range(6):
            self.rgb_g[i].value((g6 >> i) & 1)
        
        # Set blue bits (5 bits: B4-B0)
        for i in range(5):
            self.rgb_b[i].value((b5 >> i) & 1)
    
    def rgb565_to_components(self, rgb565):
        """Convert RGB565 to 5-6-5 components"""
        r5 = (rgb565 >> 11) & 0x1F  # 5 bits
        g6 = (rgb565 >> 5) & 0x3F   # 6 bits  
        b5 = rgb565 & 0x1F          # 5 bits
        return r5, g6, b5
    
    def send_pixel_clock(self):
        """Generate one pixel clock pulse"""
        self.pclk.on()
        time.sleep_us(1)  # Pixel clock high time
        self.pclk.off()
        time.sleep_us(1)  # Pixel clock low time
    
    def send_hsync_pulse(self):
        """Generate horizontal sync pulse"""
        self.hsync.off()  # Active low
        time.sleep_us(2)  # HSYNC pulse width
        self.hsync.on()
    
    def send_vsync_pulse(self):
        """Generate vertical sync pulse"""
        self.vsync.off()  # Active low
        time.sleep_us(10) # VSYNC pulse width
        self.vsync.on()
    
    def display_color_bars(self):
        """Display color bars across the screen"""
        print("Displaying color bars...")
        
        # Color bar patterns (RGB565 format)
        colors = [
            0xF800,  # Red
            0x07E0,  # Green  
            0x001F,  # Blue
            0xFFE0,  # Yellow
            0x07FF,  # Cyan
            0xF81F,  # Magenta
            0xFFFF,  # White
            0x0000,  # Black
        ]
        
        bar_width = self.width // len(colors)
        
        # Send VSYNC
        self.send_vsync_pulse()
        time.sleep_us(100)
        
        # Generate frame data
        for row in range(self.height):
            # Send HSYNC
            self.send_hsync_pulse()
            time.sleep_us(10)
            
            # Enable data
            self.de.on()
            
            # Send pixel data for this row
            for col in range(self.width):
                color_index = col // bar_width
                if color_index >= len(colors):
                    color_index = len(colors) - 1
                
                color = colors[color_index]
                r5, g6, b5 = self.rgb565_to_components(color)
                
                # Set RGB data
                self.set_rgb_pixel(r5, g6, b5)
                
                # Clock the pixel
                self.send_pixel_clock()
            
            # Disable data
            self.de.off()
            time.sleep_us(5)
        
        print("✓ Color bars displayed")
    
    def display_solid_color(self, rgb565_color):
        """Fill entire display with solid color"""
        r5, g6, b5 = self.rgb565_to_components(rgb565_color)
        
        print(f"Displaying solid color: 0x{rgb565_color:04X}")
        
        # Send VSYNC
        self.send_vsync_pulse()
        time.sleep_us(100)
        
        # Generate frame data
        for row in range(self.height):
            # Send HSYNC  
            self.send_hsync_pulse()
            time.sleep_us(10)
            
            # Enable data
            self.de.on()
            
            # Send pixel data for this row
            for col in range(self.width):
                self.set_rgb_pixel(r5, g6, b5)
                self.send_pixel_clock()
            
            # Disable data
            self.de.off()
            time.sleep_us(5)
    
    def test_display_sequence(self):
        """Run complete display test sequence"""
        print("\n" + "="*50)
        print("ST7701 RGB Display Test Sequence")
        print("="*50)
        
        # Test backlight
        print("\n--- Testing Backlight ---")
        for brightness in [0, 25, 50, 75, 100]:
            print(f"Setting brightness: {brightness}%")
            self.set_brightness(brightness)
            time.sleep(1)
        
        # Test solid colors
        print("\n--- Testing Solid Colors ---")
        test_colors = [
            (0xF800, "Red"),
            (0x07E0, "Green"), 
            (0x001F, "Blue"),
            (0xFFFF, "White"),
            (0x0000, "Black"),
        ]
        
        for color, name in test_colors:
            print(f"Displaying {name}")
            self.display_solid_color(color)
            time.sleep(2)
        
        # Test color bars
        print("\n--- Testing Color Bars ---") 
        self.display_color_bars()
        time.sleep(3)
        
        print("\n" + "="*50)
        print("Display test completed!")
        print("You should see colors on the display now.")
        print("="*50)

def main():
    """Main test function"""
    print("ESP32-S3 ST7701 RGB Display Test")
    print("If display shows colors, the RGB interface is working!")
    
    try:
        # Create display driver
        display = ST7701Driver()
        
        # Run test sequence
        display.test_display_sequence()
        
        # Keep displaying color bars
        print("\nContinuous color bar display...")
        for i in range(10):
            display.display_color_bars()
            time.sleep(1)
            
    except Exception as e:
        print(f"Error: {e}")
        import sys
        sys.print_exception(e)

if __name__ == "__main__":
    main()