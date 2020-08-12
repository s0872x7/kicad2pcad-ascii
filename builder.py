from conf import *
from builder_param import *
from pcbnew import *
import time

def build(path, param=builder_param()):
    board = LoadBoard(path)
    build = ""

    # build ascii header
    build += build_header(board, param)

    # build library table
    build += build_lib_table(board, param)

    # build netlist table

    # build pcbdoc

    # build ref table

    # pass the document
    return build

def build_header(board=BOARD(), param=builder_param()):
    build = "PCAD_ASCII \"{0}\" \n".format(board.GetFileName())
    
    # TODO: export pcb project name
    build += "asciiNameDef {0} \n\n".format("null")

    build += "(asciiHeader \r\n"
    build += "  (asciiVersion {0} {1}) \n".format(PCAD_VER_MAJOR, PCAD_VER_MINOR)
    build += "  (fileUnits {0}) \n".format("mm" if param.is_mm else "in")
    build += "  (headerString \"{0}\") \n".format("null")

    # Seoul time zone
    build += "  (timeStamp {0}) \n".format(time.strftime("%Y %m %d %I %M %S", time.localtime(1575142526.500323)))
    
    build += "  (fileAuthor \"{0}\")\n".format("unkwon author")
    build += "  (copyright \"{0}\")\n".format("unkwon license")
    build += "  (program {0} {1}) \n".format(CONVERTER_INFO, CONVERTER_VER)

    build += ") \n\n"

    return build

def build_lib_table(board=BOARD(), param=builder_param()):
    # TODO: build each kicad footprint libraries

    build = "(library \"{0}\" \n".format("all_kicadlib")

    # build style defs
    build += build_lib_pads(board, param)
    build += build_lib_vias(board, param)
    build += build_lib_texts(board, param)

    # build pattern defs


    build += ") \n\n"

    return build

def build_lib_default(board=BOARD(), param=builder_param()):
    # TODO: make sure that pcbnew and P-CAD requires default pad type.
    build = ""

    return build

def build_lib_pads(board=BOARD(), param=builder_param()):
    # TODO: build hash table for each pads

    # Due to pcbnew document has not original footprint data,
    # P-CAD ASCII library which is template data will be as modified module data of a pcbnew document

    build = ""
    unit = "mm" if param.is_mm else "in"
    tou = ToMM if param.is_mm else FromMM

    for mod in board.GetModules():
        for pad in mod.Pads():
            build += "  (padStyleDef \"{0}:{1}_pad({2})\" \n".format(
                mod.GetFPID().GetLibNickname(), mod.GetFPID().GetLibItemName(), pad.GetPadName()
            )

            # P-CAD ASCII V7.5 doesn't support pcbnew's pad to die length feature
            # P-CAD ASCII V7.5 doesn't support 2D size of pad hole
            # pcbnew support isHolePlated?
            build += "    (holeDiam {0}{4}) (holeOffset {1}{4} {2}{4}) (isHolePlated {3})\n".format(
                tou(pad.GetDrillSize().x), tou(pad.GetOffset().x), tou(pad.GetOffset().y), False, unit
            )

            # pcbnew only support micro-via in via-type
            build += "    (startRange {0}) (endRange {1}) (localSwell {2}{3})\n".format("LAYER_TOP", "LAYER_BOTTOM", 0, unit)

            build += "    (padShape \n"
            build += "      (layerNumRef {0}) (layerType {1}) \n".format( pad.GetLayer(), builder_layers[board.GetLayerType(pad.GetLayer())] )
            build += "      (padShapeType {0}) (shapeWidth {1}{3}) (shapeHeight {2}{3}) \n".format(
                builder_padshapes[pad.GetShape()], tou(pad.GetSize().x), tou(pad.GetSize().y), unit
            )

            # pcbnew doesn't support sides
            # pcbnew doesn't support outsideDiam
            build += "      (sides {0}) (rotation {1}degrees) (outsideDiam {2}{3}) \n".format(0, pad.GetOrientationDegrees(), 0, unit)

            build += "      (spokeWidth {0}{2}) (noCopperPourConnect {1}) \n".format(
                tou(pad.GetThermalWidth()), pad.GetZoneConnection() == PAD_ZONE_CONN_NONE, unit
            )
            build += "    ) \n"
            build += "  ) \n\n"

    return build
        
def build_lib_vias(board=BOARD(), param=builder_param()):
    build = ""
    unit = "mm" if param.is_mm else "in"
    tou = ToMM if param.is_mm else FromMM

    # access private variable of BOARD_DESIGN_SETTINGS
    for i in range(0, len(board.GetDesignSettings().m_ViasDimensionsList)):
        dim = board.GetDesignSettings().m_ViasDimensionsList[i]

        build += "  (viaStyleDef \"AUTO_via{0}\" \n".format(i)
        build += "    (holeDiam {0}{4}) (holeOffset {1}{4} {2}{4}) (isHolePlated {3})\n".format(
            tou(dim.m_Drill), 0, 0, False, unit
        )
        build += "    (startRange {0}) (endRange {1}) (useGlobalSwell {2}) (localSwell {3}{4})\n".format(
            "LAYER_TOP", "LAYER_BOTTOM", False, 0, unit
        )
        
        # build F_Cu pad
        build += "    (viaShape "
        build += "(layerNumRef {0}) (layerType {1}) ".format(
            F_Cu, builder_layers[board.GetLayerType(F_Cu)]
        )
        build += "(shapeWidth {0}{1}) (shapeHeight {0}{1}) ".format(
            tou(dim.m_Diameter), unit
        )
        build += ") \n"

        # build B_Cu pad
        build += "    (viaShape "
        build += "(layerNumRef {0}) (layerType {1}) ".format(
            F_Cu, builder_layers[board.GetLayerType(F_Cu)]
        )
        build += "(shapeWidth {0}{1}) (shapeHeight {0}{1}) ".format(
            tou(dim.m_Diameter), unit
        )
        build += ") \n"

        build += "  ) \n\n"   

    return build

def build_lib_texts(board=BOARD(), param=builder_param()):
    build = ""
    unit = "mm" if param.is_mm else "in"
    tou = ToMM if param.is_mm else FromMM

    # build TEXTE_PCB
    filt = [_ for _ in board.GetDrawings() if _.Type() == PCB_TEXT_T]
    for i in range(0, len(filt)):
        text = filt[i]

        build += "  (textStyleDef \"AUTO_pcbtext{0}\" \n".format(i)
        build += "    (font \n"
        build += "      (fontType {0}) (fontFamily {1}) (fontFace {2}) \n".format(
            builder_fontRenderers[builder_fontRenderer_Stroke], builder_fontFamilies[param.used_fontFamily], "null"
        )
        build += "      (fontHeigth {0}{2}) (strokeWidth {1}{2}) \n".format(
            tou(text.GetTextSize().y), tou(text.GetTextSize().x), unit
        )

        # font weight, italic, charset, OutPrecision, ClipPrecision,
        # Quality and PitchAndFamily are specified when using a TrueType

        build += "    ) \n"
        build += "    (textStyleAllowTType {0}) (textStyleDisplayTType {1}) \n".format(False, False)
        build += "  ) \n\n"

    # build TEXTE_MODULE
    filt = [_ for _ in board.GetDrawings() if _.Type() == PCB_MODULE_TEXT_T]
    for i in range(0, len(filt)):
        text = filt[i]

        build += "  (textStyleDef \"AUTO_moduletext{0}\" \n".format(i)
        build += "    (font \n"
        build += "      (fontType {0}) (fontFamily {1}) (fontFace {2}) \n".format(
            builder_fontRenderers[builder_fontRenderer_Stroke], builder_fontFamilies[param.used_fontFamily], "null"
        )
        build += "      (fontHeigth {0}{2}) (strokeWidth {1}{2}) \n".format(
            tou(text.GetTextSize().y), tou(text.GetTextSize().x), unit
        )

        # font weight, italic, charset, OutPrecision, ClipPrecision,
        # Quality and PitchAndFamily are specified when using a TrueType

        build += "    ) \n"
        build += "    (textStyleAllowTType {0}) (textStyleDisplayTType {1}) \n".format(False, False)
        build += "  ) \n\n"

    return build
            
def build_lib_pattern(board=BOARD(), param=builder_param()):
    build = ""
    unit = "mm" if param.is_mm else "in"
    tou = ToMM if param.is_mm else FromMM

    build += 
