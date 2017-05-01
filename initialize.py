def add_custom_functions(fd):
    '''Agrega funciones personalizdas de la libreria graphics'''
    fd.add_function('drawText')
    fd.set_scope('drawText')
    fd.add_var('x', 'double', 0.0, 1)
    fd.add_var('y', 'double', 0.0, 1)
    fd.add_var('color', 'string', '', 1)
    fd.add_var('text', 'string', '', 1)
    fd.add_var('size', 'int', 0, 1)
    fd.update_function_params('x', 'double')
    fd.update_function_params('y', 'double')
    fd.update_function_params('color', 'string')
    fd.update_function_params('text', 'string')
    fd.update_function_params('size', 'int')
    fd.functions['drawText'].expected_arguments = 5
    fd.set_return_type('void')

    fd.add_function('drawLine')
    fd.set_scope('drawLine')
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    fd.add_var('bx', 'double', 0.0, 1)
    fd.add_var('by', 'double', 0.0, 1)
    fd.add_var('size', 'int', 0, 1)
    fd.add_var('fill', 'string', 0, 1)
    fd.update_function_params('ax', 'double')
    fd.update_function_params('ay', 'double')
    fd.update_function_params('bx', 'double')
    fd.update_function_params('by', 'double')
    fd.update_function_params('size', 'int')
    fd.update_function_params('fill', 'string')
    fd.functions['drawLine'].expected_arguments = 6
    fd.set_return_type('void')

    fd.add_function('drawCircle')
    fd.set_scope('drawCircle')
    fd.add_var('x', 'double', 0.0, 1)
    fd.add_var('y', 'double', 0.0, 1)
    fd.add_var('radio', 'double', 1.0, 1)
    fd.add_var('size', 'int', 1, 1)
    fd.add_var('fill', 'string', '', 1)
    fd.add_var('line', 'string', '', 1)
    fd.update_function_params('x', 'double')
    fd.update_function_params('y', 'double')
    fd.update_function_params('radio', 'double')
    fd.update_function_params('size', 'int')
    fd.update_function_params('fill', 'string')
    fd.update_function_params('line', 'string')
    fd.functions['drawCircle'].expected_arguments = 6
    fd.set_return_type('void')

    fd.add_function('drawOval')
    fd.set_scope('drawOval')
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    fd.add_var('bx', 'double', 0.0, 1)
    fd.add_var('by', 'double', 0.0, 1)
    fd.add_var('size', 'int', 1, 1)
    fd.add_var('fill', 'string', '', 1)
    fd.add_var('line', 'string', '', 1)
    fd.update_function_params('ax', 'double')
    fd.update_function_params('ay', 'double')
    fd.update_function_params('bx', 'double')
    fd.update_function_params('by', 'double')
    fd.update_function_params('size', 'int')
    fd.update_function_params('fill', 'string')
    fd.update_function_params('line', 'string')
    fd.functions['drawOval'].expected_arguments = 7
    fd.set_return_type('void')

    fd.add_function('drawTriangle')
    fd.set_scope('drawTriangle')
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    fd.add_var('bx', 'double', 0.0, 1)
    fd.add_var('by', 'double', 0.0, 1)
    fd.add_var('cx', 'double', 0.0, 1)
    fd.add_var('cy', 'double', 0.0, 1)
    fd.add_var('size', 'int', 1, 1)
    fd.add_var('fill', 'string', '', 1)
    fd.add_var('line', 'string', '', 1)
    fd.update_function_params('ax', 'double')
    fd.update_function_params('ay', 'double')
    fd.update_function_params('bx', 'double')
    fd.update_function_params('by', 'double')
    fd.update_function_params('cx', 'double')
    fd.update_function_params('cy', 'double')
    fd.update_function_params('size', 'int')
    fd.update_function_params('fill', 'string')
    fd.update_function_params('line', 'string')
    fd.functions['drawTriangle'].expected_arguments = 9
    fd.set_return_type('void')

    fd.add_function('drawRectangle')
    fd.set_scope('drawRectangle')
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    fd.add_var('bx', 'double', 0.0, 1)
    fd.add_var('by', 'double', 0.0, 1)
    fd.add_var('size', 'int', 1, 1)
    fd.add_var('fill', 'string', '', 1)
    fd.add_var('line', 'string', '', 1)
    fd.update_function_params('ax', 'double')
    fd.update_function_params('ay', 'double')
    fd.update_function_params('bx', 'double')
    fd.update_function_params('by', 'double')
    fd.update_function_params('size', 'int')
    fd.update_function_params('fill', 'string')
    fd.update_function_params('line', 'string')
    fd.functions['drawRectangle'].expected_arguments = 7
    fd.set_return_type('void')

    fd.add_function('drawDot')
    fd.set_scope('drawDot')
    fd.add_var('x', 'double', 0.0, 1)
    fd.add_var('y', 'double', 0.0, 1)
    fd.add_var('fill', 'string', '', 1)
    fd.update_function_params('x', 'double')
    fd.update_function_params('y', 'double')
    fd.update_function_params('fill', 'string')
    fd.functions['drawDot'].expected_arguments = 3
    fd.set_return_type('void')

    fd.add_function('drawCurve')
    fd.set_scope('drawCurve')
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    fd.add_var('bx', 'double', 0.0, 1)
    fd.add_var('by', 'double', 0.0, 1)
    fd.add_var('fill', 'string', '', 1)
    fd.update_function_params('ax', 'double')
    fd.update_function_params('ay', 'double')
    fd.update_function_params('bx', 'double')
    fd.update_function_params('by', 'double')
    fd.update_function_params('fill', 'string')
    fd.functions['drawCurve'].expected_arguments = 5
    fd.set_return_type('void')

    fd.add_function('insertImage')
    fd.set_scope('insertImage')
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    fd.add_var('filename', 'string', '', 1)
    fd.update_function_params('ax', 'double')
    fd.update_function_params('ay', 'double')
    fd.update_function_params('filename', 'string')
    fd.functions['insertImage'].expected_arguments = 3
    fd.set_return_type('void')

    fd.reset_scope()
    return fd
