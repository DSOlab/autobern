def build_solution_ids(base_solution_id, sol_type):
    """Build final, prelim, reduced and free-net solution identifiers.

    Each identifier receives the orbit solution type suffix, for example
    ``DSO0GRC`` becomes ``DSO0GRCFIN``.
    """
    if not base_solution_id:
        raise ValueError('Final solution identifier cannot be empty')

    if base_solution_id[-1] in ('P', 'R', 'N'):
        reserved_map = {'P': 'prelim', 'R': 'reduced', 'N': 'free_net'}
        raise ValueError(
            'Final solution identifier cannot end in {:}; reserved for {:} solution'.format(
                base_solution_id[-1], reserved_map[base_solution_id[-1]]
            )
        )

    suffix = sol_type or ''
    solution_ids = {
        'final': '{:}{:}'.format(base_solution_id, suffix),
        'prelim': '{:}P{:}'.format(base_solution_id[:-1], suffix),
        'reduced': '{:}R{:}'.format(base_solution_id[:-1], suffix),
        'free_net': '{:}N{:}'.format(base_solution_id[:-1], suffix),
    }
    return solution_ids
