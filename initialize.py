def add_custom_functions(fd):
    '''Agrega funciones personalizdas de la libreria graphics'''

    # Funcion para mostrar texto
    fd.add_function('drawText')
    fd.set_scope('drawText')
    # Coordenana para el centro del texto
    fd.add_var('x', 'double', 0.0, 1)
    fd.add_var('y', 'double', 0.0, 1)
    # Color del texto
    fd.add_var('color', 'string', '', 1)
    # Valor del texto
    fd.add_var('text', 'string', '', 1)
    # Grosor
    fd.add_var('size', 'int', 0, 1)
    # Agrega como parametros de la funcion
    fd.update_function_params('x', 'double')
    fd.update_function_params('y', 'double')
    fd.update_function_params('text', 'string')
    fd.update_function_params('size', 'int')
    fd.update_function_params('color', 'string')
    fd.functions['drawText'].expected_arguments = 5
    fd.set_return_type('void')

    # Funcion para dibujar lineas
    fd.add_function('drawLine')
    fd.set_scope('drawLine')
    # Coordenada de inicio
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    # Coordenada final
    fd.add_var('bx', 'double', 0.0, 1)
    fd.add_var('by', 'double', 0.0, 1)
    # Grosor de la linea
    fd.add_var('size', 'int', 0, 1)
    # Color
    fd.add_var('fill', 'string', 0, 1)
    # Agrega como parametros de la funcion
    fd.update_function_params('ax', 'double')
    fd.update_function_params('ay', 'double')
    fd.update_function_params('bx', 'double')
    fd.update_function_params('by', 'double')
    fd.update_function_params('size', 'int')
    fd.update_function_params('fill', 'string')
    fd.functions['drawLine'].expected_arguments = 6
    fd.set_return_type('void')

    # Funcion para dibujar circulos
    fd.add_function('drawCircle')
    fd.set_scope('drawCircle')
    # Coordenada central
    fd.add_var('x', 'double', 0.0, 1)
    fd.add_var('y', 'double', 0.0, 1)
    # Radio del circulo
    fd.add_var('radio', 'double', 1.0, 1)
    # Grosor
    fd.add_var('size', 'int', 1, 1)
    # Color interno
    fd.add_var('fill', 'string', '', 1)
    # Color contorno
    fd.add_var('line', 'string', '', 1)
    # Agrega como parametros de la funcion
    fd.update_function_params('x', 'double')
    fd.update_function_params('y', 'double')
    fd.update_function_params('radio', 'double')
    fd.update_function_params('size', 'int')
    fd.update_function_params('fill', 'string')
    fd.update_function_params('line', 'string')
    fd.functions['drawCircle'].expected_arguments = 6
    fd.set_return_type('void')

    # Funcion para dibujar ovalos
    # Calcula altura y anchura con 2 coordenadas
    fd.add_function('drawOval')
    fd.set_scope('drawOval')
    # Coordanda de inicio
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    # Coordenada de fin
    fd.add_var('bx', 'double', 0.0, 1)
    fd.add_var('by', 'double', 0.0, 1)
    # Grosor
    fd.add_var('size', 'int', 1, 1)
    # Color interno
    fd.add_var('fill', 'string', '', 1)
    # Color contorno
    fd.add_var('line', 'string', '', 1)
    # Agrega como parametros de la funcion
    fd.update_function_params('ax', 'double')
    fd.update_function_params('ay', 'double')
    fd.update_function_params('bx', 'double')
    fd.update_function_params('by', 'double')
    fd.update_function_params('size', 'int')
    fd.update_function_params('fill', 'string')
    fd.update_function_params('line', 'string')
    fd.functions['drawOval'].expected_arguments = 7
    fd.set_return_type('void')

    # Funcion para dibujar triangulos
    fd.add_function('drawTriangle')
    fd.set_scope('drawTriangle')
    # Coordenada a
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    # Coordenada b
    fd.add_var('bx', 'double', 0.0, 1)
    fd.add_var('by', 'double', 0.0, 1)
    # Coordenada c
    fd.add_var('cx', 'double', 0.0, 1)
    fd.add_var('cy', 'double', 0.0, 1)
    # Grosor
    fd.add_var('size', 'int', 1, 1)
    # Color interno
    fd.add_var('fill', 'string', '', 1)
    # Color de contorno
    fd.add_var('line', 'string', '', 1)
    # Agrega como parametros de la funcion
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

    # Funcion para dibujar rectangulos
    fd.add_function('drawRectangle')
    fd.set_scope('drawRectangle')
    # Coordenada a
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    # Coordenada b
    fd.add_var('bx', 'double', 0.0, 1)
    fd.add_var('by', 'double', 0.0, 1)
    # Grosor
    fd.add_var('size', 'int', 1, 1)
    # Color interno
    fd.add_var('fill', 'string', '', 1)
    # Color de contorno
    fd.add_var('line', 'string', '', 1)
    # Agrega como parametros de la funcion
    fd.update_function_params('ax', 'double')
    fd.update_function_params('ay', 'double')
    fd.update_function_params('bx', 'double')
    fd.update_function_params('by', 'double')
    fd.update_function_params('size', 'int')
    fd.update_function_params('fill', 'string')
    fd.update_function_params('line', 'string')
    fd.functions['drawRectangle'].expected_arguments = 7
    fd.set_return_type('void')

    # Funcion para dibujar puntos
    fd.add_function('drawDot')
    fd.set_scope('drawDot')
    # Coordenada del punto
    fd.add_var('x', 'double', 0.0, 1)
    fd.add_var('y', 'double', 0.0, 1)
    # Color del punto
    fd.add_var('fill', 'string', '', 1)
    # Agrega como parametros de la funcion
    fd.update_function_params('x', 'double')
    fd.update_function_params('y', 'double')
    fd.update_function_params('fill', 'string')
    fd.functions['drawDot'].expected_arguments = 3
    fd.set_return_type('void')

    # Funcion para dibujar puntos
    fd.add_function('drawCurve')
    fd.set_scope('drawCurve')
    # Coordenada inicial
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    # Coordenada final
    fd.add_var('bx', 'double', 0.0, 1)
    fd.add_var('by', 'double', 0.0, 1)
    # Color
    fd.add_var('fill', 'string', '', 1)
    # Agrega como parametros de la funcion
    fd.update_function_params('ax', 'double')
    fd.update_function_params('ay', 'double')
    fd.update_function_params('bx', 'double')
    fd.update_function_params('by', 'double')
    fd.update_function_params('fill', 'string')
    fd.functions['drawCurve'].expected_arguments = 5
    fd.set_return_type('void')

    # Funcion para insertar imagenes en el canvas
    fd.add_function('insertImage')
    fd.set_scope('insertImage')
    # Coordenada central de la imagen
    fd.add_var('ax', 'double', 0.0, 1)
    fd.add_var('ay', 'double', 0.0, 1)
    # Nombre del archivo
    fd.add_var('filename', 'string', '', 1)
    # Agrega como parametros de la funcion
    fd.update_function_params('ax', 'double')
    fd.update_function_params('ay', 'double')
    fd.update_function_params('filename', 'string')
    fd.functions['insertImage'].expected_arguments = 3
    fd.set_return_type('void')

    # Regresa escope al main para empezar a leer archivo de entrada
    fd.reset_scope()
    return fd
