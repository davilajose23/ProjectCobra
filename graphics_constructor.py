from graphics import *

class GraphicsConstructor(object):
    def __init__(self):
        self.window = GraphWin('ProjectCobra', 900, 900)

    def construct(name, arguments):
        if name == 'vgdrawText':
            point = Point(float(arguments.get('x')), float(arguments.get('y')))
            text = Text(point, arguments.get('text'))
            text.setFill(arguments.get('color'))
            text.setSize(arguments.get('size'))
            text.setFace('courier')
            text.draw(self.window)

        elif name == 'vgdrawLine':
            a = Point(float(arguments.get('ax')), float(arguments.get('ay')))
            b = Point(float(arguments.get('bx')), float(arguments.get('by')))
            line = Line(a, b)
            line.setFill(arguments.get('fill'))
            line.setWidth(str(argumens.get('size')))
            line.draw(self.window)           

        elif name == 'vgdrawCircle':
            point = Point(float(arguments.get('x')), float(arguments.get('y')))
            circle = Circle(point, float(arguments.get('radio')))
            circle.setFill(arguments.get('fill'))
            circle.setOutline(arguments.get('line'))
            circle.setWidth(str(arguments.get('size')))
            circle.draw(self.window)          

        elif name == 'vgdrawOval':
            a = Point(float(arguments.get('ax')), float(arguments.get('ay')))
            b = Point(float(arguments.get('bx')), float(arguments.get('by')))
            oval = Oval(a, b)
            oval.setFill(arguments.get('fill'))
            oval.setOutline(arguments.get('line'))
            oval.setWidth(str(arguments.get('size')))
            oval.draw(self.window)

        elif name == 'vgdrawTriangle':
            a = Point(float(arguments.get('ax')), float(arguments.get('ay')))
            b = Point(float(arguments.get('bx')), float(arguments.get('by')))
            c = Point(float(arguments.get('cx')), float(arguments.get('cy')))
            triangle = Polygon(a, b, c)
            triangle.setFill(arguments.get('fill'))
            triangle.setOutline(arguments.get('line'))
            triangle.setWidth(str(arguments.get('size')))
            triangle.draw(self.window)

        elif name == 'vgdrawRectangle':
            a = Point(float(arguments.get('ax')), float(arguments.get('ay')))
            b = Point(float(arguments.get('bx')), float(arguments.get('by')))
            rectangle = Rectangle(a, b)
            rectangle.setFill(arguments.get('fill'))
            rectangle.setOutline(arguments.get('line'))
            rectangle.setWidth(str(arguments.get('size')))
            rectangle.draw(self.window)          

        elif name == 'vgdrawDot':
            dot = Point(float(arguments.get('x')), float(arguments.get('y')))
            dot.setFill(str(arguments.get('fill')))
            dot.draw(self.window)

        elif name == 'vgdrawCurve':
            c1 = Point(float(arguments.get('ax')), float(arguments.get('ay')))
            c1x = c1.getX()
            c1y = c1.getY()
            c2 = Point(float(arguments.get('bx')), float(arguments.get('by')))
            c2x = c2.getX()
            c2y = c2.getY()

            curvx = 300
            curvy = 400

            cont = 0.0
            while cont < 1:
                aux = 1 - cont
                x = aux**2 * c1x + 2 * aux * cont * curvx + cont**2 * c2x
                y = aux**2 * c1y + 2 * aux * cont * curvy + cont**2 * c2y
                point = Point(x, y)
                point.setOutline(arguments.get('fill'))
                point.draw(self.win)	
                cont += 0.001
    
    def display():

