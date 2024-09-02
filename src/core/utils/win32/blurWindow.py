import ctypes
from ctypes.wintypes import HWND

user32 = ctypes.windll.user32
dwm = ctypes.windll.dwmapi

# Define the ACCENTPOLICY structure
class ACCENTPOLICY(ctypes.Structure):
    _fields_ = [
        ("AccentState", ctypes.c_uint),
        ("AccentFlags", ctypes.c_uint),
        ("GradientColor", ctypes.c_uint),
        ("AnimationId", ctypes.c_uint)
    ]

# Define the WINDOWCOMPOSITIONATTRIBDATA structure
class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ("Attribute", ctypes.c_int),
        ("Data", ctypes.POINTER(ctypes.c_int)),
        ("SizeOfData", ctypes.c_size_t)
    ]

SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
SetWindowCompositionAttribute.argtypes = (HWND, ctypes.POINTER(WINDOWCOMPOSITIONATTRIBDATA))
SetWindowCompositionAttribute.restype = ctypes.c_int

# Define constants for DwmSetWindowAttribute
DWMWA_WINDOW_CORNER_PREFERENCE = 33
DWMWCP_DEFAULT = 0
DWMWCP_DONOTROUND = 1
DWMWCP_ROUND = 2
DWMWCP_ROUNDSMALL = 3
DWMWA_BORDER_COLOR = 34  # Correct constant for border color attribute

DWMWA_COLOR_NONE = 0xFFFFFFFE
DWMWA_COLOR_DEFAULT = 0xFFFFFFFF

def HEXtoRGBAint(HEX:str):
    alpha = HEX[7:]
    blue = HEX[5:7]
    green = HEX[3:5]
    red = HEX[1:3]

    gradientColor = alpha + blue + green + red
    return int(gradientColor, base=16)

def add_blur(hwnd, Acrylic=False, DarkMode=False):    
    accent = ACCENTPOLICY()
    accent.AccentState = 3  # Default window Blur #ACCENT_ENABLE_BLURBEHIND
    gradientColor = 0

    if Acrylic:
        accent.AccentState = 4  #ACCENT_ENABLE_ACRYLICBLURBEHIND
        accent.AccentFlags = 2
        gradientColor = HEXtoRGBAint('#ff000000')  # placeholder color

    accent.GradientColor = gradientColor
    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = 19  # WCA_ACCENT_POLICY
    data.SizeOfData = ctypes.sizeof(accent)
    data.Data = ctypes.cast(ctypes.pointer(accent), ctypes.POINTER(ctypes.c_int))
    SetWindowCompositionAttribute(hwnd, ctypes.byref(data))

    if DarkMode:
        data.Attribute = 26  # WCA_USEDARKMODECOLORS
        SetWindowCompositionAttribute(hwnd, ctypes.byref(data))

def set_window_corner_preference(hwnd, preference, BorderColor):
    # Set window corner preference
    preference_value = ctypes.c_int(preference)
    dwm.DwmSetWindowAttribute(hwnd, DWMWA_WINDOW_CORNER_PREFERENCE, ctypes.byref(preference_value), ctypes.sizeof(preference_value))
   
    if BorderColor == "None": 
        # Set transparent border color
        border_color_value = ctypes.c_int(DWMWA_COLOR_NONE)
    elif BorderColor == "System":
        # Set system default color
        border_color_value = ctypes.c_int(DWMWA_COLOR_DEFAULT)
    else:
        # Set custom color
         border_color_value = ctypes.c_int(HEXtoRGBAint(BorderColor))
 
    dwm.DwmSetWindowAttribute(hwnd, DWMWA_BORDER_COLOR, ctypes.byref(border_color_value), ctypes.sizeof(border_color_value))

def Blur(hwnd, Acrylic=False, DarkMode=False, RoundCorners=False, BorderColor="System"):
    hwnd = int(hwnd)
    add_blur(hwnd, Acrylic, DarkMode)
    if RoundCorners:
        set_window_corner_preference(hwnd, DWMWCP_ROUND, BorderColor)       