import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def show_image_under_dir(image_dir):
    MAX_NUM = 16  # Maximum number of images to plot
    
    # Get all image files in the directory
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    image_files = sorted(image_files)[::len(image_files) // MAX_NUM]  # Select only MAX_NUM images
    
    # Load images
    images = [cv2.imread(os.path.join(image_dir, img)) for img in image_files]
    images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images if img is not None]
    
    # Determine grid size
    num_images = len(images)
    cols = int(np.ceil(np.sqrt(num_images)))  # Square layout
    rows = int(np.ceil(num_images / cols))
    
    # Plot images
    fig, axes = plt.subplots(rows, cols, figsize=(12, 8))
    fig.suptitle(f"{image_dir}", fontsize=10)  # Set the title
    axes = axes.flatten()
    
    for i, img in enumerate(images):
        axes[i].imshow(img)
        axes[i].axis("off")
        axes[i].set_title(image_files[i])
    
    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig(image_dir + "/summary.png", dpi=300, bbox_inches="tight")
    plt.close()

for image_dir in glob.glob("/work/SuperResolutionData/sihe.chen/lognerf/20250225/GPLog/GX010571_linear_5000/render/path_renders_step_5000"):
    show_image_under_dir(image_dir)
