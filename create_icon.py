"""
Create a simple application icon for AI Prompt Generator Pro
This script generates a basic icon using PIL (Pillow)
"""

import os
import sys

def create_icon():
    """Create a simple application icon"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create icon directory
        icon_dir = os.path.join("assets", "icons")
        os.makedirs(icon_dir, exist_ok=True)
        
        # Create images at different sizes for .ico file
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        images = []
        
        for size in sizes:
            # Create image with gradient background
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Calculate dimensions
            width, height = size
            center_x, center_y = width // 2, height // 2
            
            # Draw background circle
            circle_radius = min(width, height) // 2 - 2
            draw.ellipse(
                [center_x - circle_radius, center_y - circle_radius,
                 center_x + circle_radius, center_y + circle_radius],
                fill=(233, 69, 96),  # Red accent color
                outline=(255, 255, 255),
                width=2
            )
            
            # Draw "AI" text
            try:
                # Try to use a font
                font_size = max(12, min(width, height) // 3)
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # Draw text
            text = "AI"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            text_x = center_x - text_width // 2
            text_y = center_y - text_height // 2 - 2
            
            draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
            
            # Draw small prompt symbol
            if width >= 32:
                symbol_size = max(4, width // 8)
                symbol_x = center_x + circle_radius // 2
                symbol_y = center_y - circle_radius // 2
                
                # Draw small pencil/pen icon
                draw.line(
                    [(symbol_x, symbol_y), (symbol_x + symbol_size, symbol_y + symbol_size)],
                    fill=(255, 255, 255),
                    width=max(1, width // 32)
                )
            
            images.append(img)
        
        # Save as ICO file
        icon_path = os.path.join(icon_dir, "app_icon.ico")
        images[0].save(
            icon_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:]
        )
        
        print(f"Icon created successfully: {icon_path}")
        
        # Also save as PNG for other uses
        png_path = os.path.join(icon_dir, "app_icon.png")
        images[-1].save(png_path, format='PNG')
        print(f"PNG version created: {png_path}")
        
        return True
        
    except ImportError:
        print("Pillow (PIL) is not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        print("Please run this script again to create the icon.")
        return False
    
    except Exception as e:
        print(f"Error creating icon: {e}")
        
        # Create a fallback simple icon
        try:
            import struct
            
            # Create a minimal 16x16 ICO file
            icon_path = os.path.join(icon_dir, "app_icon.ico")
            
            # ICO header
            ico_header = struct.pack('<HHH', 0, 1, 1)  # Reserved, Type=ICO, Count=1
            
            # Image entry
            width = 16
            height = 16
            colors = 0  # True color
            reserved = 0
            planes = 1
            bit_count = 32
            image_size = width * height * 4 + 40  # BMP header + pixels
            image_offset = 22  # After header + entry
            
            entry = struct.pack('<BBBBHHII', 
                              width if width < 256 else 0,
                              height if height < 256 else 0,
                              colors, reserved,
                              planes, bit_count,
                              image_size, image_offset)
            
            # BMP header
            bmp_header = struct.pack('<IiiHHIIiiII',
                                   40,  # Header size
                                   width, height * 2,  # Height doubled for XOR+AND
                                   1, 32,  # Planes, bits
                                   0, 0,  # Compression, size
                                   0, 0,  # Resolution
                                   0, 0)  # Colors
            
            # Create simple red square with white border
            pixels = bytearray()
            for y in range(height):
                for x in range(width):
                    # Border
                    if x == 0 or x == width-1 or y == 0 or y == height-1:
                        pixels.extend([255, 255, 255, 255])  # White
                    # Inner area
                    elif 2 <= x <= width-3 and 2 <= y <= height-3:
                        pixels.extend([96, 69, 233, 255])  # BGRA for red
                    else:
                        pixels.extend([0, 0, 0, 0])  # Transparent
            
            # AND mask (all zeros for no transparency)
            and_mask = bytearray(width * height // 8)
            
            # Write icon file
            with open(icon_path, 'wb') as f:
                f.write(ico_header)
                f.write(entry)
                f.write(bmp_header)
                f.write(bytes(pixels))
                f.write(bytes(and_mask))
            
            print(f"Fallback icon created: {icon_path}")
            return True
            
        except Exception as e2:
            print(f"Failed to create fallback icon: {e2}")
            return False


if __name__ == "__main__":
    print("Creating application icon...")
    if create_icon():
        print("Icon creation completed successfully!")
    else:
        print("Icon creation failed. The application will use default system icon.")