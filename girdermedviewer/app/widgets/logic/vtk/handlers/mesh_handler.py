import logging
from abc import ABC, abstractmethod

from trame_dataclass.v2 import get_instance
from vtk import vtkPolyData, vtkRenderer

from ....utils import (
    ColorPresetParser,
    DataArray,
    MeshColoringMode,
    convert_color_hex_to_normalized_rgb,
    render_mesh_in_3D,
    render_mesh_in_slice,
    render_streamline_in_slice,
    set_mesh_opacity,
    set_mesh_solid_color,
    set_mesh_visibility,
    create_scalar_bar_actor    
)

from ...scene.objects.mesh_object_logic import MeshDisplay
from .object_handler import ObjectHandler

logger = logging.getLogger(__name__)


class MeshHandler(ObjectHandler, ABC):
    def __init__(self, preset_parser: ColorPresetParser, renderer: vtkRenderer):
        super().__init__(renderer)
        self.preset_parser = preset_parser

    @abstractmethod
    def add_mesh(self, data_id: str, poly_data: vtkPolyData) -> None:
        pass

    @abstractmethod
    def update_mesh_visibility(self, data_id: str, visible: bool) -> bool:
        pass

    def update_mesh_opacity(self, data_id: str, data_display: MeshDisplay) -> bool:
        logger.debug(f"set_mesh_opacity({data_id}): {data_display.opacity}")
        modified = False
        for actor in self.get_actors(data_id):
            modified = set_mesh_opacity(actor, data_display.opacity) or modified
        return modified

    def update_mesh_solid_color(self, data_id: str, data_display: MeshDisplay) -> bool:
        color_tuple = convert_color_hex_to_normalized_rgb(data_display.solid_color)
        logger.debug(f"set_mesh_solid_color({data_id}): {color_tuple}")
        modified = False
        
        for actor in self.get_actors(data_id):
            modified = set_mesh_solid_color(actor, color_tuple) or modified
        # Hide scalarbar when solid is selected 
        self._refresh_scalar_bar(data_id, data_display)
        return modified

    def update_mesh_array_color(self, data_id: str, data_display: MeshDisplay) -> bool:
        array_color = data_display.array_color
        active_array = get_instance(data_display.active_array_id)

        logger.debug(f"set_mesh_array_color({data_id}): {array_color.name}")
        preset = self.preset_parser.get_preset_by_name(array_color.name)
        if preset is None:
            return False

        modified = False
        for actor in self.get_actors(data_id):
            modified = (
                self.preset_parser.apply_preset_to_mesh(
                    actor,
                    active_array,
                    preset,
                    array_color.array_range,
                    array_color.is_inverted,
                )
                or modified
            )
        
        # Whenever the array is changed, trigger a synchronization of the scalar bar, so that displays the values of the new array. Also, this is triggered when changing the preset.
        self._refresh_scalar_bar(data_id, data_display)
        
        return modified
       
    
    def _refresh_scalar_bar(self, data_id: str, data_display: MeshDisplay, mesh_visible: bool = True) -> bool:
        """Single source of truth for scalar bar title/visibility/lookup table."""
        scalar_bar = self.scalar_bars.get(data_id)
        if not scalar_bar:
            return False

        active_array = get_instance(data_display.active_array_id)
        actor = next(iter(self.get_actors(data_id)), None)
        if actor:
            scalar_bar.SetLookupTable(actor.GetMapper().GetLookupTable())
        
        show = (
            isinstance(active_array, DataArray)
            and data_display.show_colorbar
            and active_array.coloring_mode == MeshColoringMode.ARRAY
            and mesh_visible
        )

        if show:
            scalar_bar.SetTitle(active_array.title)

        scalar_bar.SetVisibility(show)
        return True
    
    def has_mesh(self) -> bool:
        return len(list(self.object_data)) > 0

    def apply_data_display(self, data_id: str, data_display: MeshDisplay) -> None:
        # Set opacity
        self.update_mesh_opacity(data_id, data_display)

        # Set color
        active_array = get_instance(data_display.active_array_id)
        assert isinstance(active_array, DataArray)
        if active_array.coloring_mode == MeshColoringMode.SOLID:
            self.update_mesh_solid_color(data_id, data_display)

        elif active_array.coloring_mode == MeshColoringMode.ARRAY:
            self.update_mesh_array_color(data_id, data_display)

        # Set visibility
        self.update_mesh_visibility(data_id, data_display)
        self.renderer.GetRenderWindow().Render()
        
    def unregister_data(self, data_id, only_data=None, remove=True):
        super().unregister_data(data_id, only_data=only_data, remove=remove)
        # Remove the scalarbar whenever the mesh is removed.
        if data_id not in self.object_data:
            scalar_bar = self.scalar_bars.pop(data_id, None)         
            if scalar_bar and remove:
                self.renderer.RemoveActor2D(scalar_bar)
    
    def _register_scalar_bar(self, data_id: str, actor) -> None:   
        "Function to create a scalarbar whenever an array is added."
        mapper = actor.GetMapper()
        scalar_bar = create_scalar_bar_actor(mapper)
        self.renderer.AddActor2D(scalar_bar)
        self.scalar_bars[data_id] = scalar_bar

class MeshSliceHandler(MeshHandler):
    def __init__(self, preset_parser: ColorPresetParser, renderer: vtkRenderer, orientation: int) -> None:
        super().__init__(preset_parser, renderer)
        self.orientation = orientation
        self.scalar_bars = {}
 
    def add_mesh(self, data_id: str, poly_data: vtkPolyData) -> None:
        actor = render_mesh_in_slice(poly_data, self.orientation, self.renderer)
        self.register_data(data_id, actor)
        
        # Create a scalar bar when adding a mesh.
        self._register_scalar_bar(data_id, actor)

    def add_streamline(self, data_id: str, poly_data: vtkPolyData) -> None:
        actor = render_streamline_in_slice(poly_data, self.renderer, self.orientation)
        self.register_data(data_id, actor)

    def update_mesh_visibility(self, data_id: str, data_display: MeshDisplay) -> bool:
        logger.debug(f"set_mesh_visibility({data_id}): {data_display.is_visible}")
        modified = False
        for actor in self.get_actors(data_id):
            modified = set_mesh_visibility(actor, data_display.is_visible) or modified
        
        # Update visibility fo the scalarbar based on the visibility of the mesh. 
        self._refresh_scalar_bar(data_id, data_display, mesh_visible=data_display.is_visible)
        return modified


class MeshThreedHandler(MeshHandler):
    def __init__(self, preset_parser: ColorPresetParser, renderer: vtkRenderer) -> None:
        super().__init__(preset_parser, renderer)
        self.scalar_bars = {}
        
    def add_mesh(self, data_id: str, poly_data: vtkPolyData) -> None:
        actor = render_mesh_in_3D(poly_data, self.renderer)
        self.register_data(data_id, actor)

        # Create a scalar bar when adding a mesh.
        self._register_scalar_bar(data_id, actor)
    
    def update_mesh_visibility(self, data_id: str, data_display: MeshDisplay) -> bool:
        visible = data_display.is_visible and data_display.is_threed_visible
        logger.debug(f"set_mesh_visibility({data_id}): {visible}")
        modified = False
        for actor in self.get_actors(data_id):
            modified = set_mesh_visibility(actor, visible) or modified

        # Update visibility fo the scalarbar based on the visibility of the mesh.    
        self._refresh_scalar_bar(data_id, data_display, mesh_visible=data_display.is_visible and data_display.is_threed_visible)
        return modified
