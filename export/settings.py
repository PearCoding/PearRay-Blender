def add_entry(exporter, key, v):
    exporter.w.write("(registry \'%s\' %s)"
                     % (key, str(v).lower() if type(v) is bool else
                        ('"'+v.lower()+'"' if type(v) is str else v)))


def export_settings(exporter, pr, scene):
    s = scene.pearray

    add_entry(exporter, '/renderer/common/type', s.integrator)
    add_entry(exporter, "/renderer/common/max_ray_depth", s.max_ray_depth)
    add_entry(exporter, '/renderer/common/tile/mode',
              s.render_tile_mode)

    add_entry(exporter, '/renderer/common/sampler/aa/count',
              s.sampler_max_aa_samples)
    add_entry(exporter, '/renderer/common/sampler/aa/type',
              s.sampler_aa_mode)

    add_entry(exporter, '/renderer/common/sampler/lens/count',
              s.sampler_max_lens_samples)
    add_entry(exporter, '/renderer/common/sampler/lens/type',
              s.sampler_lens_mode)

    add_entry(exporter, '/renderer/common/sampler/time/count',
              s.sampler_max_time_samples)
    add_entry(exporter, '/renderer/common/sampler/time/type',
              s.sampler_time_mode)
    add_entry(exporter, '/renderer/common/sampler/time/mapping',
              s.sampler_time_mapping_mode)
    add_entry(exporter, '/renderer/common/sampler/time/scale',
              s.sampler_time_scale)

    add_entry(exporter, '/renderer/common/pixel/filter',
              s.pixel_filter_mode)
    add_entry(exporter, '/renderer/common/pixel/radius',
              s.pixel_filter_radius)

    if s.integrator == 'DIRECT':
        add_entry(
            exporter, '/renderer/integrator/direct/light/sample_count', s.max_light_samples)
    elif s.integrator == 'AO':
        add_entry(exporter, '/renderer/integrator/ao/sample_count',
                  s.max_light_samples)
