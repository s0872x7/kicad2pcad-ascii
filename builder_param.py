builder_layers = {
    # P-CAD ASCII layer types:
    # Signal, Plane, NonSignal

    -1: "null",     # LT_UNDEFINED
    0: "Signal",    # LT_SIGNAL
    1: "Plane",     # LT_POWER
    2: "NonSignal", # LT_MIXED
    3: "Plane"      # LT_JUMPER
}

builder_padshapes = {
    # P-CAD ASCII padshape types:
    # padViaShapeType(
    #   Ellipse, Oval, Rect, RndRect, Thrm2, Thrm2_90,
    #   Thrm4, Thrm4_45, Direct, NoConnect, Polygon
    # )

    0: "Ellipse", # PAD_SHAPE_CIRCLE
    1: "Rect", # PAD_SHAPE_RECT
    2: "Oval", # PAD_SHAPE_OVAL
    3: "", # PAD_SHAPE_TRAPEZOID
    4: "RndRect", # PAD_SHAPE_ROUNDRECT
    5: "", # PAD_SHAPE_CHAMFERED_RECT
    6: "Polygon"  # PAD_SHPAE_CUSTOM
}

builder_fontRenderer_Stroke    = 0
builder_fontRenderer_TrueType  = 2

builder_fontFamily_Serif    = 0
builder_fontFamily_Sanserif = 1
builder_fontFamily_Modern   = 2

builder_fontRenderers = {
    builder_fontRenderer_Stroke: "Stroke",
    builder_fontRenderer_TrueType: "TrueType"
}

builder_fontFamilies = {
    builder_fontFamily_Serif: "Serif",
    builder_fontFamily_Sanserif: "Sanserif",
    builder_fontFamily_Modern: "Modern"
}

class builder_param:
    is_mm = True
    used_fontFamily = builder_fontFamily_Sanserif

