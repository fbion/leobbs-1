$onlinepopup = qq~<script language="JavaScript">
<!--
var oPopup = window.createPopup();
var popTop = 0;
var IsStop = false;
var popTopStep = 5;

function popmsg()
{
	if (!document.all) return;
	var winstr = '<div id=main style="width:220px; height:120px; border:solid 1px $titleborder; background-color: $menubackground; padding: 4px"><table border=0 width=97% height=97% bgcolor=$menubackground cellspacing=6 cellpadding=2 style="font-family: 宋体; font-size: 9pt"><tr><td width=100%><center><b><font color=$fonthighlight>☆ 在 线 好 友 提 示 ☆</font></b></center><p>$onlinepopup<br></td></tr></table></div>';
	oPopup.document.body.innerHTML = winstr;
	oPopup.document.body.oncontextmenu = function() {return false;}
	oPopup.document.body.onselectstart = function() {return false;}
	oPopup.document.body.onDragDrop = function() {return false;}
	oPopup.document.body.onmouseover = function() {IsStop=true;}
	oPopup.document.body.onmouseout = function() {IsStop=false;}
	onlineINT = setInterval('popshow()', 50);
}
function popshow()
{
	if (!IsStop) popTop += popTopStep;
	if (popTop > 270)
		popTopStep = -5;
	if (popTop < 0)
	{
		popTop = 0;
		popTopStep = 5;
		clearInterval(onlineINT);
		oPopup.hide();
	}
	var showheight = popTop > 120 ? 120 : popTop;
	oPopup.show(screen.width - 221, screen.height - showheight - 25, 220, showheight);
}
setTimeout('popmsg("")', 100);
-->
</script>
~;
1;