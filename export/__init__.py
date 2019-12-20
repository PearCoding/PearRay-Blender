import bpy
import mathutils
import math
import tempfile
import os

from .scene import write_scene


class Writer:
    def __init__(self, file, useTabs=True):
        self.file = file
        self.useTabs = useTabs
        self.currentLevel = 0

    def write(self, str):
        prefix = ""
        if self.useTabs:
            for i in range(self.currentLevel):
                prefix = prefix + "\t"

        self.file.write(prefix + str + "\n")

    def goIn(self):
        self.currentLevel = self.currentLevel + 1

    def goOut(self):
        self.currentLevel = self.currentLevel - 1
        if self.currentLevel < 0:
            print("DEV ERROR: PEARRAY Exporter currentLevel < 0!")


class Exporter:
    def __init__(self, filename, scene):
        self.filename = filename
        self.file = None

        self.scene = scene

        self.instances = {}
        self.instances["MESH"] = []
        self.instances["MATERIAL"] = []
        self.instances["EMISSION"] = []
        self.instances["TEXTURE"] = []
        self.instances["SPEC"] = []

        self.mesh_cache = {}
        self.MISSING_MAT = ''

        self.M_WORLD = mathutils.Matrix.Identity(4)
        self.LIGHT_POW_F = 1

        self.render = scene.render
        self.world = scene.world

    def create_file(self, name_hint=""):
        if self.scene.pearray.keep_prc:
            dir = os.path.join(os.path.dirname(self.filename), "generated")
            if not os.path.exists(dir):
                os.mkdir(dir)

            if name_hint:
                return os.path.join(dir, name_hint)
            else:
                return tempfile.NamedTemporaryFile(delete=False, dir=dir).name
        else:
            return tempfile.NamedTemporaryFile(delete=False).name

    def register_unique_name(self, type, name):
        test_name = name
        i = 1
        while test_name in self.instances[type]:
            test_name = "%s_%i" % (name, i)
            i = i + 1
        self.instances[type].append(test_name)

        return test_name

    def register_mesh_data(self, name, data):
        for n, d in self.mesh_cache.items():
            lengthEq = True
            for i in range(len(d)):
                lengthEq = lengthEq and len(d[i]) == len(data[i])

            if lengthEq and d == data:
                return n, True

        # No name check... should be done somewhere else
        self.mesh_cache[name] = data

        return name, False

    def write_scene(self, pr):
        self.file = open(self.filename, 'w')
        self.w = Writer(self.file, self.scene.pearray.beautiful_prc)

        import datetime
        self.file.write("; generated by pearray exporter v0.5 with blender %s\n" % bpy.app.version_string)
        self.file.write("; at %s\n" % datetime.datetime.now())

        scene.write_scene(self, pr)
        self.close()

    def close(self):
        self.file.close()

        if self.w.currentLevel > 0:
            print("DEV ERROR: PEARRAY Exporter currentLevel > 0 in the end!")
