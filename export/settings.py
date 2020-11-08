def export_settings(exporter, scene):
    s = scene.pearray
    w = exporter.w

    w.write("(integrator")
    w.goIn()
    w.write(":type '%s'" % s.integrator)
    w.write(":max_ray_depth %i" % s.max_ray_depth)
    w.write(":soft_max_ray_depth %i" % s.soft_max_ray_depth)
    w.write(":max_light_ray_depth %i" % s.max_light_ray_depth)
    w.write(":soft_max_light_ray_depth %i" % s.soft_max_light_ray_depth)
    if s.integrator == 'DIRECT':
        w.write(":light_sample_count %i" % s.max_light_samples)
    elif s.integrator == 'PPM':
        w.write(":photons %i" % s.ppm_photons_per_pass)
    elif s.integrator == 'AO':
        w.write(":sampe_count %i" % s.ao_sample_count)
    elif s.integrator == 'VF':
        w.write(":mode '%s'" % s.vf_mode)
        w.write(":weighting %s" % str(s.vf_apply_weighting).lower())
    w.goOut()
    w.write(")")

    # add_entry(exporter, '/renderer/common/tile/mode',
    #          s.render_tile_mode)

    w.write("(sampler")
    w.goIn()
    w.write(":slot 'aa'")
    w.write(":type '%s'" % s.sampler_aa_mode)
    w.write(":sample_count %i" % s.sampler_max_samples)
    w.goOut()
    w.write(")")

    w.write("(sampler")
    w.goIn()
    w.write(":slot 'lens'")
    w.write(":type '%s'" % s.sampler_lens_mode)
    w.write(":sample_count 1")
    w.goOut()
    w.write(")")

    w.write("(sampler")
    w.goIn()
    w.write(":slot 'time'")
    w.write(":type '%s'" % s.sampler_time_mode)
    w.write(":sample_count 1")
    w.goOut()
    w.write(")")

    # add_entry(exporter, '/renderer/common/sampler/time/mapping',
    #          s.sampler_time_mapping_mode)
    # add_entry(exporter, '/renderer/common/sampler/time/scale',
    #          s.sampler_time_scale)

    w.write("(sampler")
    w.goIn()
    w.write(":slot 'spectral'")
    w.write(":type '%s'" % s.sampler_spectral_mode)
    w.write(":sample_count 1")
    w.goOut()
    w.write(")")

    w.write("(filter")
    w.goIn()
    w.write(":slot 'pixel'")
    w.write(":type '%s'" % s.pixel_filter_mode)
    w.write(":radius %i" % s.pixel_filter_radius)
    w.goOut()
    w.write(")")
