$daohang = qq~
<table width=95% border="0" cellspacing="0" cellpadding="0" align="center"><tr><td width=131><img src=$imagesurl/images/macos/toplogo.jpg></td><td background=$imagesurl/images/macos/toplogobg.jpg width=100%></td><td width=131><img src=$imagesurl/images/macos/toplogo2.jpg></td></tr></table>
<table width=95% border="0" cellspacing="0" cellpadding="0" align="center"><tr><td width=131><img src=$imagesurl/images/macos/1.gif></td><td background=$imagesurl/images/macos/2.gif width=100%></td><td width=131><img src=$imagesurl/images/macos/3.gif></td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$titleborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr><td bgcolor=$menubackground $menubackpic><font color=$menufontcolor>>> 欢迎您，$loggedinas $myskins</td><td bgcolor=$menubackground align=right $menubackpic>$sann<a href=$homeurl target=_blank><img src=$imagesurl/images/gohome.gif height=16 border=0></a>&nbsp;</td></tr></table></td></tr></table>$newmail~;

$yemei = qq~<TABLE cellSpacing=0 cellPadding=0 width=$tablewidth align=center>
<tr><TD width=30% rowSpan=3>$forumgraphicoutput</TD>
<TD vAlign=bottom align=right>$adscript</TD></TR></TABLE>~;

$firstout = "daohang";

1;
