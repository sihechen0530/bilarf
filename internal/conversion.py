import numpy as np
from internal import chromaticity
from internal import configs
import torch
import re

def parse_ccm_string(ccm_string):
    """
    Extract a 3x3 color correction matrix from a string.
    Supports formats like:
    - "1.1,0.2,0.1,0.1,0.9,0.1,0.1,0.1,1.0"
    - "1.1 0.2 0.1 0.1 0.9 0.1 0.1 0.1 1.0"
    - "[[1.1,0.2,0.1],[0.1,0.9,0.1],[0.1,0.1,1.0]]"
    - "1.1,0.2,0.1;0.1,0.9,0.1;0.1,0.1,1.0"
    
    Args:
        ccm_string: String representation of a color correction matrix
        
    Returns:
        3x3 numpy array representing the CCM
    """
    # Clean up the string
    ccm_string = ccm_string.strip()
    
    # Remove any brackets, parentheses
    ccm_string = re.sub(r'[\[\]\(\)]', '', ccm_string)
    
    # Check if the string uses semicolons as row separators
    if ';' in ccm_string:
        rows = ccm_string.split(';')
        matrix = []
        for row in rows:
            # Split by comma or space
            values = re.split(r'[,\s]+', row.strip())
            matrix.append([float(v) for v in values if v])
        return np.array(matrix)
    
    # Try to parse as a flat list of 9 values
    values = re.split(r'[,\s]+', ccm_string)
    values = [float(v) for v in values if v]
    
    if len(values) == 9:
        return np.array(values).reshape(3, 3)
    
    raise ValueError("Could not parse the CCM string. Please use a supported format.")

def apply_ccm(image_float, ccm_str):
    # parse ccm
    if ccm_str is None:
        return image_float
    ccm = parse_ccm_string(ccm_str)

    if isinstance(image_float, torch.Tensor):
        device = image_float.device
        
        # Convert CCM to tensor and move to the same device
        ccm_tensor = torch.tensor(ccm, dtype=image_float.dtype, device=device)
        
        # Store original shape
        original_shape = image_float.shape
        
        # Reshape for matrix multiplication
        pixels = image_float.reshape(-1, 3)
        
        # Apply CCM
        corrected_pixels = torch.matmul(pixels, ccm_tensor)
        
        # Clip values
        corrected_pixels = torch.clamp(corrected_pixels, 0.0, 1.0)
        
        # Reshape back
        return corrected_pixels.reshape(original_shape)
    else:
        # Reshape image to apply matrix multiplication
        original_shape = image_float.shape
        pixels = image_float.reshape(-1, 3)
        
        # Apply CCM (matrix multiplication)
        corrected_pixels = np.dot(pixels, ccm)
        
        # Clip values to [0, 1] range
        corrected_pixels = np.clip(corrected_pixels, 0.0, 1.0)
        
        # Reshape back to image format
        return corrected_pixels.reshape(original_shape)


# def convert(images, config: configs.Config, is_torch=False):
#     converted = _convert(images, config.convert_from, config.convert_to, is_torch)
#     return converted

def convert(images, convert_from, convert_to, is_torch):
    # input data range: (0, 1)
    # output data range: (0, 1)
    exp_func = np.exp
    log_func = np.log
    if is_torch:
        exp_func = torch.exp
        # log_func = lambda x:torch.where(x > 0, torch.log(x), x)
        log_func = torch.log
    linear = None
    if convert_from == chromaticity.ChromaticityType.sRGB:
        linear = srgb_2_linear(images, exp_func, log_func)
    elif convert_from == chromaticity.ChromaticityType.GPLog:
        linear = gplog_2_linear(images, exp_func, log_func)
    elif convert_from == chromaticity.ChromaticityType.linear:
        linear = images
    elif convert_from == chromaticity.ChromaticityType.TrueLog:
        linear = truelog_2_linear(images, exp_func, log_func)
    else:
        pass
    if convert_to == chromaticity.ChromaticityType.sRGB:
        return linear_2_srgb(linear, exp_func, log_func)
    elif convert_to == chromaticity.ChromaticityType.GPLog:
        return linear_2_gplog(linear, exp_func, log_func)
    elif convert_to == chromaticity.ChromaticityType.linear:
        return linear
    elif convert_to == chromaticity.ChromaticityType.TrueLog:
        return linear_2_truelog(linear, exp_func, log_func)
    # elif convert_to == chromaticity.ChromaticityType.LuvTrueLog:
    #     return linear_2_luvtruelog(linear)
    return None


def uniform_to_sRGB(images, convert_from, is_torch=True):
    return convert(images, convert_from, chromaticity.ChromaticityType.sRGB, is_torch)

def uniform_to_linear(images, convert_from, is_torch=True):
    return convert(images, convert_from, chromaticity.ChromaticityType.linear, is_torch)


# def srgb_2_linear(srgb_img, exp_func=None, log_func=None):
#     """Convert sRGB to linear RGB.
    
#     Args:
#         srgb_img: Input image in sRGB space (numpy array or PyTorch tensor)
#         exp_func: Optional exponential function (defaults to numpy/torch equivalent)
#         log_func: Optional logarithm function (not used but kept for API compatibility)
        
#     Returns:
#         Image in linear RGB space (same type as input)
#     """    
#     low_mask = srgb_img <= 0.04045
#     high_mask = srgb_img > 0.04045
#     if isinstance(srgb_img, torch.Tensor):
#         linear = torch.zeros_like(srgb_img, dtype=torch.float32)
#     else:
#         linear = np.zeros_like(srgb_img, dtype=np.float32)
#     linear[low_mask] = srgb_img[low_mask] / 12.92
#     linear[high_mask] = ((srgb_img[high_mask] + 0.055) / 1.055) ** 2.4
        
#     return linear

def srgb_2_linear(srgb_img, exp_func, log_func):
    '''Convert sRGB to linear RGB.'''
    '''inverse of: (x/255)^(1/2.22)*255'''
    # srgb_img = np.clip(srgb_img, 0, None) if isinstance(srgb_img, np.ndarray) else torch.clamp(srgb_img, min=0)
    return srgb_img ** 2.22


def gplog_2_linear(gplog_img, exp_func, log_func):
    '''Convert GP-Log to linear RGB.'''
    '''inverse of: ln(x/255*(e-1)+1)*255'''
    return (exp_func(gplog_img) - 1) / (np.exp(1) - 1)

# def truelog_2_linear(truelog_img, exp_func, log_func):
#     return exp_func(truelog_img * (np.log(1 + 1) / 1)) - 1

def truelog_2_linear(normalized_log, exp_func, log_func):
    # Define the same clipping function as in the original
    clip_func = lambda x: np.maximum(x * 255, 1.0) if isinstance(normalized_log, np.ndarray) else torch.maximum(x * 255, torch.tensor(1.0))
    
    # Define the same final_log_func to calculate log_min and log_max
    final_log_func = lambda x: log_func(exp_func(log_func(clip_func(x)) - 1) * 255 / (np.exp(1) - 1))
    
    # Calculate the same normalization bounds
    log_min = np.log(np.exp(np.log(1) - 1) * 255 / (np.exp(1) - 1))
    log_max = np.log(np.exp(np.log(255) - 1) * 255 / (np.exp(1) - 1))
    
    # Unnormalize (reverse of the normalization step)
    final_log = normalized_log * (log_max - log_min) + log_min
    
    # Reverse the final_log_func steps one by one:
    
    # 1. Apply exp to undo the outer log
    exp_final_log = exp_func(final_log)
    
    # 2. Multiply by (exp(1) - 1) / 255 to undo the scaling
    scaled_exp = exp_final_log * (np.exp(1) - 1) / 255
    
    # 3. Apply log to undo the exp
    log_scaled_exp = log_func(scaled_exp)
    
    # 4. Add 1 to undo the subtraction
    log_clip = log_scaled_exp + 1
    
    # 5. Apply exp to undo the log
    clip_val = exp_func(log_clip)
    
    # 6. Undo the clipping function
    if isinstance(normalized_log, np.ndarray):
        linear_img = np.where(clip_val > 1.0, clip_val / 255, 0.0)
    else:
        linear_img = torch.where(clip_val > 1.0, clip_val / 255, torch.tensor(0.0))
    
    return linear_img

# def linear_2_srgb(linear_img, exp_func, log_func):
#     '''Convert linear RGB to sRGB.'''
#     '''(x/255)^(1/2.22)*255'''
#     # make sur ethe values are non negative for back propagation
#     # linear_img = linear_img if isinstance(linear_img, np.ndarray) else torch.abs(linear_img)
#     # return (linear_img / 1) ** (1 / 2.22) * 1
#     low_mask = linear_img <= 0.0031308
#     high_mask = linear_img > 0.0031308
#     if isinstance(linear_img, torch.Tensor):
#         srgb = torch.zeros_like(linear_img, dtype=torch.float32)
#     else:
#         srgb = np.zeros_like(linear_img, dtype=np.float32)    
#     # Apply the inverse transformations
#     srgb[low_mask] = linear_img[low_mask] * 12.92
#     srgb[high_mask] = 1.055 * (linear_img[high_mask] ** (1/2.4)) - 0.055
    
#     return srgb

def linear_2_srgb(linear_img, exp_func, log_func):
    '''Convert linear RGB to sRGB.'''
    '''(x/255)^(1/2.22)*255'''
    # make sur ethe values are non negative for back propagation
    # linear_img = np.clip(linear_img, 0, None) if isinstance(linear_img, np.ndarray) else torch.clamp(linear_img, min=0)
    return linear_img ** (1 / 2.22)


def linear_2_gplog(linear_img, exp_func, log_func):
    '''Convert linear RGB to GP-Log.'''
    '''ln(x/255*(e-1)+1)*255'''
    return log_func((linear_img / 1) * (np.exp(1) - 1) + 1) * 1

# def linear_2_truelog(linear_img, exp_func, log_func):
#     '''Convert linear RGB to True Log'''
#     return log_func(linear_img + 1) * (1 / np.log(1 + 1))

def linear_2_truelog(linear_img, exp_func, log_func):
    clip_func = lambda x:np.maximum(x * 255, 1.0) if isinstance(x, np.ndarray) else torch.maximum(x * 255, torch.tensor(1.0))
    final_log_func = lambda x:log_func(exp_func(log_func(clip_func(x)) - 1) * 255 / (np.exp(1) - 1))
    final_log = final_log_func(linear_img)
    # Normalize
    log_min = np.log(np.exp(np.log(1) - 1) * 255 / (np.exp(1) - 1))
    log_max = np.log(np.exp(np.log(255) - 1) * 255 / (np.exp(1) - 1))
    # log_min = final_log.min()
    # log_max = final_log.max()
    # print(log_min, log_max)
    normalized_log = (final_log - log_min) / (log_max - log_min)
    return normalized_log



# =========+> True Log
# S2 = 255
# S1 = S2 / (np.exp(1) - 1)
# inner_term = (np.exp(images) - 1) * S1
# clamped_term = np.maximum(inner_term, 1)  # Clamps lower bound to 1
# true_log = np.log(clamped_term)
# true_log_min = np.min(true_log)
# true_log_max = np.max(true_log)
# normalized_true_log = (true_log - true_log_min) / (true_log_max - true_log_min)
# images = normalized_true_log
# =========+> True Log

# def srgb_to_linear(srgb_img, max_val=255):
#     """Convert sRGB to linear RGB."""
#     # Normalize to 0-1
#     srgb_img = srgb_img / max_val

#     # Apply transfer function
#     low_mask = srgb_img <= 0.04045
#     high_mask = srgb_img > 0.04045
#     linear = np.zeros_like(srgb_img, dtype=np.float32)
#     linear[low_mask] = srgb_img[low_mask] / 12.92
#     linear[high_mask] = ((srgb_img[high_mask] + 0.055) / 1.055) ** 2.4

#     return linear

# def true_log_transform(linear_rgb):
#     """Apply log transform to linear RGB values."""
#     S2 = 255
#     S1 = S2 / (np.exp(1) - 1)

#     # Scale to 0-255 and clamp minimum to 1
#     scaled_linear = linear_rgb * 255
#     clamped_values = np.maximum(scaled_linear, 1.0)

#     # First log transform
#     first_log = np.log(clamped_values)

#     # Exp(log(x)-1) transformation
#     Y = np.exp(first_log - 1) * S1

#     # Final log transform
#     final_log = np.log(Y)

#     # Normalize
#     log_min = np.min(final_log)
#     log_max = np.max(final_log)
#     normalized_log = (final_log - log_min) / (log_max - log_min)

#     return normalized_log

# linear = srgb_to_linear(images)
# images = true_log_transform(linear)


