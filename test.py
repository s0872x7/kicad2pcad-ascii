import builder
from pcbnew import *

ToUnits = ToMM
FromUnits = FromMM

padshapes = {
    PAD_SHAPE_CIRCLE: "PAD_SHAPE_CIRCLE",
    PAD_SHAPE_OVAL: "PAD_SHAPE_OVAL",
    PAD_SHAPE_RECT: "PAD_SHAPE_RECT",
    PAD_SHAPE_TRAPEZOID: "PAD_SHAPE_TRAPEZOID"
}

pcbpath = "C:/Program Files/KiCad/share/kicad/demos/sonde xilinx/sonde xilinx.kicad_pcb"
board = LoadBoard(pcbpath)



'''
for module in board.GetModules():
    print "* Module: %s at %s"%(module.GetReference(), ToUnits(module.GetPosition()))
    print " - Pad Count: %d"%(module.GetPadCount())

    for pad in module.Pads():
        print("pad {}({}) on {}({}) at {},{} shape {} size {},{}"
            .format(pad.GetPadName(),
                    pad.GetNet().GetNetname(),
                    module.GetReference(),
                    module.GetValue(),
                    pad.GetPosition().x, pad.GetPosition().y,
                    padshapes[pad.GetShape()],
                    pad.GetSize().x, pad.GetSize().y
        ))
'''

'''
for item in board.GetDrawings():
    if type(item) is TEXTE_PCB:
        print "* Text:    '%s' at %s"%(item.GetText(), item.GetPosition())
    elif type(item) is DRAWSEGMENT:
        print "* Drawing: %s"%item.GetShapeStr() # dir(item)
    else:
        print type(item)
'''

print(builder.build(pcbpath))

