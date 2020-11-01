//3FACE 商品分类下拉菜单代码
 var h;
 var w;
 var l;
 var t;
 var topMar = 1;
 var leftMar = 0;
 var space = 1;
 var isvisible;

function mOverNav(navTD, caption)
{
	if (!navTD.contains(event.fromElement))
	{navTD.style.backgroundColor='#EEEEEE';}
}
function mOutNav(navTD, caption)
{
	if (!navTD.contains(event.toElement))
	{navTD.style.backgroundColor='#FFFFFF';}
}

function _HideMenu() 
{
 var mX;
 var mY;
 var vDiv;
 var mDiv;
 if (isvisible == true)
 {
	vDiv = document.all("_menuDiv");
	mX = window.event.clientX + document.body.scrollLeft;
	mY = window.event.clientY + document.body.scrollTop;
	if ((mX < parseInt(vDiv.style.left)) || (mX > parseInt(vDiv.style.left)+vDiv.offsetWidth) || (mY < parseInt(vDiv.style.top)-h) || (mY > parseInt(vDiv.style.top)+vDiv.offsetHeight)){
		vDiv.style.visibility = "hidden";
		_Search.style.visibility = "visible";
		isvisible = false;
	}
 }
}

function ShowMenu(vMnuCode,tWidth) {
	vSrc = window.event.srcElement;
	vMnuCode = "<table id='submenu' cellspacing=1 cellpadding=3 style='width:"+tWidth+"' bgcolor=#A0BCE7 border=0 onmouseout='_HideMenu()'>" + vMnuCode + "</table>";

	h = vSrc.offsetHeight;
	w = vSrc.offsetWidth;
	l = vSrc.offsetLeft + leftMar;
	t = vSrc.offsetTop + topMar + h + space;
	vParent = vSrc.offsetParent;
	while (vParent.tagName.toUpperCase() != "BODY")
	{
		l += vParent.offsetLeft;
		t += vParent.offsetTop;
		vParent = vParent.offsetParent;
	}
	_Search.style.visibility = "hidden";
	_menuDiv.innerHTML = vMnuCode;
	_menuDiv.style.top = t;
	_menuDiv.style.left = l;
	_menuDiv.style.visibility = "visible";
	isvisible = true;
}

//背景类
var MENU2 = "<tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('2'); onMouseOver=DispSubMenu1('2'); style=cursor:hand; title='超眩背景'>超眩背景</span></td></tr>"

//衣服类
var MENU3 = "<tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('8'); onMouseOver=DispSubMenu1('8'); style=cursor:hand; title='裤裙'>裤裙</span></td></tr><tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('9'); onMouseOver=DispSubMenu1('9'); style=cursor:hand; title='上衣'>上衣</span></td></tr>"

//头部类
var MENU4 = "<tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('14'); onMouseOver=DispSubMenu1('14'); style=cursor:hand; title='面部表情'>面部表情</span></td></tr><tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('18'); onMouseOver=DispSubMenu1('18'); style=cursor:hand; title='发型'>发型</span></td></tr><tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('20'); onMouseOver=DispSubMenu1('20'); style=cursor:hand; title='帽子'>帽子</span></td></tr><tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('21'); onMouseOver=DispSubMenu1('21'); style=cursor:hand; title='眼镜'>眼镜</span></td></tr>"

//打扮类
var MENU5 = "<tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('10'); onMouseOver=DispSubMenu1('10'); style=cursor:hand; title='项饰品'>项饰品</span></td></tr><tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('23'); onMouseOver=DispSubMenu1('23'); style=cursor:hand; title='宠物'>宠物</span></td></tr>"



function displayMenu()
{
    s = "<table cellspacing=0 cellpadding=0 border=0><tr align=center><td><span style='width=80;cursor: hand;' onMouseOver='ShowMenu(MENU2,80)' title='各种各样的背景图片1'>背景类</span></td><td><span style='width=80;cursor: hand;' onMouseOver='ShowMenu(MENU3,80)' title='上衣和裤裙'>衣服类</span></td><td><span style='width=80;cursor: hand;' onMouseOver='ShowMenu(MENU4,80)' title='包含脸型、口鼻、胡子、帽子、眼镜等'>头部类</span></td><td><span style='width=80;cursor: hand;' onMouseOver='ShowMenu(MENU5,80)' title='各类饰品'>打扮类</span></td></tr></table>";
    document.write(s);
}
