The diagram shows the inheritance relationships and main attributes/methods for each class. The classes inherit from either ``pyg.Component`` or ``pyg.Panel`` base classes. Each class has its own specific implementation of ``__init__()`` with different parameters, and most component classes implement a ``length()`` method.

The main collar types represented are:

* Basic collar without panels (NoPanelsCollar)
* Turtle neck style collar (Turtle)
* Lapel style collar (SimpleLapel with SimpleLapelPanel)
* Hood style collar (Hood2Panels with HoodPanel)

Each class manages its own interfaces and stitching rules for connecting the collar components together.

```mermaid
classDiagram
    class NoPanelsCollar {
        +interfaces
        +__init__(name, body, design)
        +length()
    }

    class Turtle {
        +interfaces
        +front
        +back
        +stitching_rules
        +__init__(tag, body, design)
        +length()
    }

    class SimpleLapelPanel {
        +edges
        +interfaces
        +__init__(name, length, max_depth)
    }

    class SimpleLapel {
        +interfaces
        +front
        +back
        +stitching_rules
        +__init__(tag, body, design)
        +length()
    }

    class HoodPanel {
        +edges
        +interfaces
        +__init__(name, f_depth, b_depth, f_length, b_length, width, in_length, depth)
    }

    class Hood2Panels {
        +interfaces
        +panel
        +__init__(tag, body, design)
        +length()
    }

    pyg.Component <|-- NoPanelsCollar
    pyg.Component <|-- Turtle
    pyg.Panel <|-- SimpleLapelPanel
    pyg.Component <|-- SimpleLapel
    pyg.Panel <|-- HoodPanel
    pyg.Component <|-- Hood2Panels
```