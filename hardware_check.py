"""
Simple Hardware Verification for ST7701
Check for missing reset pin and power issues
"""

import time
from machine import Pin, PWM

# Known working configuration for ESP32-S3-4848S040
PINS = {
    'backlight': 38,
    'rst': None,  # Reset pin - often missing in pin configs
    
    # RGB pins according to datasheet
    'r': [11, 12, 13, 14, 0],      # R0-R4
    'g': [8, 20, 3, 46, 9, 10],    # G0-G5  
    'b': [4, 5, 6, 7, 15],         # B0-B4
    
    # Control pins
    'de': 18,      # Data Enable
    'vsync': 17,   # Vertical Sync
    'hsync': 16,   # Horizontal Sync
    'pclk': 21,    # Pixel Clock
    
    # SPI pins
    'cs': 39,      # Chip Select
    'sck': 48,     # Clock
    'mosi': 47,    # Data
}

def test_basic_hardware():
    """Test most basic hardware setup"""
    print("=== Basic Hardware Test ===")
    
    # 1. Test backlight
    print("1. Testing backlight...")
    bl = PWM(Pin(PINS['backlight']))
    bl.freq(1000)
    
    for duty in [0, 512, 1023]:
        bl.duty(duty)
        print(f"   Backlight duty: {duty}/1023")
        time.sleep(2)
    
    bl.duty(1023)  # Full brightness
    print("   ✓ Backlight test complete")
    
    # 2. Try to find reset pin
    print("\n2. Looking for reset pin...")
    possible_reset_pins = [2, 42, 41, 40]  # Common reset pins
    
    for pin_num in possible_reset_pins:
        try:
            rst = Pin(pin_num, Pin.OUT)
            print(f"   Trying reset on GPIO {pin_num}")
            
            # Reset sequence
            rst.off()  # Reset low
            time.sleep_ms(10)
            rst.on()   # Reset high
            time.sleep_ms(50)
            
        except:
            pass
    
    # 3. Simplest RGB test
    print("\n3. Testing RGB pins...")
    
    # Initialize all RGB pins
    r_pins = [Pin(p, Pin.OUT) for p in PINS['r']]
    g_pins = [Pin(p, Pin.OUT) for p in PINS['g']]
    b_pins = [Pin(p, Pin.OUT) for p in PINS['b']]
    
    # Initialize control pins
    de = Pin(PINS['de'], Pin.OUT)
    de.on()  # Enable data
    
    # Test basic colors
    colors = [
        (r_pins, "RED"),
        (g_pins, "GREEN"), 
        (b_pins, "BLUE"),
        (r_pins + g_pins + b_pins, "WHITE")
    ]
    
    for pins, color in colors:
        print(f"   Testing {color}...")
        
        # Turn all off first
        for pin in r_pins + g_pins + b_pins:
            pin.off()
        
        # Turn on specific color
        for pin in pins:
            pin.on()
        
        time.sleep(3)
    
    # Turn all off
    for pin in r_pins + g_pins + b_pins:
        pin.off()
    
    print("   ✓ RGB pin test complete")

def test_alternative_configs():
    """Test alternative pin configurations"""
    print("\n=== Alternative Configuration Test ===")
    
    # Some boards have different pin mappings
    alt_configs = [
        {
            'name': 'Alternative RGB mapping',
            'r': [0, 11, 12, 13, 14],      # R0-R4 (different order)
            'g': [3, 8, 9, 10, 20, 46],    # G0-G5 (different order)
            'b': [4, 5, 6, 7, 15],         # B0-B4
        },
        {
            'name': 'Swapped color channels',
            'r': [4, 5, 6, 7, 15],         # Blue pins as red
            'g': [8, 20, 3, 46, 9, 10],    # Green pins
            'b': [11, 12, 13, 14, 0],      # Red pins as blue
        }
    ]
    
    de = Pin(PINS['de'], Pin.OUT)
    de.on()
    
    for config in alt_configs:
        print(f"\nTrying: {config['name']}")
        
        r_pins = [Pin(p, Pin.OUT) for p in config['r']]
        g_pins = [Pin(p, Pin.OUT) for p in config['g']]
        b_pins = [Pin(p, Pin.OUT) for p in config['b']]
        
        # Test red
        for pin in r_pins + g_pins + b_pins:
            pin.off()
        for pin in r_pins:
            pin.on()
        print("   RED test - do you see red?")
        time.sleep(3)
        
        # Test green
        for pin in r_pins + g_pins + b_pins:
            pin.off()
        for pin in g_pins:
            pin.on()
        print("   GREEN test - do you see green?")
        time.sleep(3)
        
        # Test blue
        for pin in r_pins + g_pins + b_pins:
            pin.off()
        for pin in b_pins:
            pin.on()
        print("   BLUE test - do you see blue?")
        time.sleep(3)
        
        # Turn all off
        for pin in r_pins + g_pins + b_pins:
            pin.off()

def test_control_signal_combinations():
    """Test different control signal combinations"""
    print("\n=== Control Signal Test ===")
    
    # Initialize pins
    de = Pin(PINS['de'], Pin.OUT)
    vsync = Pin(PINS['vsync'], Pin.OUT)
    hsync = Pin(PINS['hsync'], Pin.OUT)
    pclk = Pin(PINS['pclk'], Pin.OUT)
    
    r_pins = [Pin(p, Pin.OUT) for p in PINS['r']]
    
    # Turn on red pins for testing
    for pin in r_pins:
        pin.on()
    
    # Test different control signal combinations
    configs = [
        {'de': 1, 'vsync': 1, 'hsync': 1, 'name': 'All HIGH'},
        {'de': 1, 'vsync': 0, 'hsync': 0, 'name': 'DE HIGH, syncs LOW'},
        {'de': 1, 'vsync': 1, 'hsync': 0, 'name': 'DE+VSYNC HIGH, HSYNC LOW'},
        {'de': 1, 'vsync': 0, 'hsync': 1, 'name': 'DE+HSYNC HIGH, VSYNC LOW'},
    ]
    
    for config in configs:
        print(f"   Testing: {config['name']}")
        
        de.value(config['de'])
        vsync.value(config['vsync'])
        hsync.value(config['hsync'])
        
        print(f"   DE={config['de']}, VSYNC={config['vsync']}, HSYNC={config['hsync']}")
        print("   Do you see red?")
        time.sleep(3)
    
    # Turn off red pins
    for pin in r_pins:
        pin.off()

def manual_pin_check():
    """Manual pin check with user feedback"""
    print("\n=== Manual Pin Check ===")
    print("This will test each individual pin.")
    print("Watch for ANY change on the display!")
    
    all_pins = PINS['r'] + PINS['g'] + PINS['b'] + [PINS['de']]
    
    for pin_num in all_pins:
        pin = Pin(pin_num, Pin.OUT)
        
        print(f"\nTesting GPIO {pin_num}...")
        print("Setting HIGH...")
        pin.on()
        time.sleep(2)
        
        print("Setting LOW...")
        pin.off()
        time.sleep(1)

def main():
    """Run all hardware tests"""
    print("ST7701 Hardware Verification")
    print("Watch display carefully for ANY changes!")
    print("=" * 50)
    
    try:
        test_basic_hardware()
        test_alternative_configs()
        test_control_signal_combinations()
        
        print("\n" + "=" * 50)
        print("HARDWARE CHECK COMPLETE")
        print("=" * 50)
        print("\nIf you saw NO colors at all:")
        print("1. Check power supply (needs adequate current)")
        print("2. Verify pin connections with multimeter")
        print("3. Display may need external reset/enable pin")
        print("4. Display controller may need specific init sequence")
        print("5. RGB interface may need proper timing signals")
        
        print("\nDid you see any colors during the tests? (y/n)")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import sys
        sys.print_exception(e)

if __name__ == "__main__":
    main()