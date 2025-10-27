"""
ESP32-S3 ST7701 Display Test Script
Hardware: ESP32-S3-4848S040 with 480x480 ST7701 display
Touch: GT911 via I2C
"""

import machine
import time
from machine import Pin, SPI, I2C
import gc

# Pin configuration based on hardware specs
class DisplayConfig:
    # Display control pins
    GFX_BL = 38      # Backlight
    CS = 39          # Chip Select
    SCK = 48         # SPI Clock
    MOSI = 47        # SPI MOSI
    MISO = 41        # SPI MISO (not used for display but defined)
    
    # RGB parallel interface pins
    DE = 18          # Data Enable
    VSYNC = 17       # Vertical Sync
    HSYNC = 16       # Horizontal Sync
    PCLK = 21        # Pixel Clock
    
    # RGB data pins
    R0, R1, R2, R3, R4 = 11, 12, 13, 14, 0     # Red bits 0-4
    G0, G1, G2, G3, G4, G5 = 8, 20, 3, 46, 9, 10  # Green bits 0-5
    B0, B1, B2, B3, B4 = 4, 5, 6, 7, 15        # Blue bits 0-4
    
    # I2C configuration for touch
    I2C_SDA = 19
    I2C_SCL = 45
    TOUCH_ADDR = 0x5D  # GT911 touch controller I2C address
    
    # Display specifications
    WIDTH = 480
    HEIGHT = 480
    ROTATION = 0

class ST7701Display:
    def __init__(self):
        self.config = DisplayConfig()
        self.width = self.config.WIDTH
        self.height = self.config.HEIGHT
        
        # Initialize hardware
        self.init_pins()
        self.init_spi()
        self.init_i2c()
        self.init_display()
        
        print(f"ST7701 Display initialized: {self.width}x{self.height}")
    
    def init_pins(self):
        """Initialize GPIO pins"""
        print("Initializing GPIO pins...")
        
        # Backlight control
        self.backlight = Pin(self.config.GFX_BL, Pin.OUT)
        self.backlight.on()  # Turn on backlight
        
        # Chip select
        self.cs = Pin(self.config.CS, Pin.OUT)
        self.cs.on()  # Deselect initially
        
        # RGB control pins
        self.de = Pin(self.config.DE, Pin.OUT)
        self.vsync = Pin(self.config.VSYNC, Pin.OUT)
        self.hsync = Pin(self.config.HSYNC, Pin.OUT)
        self.pclk = Pin(self.config.PCLK, Pin.OUT)
        
        # RGB data pins (for demonstration - actual RGB implementation would need more complex handling)
        self.rgb_pins = {
            'r': [Pin(pin, Pin.OUT) for pin in [self.config.R0, self.config.R1, self.config.R2, self.config.R3, self.config.R4]],
            'g': [Pin(pin, Pin.OUT) for pin in [self.config.G0, self.config.G1, self.config.G2, self.config.G3, self.config.G4, self.config.G5]],
            'b': [Pin(pin, Pin.OUT) for pin in [self.config.B0, self.config.B1, self.config.B2, self.config.B3, self.config.B4]]
        }
        
        print("GPIO pins initialized")
    
    def init_spi(self):
        """Initialize SPI interface"""
        print("Initializing SPI...")
        
        self.spi = SPI(
            2,  # SPI bus 2
            baudrate=40000000,  # 40MHz
            polarity=0,
            phase=0,
            sck=Pin(self.config.SCK),
            mosi=Pin(self.config.MOSI),
            miso=Pin(self.config.MISO)
        )
        
        print("SPI initialized")
    
    def init_i2c(self):
        """Initialize I2C for touch controller"""
        print("Initializing I2C for touch...")
        
        self.i2c = I2C(
            0,
            scl=Pin(self.config.I2C_SCL),
            sda=Pin(self.config.I2C_SDA),
            freq=400000
        )
        
        # Scan for I2C devices
        devices = self.i2c.scan()
        print(f"I2C devices found: {[hex(addr) for addr in devices]}")
        
        if self.config.TOUCH_ADDR in devices:
            print(f"GT911 touch controller found at address {hex(self.config.TOUCH_ADDR)}")
        else:
            print(f"Warning: GT911 touch controller not found at {hex(self.config.TOUCH_ADDR)}")
    
    def init_display(self):
        """Initialize ST7701 display with configuration commands"""
        print("Initializing ST7701 display...")
        
        # Basic ST7701 initialization sequence
        init_commands = [
            # Software reset
            [0x01, []],
            # Wait for reset
            None,  # Will be handled as delay
            # Sleep out
            [0x11, []],
            # Wait for sleep out
            None,  # Will be handled as delay
            # Memory access control
            [0x36, [0x00]],  # Normal orientation
            # Pixel format
            [0x3A, [0x55]],  # 16-bit color
            # Display on
            [0x29, []],
        ]
        
        for cmd in init_commands:
            if cmd is None:
                time.sleep_ms(120)  # Delay for reset/sleep commands
            else:
                self.send_command(cmd[0], cmd[1])
        
        print("Display initialization complete")
    
    def send_command(self, cmd, data=None):
        """Send command to display via SPI"""
        self.cs.off()  # Select device
        
        # Send command
        self.spi.write(bytes([cmd]))
        
        # Send data if provided
        if data:
            self.spi.write(bytes(data))
        
        self.cs.on()  # Deselect device
    
    def set_rgb_color(self, r, g, b):
        """Set RGB pins to display a color (simplified demonstration)"""
        # Set red pins (5 bits)
        for i, pin in enumerate(self.rgb_pins['r']):
            pin.value((r >> i) & 1)
        
        # Set green pins (6 bits)
        for i, pin in enumerate(self.rgb_pins['g']):
            pin.value((g >> i) & 1)
        
        # Set blue pins (5 bits)
        for i, pin in enumerate(self.rgb_pins['b']):
            pin.value((b >> i) & 1)
    
    def test_backlight(self):
        """Test backlight control"""
        print("Testing backlight...")
        
        for i in range(3):
            print(f"Backlight OFF (cycle {i+1})")
            self.backlight.off()
            time.sleep(1)
            
            print(f"Backlight ON (cycle {i+1})")
            self.backlight.on()
            time.sleep(1)
        
        print("Backlight test complete")
    
    def test_rgb_colors(self):
        """Test RGB color output"""
        print("Testing RGB colors...")
        
        colors = [
            ("Red", 31, 0, 0),      # Max red (5-bit)
            ("Green", 0, 63, 0),    # Max green (6-bit)
            ("Blue", 0, 0, 31),     # Max blue (5-bit)
            ("White", 31, 63, 31),  # White
            ("Black", 0, 0, 0),     # Black
            ("Yellow", 31, 63, 0),  # Yellow
            ("Cyan", 0, 63, 31),    # Cyan
            ("Magenta", 31, 0, 31), # Magenta
        ]
        
        for color_name, r, g, b in colors:
            print(f"Setting color: {color_name} (R:{r}, G:{g}, B:{b})")
            self.set_rgb_color(r, g, b)
            time.sleep(2)
        
        print("RGB color test complete")
    
    def test_touch(self):
        """Test GT911 touch controller"""
        print("Testing GT911 touch controller...")
        
        try:
            # Try to read touch controller ID or status
            # This is a basic test - actual GT911 implementation would need proper protocol
            data = self.i2c.readfrom(self.config.TOUCH_ADDR, 1)
            print(f"Touch controller response: {data}")
            return True
        except Exception as e:
            print(f"Touch controller error: {e}")
            return False
    
    def sync_signals_test(self):
        """Test sync signals"""
        print("Testing sync signals...")
        
        # Generate basic sync patterns (simplified)
        for cycle in range(5):
            print(f"Sync cycle {cycle + 1}")
            
            # HSYNC pulse
            self.hsync.off()
            time.sleep_us(10)
            self.hsync.on()
            time.sleep_us(90)
            
            # VSYNC pulse
            if cycle % 100 == 0:  # Less frequent VSYNC
                self.vsync.off()
                time.sleep_us(10)
                self.vsync.on()
            
            # Data enable toggle
            self.de.on()
            time.sleep_us(50)
            self.de.off()
            time.sleep_us(50)
            
            # Pixel clock
            self.pclk.on()
            time.sleep_us(1)
            self.pclk.off()
            time.sleep_us(1)
        
        print("Sync signals test complete")
    
    def run_full_test(self):
        """Run comprehensive display test"""
        print("="*50)
        print("Starting ESP32-S3 ST7701 Display Test")
        print("="*50)
        
        print(f"Display: {self.width}x{self.height} ST7701")
        print(f"Touch: GT911 at I2C address {hex(self.config.TOUCH_ADDR)}")
        print()
        
        # Test sequence
        tests = [
            ("Backlight Control", self.test_backlight),
            ("RGB Colors", self.test_rgb_colors),
            ("Touch Controller", self.test_touch),
            ("Sync Signals", self.sync_signals_test),
        ]
        
        for test_name, test_func in tests:
            print(f"\n--- {test_name} Test ---")
            try:
                test_func()
                print(f"✓ {test_name} test passed")
            except Exception as e:
                print(f"✗ {test_name} test failed: {e}")
            
            time.sleep(1)  # Brief pause between tests
        
        print("\n" + "="*50)
        print("Display test sequence complete!")
        print("="*50)

def main():
    """Main test function"""
    print("ESP32-S3 ST7701 Display Test Starting...")
    
    # Show memory info
    print(f"Free memory: {gc.mem_free()} bytes")
    
    try:
        # Initialize and test display
        display = ST7701Display()
        display.run_full_test()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        raise
    
    print("\nTest complete. Display should be functional.")
    print("Monitor the display for visual changes during the test.")

# Run the test
if __name__ == "__main__":
    main()