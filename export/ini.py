import math


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
    exporter.w.write("tile_mode=%s" % s.render_tile_mode.lower())

    exporter.w.write("[sampler]")
    exporter.w.write("aa_mode=%s" % s.sampler_aa_mode.lower())
    exporter.w.write("aa_max=%i" % s.sampler_max_aa_samples)
    exporter.w.write("lens_mode=%s" % s.sampler_lens_mode.lower())
    exporter.w.write("lens_max=%i" % s.sampler_max_lens_samples)
    exporter.w.write("time_mode=%s" % s.sampler_time_mode.lower())
    exporter.w.write("time_max=%i" % s.sampler_max_time_samples)
    exporter.w.write("time_mapping=%s" % s.sampler_time_mapping_mode.lower())
    exporter.w.write("time_scale=%f" % s.sampler_time_scale)
    exporter.w.write("spectral_mode=%s" % s.sampler_spectral_mode.lower())
    exporter.w.write("spectral_max=%i" % s.sampler_max_spectral_samples)

    exporter.w.write("[globalillumination]")
    exporter.w.write("diffuse_bounces=%i" % s.max_diffuse_bounces)
    exporter.w.write("light_samples=%i" % s.max_light_samples)

    exporter.w.write("[ppm]")
    exporter.w.write("count=%i" % s.photon_count)
    exporter.w.write("passes=%i" % s.photon_passes)
    exporter.w.write("radius=%f" % s.photon_gather_radius)
    exporter.w.write("max=%i" % s.photon_max_gather_count)
    exporter.w.write("gathering_mode=%s" % s.photon_gathering_mode.lower())
    exporter.w.write("squeeze=%f" % (s.photon_squeeze/100))
    exporter.w.write("ratio=%f" % (s.photon_ratio/100))
    exporter.w.write("proj=%f" % (s.photon_proj_weight/100))
    exporter.w.write("proj_qual=%f" % (s.photon_proj_qual/100))
    exporter.w.write("proj_caustic=%f" % (s.photon_proj_caustic/100))
