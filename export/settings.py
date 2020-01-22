def export_settings(exporter, pr, scene):
    s = scene.pearray
    w = exporter.w

    w.write("(integrator")
    w.goIn()
    w.write(":type '%s'" % s.integrator)
    w.write(":max_ray_depth %i" % s.max_ray_depth)
    w.write(":light_sampe_count %i" % s.max_light_samples)
    w.write(":msi %s" % str(s.msi).lower())
    w.goOut()
    w.write(")")

    # add_entry(exporter, '/renderer/common/tile/mode',
    #          s.render_tile_mode)

    w.write("(sampler")
    w.goIn()
    w.write(":slot 'aa'")
    w.write(":type '%s'" % s.sampler_aa_mode)
    w.write(":sample_count %i" % s.sampler_max_aa_samples)
    w.goOut()
    w.write(")")

    w.write("(sampler")
    w.goIn()
    w.write(":slot 'lens'")
    w.write(":type '%s'" % s.sampler_lens_mode)
    w.write(":sample_count %i" % s.sampler_max_lens_samples)
    w.goOut()
    w.write(")")

    w.write("(sampler")
    w.goIn()
    w.write(":slot 'time'")
    w.write(":type '%s'" % s.sampler_time_mode)
    w.write(":sample_count %i" % s.sampler_max_time_samples)
    w.goOut()
    w.write(")")

    # add_entry(exporter, '/renderer/common/sampler/time/mapping',
    #          s.sampler_time_mapping_mode)
    # add_entry(exporter, '/renderer/common/sampler/time/scale',
    #          s.sampler_time_scale)

    w.write("(filter")
    w.goIn()
    w.write(":slot 'pixel'")
    w.write(":type '%s'" % s.pixel_filter_mode)
    w.write(":radius %i" % s.pixel_filter_radius)
    w.goOut()
    w.write(")")
