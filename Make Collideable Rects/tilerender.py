"""
This is a test of using the pytmx library with Tiled.
"""
import pygame as pg

import pytmx
from pytmx.util_pygame import load_pygame


class Renderer(object):
    """ This object renders tile maps from Tiled

    Use Renderer.make_map to make the initial map,
    use Renderer.render to update an existing map.
    """
    def __init__(self, filename):
        # load our data and images
        tm = load_pygame(filename)
        # pixel size is used to determine the pixel size of the entire map
        self.pixel_size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm

    def render(self, surface):
        """ Render map data to an existing pygame surface

        The supplide surface should be the same size or larger than
        this object's pixel_size.  If you want to create a new Surface
        automatically, then use Renderer.make_map, but use it only
        only once; it is a slower operation because it create a new
        pygame Surface each time.

        :param surface: pygame.Surface
        :return: None
        """
        # these names are declared here to speed up attribute lookup
        # tldr; the 'dots' in the names are slow, so we look them up here
        # https://wiki.python.org/moin/PythonSpeed/PerformanceTips#Avoiding_dots...
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        gt = self.tmx_data.get_tile_image_by_gid

        # Tiled stores colors in the hex web color format
        # we can use it for the background color
        if self.tmx_data.background_color:
            # the pygame.Color class is used to convert hex to RGB tuple colors
            color = pg.Color(self.tmx_data.background_color)
            surface.fill(color)

        # iterate over each layer in the map from top to bottom
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                # TiledTileLayers support iteration
                # here we get the tile x,y coordinates, and the tile GID
                # Tiled stores tile images as GID, so that is how we will, too
                for x, y, gid in layer:
                    # if there is no tile in this position, GID will == 0
                    if gid:
                        # get the tile for this GID.
                        tile = gt(gid)
                        # x and y are in tile coordinates
                        # to get screen coordinates, we must multiply by
                        # byt the size of the tile (tw and th)
                        surface.blit(tile, (x * tw, y * th))

            # TODO
            elif isinstance(layer, pytmx.TiledObjectGroup):
                pass

            # TiledImageLayers are a special layer where a spcific GID/Image
            # is positioned with the upper-left corner at (0, 0)
            elif isinstance(layer, pytmx.TiledImageLayer):
                if layer.gid:
                    image = gt(layer.gid)
                    surface.blit(image, (0, 0))

    def make_map(self):
        """ Create a new pygame Surface with map data rendered to it

        Please, do not use this each loop.  This is creating a new
        pygame Surface.  You can instead create a map here, then
        call Renderer.render(map_surface) when you want to render again.
        map_surface would be the surface returned from this function.

        :return: pygame.Surface
        """
        temp_surface = pg.Surface(self.pixel_size)
        self.render(temp_surface)
        return temp_surface
