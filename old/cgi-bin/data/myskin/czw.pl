$yemei = qq~
<table width=$tablewidth border="0" cellspacing="0" cellpadding="0" align="center"><tr><td><img src=$imagesurl/images/czw/toplogo-1.jpg></td><td><img src=$imagesurl/images/czw/toplogo-2.jpg></td></tr></table>

<table width=$tablewidth border="0" cellspacing="0" cellpadding="0" align="center"><tr><td>
<img src=$imagesurl/images/czw/toplogo-3.jpg border=0></td>
<td><img src=$imagesurl/images/czw/topan-1.jpg border=0></td>
<td><img src=$imagesurl/images/czw/topan-2.jpg border=0></td>
<td><a href=leoboard.cgi title=论坛首页><img src=$imagesurl/images/czw/topan-3.jpg border=0></a></td>
</td></tr></table>

<table width=$tablewidth border="0" cellspacing="0" cellpadding="0" align="center"><tr><td><img src=$imagesurl/images/czw/toplogo-4.jpg border=0></td></tr></table>
<table width=$tablewidth cellspacing=0 cellpadding=0 align=center></table><br>
<TABLE cellSpacing=0 cellPadding=0 width=$tablewidth align=center>
<tr><TD width=30% rowSpan=3>$forumgraphicoutput</TD>
<TD vAlign=bottom align=right>$adscript</TD></TR></TABLE><br>~;

$daohang = qq~<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$titleborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr><td bgcolor=$menubackground $menubackpic><font color=$menufontcolor>>> 欢迎您，$loggedinas </td><td bgcolor=$menubackground align=right $menubackpic>$sann<a href=$homeurl target=_blank><img src=$imagesurl/images/gohome.gif height=16 border=0></a>&nbsp;</td></tr></table></td></tr></table>$newmail~;

$firstout = "yemei";
1;
