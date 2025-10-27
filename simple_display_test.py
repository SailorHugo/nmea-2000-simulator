"""
Simple ESP32-S3 ST7701 Display Test (No LVGL)
Basic hardware testing for ESP32-S3-4848S040
"""

import machine
import time
from machine import Pin, SPI, I2C

# Hardware pin definitions
PINS = {
    # Display control
    'backlight': 38,
    'cs': 39,
    'sck': 48,
    'mosi': 47,
    'miso': 41,
    
    # RGB interface
    'de': 18,
    'vsync': 17, 
    'hsync': 16,
    'pclk': 21,
    
    # RGB data lines
    'r': [11, 12, 13, 14, 0],      # R0-R4
    'g': [8, 20, 3, 46, 9, 10],    # G0-G5  
    'b': [4, 5, 6, 7, 15],         # B0-B4
    
    # Touch I2C
    'sda': 19,
    'scl': 45
}

class SimpleDisplayTest:
    def __init__(self):
        print("Initializing ESP32-S3 ST7701 Display Test...")
        self.setup_hardware()
    
    def setup_hardware(self):
        """Initialize basic hardware components"""
        
        # Backlight control
        self.backlight = Pin(PINS['backlight'], Pin.OUT)
        self.backlight.on()
        print("✓ Backlight initialized and turned ON")
        
        # SPI for display commands
        self.spi = SPI(2, 
                      baudrate=10000000,
                      sck=Pin(PINS['sck']),
                      mosi=Pin(PINS['mosi']),
                      miso=Pin(PINS['miso']))
        
        self.cs = Pin(PINS['cs'], Pin.OUT)
        self.cs.on()  # Deselect
        print("✓ SPI interface initialized")
        
        # I2C for touch
        self.i2c = I2C(0, 
                      scl=Pin(PINS['scl']),
                      sda=Pin(PINS['sda']),
                      freq=400000)
        print("✓ I2C interface initialized")
        
        # RGB control signals
        self.de = Pin(PINS['de'], Pin.OUT)
        self.vsync = Pin(PINS['vsync'], Pin.OUT) 
        self.hsync = Pin(PINS['hsync'], Pin.OUT)
        self.pclk = Pin(PINS['pclk'], Pin.OUT)
        print("✓ RGB control signals initialized")
        
        # RGB data pins
        self.rgb_r = [Pin(p, Pin.OUT) for p in PINS['r']]
        self.rgb_g = [Pin(p, Pin.OUT) for p in PINS['g']]
        self.rgb_b = [Pin(p, Pin.OUT) for p in PINS['b']]
        print("✓ RGB data pins initialized")
    
    def send_display_cmd(self, cmd, data=None):
        """Send command to ST7701 via SPI"""
        self.cs.off()
        self.spi.write(bytes([cmd]))
        if data:
            self.spi.write(bytes(data))
        self.cs.on()
    
    def init_st7701(self):
        """Basic ST7701 initialization sequence"""
        print("Initializing ST7701 display controller...")
        
        # Reset and basic setup
        self.send_display_cmd(0x01)  # Software reset
        time.sleep_ms(150)
        
        self.send_display_cmd(0x11)  # Sleep out
        time.sleep_ms(150)
        
        # Color format: 16-bit RGB565
        self.send_display_cmd(0x3A, [0x55])
        
        # Memory access control
        self.send_display_cmd(0x36, [0x00])
        
        # Display on
        self.send_display_cmd(0x29)
        time.sleep_ms(50)
        
        print("✓ ST7701 display controller initialized")
    
    def test_backlight(self):
        """Test backlight on/off"""
        print("\n--- Testing Backlight ---")
        
        for i in range(3):
            print(f"Cycle {i+1}: Backlight OFF")
            self.backlight.off()
            time.sleep(1)
            
            print(f"Cycle {i+1}: Backlight ON") 
            self.backlight.on()
            time.sleep(1)
        
        print("✓ Backlight test completed")
    
    def test_i2c_scan(self):
        """Scan I2C bus for devices"""
        print("\n--- Scanning I2C Bus ---")
        
        devices = self.i2c.scan()
        print(f"Found {len(devices)} I2C device(s):")
        
        for addr in devices:
            print(f"  - Device at address: 0x{addr:02X}")
            if addr == 0x5D:
                print("    └─ GT911 Touch Controller detected!")
        
        if 0x5D not in devices:
            print("  ⚠ GT911 Touch Controller (0x5D) not found")
        
        print("✓ I2C scan completed")
    
    def set_rgb_color(self, r5, g6, b5):
        """Set RGB output pins to specific color values
        r5: 5-bit red (0-31)
        g6: 6-bit green (0-63) 
        b5: 5-bit blue (0-31)
        """
        # Set red pins (5 bits)
        for i in range(5):
            self.rgb_r[i].value((r5 >> i) & 1)
        
        # Set green pins (6 bits)
        for i in range(6):
            self.rgb_g[i].value((g6 >> i) & 1)
        
        # Set blue pins (5 bits)
        for i in range(5):
            self.rgb_b[i].value((b5 >> i) & 1)
    
    def test_rgb_colors(self):
        """Test RGB color output"""
        print("\n--- Testing RGB Colors ---")
        
        test_colors = [
            ("Black",   0,  0,  0),
            ("Red",    31,  0,  0),
            ("Green",   0, 63,  0),
            ("Blue",    0,  0, 31),
            ("Yellow", 31, 63,  0),
            ("Cyan",    0, 63, 31),
            ("Magenta",31,  0, 31),
            ("White",  31, 63, 31),
        ]
        
        for name, r, g, b in test_colors:
            print(f"Setting color: {name}")
            self.set_rgb_color(r, g, b)
            time.sleep(2)
        
        print("✓ RGB color test completed")
    
    def test_sync_signals(self):
        """Test RGB interface sync signals"""
        print("\n--- Testing Sync Signals ---")
        
        print("Generating sync patterns...")
        
        for frame in range(3):
            print(f"Frame {frame + 1}")
            
            # Simulate frame sync
            self.vsync.off()
            time.sleep_us(100)
            self.vsync.on()
            
            # Simulate some line syncs
            for line in range(10):
                self.hsync.off()
                time.sleep_us(10)
                self.hsync.on()
                
                # Data enable active period
                self.de.on()
                
                # Pixel clock cycles
                for pixel in range(20):
                    self.pclk.on()
                    time.sleep_us(1)
                    self.pclk.off()
                    time.sleep_us(1)
                
                self.de.off()
                time.sleep_us(50)
            
            time.sleep_ms(16)  # ~60Hz frame rate
        
        print("✓ Sync signal test completed")
    
    def run_tests(self):
        """Run all hardware tests"""
        print("="*60)
        print("ESP32-S3 ST7701 Display Hardware Test")
        print("Board: ESP32-S3-4848S040")
        print("Display: 480x480 ST7701")
        print("Touch: GT911 (I2C 0x5D)")
        print("="*60)
        
        try:
            # Initialize display
            self.init_st7701()
            
            # Run test sequence
            self.test_backlight()
            self.test_i2c_scan()
            self.test_rgb_colors()
            self.test_sync_signals()
            
            print("\n" + "="*60)
            print("✓ All tests completed successfully!")
            print("The display hardware should now be functional.")
            print("="*60)
            
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}")
            print("Check connections and power supply.")

def main():
    """Main entry point"""
    test = SimpleDisplayTest()
    test.run_tests()

if __name__ == "__main__":
    main()