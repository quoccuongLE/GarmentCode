This diagram shows:

1. Inheritance relationships:
* BodiceFrontHalf and BodiceBackHalf inherit from BaseBodicePanel
* BodiceHalf and Shirt inherit from pyg.Component
* FittedShirt inherits from Shirt

2. Composition relationships:
* BodiceHalf contains BodiceFrontHalf and BodiceBackHalf
* Shirt contains two BodiceHalf instances (right and left)
* Key methods and attributes for each class

```mermaid
classDiagram
    class BaseBodicePanel {
        <<abstract>>
    }
    
    class BodiceFrontHalf {
        -width
        +__init__(name, body, design)
    }
    
    class BodiceBackHalf {
        -width
        +__init__(name, body, design)
        +get_width(level)
    }
    
    class BodiceHalf {
        -ftorso
        -btorso
        -sleeve
        -collar_comp
        +__init__(name, body, design, fitted)
        +eval_dep_params(body, design)
        +add_sleeves(name, body, design)
        +add_collars(name, body, design)
        +make_strapless(body, design)
        -_adjust_top_level(panel, out_level, in_level, target_remove)
        +length()
    }
    
    class Shirt {
        -right
        -left
        +__init__(body, design, fitted)
        +eval_dep_params(design)
        +length()
    }
    
    class FittedShirt {
        +__init__(body, design)
    }

    BaseBodicePanel <|-- BodiceFrontHalf
    BaseBodicePanel <|-- BodiceBackHalf
    pyg.Component <|-- BodiceHalf
    pyg.Component <|-- Shirt
    Shirt <|-- FittedShirt
    
    BodiceHalf *-- BodiceFrontHalf
    BodiceHalf *-- BodiceBackHalf
    Shirt *-- BodiceHalf

```