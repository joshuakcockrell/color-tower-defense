#!/usr/bin/python
# -*- coding: utf-8 -*-

u"""
TileMap loader for python for Tiled, a generic tile map editor
from http://mapeditor.org/ .
It loads the \*.tmx files produced by Tiled.
"""

__version__ = u'$Id$'
__author__ = u'DR0ID_ @ 2009'

if __debug__:
    import sys
    import time
    _start_time = time.time()

#-------------------------------------------------------------------------------

import sys
import math # for map collision
from xml.dom import minidom, Node
import base64
import gzip
import StringIO
import os.path
import pygame
#import codecs
# TODO: ideas: save indexed_tiles as {type:data} so no image loader is needed
# user would have to write its own image loading
# different types would be : {gid : ('img_parts', (margin, spacing, path, tile_w, tile_h, colorkey))}
#                            {gid : ('img_path', ('C:/...', colorkey)}
#                            {gid : ('file_like', (file_like_obj, colorkey))}
#
# maybe use cStringIO instead of StringIO

#-------------------------------------------------------------------------------
class IImageLoader(object):
    u"""
    Interface for image loading. Depending on the framework used the
    images have to be loaded differently.
    """

    def load_image(self, filename, colorkey=None): # -> image
        u"""
        Load a single image.

        :Parameters:
            filename : string
                Path to the file to be loaded.
            colorkey : tuple
                The (r, g, b) color that should be used as colorkey (or magic color).
                Default: None

        :rtype: image

        """
        raise NotImplementedError(u'This should be implemented in a inherited class')

    def load_image_file_like(self, file_like_obj, colorkey=None): # -> image
        u"""
        Load a image from a file like object.

        :Parameters:
            file_like_obj : file
                This is the file like object to load the image from.
            colorkey : tuple
                The (r, g, b) color that should be used as colorkey (or magic color).
                Default: None

        :rtype: image
        """
        raise NotImplementedError(u'This should be implemented in a inherited class')

    def load_image_parts(self, filename, margin, spacing, tile_width, tile_height, colorkey=None): #-> [images]
        u"""
        Load different tile images from one source image.

        :Parameters:
            filename : string
                Path to image to be loaded.
            margin : int
                The margin around the image.
            spacing : int
                The space between the tile images.
            tile_width : int
                The width of a single tile.
            tile_height : int
                The height of a single tile.
            colorkey : tuple
                The (r, g, b) color that should be used as colorkey (or magic color).
                Default: None

        Luckily that iteration is so easy in python::

            ...
            w, h = image_size
            for y in xrange(margin, h, tile_height + spacing):
                for x in xrange(margin, w, tile_width + spacing):
                    ...

        :rtype: a list of images
        """
        raise NotImplementedError(u'This should be implemented in a inherited class')

#-------------------------------------------------------------------------------
class ImageLoaderPygame(IImageLoader):
    u"""
    Pygame image loader.

    It uses an internal image cache. The methods return Surface.

    :Undocumented:
        pygame
    """


    def __init__(self):
        self.pygame = __import__('pygame')
        self._img_cache = {} # {name: surf}

    def load_image(self, filename, colorkey=None):
        img = self._img_cache.get(filename, None)
        if img is None:
            img = self.pygame.image.load(filename)
            self._img_cache[filename] = img
        if colorkey:
            img.set_colorkey(colorkey)
        return img

    def load_image_part(self, filename, x, y, w, h, colorkey=None):
        source_rect = self.pygame.Rect(x, y, w, h)
        img = self._img_cache.get(filename, None)
        if img is None:
            img = self.pygame.image.load(filename)
            self._img_cache[filename] = img
        img_part = self.pygame.Surface((w, h), 0, img)
        img_part.blit(img, (0, 0), source_rect)
        if colorkey:
            img_part.set_colorkey(colorkey)
        return img_part

    def load_image_parts(self, filename, margin, spacing, tile_width, tile_height, colorkey=None): #-> [images]
        source_img = self._img_cache.get(filename, None)
        if source_img is None:
            source_img = self.pygame.image.load(filename)
            self._img_cache[filename] = source_img
        w, h = source_img.get_size()
        images = []
        for y in xrange(margin, h, tile_height + spacing):
            for x in xrange(margin, w, tile_width + spacing):
                img_part = self.pygame.Surface((tile_width, tile_height), 0, source_img)
                img_part.blit(source_img, (0, 0), self.pygame.Rect(x, y, tile_width, tile_height))
                if colorkey:
                    img_part.set_colorkey(colorkey)
                images.append(img_part)
        return images

    def load_image_file_like(self, file_like_obj, colorkey=None): # -> image
        # pygame.image.load can load from a path and from a file-like object
        # that is why here it is redirected to the other method
        return self.load_image(file_like_obj, colorkey)

#-------------------------------------------------------------------------------
class TileMap(object):
    u"""

    The TileMap holds all the map data.

    :Ivariables:
        orientation : string
            orthogonal or isometric or hexagonal or shifted
        tilewidth : int
            width of the tiles (for all layers)
        tileheight : int
            height of the tiles (for all layers)
        width : int
            width of the map (number of tiles)
        height : int
            height of the map (number of tiles)
        version : string
            version of the map format
        tile_sets : list
            list of TileSet
        properties : dict
            the propertis set in the editor, name-value pairs, strings
        pixel_width : int
            width of the map in pixels
        pixel_height : int
            height of the map in pixels
        layers : list
            list of TileLayer
        map_file_name : dict
            file name of the map
        object_groups : list
            list of :class:MapObjectGroup
        indexed_tiles : dict
            dict containing {gid : (offsetx, offsety, surface} if load() was called
            when drawing just add the offset values to the draw point
        named_layers : dict of string:TledLayer
            dict containing {name : TileLayer}
        named_tile_sets : dict
            dict containing {name : TileSet}

    """


    def __init__(self):
#        This is the top container for all data. The gid is the global id (for a image).
#        Before calling convert most of the values are strings. Some additional
#        values are also calculated, see convert() for details. After calling
#        convert, most values are integers or floats where appropriat.
        u"""
        The TileMap holds all the map data.
        """
        # set through parser
        self.orientation = None
        self.tileheight = 0
        self.tilewidth = 0
        self.width = 0
        self.height = 0
        self.version = 0
        self.tile_sets = [] # TileSet
        self.layers = [] # WorldTileLayer <- what order? back to front (guessed)
        self.indexed_tiles = {} # {gid: (offsetx, offsety, image}
        self.object_groups = []
        self.properties = {} # {name: value}
        # additional info
        self.pixel_width = 0
        self.pixel_height = 0
        self.named_layers = {} # {name: layer}
        self.named_tile_sets = {} # {name: tile_set}
        self.map_file_name = ""
        self._image_loader = None

    def convert(self):
        u"""
        Converts numerical values from strings to numerical values.
        It also calculates or set additional data:
        pixel_width
        pixel_height
        named_layers
        named_tile_sets
        """
        self.tilewidth = int(self.tilewidth)
        self.tileheight = int(self.tileheight)
        self.width = int(self.width)
        self.height = int(self.height)
        self.pixel_width = self.width * self.tilewidth
        self.pixel_height = self.height * self.tileheight
        for layer in self.layers:
            self.named_layers[layer.name] = layer
            layer.opacity = float(layer.opacity)
            layer.x = int(layer.x)
            layer.y = int(layer.y)
            layer.width = int(layer.width)
            layer.height = int(layer.height)
            layer.pixel_width = layer.width * self.tilewidth
            layer.pixel_height = layer.height * self.tileheight
            layer.visible = bool(int(layer.visible))
        for tile_set in self.tile_sets:
            self.named_tile_sets[tile_set.name] = tile_set
            tile_set.spacing = int(tile_set.spacing)
            tile_set.margin = int(tile_set.margin)
            for img in tile_set.images:
                if img.trans:
                    img.trans = (int(img.trans[:2], 16), int(img.trans[2:4], 16), int(img.trans[4:], 16))
        for obj_group in self.object_groups:
            obj_group.x = int(obj_group.x)
            obj_group.y = int(obj_group.y)
            obj_group.width = int(obj_group.width)
            obj_group.height = int(obj_group.height)
            for map_obj in obj_group.objects:
                map_obj.x = int(map_obj.x)
                map_obj.y = int(map_obj.y)
                map_obj.width = int(map_obj.width)
                map_obj.height = int(map_obj.height)

    def load(self, image_loader):
        u"""
        loads all images using a IImageLoadermage implementation and fills up
        the indexed_tiles dictionary.
        The image may have per pixel alpha or a colorkey set.
        """
        self._image_loader = image_loader
        for tile_set in self.tile_sets:
            # do images first, because tiles could reference it
            for img in tile_set.images:
                if img.source:
                    self._load_image_from_source(tile_set, img)
                else:
                    tile_set.indexed_images[img.id] = self._load_image(img)
            # tiles
            for tile in tile_set.tiles:
                for img in tile.images:
                    if not img.content and not img.source:
                        # only image id set
                        indexed_img = tile_set.indexed_images[img.id]
                        self.indexed_tiles[int(tile_set.firstgid) + int(tile.id)] = (0, 0, indexed_img)
                    else:
                        if img.source:
                            self._load_image_from_source(tile_set, img)
                        else:
                            indexed_img = self._load_image(img)
                            self.indexed_tiles[int(tile_set.firstgid) + int(tile.id)] = (0, 0, indexed_img)

    def _load_image_from_source(self, tile_set, a_tile_image):
        # relative path to file
        img_path = os.path.join(os.path.dirname(self.map_file_name), a_tile_image.source)
        tile_width = int(self.tilewidth)
        tile_height = int(self.tileheight)
        if tile_set.tileheight:
            tile_width = int(tile_set.tilewidth)
        if tile_set.tilewidth:
            tile_height = int(tile_set.tileheight)
        offsetx = 0
        offsety = 0
#        if tile_width > self.tilewidth:
#            offsetx = tile_width
        if tile_height > self.tileheight:
            offsety = tile_height - self.tileheight
        idx = 0
        for image in self._image_loader.load_image_parts(img_path, \
                    tile_set.margin, tile_set.spacing, tile_width, tile_height, a_tile_image.trans):
            self.indexed_tiles[int(tile_set.firstgid) + idx] = (offsetx, -offsety, image)
            idx += 1

    def _load_image(self, a_tile_image):
        img_str = a_tile_image.content
        if a_tile_image.encoding:
            if a_tile_image.encoding == u'base64':
                img_str = decode_base64(a_tile_image.content)
            else:
                raise Exception(u'unknown image encoding %s' % a_tile_image.encoding)
        sio = StringIO.StringIO(img_str)
        new_image = self._image_loader.load_image_file_like(sio, a_tile_image.trans)
        return new_image

    def decode(self):
        u"""
        Decodes the TileLayer encoded_content and saves it in decoded_content.
        """
        for layer in self.layers:
            layer.decode()
#-------------------------------------------------------------------------------


class TileSet(object):
    u"""
    A tileset holds the tiles and its images.

    :Ivariables:
        firstgid : int
            the first gid of this tileset
        name : string
            the name of this TileSet
        images : list
            list of TileImages
        tiles : list
            list of Tiles
        indexed_images : dict
            after calling load() it is dict containing id: image
        indexed_tiles : dict
            after calling load() it is a dict containing
            gid: (offsetx, offsety, image) , the image corresponding to the gid
        spacing : int
            the spacing between tiles
        marging : int
            the marging of the tiles
        properties : dict
            the propertis set in the editor, name-value pairs
        tilewidth : int
            the actual width of the tile, can be different from the tilewidth of the map
        tilehight : int
            the actual hight of th etile, can be different from the tilehight of the  map

    """

    def __init__(self):
        self.firstgid = 0
        self.name = None
        self.images = [] # TileImage
        self.tiles = [] # Tile
        self.indexed_images = {} # {id:image}
        self.indexed_tiles = {} # {gid: (offsetx, offsety, image} <- actually in map data
        self.spacing = 0
        self.margin = 0
        self.properties = {}
        self.tileheight = 0
        self.tilewidth = 0

#-------------------------------------------------------------------------------

class TileImage(object):
    u"""
    An image of a tile or just an image.

    :Ivariables:
        id : int
            id of this image (has nothing to do with gid)
        format : string
            the format as string, only 'png' at the moment
        source : string
            filename of the image. either this is set or the content
        encoding : string
            encoding of the content
        trans : tuple of (r,g,b)
            the colorkey color, raw as hex, after calling convert just a (r,g,b) tuple
        properties : dict
            the propertis set in the editor, name-value pairs
        image : TileImage
            after calling load the pygame surface
    """

    def __init__(self):
        self.id = 0
        self.format = None
        self.source = None
        self.encoding = None # from <data>...</data>
        self.content = None # from <data>...</data>
        self.image = None
        self.trans = None
        self.properties = {} # {name: value}

#-------------------------------------------------------------------------------

class Tile(object):
    u"""
    A single tile.

    :Ivariables:
        id : int
            id of the tile gid = TileSet.firstgid + Tile.id
        images : list of :class:TileImage
            list of TileImage, either its 'id' or 'image data' will be set
        properties : dict of name:value
            the propertis set in the editor, name-value pairs
    """

    def __init__(self):
        self.id = 0
        self.images = [] # uses TileImage but either only id will be set or image data
        self.properties = {} # {name: value}

#-------------------------------------------------------------------------------

class TileLayer(object):
    u"""
    A layer of the world.

    :Ivariables:
        x : int
            position of layer in the world in number of tiles (not pixels)
        y : int
            position of layer in the world in number of tiles (not pixels)
        width : int
            number of tiles in x direction
        height : int
            number of tiles in y direction
        pixel_width : int
            width of layer in pixels
        pixel_height : int
            height of layer in pixels
        name : string
            name of this layer
        opacity : float
            float from 0 (full transparent) to 1.0 (opaque)
        decoded_content : list
            list of graphics id going through the map::

                e.g [1, 1, 1, ]
                where decoded_content[0] is (0,0)
                      decoded_content[1] is (1,0)
                      ...
                      decoded_content[1] is (width,0)
                      decoded_content[1] is (0,1)
                      ...
                      decoded_content[1] is (width,height)

                usage: graphics id = decoded_content[tile_x + tile_y * width]
        content2D : list
            list of list, usage: graphics id = content2D[x][y]

    """

    def __init__(self):
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.pixel_width = 0
        self.pixel_height = 0
        self.name = None
        self.opacity = -1
        self.encoding = None
        self.compression = None
        self.encoded_content = None
        self.decoded_content = []
        self.visible = True
        self.properties = {} # {name: value}
        self.content2D = None
    def decode(self):
        u"""
        Converts the contents in a list of integers which are the gid of the used
        tiles. If necessairy it decodes and uncompresses the contents.
        """
        s = self.encoded_content
        if self.encoded_content:
            if self.encoding:
                if self.encoding == u'base64':
                    s = decode_base64(s)
                else:
                    raise Exception(u'unknown data encoding %s' % (self.encoding))
            if self.compression:
                if self.compression == u'gzip':
                    s = decompress_gzip(s)
                else:
                    raise Exception(u'unknown data compression %s' %(self.compression))
        else:
            raise Exception(u'no encoded content to decode')
        self.decoded_content = []
        for idx in xrange(0, len(s), 4):
            val = ord(str(s[idx])) | (ord(str(s[idx + 1])) << 8) | \
                 (ord(str(s[idx + 2])) << 16) | (ord(str(s[idx + 3])) << 24)
            self.decoded_content.append(val)
        # generate the 2D version
        self._gen_2D()

    def _gen_2D(self):
        self.content2D = []
        # generate the needed lists
        for xpos in xrange(self.width):
            self.content2D.append([])
        # fill them
        for xpos in xrange(self.width):
            for ypos in xrange(self.height):
                self.content2D[xpos].append(self.decoded_content[xpos + ypos * self.width])

    def pretty_print(self):
        num = 0
        for y in range(int(self.height)):
            s = u""
            for x in range(int(self.width)):
                s += str(self.decoded_content[num])
                num += 1
            print s
#-------------------------------------------------------------------------------


class MapObjectGroup(object):
    u"""
    Group of objects on the map.

    :Ivariables:
        x : int
            the x position
        y : int
            the y position
        width : int
            width of the bounding box (usually 0, so no use)
        height : int
            height of the bounding box (usually 0, so no use)
        name : string
            name of the group
        objects : list
            list of the map objects

    """

    def __init__(self):
        self.width = 0
        self.height = 0
        self.name = None
        self.objects = []
        self.x = 0
        self.y = 0
        self.properties = {} # {name: value}

#-------------------------------------------------------------------------------

class MapObject(object):
    u"""
    A single object on the map.

    :Ivariables:
        x : int
            x position relative to group x position
        y : int
            y position relative to group y position
        width : int
            width of this object
        height : int
            height of this object
        type : string
            the type of this object
        image_source : string
            source path of the image for this object
        image : :class:TileImage
            after loading this is the pygame surface containing the image
    """
    def __init__(self):
        self.name = None
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.type = None
        self.image_source = None
        self.image = None
        self.properties = {} # {name: value}

#-------------------------------------------------------------------------------
def decode_base64(in_str):
    u"""
    Decodes a base64 string and returns it.

    :Parameters:
        in_str : string
            base64 encoded string

    :returns: decoded string
    """
    return base64.decodestring(in_str)

#-------------------------------------------------------------------------------
def decompress_gzip(in_str):
    u"""
    Uncompresses a gzip string and returns it.

    :Parameters:
        in_str : string
            gzip compressed string

    :returns: uncompressed string
    """
    # gzip can only handle file object therefore using StringIO
    copmressed_stream = StringIO.StringIO(in_str)
    gzipper = gzip.GzipFile(fileobj=copmressed_stream)
    s = gzipper.read()
    gzipper.close()
    return s

#-------------------------------------------------------------------------------
def printer(obj, ident=''):
    u"""
    Helper function, prints a hirarchy of objects.
    """
    import inspect
    print ident + obj.__class__.__name__.upper()
    ident += '    '
    lists = []
    for name in dir(obj):
        elem = getattr(obj, name)
        if isinstance(elem, list) and name != u'decoded_content':
            lists.append(elem)
        elif not inspect.ismethod(elem):
            if not name.startswith('__'):
                if name == u'data' and elem:
                    print ident + u'data = '
                    printer(elem, ident + '    ')
                else:
                    print ident + u'%s\t= %s' % (name, getattr(obj, name))
    for l in lists:
        for i in l:
            printer(i, ident + '    ')

#-------------------------------------------------------------------------------
class TileMapParser(object):
    u"""
    Allows to parse and decode map files for 'Tiled', a open source map editor
    written in java. It can be found here: http://mapeditor.org/
    """

    def _build_tile_set(self, tile_set_node, world_map):
        tile_set = TileSet()
        self._set_attributes(tile_set_node, tile_set)
        for node in self._get_nodes(tile_set_node.childNodes, u'image'):
            self._build_tile_set_image(node, tile_set)
        for node in self._get_nodes(tile_set_node.childNodes, u'tile'):
            self._build_tile_set_tile(node, tile_set)
        self._set_attributes(tile_set_node, tile_set)
        world_map.tile_sets.append(tile_set)

    def _build_tile_set_image(self, image_node, tile_set):
        image = TileImage()
        self._set_attributes(image_node, image)
        # id of TileImage has to be set!! -> Tile.TileImage will only have id set
        for node in self._get_nodes(image_node.childNodes, u'data'):
            self._set_attributes(node, image)
            image.content = node.childNodes[0].nodeValue
        tile_set.images.append(image)

    def _build_tile_set_tile(self, tile_set_node, tile_set):
        tile = Tile()
        self._set_attributes(tile_set_node, tile)
        for node in self._get_nodes(tile_set_node.childNodes, u'image'):
            self._build_tile_set_tile_image(node, tile)
        tile_set.tiles.append(tile)

    def _build_tile_set_tile_image(self, tile_node, tile):
        tile_image = TileImage()
        self._set_attributes(tile_node, tile_image)
        for node in self._get_nodes(tile_node.childNodes, u'data'):
            self._set_attributes(node, tile_image)
            tile_image.content = node.childNodes[0].nodeValue
        tile.images.append(tile_image)

    def _build_layer(self, layer_node, world_map):
        ###ERRRRORRRES
        layer = TileLayer()
        self._set_attributes(layer_node, layer) # gets correct properties
        for node in self._get_nodes(layer_node.childNodes, u'data'):
            self._set_attributes(node, layer) # gets incorrect properties and over rides other ones
            layer.encoded_content = node.lastChild.nodeValue
        world_map.layers.append(layer)

    def _build_world_map(self, world_node):
        world_map = TileMap()
        self._set_attributes(world_node, world_map)
        if world_map.version != u"1.0":
            raise Exception(u'this parser was made for maps of version 1.0, found version %s' % world_map.version)
        for node in self._get_nodes(world_node.childNodes, u'tileset'):
            self._build_tile_set(node, world_map)
        for node in self._get_nodes(world_node.childNodes, u'layer'):
            self._build_layer(node, world_map)
        for node in self._get_nodes(world_node.childNodes, u'objectgroup'):
            self._build_object_groups(node, world_map)
        return world_map

    def _build_object_groups(self, object_group_node, world_map):
        object_group = MapObjectGroup()
        self._set_attributes(object_group_node,  object_group)
        for node in self._get_nodes(object_group_node.childNodes, u'object'):
            tiled_object = MapObject()
            self._set_attributes(node, tiled_object)
            for img_node in self._get_nodes(node.childNodes, u'image'):
                tiled_object.image_source = img_node.attributes[u'source'].nodeValue
            object_group.objects.append(tiled_object)
        world_map.object_groups.append(object_group)

    #-- helpers --#
    def _get_nodes(self, nodes, name):
        for node in nodes:
            if node.nodeType == Node.ELEMENT_NODE and node.nodeName == name:
                yield node

    def _set_attributes(self, node, obj):
        attrs = node.attributes
        for attr_name in attrs.keys():
            setattr(obj, attr_name, attrs.get(attr_name).nodeValue)
        self._get_properties(node, obj)


    def _get_properties(self, node, obj):
        props = {}
        for properties_node in self._get_nodes(node.childNodes, u'properties'):
            for property_node in self._get_nodes(properties_node.childNodes, u'property'):
                try:
                    props[property_node.attributes[u'name'].nodeValue] = property_node.attributes[u'value'].nodeValue
                except KeyError:
                    props[property_node.attributes[u'name'].nodeValue] = property_node.lastChild.nodeValue
        obj.properties.update(props)



    #-- parsers --#
    def parse(self, file_name):
        u"""
        Parses the given map. Does no decoding nor loading the data.
        :return: instance of TileMap
        """
        #dom = minidom.parseString(codecs.open(file_name, "r", "utf-8").read())
        dom = minidom.parseString(open(file_name, "rb").read())
        for node in self._get_nodes(dom.childNodes, 'map'):
            world_map = self._build_world_map(node)
            break
        world_map.map_file_name = os.path.abspath(file_name)
        world_map.convert()
        return world_map

    def parse_decode(self, file_name):
        u"""
        Parses the map but additionally decodes the data.
        :return: instance of TileMap
        """
        world_map = TileMapParser().parse(file_name)
        world_map.decode()
        return world_map

    def parse_decode_load(self, file_name, image_loader):
        u"""
        Parses the data, decodes them and loads the images using the image_loader.
        :return: instance of TileMap
        """
        world_map = self.parse_decode(file_name)
        world_map.load(image_loader)
        return world_map



#############################3


class World_map(pygame.sprite.Sprite):

    def __init__(self, file_name):
        pygame.sprite.Sprite.__init__(self, self.groups) # ERRRROR
        self.world_map = TileMapParser().parse_decode(file_name)
        self.world_map.load(ImageLoaderPygame())
        self.screen_width = min(600, self.world_map.pixel_width)
        self.screen_height = min(600, self.world_map.pixel_height)
        assert self.world_map.orientation == "orthogonal"
        self.cam_offset_x = 0
        self.cam_offset_y = 0
        self.tiles = [] # holds image, position, and offset of all tiles on this map
        self.collision = [] # holds collision values of all tiles in this map
        self.image = pygame.Surface((750,600))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)



        for layer in self.world_map.layers[:]:
            
            ##### create a collision grid #####
            if layer.name == 'collision':
                # goes left right top down
                for row_idx in xrange(0, (layer.height / self.world_map.tileheight)):
                    self.collision.append([]) # add a new collision row
                    for col_idx in xrange(0, (layer.width / self.world_map.tilewidth)):
                        tile = layer.content2D[col_idx][row_idx]
                        if tile: # not walkable tile
                            self.collision[-1].append(True) # add a new tile value
                        else: # walkable tile
                            self.collision[-1].append(False)

                
            if layer.visible:
                idx = 0
                # loop over all tiles
                for ypos in xrange(0, layer.height):
                    self.tiles.append([])
                    for xpos in xrange(0, layer.width):
                        # add offset in number of tiles
                        x = (xpos + layer.x) * self.world_map.tilewidth
                        y = (ypos + layer.y) * self.world_map.tileheight
                        # get the gid at this position
                        img_idx = layer.content2D[xpos][ypos]
                        idx += 1
                        if img_idx:
                            # get the actual image and its offset
                            offx, offy, self.screen_img = self.world_map.indexed_tiles[img_idx]
                            # only draw the tiles thast are relly visible (speed up)
                            if x >= self.cam_offset_x - 3 * self.world_map.tilewidth and x + self.cam_offset_x <= self.screen_width + self.world_map.tilewidth\
                               and y >= self.cam_offset_y - 3 * self.world_map.tileheight and y + self.cam_offset_y <= self.screen_height + 3 * self.world_map.tileheight:
                                if self.screen_img.get_alpha():
                                    self.screen_img = self.screen_img.convert_alpha()
                                else:
                                    self.screen_img = self.screen_img.convert()
                                    if layer.opacity > -1:
                                        #print 'pe r surf alpha', layer.opacity
                                        self.screen_img.set_alpha(None)
                                        alpha_value = int(255. * float(layer.opacity))
                                        self.screen_img.set_alpha(alpha_value)
                                self.screen_img = self.screen_img.convert_alpha()
        # draw the map
        
        # draw image at right position using its offset

                            
                            
                                self.tiles[-1].append([self.screen_img, x, y, offx, offy])
            self.draw_to_image() # draw all the tiles onto the big image
            
            #map objects
            for obj_group in self.world_map.object_groups:
                goffx = obj_group.x
                goffy = obj_group.y
                if goffx >= self.cam_offset_x - 3 * self.world_map.tilewidth and goffx + self.cam_offset_x <= self.screen_width + self.world_map.tilewidth \
                   and goffy >= self.cam_offset_y - 3 * self.world_map.tileheight and goffy + self.cam_offset_y <= screen_height + 3 * self.world_map.tileheight:
                    for map_obj in obj_group.objects:
                        size = (map_obj.width, map_obj.height)
                        if map_obj.image_source:
                            surf = pygame.image.load(map_obj.image_source)
                            surf = pygame.transform.scale(surf, size)
                            screen.blit(surf, (goffx + map_obj.x + self.cam_offset_x, goffy + map_obj.y + self.cam_offset_y))
                        else:
                            r = pygame.Rect((goffx + map_obj.x + self.cam_offset_x, goffy + map_obj.y + self.cam_offset_y), size)
                            pygame.draw.rect(screen, (255, 255, 0), r, 1)


    def map_collision(self, rect):
        '''
        checks all corners of the rect to see if they
        are colliding with the self.collision list
        return true if there is a collision
        .. yeah, its complicated
        '''
        # convert corners to grid positions according to the allignment of the collision list
        top_left_y = int(math.floor((rect.topleft[1])/self.world_map.tileheight))
        top_left_x = int(math.ceil((rect.topleft[0])/self.world_map.tilewidth))

        top_right_y = int(math.floor((rect.topright[1])/self.world_map.tileheight))
        top_right_x = int(math.ceil((rect.topright[0])/self.world_map.tilewidth))

        bottom_right_y = int(math.floor((rect.bottomright[1])/self.world_map.tileheight))
        bottom_right_x = int(math.ceil((rect.bottomright[0])/self.world_map.tilewidth))

        bottom_left_y = int(math.floor((rect.bottomleft[1])/self.world_map.tileheight))
        bottom_left_x = int(math.ceil((rect.bottomleft[0])/self.world_map.tilewidth))

        collision = False
        top_left_collision = False
        top_right_collision = False
        bottom_right_collision = False
        bottom_left_collision = False

        try:
            if self.collision[top_left_y][top_left_x]:
                top_left_collision = True
            else:
                top_left_collision = False
        except IndexError:
            top_left_collision = True

        try:
            if self.collision[top_right_y][top_right_x]:
                top_right_collision = True
            else:
                top_right_collision = False
        except IndexError:
            top_right_collision = True

        try:
            if self.collision[bottom_right_y][bottom_right_x]:
                bottom_right_collision = True
            else:
                bottom_right_collision = False
        except IndexError:
            bottom_right_collision = True

        try:
            if self.collision[bottom_left_y][bottom_left_x]:
                bottom_left_collision = True
            else:
                bottom_left_collision = False
        except IndexError:
            bottom_left_collision = True

        '''
            
        
        if len(self.collision) > top_left_y: # if the y value is in range of the collision list
            if len(self.collision[top_left_y]) > top_left_x: # if the x value is in range of the collision list
                if self.collision[top_left_y][top_left_x]: #checking topleft coordinate for collision
                    top_left_collision = True
                else:
                   top_left_collision = False
            else:
                top_left_collision = True
        else:
            top_left_collision = True

        if len(self.collision) > top_right_y:
            if len(self.collision[top_right_y]) > top_right_x:
                if self.collision[top_right_y][top_right_x]: #checking topright coordinate for collision
                    top_right_collision = True
                else:
                   top_right_collision = False
            else:
                top_right_collision = True
        else:
            top_right_collision = True

        if len(self.collision) > bottom_right_y:
            if len(self.collision[bottom_right_y]) > bottom_right_x:
                if self.collision[bottom_right_y][bottom_right_x]: #checking bottomright coordinate for collision
                    bottom_right_collision = True
                else:
                   bottom_right_collision = False
            else:
                bottom_right_collision = True
        else:
            bottom_right_collision = True

        if len(self.collision) > bottom_left_y:
            if len(self.collision[bottom_left_y]) > bottom_left_x:
                if self.collision[bottom_left_y][bottom_left_x]: #checking bottomleft coordinate for collision
                    bottom_left_collision = True
                else:
                   bottom_left_collision = False
            else:
                bottom_left_collision = True
        else:
            bottom_left_collision = True

        '''

        
        # If there is no collision on any of the corners
        if not top_left_collision and not top_right_collision and not bottom_right_collision and not bottom_left_collision:
            collision = False
        else:
            collision = True
        return collision
        

    def set_collision(self, position, open_or_close):
        '''
        position = tuple x,y coordinate
        open_or_close = string
        changes a tile in the collision list to
        either on or off
        '''
        x = position[0] # get value
        x //= self.world_map.tilewidth # break down into ammount of tiles two division signs rounds to the nearest integer
        y = position[1]
        y //= self.world_map.tileheight
        
        if open_or_close == 'open':
            self.collision[y][x] = False # set the position to open
        if open_or_close == 'close':
            self.collision[y][x] = True # set the position to collidable
            
    def draw_to_image(self):
            
        for row in self.tiles:
            for tile in row:
                self.image.blit(tile[0], [tile[1], tile[2], tile[3], tile[4]])        


#############################################
                #############################################

#-------------------------------------------------------------------------------
def demo_pygame(file_name):
    pygame = __import__('pygame')

    # parser the map
    world_map = TileMapParser().parse_decode(file_name)
    # init pygame and set up a screen
    pygame.init()
    pygame.display.set_caption("tiledtmxloader - " + file_name)
    screen_width = min(1024, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load the images using pygame
    world_map.load(ImageLoaderPygame())
    #printer(world_map)

    # an example on how to access the map data and draw an orthoganl map
    # draw the map
    assert world_map.orientation == "orthogonal"

    running = True
    dirty = True
    # cam_offset is for scrolling
    cam_offset_x = 0
    cam_offset_y = 0
    # mainloop
    while running:
        # eventhandling
        events = [pygame.event.wait()]
        events.extend(pygame.event.get())
        for event in events:
            dirty = True
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    cam_offset_y -= world_map.tileheight
                elif event.key == pygame.K_UP:
                    cam_offset_y += world_map.tileheight
                elif event.key == pygame.K_LEFT:
                    cam_offset_x += world_map.tilewidth
                elif event.key == pygame.K_RIGHT:
                    cam_offset_x -= world_map.tilewidth

        # draw the map
        if dirty:
            dirty = False
            for layer in world_map.layers[:]:
                if layer.visible:
                    idx = 0
                    # loop over all tiles
                    for ypos in xrange(0, layer.height):
                        for xpos in xrange(0, layer.width):
                            # add offset in number of tiles
                            x = (xpos + layer.x) * world_map.tilewidth
                            y = (ypos + layer.y) * world_map.tileheight
                            # get the gid at this position
                            img_idx = layer.content2D[xpos][ypos]
                            idx += 1
                            if img_idx:
                                # get the actual image and its offset
                                offx, offy, screen_img = world_map.indexed_tiles[img_idx]
                                # only draw the tiles that are relly visible (speed up)
                                if x >= cam_offset_x - 3 * world_map.tilewidth and x + cam_offset_x <= screen_width + world_map.tilewidth\
                                   and y >= cam_offset_y - 3 * world_map.tileheight and y + cam_offset_y <= screen_height + 3 * world_map.tileheight:
                                    if screen_img.get_alpha():
                                        screen_img = screen_img.convert_alpha()
                                    else:
                                        screen_img = screen_img.convert()
                                        if layer.opacity > -1:
                                            #print 'per surf alpha', layer.opacity
                                            screen_img.set_alpha(None)
                                            alpha_value = int(255. * float(layer.opacity))
                                            screen_img.set_alpha(alpha_value)
                                    screen_img = screen_img.convert_alpha()
                                    # draw image at right position using its offset
                                    screen.blit(screen_img, (x + cam_offset_x + offx, y + cam_offset_y + offy))
            # map objects
            for obj_group in world_map.object_groups:
                goffx = obj_group.x
                goffy = obj_group.y
                if goffx >= cam_offset_x - 3 * world_map.tilewidth and goffx + cam_offset_x <= screen_width + world_map.tilewidth \
                   and goffy >= cam_offset_y - 3 * world_map.tileheight and goffy + cam_offset_y <= screen_height + 3 * world_map.tileheight:
                    for map_obj in obj_group.objects:
                        size = (map_obj.width, map_obj.height)
                        if map_obj.image_source:
                            surf = pygame.image.load(map_obj.image_source)
                            surf = pygame.transform.scale(surf, size)
                            screen.blit(surf, (goffx + map_obj.x + cam_offset_x, goffy + map_obj.y + cam_offset_y))
                        else:
                            r = pygame.Rect((goffx + map_obj.x + cam_offset_x, goffy + map_obj.y + cam_offset_y), size)
                            pygame.draw.rect(screen, (255, 255, 0), r, 1)
            # simple pygame
            pygame.display.flip()


#-------------------------------------------------------------------------------
def main():

    args = sys.argv[1:]
    if len(args) != 2:
        #print 'usage: python test.py mapfile.tmx [pygame|pyglet]'
        print('usage: python %s your_map.tmx [pygame|pyglet]' % \
            os.path.basename(__file__))
        return

    if args[1] == 'pygame':
        demo_pygame(args[0])
    elif args[1] == 'pyglet':
        demo_pyglet(args[0])
    else:
        print 'missing framework, usage: python test.py mapfile.tmx [pygame|pyglet]'
        sys.exit(-1)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    game_map = World_map('Resources/Map Data/map0.tmx')
    #main()


if __debug__:
    _dt = time.time() - _start_time

