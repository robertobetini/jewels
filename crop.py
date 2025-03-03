from PIL import Image
 
im = Image.open(r"../../Downloads/gems.png")
 
size = 16

for i in range(7):
	for j in range(7):
		cropped = im.crop((i * size, j * size, (i + 1) * size, (j + 1) * size))
		cropped.save(f"../../home/fedora/Downloads/gems_{i}_{j}.png")
		