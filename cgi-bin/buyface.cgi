#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

BEGIN {
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use LBCGI;
$LBCGI::POST_MAX=600000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "data/cityinfo.cgi";
require "face/config.pl";
require "facelib.pl";
$|++;
$query = new LBCGI;
$thisprog = "buyface.cgi";

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
}

$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$action = $query->param('action');

&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));

if ($inmembername eq "" || $inmembername eq "客人" ) {
    &error("不能进入 $plugname &你目前的身份是访客，请先登陆!");
    exit;
} else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie  = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie  = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
     }
}

$tempmembername = $inmembername;
$tempmembername =~ s/ /\_/g;
$tempmembername =~ tr/A-Z/a-z/;

$mymoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

&readface("$tempmembername",0);

$currenttime = time();
$currenttime = &dateformat("$currenttime");

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print qq~
<html>
<head>
<title>$plugname</title>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<style>
A:visited{TEXT-DECORATION: none}
A:active{TEXT-DECORATION: none}
A:hover{TEXT-DECORATION: underline overline}
A:link{text-decoration: none;}
TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: 宋体; FONT-SIZE: 9pt} 
.S1{LINE-HEIGHT: 1.2}
</style>
</head>
<body bgcolor="#ffffff" topmargin=0 leftmargin=0>~;

my %Mode = ('buy' => \&buy_sp,'save' => \&savesp,'bag' => \&bag,'delsp' => \&delsp,'zeng' => \&zengsp,'zengok' => \&zengok);

if ($Mode{$action})
{
$Mode{$action} -> ();
}
else{&error("$plugname&老大，别乱黑我的程序呀！！");}

sub buy_sp
{
    $cartLength = $query->cookie("cartLength");
    &errorout("购物商品&当前的购物袋为空！&1") if(($cartLength eq '')||($cartLength eq '0'));

    for ($i = 0; $i < $cartLength; $i++)
    {
	$itemsinfo = $query->cookie("items[$i]");
	($name,$sort_id,$id,$buy_num,$x,$x)=split(/\|/,$itemsinfo);
###
	$/="";
	my $filetoopen = "$lbdir" . "face/wpdata/$sort_id.pl";
	&errorout("购物商品&商品类别的文件不存在！&1") if (!( -e "$filetoopen")); # 如果不存在文件
	open(FILE,"$filetoopen");
	my $sort=<FILE>;
	close(FILE);
	$/="\n";

	&errorout("购物商品&非常抱歉，$name 商品在数据库中不存在！&1") if($sort !~ /$id\t(.*)/); # 找到指定的商品ID
        ($sp_name,$sp_money,$x,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$sp_suit,$sp_suitid)=split(/\t/,$1);

###
	for($j=0;$j<$buy_num;$j++)
	{
	    $array1{$sort_id} .= "$id,N\_";	# 保存格式
	}
	$array2{$sort_id} += "$buy_num";					# 关联数组格式：类别号、数量
	$array3{$id} = "1\t$sp_name\t$buy_num\t$sp_money\t$currenttime\t\t\n";	# 记录个人购买信息
    }

    @array2 = keys(%array2);

    for($i=0;$i<@array2;$i++)
    {
	$aaaa = @array2[$i];
	@tempnum = split(/\_/,@buy_sp[$aaaa]);
	$tempnum = @tempnum;
	$temp = $tempnum + $array2{$aaaa};
	&errorout("购物商品&非常抱歉，相同的商品数量超出规定值：$samnum 件(含已购买的)！&1") if($temp > $samnum);
    }

    $TotalCost = $query->cookie("totalCost");	# 获取总价格
    &errorout("购物商品&非常抱歉，您的现金不够支付购物袋的商品！&1") if ($mymoney < $TotalCost);

    @array1 = keys(%array1);

    for($i=0;$i<@array1;$i++)
    {
	$aaaa = @array1[$i];
	@buy_sp[$aaaa] = @buy_sp[$aaaa] ne '' ? "@buy_sp[$aaaa]_$array1{$aaaa}" : "$array1{$aaaa}";
	chop(@buy_sp[$aaaa]);
    }

    for($i=1;$i<26;$i++)
    {
	$newdata .= "@buy_sp[$i]-";
    }
    chop($newdata);

    &upplugdata("$tempmembername","$currequip|$newdata|$loadface","-$TotalCost");

##### 统计使用数
    $filetoopen = "$lbdir" . "face/totaluser.cgi";
    open(FILE,"$filetoopen");
    my $totaluser=<FILE>;
    close(FILE);
    if($totaluser !~ /$tempmembername\t/)
    {
	open(FILE, ">>$filetoopen");
	print FILE "$tempmembername\t";
	close(FILE);
    }
#####

    $filetoopen = "$lbdir" . "face/log/$tempmembername.pl";
    open(FILE,"$filetoopen");
    my @mylog=<FILE>;
    open(FILE, ">$filetoopen");
    @array3 = values(%array3);
    foreach (@array3)
    {
	print FILE $_;
    }

    foreach $z (@mylog){
	$a=$a+1;
	if ($a < $lognum){print FILE "$z";}
    }
    close(FILE);

    print qq~
<SCRIPT language="javaScript" SRC="$imagesurl/face/js/buy.js"></SCRIPT>
<SCRIPT>
function delAlls()
{
  var cartLength = getCookie('cartLength');
  if((cartLength  == "") || (cartLength == 0))
      return;

  for (var i = 0; i < cartLength; i ++)
  {
      eval("deleteCookie('items["+i+"]')");
  }
  cartLength = 0;
  setCookie('cartLength', cartLength);
}
delAlls();
alert("商品购买成功，请到 我的衣柜 装备！");
self.close();
</SCRIPT>~;
}

sub savesp
{
    &errorout("保存失败&你的虚拟形象数据不存在，保存失败&1！") if ($userface eq '');

    my $spsort1	= $query->cookie("_SortArray");	# 分类号
    my $spid1	= $query->cookie("_SPIDArray");	# 商品ID号
    my $spstate1= $query->cookie("_StateArray");# 商品状态
    my @SPSort = split(/\,/,$spsort1);
    my @SPID = split(/\,/,$spid1);
    my @SPState = split(/\,/,$spstate1);

    for($i=0;$i<@SPSort;$i++)
    {
	$SPINFO{@SPSort[$i]} .= "@SPID[$i]-@SPState[$i]|";
    }

    for($i=1;$i<26;$i++)
    {
	@tempsp=split(/\_/,@buy_sp[$i]);
	next if(@tempsp eq "");

	$/="";
	my $filetoopen = "$lbdir" . "face/wpdata/$i.pl";
	open(FILE,"$filetoopen");
	my $sort=<FILE>;
	close(FILE);
	$/="\n";
	$temp1 = 0;
	$tempdata = '';
	for($j=0;$j<@tempsp;$j++)
	{
	    my ($info1,$info2)=split(/\,/,@tempsp[$j]);
	    my $ladesign = $info2 eq 'Y' ? 1 : 0 ;
	    $spsort2 .= qq~$i,~;
	    $spid2 .= qq~$info1,~;
	    $spstate2 .= qq~$ladesign,~;

	    if($SPINFO{$i} ne '')
	    {
		my @temparray = split(/\|/,$SPINFO{$i});
		my ($tempid,$tempstate) = split(/\-/,@temparray[$j]);
		my $ladesign = $tempstate eq '1' ? 'Y' : 'N';
		$info2 = $ladesign if($tempid eq $info1);
		$tempdata .= qq~$info1,$info2\_~;
	    }
###
	    if($sort =~ /$info1\t(.*)/)
	    {
	        my ($sp_name,$sp_money,$x,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$sp_suit,$sp_suitid)=split(/\t/,$1);

	        if($info2 eq 'Y')
	        {
		    $sp_graphic =~s /\.gif//;
		    @currequip[$i] = $sp_graphic;
		    $temp1 = 1;
	        }
	        else
	        {
		     next if($temp1 eq '1');
		     if(($i eq '7')||($i eq '8')||($i eq '9')||($i eq '11')||($i eq '13')||($i eq '14')||($i eq '18'))
		     {
			@currequip[$i] = $sex eq 'f' ? "initf" : "init";
		     }
		     else
		     {
			@currequip[$i] = 0;
		     }
		}
	    }
###
	}
	chop($tempdata);
	$outinfo .= qq~$tempdata-~;
    }
    chop($spsort2);
    chop($spid2);
    chop($spstate2);
    chop($outinfo);

    &errorout("保存失败&请不要乱来&1！") if(($spsort1 ne $spsort2) || ($spid1 ne $spid2));
    &errorout("保存失败&系统发现您的装备状态没有改变，并不需要保存！&1") if($spstate1 eq $spstate2);

    $newequip = join('-',@currequip);
    &upplugdata("$tempmembername","$newequip|$outinfo|$loadface","");

print qq~
<SCRIPT LANGUAGE="JavaScript">
document.cookie = "_SortArray=" + "" +"; path=$cookiepath/";
document.cookie = "_SPIDArray=" + "" +"; path=$cookiepath/";
document.cookie = "_StateArray=" + "" +"; path=$cookiepath/";
opener.location.reload();
alert("当前形象保存成功！");
self.close();
</SCRIPT>~;
    exit;
}

sub bag
{ # 购物袋
    print qq~
<SCRIPT>
function openCart() 
{
   var url="$boardurl/buyface.cgi?action=bag"
   var cart;
   cart =window.open(url,"Cart","menubar=no,toolbar=no,location=no,directories=no,status=no,width=530,height=400,left=150,top=100,scrollbars=yes");
   cart.focus();
}
</SCRIPT>
<SCRIPT language="javaScript" type="text/javascript" SRC="$imagesurl/face/js/buy.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
function subItemQuantity(num, typeid) 
{
	var i;
	var infoArray = new Array;
	var cartLength = getCookie('cartLength');
	if(cartLength  == "" || cartLength == 0) 
	    return;
	infoArray[1] = typeid;
	infoArray[2] = num;

	var i = checkExistItem(infoArray, cartLength);
	if(i != -1) //找到了item[i]
	{
	    infoArray = getItemsInfo(i); 
	    var count = infoArray[3];
	    count --;
	    if(count == 0) //item数量减到了0
	    {
		delItem(i);
		return;
	    }

	    infoArray[3] = count;
	    saveItemsinfo(infoArray, i);
	    openCart();
	    return;
	}
}

function delItem(i)
{
  var tmpArray = new Array;
  var cartLength = getCookie('cartLength');
  if((cartLength  == "") || (cartLength == 0))
      return;

  if(cartLength == 1)
  {
      deleteCookie('items[0]');
      setCookie('cartLength', 0);  
      openCart();
      return;
  }
  cartLength --;
      for (i = i; i < cartLength; i ++)
      {
	tmpArray = getItemsInfo(i + 1);
	saveItemsinfo(tmpArray, i);
      }
      eval("deleteCookie('items["+cartLength+"]')");
      setCookie('cartLength', cartLength);
      openCart();
}

function delAll()
{
  var cartLength = getCookie('cartLength');
  if((cartLength  == "") || (cartLength == 0))
      return;
  for (var i = 0; i < cartLength; i ++)
  {
      eval("deleteCookie('items["+i+"]')");
  }
  cartLength = 0;
  setCookie('cartLength', cartLength);
  alert("购物袋已经清空！");
  self.close();
}

function delAlls()
{
  var cartLength = getCookie('cartLength');
  if((cartLength  == "") || (cartLength == 0))
      return;

  for (var i = 0; i < cartLength; i ++)
  {
      eval("deleteCookie('items["+i+"]')");
  }
  cartLength = 0;
  setCookie('cartLength', cartLength);
}

function displayCart()
{
  var s = '';
  var totalCost = 0;
  var name, typeid, num, price, quantity;
  var cartLength = getCookie('cartLength');

  var infoArray = new Array;
  if ((cartLength == "") || (cartLength == 0))
  {
    alert("目前购物袋为空！");
    self.close();
    return;
  }
  for (var i = 0; i < cartLength; i++)
  {
	infoArray = getItemsInfo(i);

	if(infoArray == -1)
	{
		alert("取购物车信息出错，现在自动清空购物车一次!");
		delAll();
		return;
	}
	name = infoArray[0];
	typeid = infoArray[1];
	num = infoArray[2];
	quantity = infoArray[3];
	price = infoArray[4];

	total = price*quantity;
	totalCost = totalCost + total;

	ID = typeid+""+num;
	s = s + '<tr align=center bgcolor=$miscbackone>';
	s = s + '<td width=60>' + ID + '</td>';
	s = s + "<td width=260 align=center>";
	s = s + ''+ name + '';
	s = s + '</td>';
	s = s + '<td width=80>';
        s = s + '' + quantity + '　<img src="$imagesurl/face/images/del.gif" style=cursor:hand alt = "减少" width=11 height=11'; 
	s = s + ' onClick="subItemQuantity(';
	s = s + "'" + num + "','" + typeid + "');";
	s = s + '"> ';
        s = s + '<img src="$imagesurl/face/images/add.gif" alt="增加" width="11" height="11" style=cursor:hand onClick="addItemQuantity(';
	s = s + "'" + name + "','" + typeid + "'," + num + "," + price + ");";
	s = s + '"></td>';
        s = s + '<td width=60 align=right>';
	s = s + price ; 
	s = s + '</td>';
 	s = s + '<td width="40" align=center><img src="$imagesurl/face/images/delt.gif" style=cursor:hand width="24" height="11" alt="删除" onclick="var truth =confirm(';
	s = s + "'确定要删除吗？'); if (truth)  delItem(" + i + ");";
	s = s + '" > </td>'; 
	s = s + '</tr>';
  }
  setCookie('totalCost', totalCost);
  document.write(s);
}

function displayTotal()
{
  var totalCost;
  var cartLength = getCookie('cartLength');  
  if ((cartLength == "") || (cartLength == 0))
      totalCost = 0;
  else
  {
      totalCost = getCookie('totalCost');
  }
  document.write(totalCost);
}
function jz()
{
totalCost = getCookie('totalCost');
  if (confirm('总计：'+totalCost+' $moneyname ，您是否确认购买？'))
	window.location='buyface.cgi?action=buy';
}
</SCRIPT>

<table cellspacing=1 cellpadding=5 width=100% bgcolor=$tablebordercolor border=0>
<tr bgcolor=$miscbacktwo align=left><td><font color=$titlefont size=2><B>我的购物袋</B></font></td></tr>
</table>
<BR>
<table cellspacing=1 cellpadding=5 width=100% bgcolor=$tablebordercolor border=0>
<tr bgcolor=$miscbacktwo align=center>
   <td width=60>商品ID</td>
   <td width=260>商品名称</td>
   <td width=80>订购数量</td>
   <td width=60>商品单价</td>
   <td width=40>&nbsp;</td>
</tr>
<SCRIPT>displayCart();</SCRIPT>
<tr bgcolor=$miscbacktwo>
   <td width=60></td>
   <td width=260></td>
   <td width=80 align=right>总计：</td>
   <td width=60 align=right><SCRIPT>displayTotal();</SCRIPT></td>
   <td width=40>&nbsp;</td>
</tr>
<tr bgcolor=$miscbackone>
   <td width=60></td>
   <td width=260></td>
   <td width=80 align=right>您当前现金：</td>
   <td width=60 align=right>$mymoney</td>
   <td width=40>$moneyname</td>
</tr>
</table>

<table width="100%" border="0" cellspacing="0" cellpadding="0" height="20">
<tr><td>&nbsp;</td></tr>
<tr> 
<td align="center">
<a href="javascript:jz();">我要结帐</a> <a href="#" onclick="if (confirm('确定要全部删除吗？')) delAll(); else return false; ">清空购物袋</a> <a href="javascript:window.close();">继续购物</a>
</td>
</tr>
</table>~;
exit;
}

sub delsp
{
    $class	= $query -> param('class');	# 商品类别号
    $id		= $query -> param('id');	# 商品ID号

    @tempsp = split(/\_/, @buy_sp[$class]);	# 将商品图片分开，使之与商品数量对应

    ($info1,$info2)=split(/\,/,@tempsp[$id]);
    &errorout("丢弃失败&你是否已经丢弃了该商品？&1") if(@tempsp[$id] eq '');
    &errorout("丢弃失败&该商品正在装备中，不能进行丢弃操作！&1") if($info2 eq 'Y');


    for($i=0;$i<@tempsp;$i++)
    {
	$newid .= qq~@tempsp[$i]_~ if($i ne $id);
    }
    chop($newid);
    @buy_sp[$class] = $newid;

    for($i=1;$i<26;$i++)
    {
	$newdata .= "@buy_sp[$i]-";
    }
    chop($newdata);

    &upplugdata("$tempmembername","$currequip|$newdata|$loadface","");

print qq~
<SCRIPT LANGUAGE="JavaScript">
document.cookie = "tempequip=" + "$currequip" +"; path=$cookiepath/";
opener.location.reload();
alert("商品丢弃成功！");
self.close();
</SCRIPT>
~;
    exit;
}

sub zengsp
{
    $class      = $query -> param('class');		# 商品类别文件
    $id	        = $query -> param('id');		# 商品的ID号

    @tempsp = split(/\_/, @buy_sp[$class]);		# 将商品图片分开，使之与商品数量对应

    ($info1,$info2)=split(/\,/,@tempsp[$id]);

    &errorout("赠送商品&建立页面出错，指定的商品号有误&1！") if(@tempsp[$id] eq '');
    &errorout("赠送商品&该商品装备中，必须卸下才能赠送，如果商品\\n已经卸下，您是否忘记点击 '保存当前形象' 了？&1") if($info2 eq 'Y');

###
    $/="";
    my $filetoopen = "$lbdir" . "face/wpdata/$class.pl";
    open(FILE,"$filetoopen");
    my $sort=<FILE>;
    close(FILE);
    $/="\n";

    if($sort =~ /$info1\t(.*)/)	# 找到指定的商品ID
    {
	($sp_name,$sp_money,$x,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$sp_suit,$sp_suitid)=split(/\t/,$1);
	&errorout("赠送商品&小气鬼，免费商品不能赠送给朋友的！&1") if($sp_money eq '0');
	$fitherd = "男" if($sp_fitherd eq 'm');
	$fitherd = "女" if($sp_fitherd eq 'f');
	$fitherd = "通用" if($sp_fitherd eq 't');
    }
    else
    {
	&errorout("赠送商品&建立页面出错，此商品已经不存在，请丢弃此商品！&1");
    }
###
## 好友列表 ###
    if (open(FILE, "${lbdir}memfriend/$tempmembername.cgi"))
    {
	$/="";
	my $currentlist = <FILE>;
	close(FILE);
	$/="\n";
	@currentlist = split (/\n/, $currentlist);
    }

    my $friendlist = qq~<select name=friends onchange="myfriend();"><option style=background-color:$miscbacktwo>好友列表</option>~;

    foreach (@currentlist)
    {
	chomp;
	s/^＊＃！＆＊//isg;
	$friendlist .= qq~<option value="$_">$_</option>~;
    }
## 结束 ##

    print qq~<SCRIPT>
function checkzeng()
{
   if(document.Zeng.zengname.value == "")
   {
	alert("对方的名字不能为空！");
	document.Zeng.zengname.focus();
	return false;
   }
   if(document.Zeng.zengly.value == "")
   {
	alert("留言不能为空！");
	document.Zeng.zengly.focus();
	return false;
   }
   if(!confirm("赠送信息：$sp_name 壹件；您是否确认赠送给 " + document.Zeng.zengname.value + "？"))return false;
}
function myfriend()
{
    var myfriend = document.Zeng.friends.options[document.Zeng.friends.selectedIndex].value;
    if (myfriend != "") document.Zeng.zengname.value = myfriend;
}
</SCRIPT>
<table width=100% border=0 cellspacing=1 cellpadding=5 bgcolor=$tablebordercolor>
<tr><td bgcolor=$miscbacktwo height=20><font color=$titlefont size=2><B>赠送商品</B></font></td></tr>
</table>
<table width=100% border=0 cellspacing=0 cellpadding=4>
<form action="$thisprog" method="post" name=Zeng>
<input type=hidden name="action" value="zengok">
<input type=hidden name="class" value="$class">
<input type=hidden name="id" value="$id">
<TR align=center bgColor=$miscbackone>
  <TD width=40%>商品名称</TD><TD width=30%>适用人群</TD><TD width=30%>商品价格</TD>
</TR>
<TR align=center bgcolor=$miscbacktwo>
  <TD>$sp_name</TD><TD>$fitherd</TD><TD>$sp_money</TD>
</TR>
<TR align=center bgColor=$miscbackone> 
  <TD colspan=3> 　</TD>
</TR>
<TR bgColor=$miscbacktwo> 
  <TD align=center>赠送给</TD><TD colspan=2><input type=text size=12 name="zengname"> $friendlist</TD>
</TR>
<TR bgColor=$miscbacktwo> 
  <TD align=center>留言</TD><TD colspan=2><input type=text size=30 name="zengly"></TD>
</TR>
<TR align=center bgColor=$miscbackone>
  <TD colspan=3><input type=submit value="确 定" onClick="return checkzeng();">
  </TD>
</TR>
</form>
</table>~;
}

sub zengok
{
    $class	= $query -> param('class');	# 商品类别号
    $id		= $query -> param('id');	# 商品ID号
    $zengname	= $query -> param('zengname');	# 赠送人名称
    $zengname	= &cleanarea("$zengname");
    $zengly	= $query -> param('zengly');	# 给赠送人留言
    $zengly	= &cleanarea("$zengly");

    $zengname = &unHTML("$zengname");
    $zengname =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    $zengname =~ s/ /\_/g;
    $zengname =~ tr/A-Z/a-z/;

    my $namenumber = &getnamenumber($zengname);
    &checkmemfile($zengname,$namenumber);
    my $filetoopen = "${lbdir}$memdir/$namenumber/$zengname.cgi";
    &errorout("赠送商品&非常抱歉，社区中不存在此用户名！&0") unless(-e $filetoopen);
    &errorout("赠送商品&你头脑还清醒吗？怎么能给自己赠送？！！&0") if($tempmembername eq $zengname);

    @tempsp = split(/\_/, @buy_sp[$class]);			# 将商品图片分开，使之与商品数量对应
    &errorout("赠送商品&非常抱歉，你的赠送商品选择错误！&1") if(@tempsp[$id] eq '');
    ($info1,$info2)=split(/\,/,@tempsp[$id]);

###
    $/="";
    my $filetoopen = "$lbdir" . "face/wpdata/$class.pl";
    open(FILE,"$filetoopen");
    my $sort=<FILE>;
    close(FILE);
    $/="\n";

    if($sort =~ /$info1\t(.*)/)	# 找到指定的商品ID
    {
	($sp_name,$sp_money,$x,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$sp_suit,$sp_suitid)=split(/\t/,$1);
    }
    else
    {
	&errorout("赠送商品&建立页面出错，此商品已经不存在，请丢弃此商品！&1");
    }
###

    for($i=0;$i<@tempsp;$i++)
    {
	$newid .= qq~@tempsp[$i]_~ if($i ne $id);
    }
    chop($newid);
    @buy_sp[$class] = $newid;

    for($i=1;$i<26;$i++)
    {
	$newdata .= "@buy_sp[$i]-";
    }
    chop($newdata);

    &upplugdata("$tempmembername","$currequip|$newdata|$loadface","");
#####

    my $filetoopen = "$lbdir" . "face/log/$tempmembername.pl";	# 写入用户记录文件：类型为 1
    open(FILE,"$filetoopen");
    my @mylog=<FILE>;
    close(FILE);

    open(FILE, ">$filetoopen");
    print FILE "2\t$sp_name\t1\t$sp_money\t$currenttime\t$zengname\t$zengly\n";

    foreach $m (@mylog){
	$a=$a+1;
	if ($a < $lognum){print FILE "$m";}
    }
    close(FILE);
######

    my $filetoopen = "$lbdir" . "face/log/$zengname.pl";	# 写入用户记录文件：类型为 1
    open(FILE,"$filetoopen");
    my @mylog=<FILE>;
    open(FILE, ">$filetoopen");
    print FILE "3\t$sp_name\t1\t$sp_money\t$currenttime\t$tempmembername\t$zengly\n";

    foreach $z (@mylog){
	$a=$a+1;
	if ($a < $lognum){print FILE "$z";}
    }
    close(FILE);

    my $mcon = qq~你的朋友 <font color=blue>$tempmembername</font> 给你送了一件商品： $sp_name ，并想对你说： <font color=blue>$zengly</font><BR><BR><a href=face.cgi?action=mybureau target=_blank>查看您的虚拟形象</a>~;
    &write_messages("$tempmembername","$zengname","虚拟形象赠送讯息","$mcon");

######

    &readface("$zengname",1);

    @buy_sp[$class] = @buy_sp[$class] ne '' ? "@buy_sp[$class]_$info1,N" : "$info1,N";

    $newdata = '';
    for($i=1;$i<26;$i++)
    {
	$newdata .= "@buy_sp[$i]-";
    }
    chop($newdata);

    &upplugdata("$zengname","$currequip|$newdata|$loadface","");
    print qq~<SCRIPT>opener.location.reload();setTimeout("self.close()",100);alert("商品赠送成功！");</SCRIPT>~;
    exit;
}