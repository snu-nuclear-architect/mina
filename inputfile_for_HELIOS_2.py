from __future__ import division
import  Initial_condition as Initial_condition
import components as components
import math


# region 1 core
Node1  = components.pipe("core inlet","pipe", 0.181, 0.02475 * 2, 'horizontal', 2.53e-6,1)
Node2  = components.discharge_into_vessel("inlet to downcomer","discharge_into_vessel",(0.1255-0.0605)/2,0.0495,0)
Node3  = components.pipe("down comer", "ring pipe", 1.403-0.181, [0.1255, 0.0605],"horizontal", 2.53e-6,1 )
Node4  = components.entrance_from_vessel_to_tube("lower plenum", "entrance_from_vessel_to_tube", 0.0055, 0, (4 * math.pi * (0.0495/2)**2 - 4 * math.pi * (0.00835)**2) / (math.pi * 0.0495 +  math.pi * (2 * 0.00835) ) )
Node5  = components.grid("grids","grids", 0.005,0.000693342598153,0.00141771437077,0.00173120427499,0,0.346240854998,0.315101743155,"horizontal")
Node6  = components.bundles("core bundles", "bundles",0.534,0.0495,"round","square",4,0.0127,0.01829,"horizontal")
Node7  = components.grid("grids","grids", 0.005,0.000693342598153,0.00141771437077,0.00173120427499,0,0.346240854998,0.315101743155,"horizontal")
Node8  = components.bundles("core bundles", "bundles",0.43876,0.0495,"round","square",4,0.0127,0.01829,"horizontal")
Node9  = components.grid("grids","grids", 0.005,0.000693342598153,0.00141771437077,0.00173120427499,0,0.346240854998,0.315101743155,"horizontal")
Node10 = components.bundles("core bundles", "bundles",0.32502,0.0495,"round","square",4,0.0127,0.01829,"horizontal")
Node11 = components.sudden_change("from bundles to upper plenum", "sudden expansion (area)", (math.pi * (0.0495 / 2) ** 2 - 4 * math.pi * (0.0127 / 2)**2 ), math.pi * (0.0495 / 2)**2 )
Node12 = components.pipe("upper plenum", "pipe", 2.11004-1.4284,0.0495,"horizontal",2.53e-6,1)



# endregion

# region 2
Node13 = components.pipe("pipe", "pipe", 0.3, 0.0495, "horizontal", 2.53e-6, 1)
Node14 = components.tee("tee-straight", "tee-straight", 0.3, 0.0495, 1, 2.53e-6,"horizontal")
Node15 = components.pipe("pipe", "pipe", 0.3, 0.0495, "horizontal", 2.53e-6, 1)

# endregion


# region 3
Node16 = components.pipe("pipe", "pipe", 1.045, 0.0495, "horizontal", 2.53e-6, 1)

# endregion

# region 4 (elbow with flange need more treatment)
Node17 = components.elbow("elbow", "elbow", 0.0495, 0.10104, 45, "horizontal", 2.53e-6)
Node18 = components.pipe("pipe", "pipe", 0.18068, 0.0495, "horizontal", 2.53e-6, 1)
Node19 = components.elbow("elbow", "elbow", 0.0495, 0.10104, 45, "horizontal", 2.53e-6)
Node20 = components.pipe("pipe", "pipe", 0.71886, 0.0495, "horizontal", 2.53e-6, 1)
Node21 = components.tee("tee-straight", "tee-straight", 0.3, 0.0495, 1, 2.53e-6,"horizontal")
Node22 = components.pipe("pipe", "pipe", 0.17111, 0.0495, "horizontal", 2.53e-6, 1)
Node23 = components.elbow("elbow", "elbow", 0.0495, 0.10104, 45, "horizontal", 2.53e-6)
Node24 = components.pipe("pipe", "pipe", 0.18068, 0.0495, "horizontal", 2.53e-6, 1)
Node25 = components.elbow("elbow", "elbow", 0.0495, 0.10104, 45, "horizontal", 2.53e-6)
# endregion


# region 5
Node26 = components.sudden_change("sudden expansion", "sudden expansion", 0.0495, 0.052)
Node27 = components.gate_valve("gate valve", "gate valve", 0.216, 0.052, 0.037, "horizontal")
Node28 = components.sudden_change("sudden contraction", "sudden expansion", 0.052, 0.0495)
# endregion

# region 6
Node29 = components.pipe("pipe", "pipe", 1, 0.0495, "horizontal", 2.53e-6, 1)
# endregion

# region 7
Node30 = components.pipe("pipe", "pipe", 1, 0.0495, "horizontal", 2.53e-6, 1)
# endregion


# region 8

Node31 = components.pipe("pipe", "pipe", 0.2, 0.0495, "horizontal", 2.53e-6, 1)
Node32 = components.sudden_change("sudden expansion", "sudden expansion", 0.0495, 0.0529)
Node33 = components.orifice("orifice", "orifice", 0.4, 0.0529, "horizontal", 2.53e-6, 0.03246)
Node34 = components.sudden_change("sudden contraction", "sudden expansion", 0.0529, 0.0495)
Node35 = components.pipe("pipe", "pipe", 0.2, 0.0495, "horizontal", 2.53e-6, 1)
# endregion

# region 9
Node36 = components.pipe("pipe", "pipe", 0.5, 0.0495, "horizontal", 2.53e-6, 1)
# endregion

# region 10
Node37 = components.pipe("expansion tank inlet pipe", "pipe", 0.334, 0.0495, "horizontal",2.53e-6,1)
Node38 = components.discharge_into_vessel("discharge into expansion tank", "discharge into vessel", 0.15, 0.0495, 0)
Node39 = components.entrance_from_vessel_to_tube("entrance into pipe from expansion tank", "entrence from vessel to tube", 0.0055, 0, 0.0495)
Node40 = components.elbow("elbow", "elbow", 0.0495, 0.10095, 45, "horizontal", 2.53e-6)
# endregion

# region 11
Node41 = components.pipe("pipe", "pipe", 0.5, 0.0495, "horizontal", 2.53e-6, 1)
# endregion

# region 12
Node42 = components.pipe("pipe", "pipe", 0.3, 0.0495, "horizontal", 2.53e-6, 1)
Node43 = components.tee("tee-straight", "tee-straight", 0.3, 0.0495, 1, 2.53e-6,"horizontal")
Node44 = components.pipe("pipe", "pipe", 0.30511, 0.0495, "horizontal", 2.53e-6, 1)
Node45 = components.elbow("elbow", "elbow", 0.0495, 0.10095, 90, "horizontal", 2.53e-6)
Node46 = components.elbow("elbow", "elbow", 0.0495, 0.10095, 90, "horizontal", 2.53e-6)
Node47 = components.pipe("pipe", "pipe", 0.2, 0.0495, "horizontal", 2.53e-6, 1)
# endregion

# region 13
Node48 = components.sudden_change("sudden expansion", "sudden expansion", 0.0495, 0.052)
Node49 = components.gate_valve("gate valve", "gate valve", 0.216, 0.052, 0.037, "horizontal")
Node50 = components.sudden_change("sudden contraction", "sudden expansion", 0.052, 0.0495)
# endregion

# region 14
Node51 = components.pipe("pipe", "pipe", 0.2, 0.0495, "horizontal", 2.53e-6, 1)
Node52 = components.tee("tee-straight", "tee-straight", 0.3, 0.0495, 1, 2.53e-6,"horizontal")
Node53 = components.pipe("pipe", "pipe", 0.38232, 0.0495, "horizontal", 2.53e-6, 1)
# endregion

# region 15 heat exchanger
Node54 = components.pipe("heat exchanger inlet", "pipe", 0.1392,0.0495, "horizontal",2.53e-6, 1)
Node55 = components.discharge_into_vessel("inlet to downcomer", "discharge_into_vessel", 0.1266/2, 0.0495, 0)
Node56 = components.bundles("heat exchanger bundles", "bundles", 0.305 - (0.13025 + 0.035 - 0.08467), 0.1266, "round", "square", 2, 0.034, 0.0305 + 0.034, "horizontal")
Node57 = components.grid("heat exchanger grid", "grid", 0.005, 0.00378, 0.010772175634, 0.00284128113769,0, 0.568256227539, 0.106814150222, "horizontal")
Node58 = components.bundles("heat exchanger bundles", "bundles", 0.295, 0.1266, "round", "square", 2, 0.034, 0.0305 + 0.034, "horizontal")
Node59 = components.grid("heat exchanger grid", "grid", 0.005, 0.00378, 0.010772175634, 0.00284128113769,0, 0.568256227539, 0.106814150222, "horizontal")
Node60 = components.bundles("heat exchanger bundles", "bundles", 0.295, 0.1266, "round", "square", 2, 0.034, 0.0305 + 0.034, "horizontal")
Node61 = components.grid("heat exchanger grid", "grid", 0.005, 0.00378, 0.010772175634, 0.00284128113769,0, 0.568256227539, 0.106814150222, "horizontal")
Node62 = components.bundles("heat exchanger bundles", "bundles", 0.295, 0.1266, "round", "square", 2, 0.034, 0.0305 + 0.034, "horizontal")
Node63 = components.grid("heat exchanger grid", "grid", 0.005, 0.00378, 0.010772175634, 0.00284128113769,0, 0.568256227539, 0.106814150222, "horizontal")
Node64 = components.bundles("heat exchanger bundles", "bundles", 0.295, 0.1266, "round", "square", 2, 0.034, 0.0305 + 0.034, "horizontal")
Node65 = components.grid("heat exchanger grid", "grid", 0.005, 0.00378, 0.010772175634, 0.00284128113769,0, 0.568256227539, 0.106814150222, "horizontal")
Node66 = components.bundles("heat exchanger bundles", "bundles", 0.295, 0.1266, "round", "square", 2, 0.034, 0.0305 + 0.034, "horizontal")
Node67 = components.grid("heat exchanger grid", "grid", 0.005, 0.00378, 0.010772175634, 0.00284128113769,0, 0.568256227539, 0.106814150222, "horizontal")
Node68 = components.bundles("heat exchanger bundles", "bundles", 0.306 + 0.14033 - 0.035 - 0.13025, 0.1266, "round", "square", 2, 0.034, 0.0305 + 0.034, "horizontal")
Node69 = components.pipe("heat exchanger inlet", "pipe", 0.1392,0.0495, "horizontal",2.53e-6, 1)
# endregion

# region 16
Node70 = components.pipe("pipe", "pipe", 0.21975, 0.0495, "horizontal", 2.53e-6, 1)
Node71 = components.elbow("elbow", "elbow", 0.0495, 0.10095, 90, "horizontal", 2.53e-6)
Node72 = components.pipe("pipe", "pipe", 0.7855, 0.0495, "horizontal", 2.53e-6, 1)
Node73 = components.tee("tee-straight", "tee-straight", 0.3, 0.0495, 1, 2.53e-6,"horizontal")
Node74 = components.pipe("pipe", "pipe", 0.5, 0.0495, "horizontal", 2.53e-6, 1)
# endregion

# region 17
Node75 = components.sudden_change("sudden expansion", "sudden expansion", 0.0495, 0.052)
Node76 = components.gate_valve("gate valve", "gate valve", 0.216, 0.052, 0.037, "horizontal")
Node77 = components.sudden_change("sudden contraction", "sudden expansion", 0.052, 0.0495)
# endregion

# region 18
Node78 = components.pipe("pipe", "pipe", 0.5, 0.0495, "horizontal", 2.53e-6, 1)
Node79 = components.tee("tee-straight", "tee-straight", 0.3, 0.0495, 1, 2.53e-6,"horizontal")
Node80 = components.pipe("pipe", "pipe", 0.5, 0.0495, "horizontal", 2.53e-6, 1)
# endregion

# region 19
Node81 = components.pipe("pipe", "pipe", 1, 0.0495, "horizontal", 2.53e-6, 1)
# endregion

# region 20
Node82 = components.pipe("pipe", "pipe", 0.5, 0.0495, "horizontal", 2.53e-6, 1)
Node83 = components.tee("tee-straight", "tee-straight", 0.3, 0.0495, 1, 2.53e-6,"horizontal")
# endregion


# region 24
Node84 = components.pipe("pipe", "pipe", 1, 0.0495, "horizontal", 2.53e-6, 1)
Node85 = components.pipe("pipe", "pipe", 1, 0.0495, "horizontal", 2.53e-6, 1)
Node86 = components.pipe("pipe", "pipe", 0.05227, 0.0495, "horizontal", 2.53e-6, 1)
Node87 = components.elbow("elbow", "elbow", 0.0495, 0.10095, 90, "horizontal", 2.53e-6)
Node88 = components.elbow("elbow", "elbow", 0.0495, 0.10095, 45, "horizontal", 2.53e-6)
Node89 = components.pipe("pipe", "pipe", 0.2172, 0.0495, "horizontal", 2.53e-6, 1)
Node90 = components.sudden_change("sudden expansion", "sudden expansion", 0.0495, 0.052)
Node91 = components.gate_valve("gate valve", "gate valve", 0.216, 0.052, 0.037, "horizontal")
Node92 = components.sudden_change("sudden contraction", "sudden expansion", 0.052, 0.0495)
Node93 = components.pipe("pipe", "pipe", 0.3, 0.0495, "horizontal", 2.53e-6, 1)
Node94 = components.tee("tee-straight", "tee-straight", 0.3, 0.0495, 1, 2.53e-6,"horizontal")
Node95 = components.pipe("pipe", "pipe", 0.3, 0.0495, "horizontal", 2.53e-6, 1)
# endregion

Node96 = components.gate_valve("gate valve", "gate valve", 0.216, 0.052, 0.037, "horizontal")
Node97 = components.sudden_change("sudden contraction", "sudden expansion", 0.052, 0.0495)
Node98 = components.elbow("elbow", "elbow", 0.0495, 0.10095, 45, "horizontal", 2.53e-6)
Node99 = components.pipe("pipe", "pipe", 0.18068, 0.0495, "horizontal", 2.53e-6, 1)
Node100 = components.elbow("elbow", "elbow", 0.0495, 0.10095, 45, "horizontal", 2.53e-6)
Node101 = components.tee("tee-straight", "tee-straight", 0.3, 0.0495, 1, 2.53e-6,"horizontal")
Node102 = components.elbow("elbow", "elbow", 0.0495, 0.10095, 45, "horizontal", 2.53e-6)
Node103 = components.pipe("pipe", "pipe", 0.18068, 0.0495, "horizontal", 2.53e-6, 1)
Node104 = components.elbow("elbow", "elbow", 0.0495, 0.10095, 45, "horizontal", 2.53e-6)

Node_init = Initial_condition.Initial_condition(273 + 250, 0, 10)
Node1.calculation(Node_init)



for i in range(1, 102):
    print i
    eval( 'Node{0}.calculation( Node{1} )'.format( i+1, i ) )
    accumulated_length += eval("Node{0}.length".format(i+1))
print Node102.P_out

print "core region pressure drop:", Node12.P_out - 0
print "accumulated_length=",accumulated_length