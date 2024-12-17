import segno
import qrcode_artistic
from PIL import Image, ImageDraw, ImageFilter

def add_line_pattern(image):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for x in range(0, width, 10):
        for y in range(0, height, 10):
            if image.getpixel((x, y)) == (0, 0, 0):  # If the module is black
                draw.line((x, y, x + 10, y + 10), fill='black', width=1)
                draw.line((x, y + 10, x + 10, y), fill='black', width=1)
    return image

# Function to generate an artistic QR code with a logo in the center
def generate_artistic_qr_with_logo(data, logo_path=None, filename='badgatewayQR.png'):
    background_color = (22, 22, 22)  # Black for the QR code modules
    foreground_color = (255, 253, 250)  # White background

    
    # Create a QR Code instance with segno
    qr = segno.make(data, error='H')

    # Create an image from the QR code using qrcode_artistic
    img = qr.to_pil( scale=15, dark=foreground_color, light=background_color, border=1)  # Scale adjusts the size

    # Optional: Add artistic style (e.g., dotted or line)
    img = img.convert('RGB')
    #img = img.filter(ImageFilter.GaussianBlur(radius=2))  # You can adjust this for softer look

    if logo_path:
        # Open the logo image
        logo = Image.open(logo_path)

        # Calculate the size for the logo (18% of the QR code size)
        logo_size = int(img.size[0] * 0.18)  # Adjust the 0.2 to control logo size

        # Resize the logo to fit in the center of the QR code
        logo = logo.resize((logo_size, logo_size), Image.Resampling.BICUBIC)
        logo = logo.filter(ImageFilter.SHARPEN)

        # Calculate the position to place the logo at the center
        pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)

        # Create a rounded rectangle behind the logo to ensure visibility
        draw = ImageDraw.Draw(img)
        box_size = int(logo_size * 1.15)  # Slightly larger than the logo to ensure QR code clearance

        # Calculate the position for the box centered around the logo
        box_pos = ((img.size[0] - box_size) // 2, (img.size[1] - box_size) // 2)

        # Draw two rounded rectangles: one for the outer box and one for the inner box
        draw.rounded_rectangle([box_pos, (box_pos[0] + box_size, box_pos[1] + box_size)], radius=10, fill=foreground_color)
        draw.rounded_rectangle([box_pos[0] + 5, box_pos[1] + 5, box_pos[0] + box_size - 5, box_pos[1] + box_size - 5], radius=10, fill=background_color)

        # Paste the logo onto the cleared area
        img.paste(logo, pos, mask=logo)


    # Save the final image
    img.save(filename)
    print(f"Artistic QR code with logo generated and saved as {filename}")

# Example usage:
data_to_encode = "https://badgateway.us"  # Make sure this URL is valid and reachable
logo_image_path = "dark_half_icon (1).png"  # Path to your logo image
generate_artistic_qr_with_logo(data_to_encode, logo_image_path)






