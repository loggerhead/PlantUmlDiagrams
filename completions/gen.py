import json

kk = [
"actor", "participant", "usecase", "class", "interface", "abstract", "enum", "component", "state", "object", "artifact", "folder", "rectangle", "node", "frame", "cloud", "database", "storage", "agent", "stack", "boundary", "control", "entity", "card", "file", "package", "queue", "archimate", "diamond", "detach", "collections",
"@startuml", "@enduml", "@startdot", "@enddot", "@startsalt", "@endsalt",
"alt", "else", "opt", "looppar", "break", "critical", "group",
"as", "also", "autonumber", "caption", "title", "newpage", "box", "alt", "else", "opt", "loop", "par", "break", "critical", "note", "rnote", "hnote", "legend", "group", "left", "right", "of", "on", "link", "over", "end", "activate", "deactivate", "destroy", "create", "footbox", "hide", "show", "skinparam", "skin", "top", "bottom", "toptobottomdirection", "package", "namespace", "page", "up", "down", "if", "else", "elseif", "endif", "partition", "footer", "header", "center", "rotate", "ref", "return", "is", "repeat", "start", "stop", "while", "endwhile", "fork", "again", "kill", "order", "allow_mixing", "allowmixing", "mainframe", "accross", "colors", "chocolate", "lastpage",
"!exit", "!include", "!pragma", "!define", "!undef", "!if", "!ifdef", "!endif", "!ifndef", "!else", "!definelong", "!enddefinelong",
"AliceBlue", "AntiqueWhite", "Aqua", "Aquamarine", "Azure", "Beige", "Bisque", "Black", "BlanchedAlmond", "Blue", "BlueViolet", "Brown", "BurlyWood", "CadetBlue", "Chartreuse", "Chocolate", "Coral", "CornflowerBlue", "Cornsilk", "Crimson", "Cyan", "DarkBlue", "DarkCyan", "DarkGoldenRod", "DarkGray", "DarkGreen", "DarkGrey", "DarkKhaki", "DarkMagenta", "DarkOliveGreen", "DarkOrchid", "DarkRed", "DarkSalmon", "DarkSeaGreen", "DarkSlateBlue", "DarkSlateGray", "DarkSlateGrey", "DarkTurquoise", "DarkViolet", "Darkorange", "DeepPink", "DeepSkyBlue", "DimGray", "DimGrey", "DodgerBlue", "FireBrick", "FloralWhite", "ForestGreen", "Fuchsia", "Gainsboro", "GhostWhite", "Gold", "GoldenRod", "Gray", "Green", "GreenYellow", "Grey", "HoneyDew", "HotPink", "IndianRed", "Indigo", "Ivory", "Khaki", "Lavender", "LavenderBlush", "LawnGreen", "LemonChiffon", "LightBlue", "LightCoral", "LightCyan", "LightGoldenRodYellow", "LightGray", "LightGreen", "LightGrey", "LightPink", "LightSalmon", "LightSeaGreen", "LightSkyBlue", "LightSlateGray", "LightSlateGrey", "LightSteelBlue", "LightYellow", "Lime", "LimeGreen", "Linen", "Magenta", "Maroon", "MediumAquaMarine", "MediumBlue", "MediumOrchid", "MediumPurple", "MediumSeaGreen", "MediumSlateBlue", "MediumSpringGreen", "MediumTurquoise", "MediumVioletRed", "MidnightBlue", "MintCream", "MistyRose", "Moccasin", "NavajoWhite", "Navy", "OldLace", "Olive", "OliveDrab", "Orange", "OrangeRed", "Orchid", "PaleGoldenRod", "PaleGreen", "PaleTurquoise", "PaleVioletRed", "PapayaWhip", "PeachPuff", "Peru", "Pink", "Plum", "PowderBlue", "Purple", "Red", "RosyBrown", "RoyalBlue", "SaddleBrown", "Salmon", "SandyBrown", "SeaGreen", "SeaShell", "Sienna", "Silver", "SkyBlue", "SlateBlue", "SlateGray", "SlateGrey", "Snow", "SpringGreen", "SteelBlue", "Tan", "Teal", "Thistle", "Tomato", "Turquoise", "Violet", "Wheat", "White", "WhiteSmoke", "Yellow", "YellowGreen",
]

d = {
  "scope": "source.plantuml",
  "completions": [
  ]
}

with open('plantuml.sublime-completions', 'w') as f:
    for k in sorted(kk):
        d["completions"].append({ "trigger": k.lower(), "contents": k })
    f.write(json.dumps(d, indent=4))