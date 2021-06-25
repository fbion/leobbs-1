function buyface(classid,id,action)
{
   if(action == 'delsp')
   {
	if(!confirm("本操作不可恢复，你是否确认系统回收此商品？"))return false;
   }
   var Win=window.open("buyface.cgi?action="+action+"&class="+classid+"&id="+id,"BUY",'width=420,height=270,resizable=0,scrollbars=0,menubar=0,status=1');
}

function GetCookie(name){
var cname = name + "=";
var dc = document.cookie;
if (dc.length > 0) {
begin = dc.indexOf(cname);
if (begin != -1) {
begin += cname.length;
end = dc.indexOf(";", begin);
if (end == -1) end = dc.length;
return dc.substring(begin, end); }
}
return null;
}

var currface = GetCookie('tempequip');
Fitting(currface,Show);

function CHECK(par1,par2,par3,par4)
{
    if ((par3 != par4) && (par3 != 't'))
    {
	alert("对不起，性别不符，您无法试穿！");
	return;
    }
    par4 = (par4 == 'm') ? 'init': 'initf';

    var CFace = GetCookie('tempequip');
    var showArray = CFace.split('-');
    var showArrayLen = showArray.length;

    if(showArray[par1] == par2)
    {
	showArray[par1] = ((par1 == 7) || (par1 == 8) || (par1 == 9) || (par1 == 11) || (par1 == 13) || (par1 == 14) || (par1 == 18)) ? par4 : 0;
    }
    else
    {	showArray[par1] = par2;    }

    var newequip = "0";
    for (var i=1; i<=25; i++)
    {
	newequip += "-" + showArray[i] + "";
    }
    Fitting(newequip,Show);
    document.cookie = "tempequip=" + newequip + ";";
}

function myfriend()
{
    var myfriend = document.FORM.friends.options[document.FORM.friends.selectedIndex].value;
    if (myfriend != "") document.FORM.sendname.value = myfriend;
}
function seletype()
{
   var id = document.SEARFORM.type_search.value;
   if(id == 0)
    typeinfo.innerHTML = "<select name='key_type'><option value='b'>大于<option value='s'>小于<option value='e'>等于</select> <input type=text size=6 name='search_key'>";
   if(id == 1)
    typeinfo.innerHTML = "<select name='search_key'><option value='m'>男性<option value='f'>女性<option value='t'>男女适用</select>";
   if(id == 2)
    typeinfo.innerHTML = "<input type=text size=16 name='search_key'>";
}

function checksear()
{
   if(document.SEARFORM.type_search.value == "")
   {
	alert("请选择搜索类别！");
	document.SEARFORM.type_search.focus();
	return false;
   }
   if(document.SEARFORM.search_key.value == "")
   {
	alert("请输入搜索的关键字！");
	document.SEARFORM.search_key.focus();
	return false;
   }
}
