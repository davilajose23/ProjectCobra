(Goto, None, None, 27)
(=, 0, , itfirst)
(=, 9, , itlast)
(=, false, , btfound)
(<=, itfirst, itlast, btt1)
(!=, btfound, true, btt2)
(and, btt1, btt2, btt3)
(GotoF, btt3, None, 25)
(+, itfirst, itlast, itt4)
(/, itt4, 2, itt5)
(=, itt5, , itmid)
(Verify, itmid, 0, 10)
(==, iglist.itmid, ititem, btt6)
(GotoF, btt6, None, 16)
(=, true, , btfound)
(Goto, None, None, 24)
(Verify, itmid, 0, 10)
(<, ititem, iglist.itmid, btt7)
(GotoF, btt7, None, 22)
(-, itmid, 1, itt8)
(=, itt8, , itlast)
(Goto, None, None, 24)
(+, itmid, 1, itt9)
(=, itt9, , itfirst)
(Goto, None, None, 4)
(Return, btfound, None, None)
(EndProc, , , )
(=, 0, , ili)
(<, ili, 10, blt1)
(GotoF, blt1, None, 35)
(Verify, ili, 0, 10)
(=, ili, , iglist.ili)
(+, ili, 1, ilt2)
(=, ilt2, , ili)
(Goto, None, None, 28)
(ERA, bgbinary_search, , )
(Param, 2, , ititem)
(Gosub, bgbinary_search, , 1)
(=, bgbinary_search, None, blt3)
(Print, blt3, \n, )
(ERA, bgbinary_search, , )
(Param, 20, , ititem)
(Gosub, bgbinary_search, , 1)
(=, bgbinary_search, None, blt4)
(Print, blt4, \n, )
(END, , , )
