
## Writes a configuration file to be used by the render context.
def write_ini(exporter):
    scene = exporter.scene
    s = scene.pearray

    exporter.w.write("[renderer]")
    exporter.w.write("integrator=%s" % s.integrator.lower())
    exporter.w.write("debug=%s" % s.debug_mode.lower())
    exporter.w.write("incremental=%i" % int(s.incremental))
    exporter.w.write("max=%i" % s.max_ray_depth)

    exporter.w.write("[threads]")
    threads = 0
    if scene.render.threads_mode == 'FIXED':
        threads = scene.render.threads
    exporter.w.write("count=%i" % threads)
    exporter.w.write("tile_x=%i" % scene.render.tile_x)
    exporter.w.write("tile_y=%i" % scene.render.tile_y)

    exporter.w.write("[pixelsampler]")
    exporter.w.write("mode=%s" % s.pixel_sampler_mode.lower())
    exporter.w.write("max=%i" % s.max_pixel_samples)

    exporter.w.write("[globalillumination]")
    exporter.w.write("diffuse_bounces=%i" % s.max_diffuse_bounces)
    exporter.w.write("light_samples=%i" % s.max_light_samples)

    exporter.w.write("[photon]")
    exporter.w.write("count=%i" % s.photon_count)
    exporter.w.write("radius=%f" % s.photon_gather_radius)
    exporter.w.write("max=%i" % s.photon_max_gather_count)
    exporter.w.write("max_diffuse_bounces=%i" % s.photon_max_diffuse_bounces)
    exporter.w.write("min_specular_bounces=%i" % s.photon_min_specular_bounces)
    exporter.w.write("gathering_mode=%s" % s.photon_gathering_mode.lower())
    exporter.w.write("squeeze=%f" % s.photon_squeeze)