(Goto, None, None, 1)
(Verify, 0, 0, 1)
(=, 1, , ilb.0)
(=, 0, , ili)
(<, ili, 5, blt1)
(GotoF, blt1, None, 13)
(Verify, ili, 0, 5)
(=, ili, , iga.ili)
(Verify, ili, 0, 5)
(Print, iga.ili, \n, )
(+, ili, 1, ilt2)
(=, ilt2, , ili)
(Goto, None, None, 4)
(Verify, 0, 0, 1)
(Verify, ilb.0, 0, 5)
(=, 50, , iga.ilb.0)
(Verify, 0, 0, 1)
(Verify, ilb.0, 0, 5)
(Print, iga.ilb.0, \n, )
(END, , , )
