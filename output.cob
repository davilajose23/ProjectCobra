(Goto, None, None, 17)
(==, itx, 0, btt1)
(GotoF, btt1, None, 5)
(=, itacum, , itres)
(Goto, None, None, 15)
(+, itacum, itx, itt2)
(=, itt2, , itacum)
(-, itx, 1, itt3)
(=, itt3, , itx)
(ERA, igsumaRecursiva, , )
(Param, itx, , itx)
(Param, itacum, , itacum)
(Gosub, igsumaRecursiva, , 1)
(=, igsumaRecursiva, None, itt4)
(=, itt4, , itres)
(Return, itres, None, None)
(EndProc, , , )
(ERA, igsumaRecursiva, , )
(Param, 3, , itx)
(Param, 0, , itacum)
(Gosub, igsumaRecursiva, , 1)
(=, igsumaRecursiva, None, ilt1)
(=, ilt1, , ilx)
(Print, ilx, \n, )
(END, , , )
