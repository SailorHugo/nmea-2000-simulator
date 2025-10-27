"""
Basic RGB Pin Test - Direct Hardware Control
Simple test to verify RGB pins are working
"""

import time
from machine import Pin, PWM

# Pin definitions for ESP32-S3-4848S040
BL = 38   # Backlight

# RGB pins
R_PINS = [11, 12, 13, 14, 0]    # R0-R4
G_PINS = [8, 20, 3, 46, 9, 10]  # G0-G5  
B_PINS = [4, 5, 6, 7, 15]       # B0-B4

# Control pins
DE = 18      # Data Enable
VSYNC = 17   # Vertical Sync
HSYNC = 16   # Horizontal Sync
PCLK = 21    # Pixel Clock

class BasicRGBTest:
    def __init__(self):
        print("Basic RGB Hardware Test")
        print("=" * 40)
        
        # Initialize backlight
        self.backlight = PWM(Pin(BL))
        self.backlight.freq(1000)
        self.backlight.duty(1023)  # Full brightness
        print("✓ Backlight ON")
        
        # Initialize RGB pins
        self.r_pins = [Pin(p, Pin.OUT) for p in R_PINS]
        self.g_pins = [Pin(p, Pin.OUT) for p in G_PINS]
        self.b_pins = [Pin(p, Pin.OUT) for p in B_PINS]
        print("✓ RGB pins initialized")
        
        # Initialize control pins
        self.de = Pin(DE, Pin.OUT)
        self.vsync = Pin(VSYNC, Pin.OUT) 
        self.hsync = Pin(HSYNC, Pin.OUT)
        self.pclk = Pin(PCLK, Pin.OUT)
        
        # Set control signals active
        self.de.on()      # Enable data
        self.vsync.on()   # Sync signals high
        self.hsync.on()
        self.pclk.off()
        print("✓ Control signals set")
    
    def set_all_rgb_pins(self, r_val, g_val, b_val):
        """Set all RGB pins to specific values (0-255)"""
        # Convert 8-bit to actual pin values
        r5 = (r_val >> 3) & 0x1F  # 5 bits for red
        g6 = (g_val >> 2) & 0x3F  # 6 bits for green  
        b5 = (b_val >> 3) & 0x1F  # 5 bits for blue
        
        # Set red pins
        for i in range(5):
            self.r_pins[i].value((r5 >> i) & 1)
        
        # Set green pins
        for i in range(6):
            self.g_pins[i].value((g6 >> i) & 1)
        
        # Set blue pins
        for i in range(5):
            self.b_pins[i].value((b5 >> i) & 1)
    
    def all_pins_off(self):
        """Turn off all RGB pins"""
        for pin in self.r_pins + self.g_pins + self.b_pins:
            pin.off()
    
    def all_pins_on(self):
        """Turn on all RGB pins"""
        for pin in self.r_pins + self.g_pins + self.b_pins:
            pin.on()
    
    def test_individual_colors(self):
        """Test each color individually"""
        print("\n--- Testing Individual Colors ---")
        
        colors = [
            (255, 0, 0, "RED"),
            (0, 255, 0, "GREEN"), 
            (0, 0, 255, "BLUE"),
            (255, 255, 0, "YELLOW"),
            (255, 0, 255, "MAGENTA"),
            (0, 255, 255, "CYAN"),
            (255, 255, 255, "WHITE"),
            (0, 0, 0, "BLACK"),
        ]
        
        for r, g, b, name in colors:
            print(f"Setting color: {name}")
            self.set_all_rgb_pins(r, g, b)
            time.sleep(3)  # Hold each color for 3 seconds
    
    def test_brightness_levels(self):
        """Test different brightness levels"""
        print("\n--- Testing Brightness Levels ---")
        
        for level in [0, 64, 128, 192, 255]:
            print(f"Setting brightness level: {level}")
            self.set_all_rgb_pins(level, level, level)  # White at different levels
            time.sleep(2)
    
    def test_pin_scan(self):
        """Test individual pins one by one"""
        print("\n--- Testing Individual Pins ---")
        
        # Turn all pins off first
        self.all_pins_off()
        time.sleep(1)
        
        # Test red pins
        print("Testing RED pins...")
        for i, pin in enumerate(self.r_pins):
            print(f"  R{i} (GPIO {R_PINS[i]})")
            pin.on()
            time.sleep(1)
            pin.off()
        
        # Test green pins  
        print("Testing GREEN pins...")
        for i, pin in enumerate(self.g_pins):
            print(f"  G{i} (GPIO {G_PINS[i]})")
            pin.on()
            time.sleep(1)
            pin.off()
        
        # Test blue pins
        print("Testing BLUE pins...")
        for i, pin in enumerate(self.b_pins):
            print(f"  B{i} (GPIO {B_PINS[i]})")
            pin.on()
            time.sleep(1)
            pin.off()
    
    def test_backlight_control(self):
        """Test backlight PWM control"""
        print("\n--- Testing Backlight Control ---")
        
        for brightness in [0, 25, 50, 75, 100]:
            duty = int(1023 * brightness / 100)
            print(f"Backlight: {brightness}%")
            self.backlight.duty(duty)
            time.sleep(2)
        
        # Reset to full brightness
        self.backlight.duty(1023)
    
    def run_all_tests(self):
        """Run complete test sequence"""
        print("\nStarting RGB Hardware Tests...")
        print("Watch the display for color changes!")
        
        try:
            # Test 1: Backlight control
            self.test_backlight_control()
            
            # Test 2: Individual colors
            self.test_individual_colors()
            
            # Test 3: Brightness levels
            self.test_brightness_levels()
            
            # Test 4: Individual pin scanning
            self.test_pin_scan()
            
            print("\n" + "=" * 40)
            print("✓ All tests completed!")
            print("If you saw colors, the RGB interface is working!")
            print("=" * 40)
            
        except Exception as e:
            print(f"Test failed: {e}")
            import sys
            sys.print_exception(e)

def quick_color_test():
    """Quick test function - just show basic colors"""
    print("Quick RGB Color Test")
    
    # Initialize hardware
    backlight = PWM(Pin(BL))
    backlight.freq(1000)
    backlight.duty(1023)
    
    r_pins = [Pin(p, Pin.OUT) for p in R_PINS]
    g_pins = [Pin(p, Pin.OUT) for p in G_PINS]
    b_pins = [Pin(p, Pin.OUT) for p in B_PINS]
    
    de = Pin(DE, Pin.OUT)
    de.on()  # Enable data output
    
    def set_color(r, g, b):
        # Turn off all pins first
        for pin in r_pins + g_pins + b_pins:
            pin.off()
        
        # Set pins based on color values
        if r > 0:
            for pin in r_pins:
                pin.on()
        if g > 0:
            for pin in g_pins:
                pin.on()  
        if b > 0:
            for pin in b_pins:
                pin.on()
    
    # Test basic colors
    colors = [(1,0,0,"RED"), (0,1,0,"GREEN"), (0,0,1,"BLUE"), (1,1,1,"WHITE")]
    
    for r, g, b, name in colors:
        print(f"Showing {name}")
        set_color(r, g, b)
        time.sleep(3)
    
    print("Quick test done!")

def main():
    """Main function"""
    print("ESP32-S3 ST7701 RGB Pin Test")
    print("Choose test mode:")
    print("1. Full test suite")
    print("2. Quick color test")
    
    # For automated testing, run full suite
    test = BasicRGBTest()
    test.run_all_tests()

if __name__ == "__main__":
    main()