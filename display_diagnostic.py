"""
ST7701 Display Diagnostic Script
Helps identify why colors are not appearing on display
"""

import time
from machine import Pin, PWM, SPI
import gc

# Pin definitions
BL = 38   # Backlight
CS = 39   # SPI Chip Select
SCK = 48  # SPI Clock  
MOSI = 47 # SPI Data

# RGB pins
R_PINS = [11, 12, 13, 14, 0]    # R0-R4
G_PINS = [8, 20, 3, 46, 9, 10]  # G0-G5
B_PINS = [4, 5, 6, 7, 15]       # B0-B4

# Control pins
DE = 18      # Data Enable
VSYNC = 17   # Vertical Sync  
HSYNC = 16   # Horizontal Sync
PCLK = 21    # Pixel Clock

class DisplayDiagnostic:
    def __init__(self):
        print("ST7701 Display Diagnostic Tool")
        print("=" * 50)
        
        self.init_hardware()
        
    def init_hardware(self):
        """Initialize all hardware"""
        # Backlight
        self.backlight = PWM(Pin(BL))
        self.backlight.freq(1000)
        self.backlight.duty(1023)
        print("✓ Backlight initialized")
        
        # SPI for display controller
        self.spi = SPI(2, baudrate=10000000, sck=Pin(SCK), mosi=Pin(MOSI))
        self.cs = Pin(CS, Pin.OUT)
        self.cs.on()
        print("✓ SPI initialized")
        
        # RGB pins
        self.r_pins = [Pin(p, Pin.OUT) for p in R_PINS]
        self.g_pins = [Pin(p, Pin.OUT) for p in G_PINS]
        self.b_pins = [Pin(p, Pin.OUT) for p in B_PINS]
        print("✓ RGB pins initialized")
        
        # Control pins
        self.de = Pin(DE, Pin.OUT)
        self.vsync = Pin(VSYNC, Pin.OUT)
        self.hsync = Pin(HSYNC, Pin.OUT) 
        self.pclk = Pin(PCLK, Pin.OUT)
        print("✓ Control pins initialized")
    
    def send_spi_command(self, cmd, data=None):
        """Send command to ST7701 via SPI"""
        self.cs.off()
        time.sleep_us(1)
        self.spi.write(bytes([cmd]))
        if data:
            self.spi.write(bytes(data))
        time.sleep_us(1)
        self.cs.on()
        time.sleep_us(10)
    
    def test_1_backlight(self):
        """Test 1: Backlight Control"""
        print("\n--- Test 1: Backlight Control ---")
        
        for brightness in [0, 50, 100]:
            duty = int(1023 * brightness / 100)
            self.backlight.duty(duty)
            print(f"Backlight: {brightness}% - Can you see the display light up?")
            time.sleep(2)
        
        self.backlight.duty(1023)  # Full brightness
        print("Result: If display lights up, backlight is working ✓")
    
    def test_2_display_controller_init(self):
        """Test 2: ST7701 Controller Initialization"""
        print("\n--- Test 2: ST7701 Controller Initialization ---")
        
        try:
            # Extended ST7701 initialization sequence
            init_commands = [
                # Basic reset and wake up
                (0x01, None, 150),    # Software reset
                (0x11, None, 150),    # Sleep out
                
                # ST7701 specific initialization
                (0xFF, [0x77, 0x01, 0x00, 0x00, 0x10], 10),  # CMD2 Enable
                (0xC0, [0x3C, 0x00], 10),                     # Display control
                (0xC1, [0x0D, 0x02], 10),                     # Display control
                (0xC2, [0x21, 0x08], 10),                     # Display control
                (0xCD, [0x08], 10),                           # RGB Interface Control
                
                # Color format and orientation
                (0x3A, [0x66], 10),   # 18-bit RGB666 format
                (0x36, [0x00], 10),   # Memory access control
                
                # Display timing
                (0xB0, [0x00, 0x11, 0x16, 0x0E, 0x11, 0x06, 0x05, 0x09, 0x08, 0x21, 0x06, 0x13, 0x10, 0x29, 0x31, 0x18], 10),
                (0xB1, [0x00, 0x11, 0x16, 0x0E, 0x11, 0x07, 0x05, 0x09, 0x09, 0x21, 0x05, 0x13, 0x11, 0x2A, 0x31, 0x18], 10),
                
                # Enable display
                (0x21, None, 10),     # Display inversion on
                (0x29, None, 50),     # Display on
            ]
            
            for cmd_data in init_commands:
                cmd, data, delay = cmd_data
                self.send_spi_command(cmd, data)
                if delay:
                    time.sleep_ms(delay)
                print(f"Sent command: 0x{cmd:02X}")
            
            print("✓ ST7701 controller initialized with extended sequence")
            
        except Exception as e:
            print(f"✗ Controller initialization failed: {e}")
    
    def test_3_rgb_pin_verification(self):
        """Test 3: Individual RGB Pin Testing"""
        print("\n--- Test 3: RGB Pin Verification ---")
        
        # Turn off all pins first
        for pin in self.r_pins + self.g_pins + self.b_pins:
            pin.off()
        
        # Enable data output
        self.de.on()
        print("Data Enable (DE) set HIGH")
        
        # Test each color channel
        print("Testing RED pins (should see red if working)...")
        for pin in self.r_pins:
            pin.on()
        time.sleep(3)
        
        for pin in self.r_pins:
            pin.off()
        
        print("Testing GREEN pins (should see green if working)...")
        for pin in self.g_pins:
            pin.on()
        time.sleep(3)
        
        for pin in self.g_pins:
            pin.off()
        
        print("Testing BLUE pins (should see blue if working)...")
        for pin in self.b_pins:
            pin.on()
        time.sleep(3)
        
        for pin in self.b_pins:
            pin.off()
        
        print("Testing ALL pins (should see white if working)...")
        for pin in self.r_pins + self.g_pins + self.b_pins:
            pin.on()
        time.sleep(3)
        
        for pin in self.r_pins + self.g_pins + self.b_pins:
            pin.off()
    
    def test_4_control_signal_states(self):
        """Test 4: Control Signal State Testing"""
        print("\n--- Test 4: Control Signal Testing ---")
        
        # Test different DE states
        print("Testing Data Enable (DE) states...")
        self.de.off()
        print("DE = LOW (no data)")
        time.sleep(2)
        
        self.de.on()
        print("DE = HIGH (data enabled)")
        
        # Set a simple color pattern
        for pin in self.r_pins:
            pin.on()  # Red
        time.sleep(3)
        
        # Test sync signal states
        print("Testing sync signals...")
        
        # Try different VSYNC states
        self.vsync.off()
        print("VSYNC = LOW")
        time.sleep(1)
        self.vsync.on()
        print("VSYNC = HIGH")
        time.sleep(1)
        
        # Try different HSYNC states  
        self.hsync.off()
        print("HSYNC = LOW")
        time.sleep(1)
        self.hsync.on()
        print("HSYNC = HIGH")
        
        # Clean up
        for pin in self.r_pins:
            pin.off()
    
    def test_5_alternative_pin_mapping(self):
        """Test 5: Verify Pin Mapping"""
        print("\n--- Test 5: Pin Mapping Verification ---")
        
        print("Current pin mapping:")
        print(f"RED pins:   {R_PINS}")
        print(f"GREEN pins: {G_PINS}")
        print(f"BLUE pins:  {B_PINS}")
        print(f"DE pin:     {DE}")
        print(f"VSYNC pin:  {VSYNC}")
        print(f"HSYNC pin:  {HSYNC}")
        print(f"PCLK pin:   {PCLK}")
        
        # Try alternative Data Enable pin states
        print("\nTrying different DE pin configurations...")
        
        # Make sure DE is enabled
        self.de.on()
        
        # Set RGB pins to maximum values
        for pin in self.r_pins + self.g_pins + self.b_pins:
            pin.on()
        
        print("All RGB pins HIGH, DE HIGH - Do you see white?")
        time.sleep(5)
        
        # Try toggling PCLK
        print("Toggling pixel clock...")
        for i in range(100):
            self.pclk.on()
            time.sleep_us(10)
            self.pclk.off()
            time.sleep_us(10)
    
    def test_6_rgb666_mode(self):
        """Test 6: Try RGB666 (18-bit) mode"""
        print("\n--- Test 6: RGB666 Mode Test ---")
        
        # Reinitialize with RGB666
        self.send_spi_command(0x3A, [0x66])  # 18-bit RGB666
        time.sleep_ms(10)
        
        print("Switched to RGB666 mode")
        
        # Enable DE
        self.de.on()
        
        # Test with RGB666 - use only higher bits
        print("Testing RGB666 colors...")
        
        # Red in RGB666
        for pin in self.r_pins[2:]:  # Use higher red bits
            pin.on()
        time.sleep(2)
        for pin in self.r_pins:
            pin.off()
        
        # Green in RGB666  
        for pin in self.g_pins[2:]:  # Use higher green bits
            pin.on()
        time.sleep(2)
        for pin in self.g_pins:
            pin.off()
        
        # Blue in RGB666
        for pin in self.b_pins[2:]:  # Use higher blue bits
            pin.on()
        time.sleep(2)
        for pin in self.b_pins:
            pin.off()
    
    def run_full_diagnostic(self):
        """Run complete diagnostic sequence"""
        print("\nRunning complete ST7701 diagnostic...")
        print("Watch the display carefully during each test!")
        print("=" * 50)
        
        tests = [
            self.test_1_backlight,
            self.test_2_display_controller_init,
            self.test_3_rgb_pin_verification,
            self.test_4_control_signal_states,
            self.test_5_alternative_pin_mapping,
            self.test_6_rgb666_mode,
        ]
        
        for i, test in enumerate(tests, 1):
            try:
                test()
                print(f"✓ Test {i} completed")
                time.sleep(1)
            except Exception as e:
                print(f"✗ Test {i} failed: {e}")
        
        print("\n" + "=" * 50)
        print("DIAGNOSTIC COMPLETE")
        print("=" * 50)
        print("\nPossible issues if no colors appeared:")
        print("1. Display controller not properly initialized")
        print("2. Wrong pin mapping for your specific board")
        print("3. Display needs different color format (RGB666 vs RGB565)")
        print("4. Hardware connection issues")
        print("5. Display may need external crystal/clock")
        print("\nNext steps:")
        print("- Check if any test showed colors")
        print("- Verify pin connections with multimeter")
        print("- Try different initialization sequences")

def main():
    """Run diagnostic"""
    diag = DisplayDiagnostic()
    diag.run_full_diagnostic()

if __name__ == "__main__":
    main()