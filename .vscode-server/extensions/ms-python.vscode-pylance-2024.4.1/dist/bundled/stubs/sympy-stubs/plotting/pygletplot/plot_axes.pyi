from sympy.plotting.pygletplot.plot_object import PlotObject

class PlotAxes(PlotObject):
    def __init__(self, *args, style=..., none=..., frame=..., box=..., ordinate=..., stride=..., visible=..., overlay=..., colored=..., label_axes=..., label_ticks=..., tick_length=..., font_face=..., font_size=..., **kwargs) -> None:
        ...
    
    def reset_resources(self) -> None:
        ...
    
    def reset_bounding_box(self) -> None:
        ...
    
    def draw(self) -> None:
        ...
    
    def adjust_bounds(self, child_bounds) -> None:
        ...
    
    def toggle_visible(self) -> None:
        ...
    
    def toggle_colors(self) -> None:
        ...
    


class PlotAxesBase(PlotObject):
    def __init__(self, parent_axes) -> None:
        ...
    
    def draw(self) -> None:
        ...
    
    def draw_background(self, color) -> None:
        ...
    
    def draw_axis(self, axis, color):
        ...
    
    def draw_text(self, text, position, color, scale=...) -> None:
        ...
    
    def draw_line(self, v, color) -> None:
        ...
    


class PlotAxesOrdinate(PlotAxesBase):
    def __init__(self, parent_axes) -> None:
        ...
    
    def draw_axis(self, axis, color) -> None:
        ...
    
    def draw_axis_line(self, axis, color, a_min, a_max, labels_visible) -> None:
        ...
    
    def draw_axis_line_labels(self, axis, color, axis_line) -> None:
        ...
    
    def draw_tick_line(self, axis, color, radius, tick, labels_visible) -> None:
        ...
    
    def draw_tick_line_label(self, axis, color, radius, tick) -> None:
        ...
    


class PlotAxesFrame(PlotAxesBase):
    def __init__(self, parent_axes) -> None:
        ...
    
    def draw_background(self, color) -> None:
        ...
    
    def draw_axis(self, axis, color):
        ...
    


