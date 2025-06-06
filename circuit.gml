graph [
  directed 1
  node [
    id 0
    label "1"
    type "resistor"
    value "1k&#937;"
  ]
  node [
    id 1
    label "2"
    type "capacitor"
    value "10&#956;F"
  ]
  node [
    id 2
    label "3"
    type "voltage_source"
    value "5V"
  ]
  node [
    id 3
    label "4"
    type "ground"
  ]
  edge [
    source 0
    target 1
    label "&#36830;&#25509;"
    resistance "0&#937;"
  ]
  edge [
    source 1
    target 2
    label "&#36830;&#25509;"
    resistance "0&#937;"
  ]
  edge [
    source 2
    target 3
    label "&#36820;&#22238;"
    resistance "0&#937;"
  ]
  edge [
    source 3
    target 0
    label "&#36820;&#22238;"
    resistance "0&#937;"
  ]
]
