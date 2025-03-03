import numpy as np
from internal import chromaticity
from internal import configs

DEFAULT_MAX_VAL = 255

def convert(images, config: configs.Config):
    return _convert(images, config.convert_from, config.convert_to, config.normalize)

def _convert(images, convert_from, convert_to, normalize=True):
    # input data range: (0, 1)
    # output data range: (0, 1)
    # rescale to 0-255
    images = images * DEFAULT_MAX_VAL
    linear = None
    if convert_from == chromaticity.ChromaticityType.sRGB:
        linear = srgb_2_linear(images)
    elif convert_from == chromaticity.ChromaticityType.GPLog:
        linear = gplog_2_linear(images)
    elif convert_from == chromaticity.ChromaticityType.linear:
        linear = images
    elif convert_from == chromaticity.ChromaticityType.TrueLog:
        linear = truelog_2_linear(images)
    divisor = 1
    if normalize:
        divisor = DEFAULT_MAX_VAL
    if convert_to == chromaticity.ChromaticityType.sRGB:
        return linear_2_srgb(linear) / divisor
    elif convert_to == chromaticity.ChromaticityType.GPLog:
        return linear_2_gplog(linear) / divisor
    elif convert_to == chromaticity.ChromaticityType.linear:
        return linear / divisor
    elif convert_to == chromaticity.ChromaticityType.TrueLog:
        return linear_2_truelog(linear) / divisor
    # elif convert_to == chromaticity.ChromaticityType.LuvTrueLog:
    #     return linear_2_luvtruelog(linear) / divisor
    return None


def uniform_to_sRGB(images, config):
    return _convert(images, config.convert_to, chromaticity.ChromaticityType.sRGB)


def srgb_2_linear(srgb_img, max_val=DEFAULT_MAX_VAL):
    '''Convert sRGB to linear RGB.'''
    '''inverse of: (x/255)^(1/2.22)*255'''
    return (srgb_img / max_val) ** 2.22 * max_val

def gplog_2_linear(gplog_img, max_val=DEFAULT_MAX_VAL):
    '''Convert GP-Log to linear RGB.'''
    '''inverse of: ln(x/255*(e-1)+1)*255'''
    return ((np.exp(gplog_img / max_val) - 1) / (np.exp(1) - 1)) * max_val

def truelog_2_linear(truelog_img, max_val=DEFAULT_MAX_VAL):
    return np.exp(log_img * (np.log(max_val + 1) / max_val)) - 1

def linear_2_srgb(linear_img, max_val=DEFAULT_MAX_VAL):
    '''Convert linear RGB to sRGB.'''
    '''(x/255)^(1/2.22)*255'''
    return (linear_img / max_val) ** (1 / 2.22) * max_val

def linear_2_gplog(linear_img, max_val=DEFAULT_MAX_VAL):
    '''Convert linear RGB to GP-Log.'''
    '''ln(x/255*(e-1)+1)*255'''
    return np.log((linear_img / max_val) * (np.exp(1) - 1) + 1) * max_val

def linear_2_truelog(linear_img, max_val=DEFAULT_MAX_VAL):
    '''Convert linear RGB to True Log'''
    return np.log(linear_img + 1) * (max_val / np.log(max_val + 1))

# def linear_2_luvtruelog(linear_image, max_val=DEFAULT_MAX_VAL):
#     S1 = max_val / (np.exp(1) - 1)

#     # Scale to 0-255 and clamp minimum to 1
#     clamped_values = np.maximum(linear_image, 1.0)

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

#     return normalized_log * max_val



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


