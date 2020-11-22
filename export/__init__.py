import bpy
import mathutils
import math
import tempfile
import os

from .scene import write_scene


class Writer:
    def __init__(self, filename, useTabs=True):
        self.file = open(filename, 'w')
        self.useTabs = useTabs
        self.currentLevel = 0

        import datetime
        self.file.write(
            "; generated by pearray exporter v0.7 with blender %s\n" % bpy.app.version_string)
        self.file.write("; at %s\n" % datetime.datetime.now())

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

    def close(self):
        self.file.close()

        if self.currentLevel > 0:
            print("DEV ERROR: PEARRAY Exporter currentLevel > 0 in the end!")


class Exporter:
    def __init__(self, filename, depsgraph):
        self.filename = filename

        self.depsgraph = depsgraph
        self.scene = depsgraph.scene

        self.instances = {}
        self.instances["MESH"] = []
        self.instances["MATERIAL"] = []
        self.instances["EMISSION"] = []
        self.instances["NODE"] = []

        self.mesh_cache = {}
        self.MISSING_MAT = ''

        self.M_WORLD = mathutils.Matrix.Identity(4)
        self.LIGHT_POW_F = 1
        self.EXTERNAL_MESH_FILES = True

        self.render = self.scene.render
        self.world = self.scene.world

        self._writer = []

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

    def register_mesh(self, name, mesh_obj):
        self.mesh_cache[mesh_obj] = name

    def get_mesh_name(self, mesh_obj):
        if mesh_obj in self.mesh_cache:
            return self.mesh_cache[mesh_obj]
        else:
            return None

    def write_scene(self):
        self.push_writer(self.filename)

        write_scene(self)

        self.pop_writer()

    def push_writer(self, filename):
        self._writer.append(
            Writer(filename, self.scene.pearray.beautiful_prc))

    def pop_writer(self):
        self.w.close()
        self._writer.pop()

    @property
    def w(self):
        return self._writer[-1]
