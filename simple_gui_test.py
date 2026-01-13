"""
Simple GUI Test for Terry without requiring tkinter
"""

import sys
import time

def simple_gui_test():
    """Test basic GUI functionality without dependencies"""
    print("🎯 Simple GUI Test")
    print("Testing basic GUI components...")
    
    # Test 1: Create window
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title("Terry Test")
        root.geometry("300x200")
        
        label = tk.Label(root, text="✅ GUI Test Successful")
        label.pack(pady=20)
        
        # Update after 1 second
        root.update()
        time.sleep(1)
        
        # Test 2: Add widgets
        button = tk.Button(root, text="Test Button")
        button.pack()
        
        # Update after 1 second
        root.update()
        time.sleep(1)
        
        # Test 3: Event handling
        def on_button_click():
            print("Button clicked!")
        
        button.config(command=on_button_click)
        
        # Run for 5 seconds
        root.after(5000, root.destroy)
        
        root.mainloop()
        
        print("✅ Simple GUI test completed successfully!")
        return True
    
    except Exception as e:
        print(f"❌ GUI test failed: {str(e)}")
        return False

if __name__ == "__main__":
    simple_gui_test()