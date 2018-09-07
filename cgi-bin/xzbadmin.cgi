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
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "code.cgi";
require "bbs.lib.pl";
require "postjs.cgi";
$|++;
$thisprog	= "xzbadmin.cgi";
$query		= new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

if (int($hownews) < 50)
{	#字数预设值
	$hownews = 100;
}
#取得数据
for ('forum','membername','password','action','inpost','message','xzbid','checked') {
    next unless defined $_;
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$inforum		= $forum;
if (($inforum eq "")||($inforum !~ /^[0-9]+$/))
{	#验证分论坛编号
	&error("普通错误&老大，别乱黑我的程序呀！");
}
if (-e "${lbdir}data/style${inforum}.cgi")
{	#读取专属风格
	require "${lbdir}data/style${inforum}.cgi";
}
$inmembername	= $membername;			#转换变数
$inpassword	= $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$currenttime	= time;
$inmembername	= &stripMETA($inmembername);

#个人风格
$inselectstyle	= $query->cookie("selectstyle");	#读取资料
$inselectstyle   = $skinselected if ($inselectstyle eq "");
if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./))
{	#个人风格不正确
	&error("普通错误&老大，别乱黑我的程序呀！");	#输出错误页
}
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi"))
{	#有指定个人风格
	require "${lbdir}data/skin/${inselectstyle}.cgi";	#读取个人风格
}
#会员帐号
if ($inmembername eq "")
{	#没提供会员名称
	$inmembername	= $query->cookie("amembernamecookie");	#从 COOKIE 读取
}
if ($inpassword eq "")
{	#没提供密码
	$inpassword		= $query->cookie("apasswordcookie");	#从 COOKIE 读取
}
$inmembername	=~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;	#字串处理
$inpassword		=~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

#检查帐号
if (($inmembername eq "")||($inmembername eq "客人"))
{	#客人
	&error("普通错误&只限会员进入！");	#禁止进入
}
else
{	#会员
	&getmember("$inmembername","no");	#读取帐号资料
	if ($userregistered eq "no")
	{	#未注册帐号
		&error("普通错误&此用户根本不存在！");				#禁止进入
	}
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
     }
}
$addtimes		= ($timedifferencevalue + $timezone)*3600;	#时差
#论坛状态
&doonoff;  #论坛开放与否

&error("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz!~/,$membercode,/);
    if ($allowusers ne '') {
	&error('进入论坛&你不允许进入该论坛！') if (",$allowusers," !~ /\Q,$inmembername,\E/i);
    }

#读取分论坛资料
my $forumdata	= "${lbdir}forum${inforum}/foruminfo.cgi";
if (-e $forumdata)
{	#找到该分论坛资料
	&getoneforum("$inforum");							#读取资料
}
else
{	#找不到资料
	&error("普通错误&老大，别乱黑我的程序呀！");	#输出错误页
}
#验证权限
if (($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes"))
{	#有权限的人：坛主，总版主，版主栏中的
	&error("删除小字报&你没权力删除！");					#输出错误页
}
#说明连结
$helpurl		= &helpfiles("阅读标记");
$helpurl		= qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;
#指定模式
my %Mode = (
	'delete'		=> \&deletexzb,		#删除
	'deleteover'	=> \&deleteoverxzb,	#删除 2
	'edit'			=> \&editxzb,		#编辑
);
#输出档头
print header(-charset=>utf8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
#验证模式
if (defined $Mode{$action})
{	#有该模式
	$Mode{$action}->();		#执行模式
}
else
{	#没有该模式
	&toppage;				#执行预设模式 -> 首页
}
#输出页面
&output("$forumname - 小字报管理",\$output);
#处理结束
exit;
#模式内容
sub toppage
{	#模式 -> 首页
	#输出页面头
	&mischeader("小字报管理");
	#读取资料
	my @xzbdata = ();								#初始化
	open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");	#开启文件
	while (my $line = <FILE>)
	{	#每次读取一行内容 loop 1
		chomp $line;			#去掉换行符
		push(@xzbdata,$line);	#放进结果 ARRAY
	}#loop 1 end
	close(FILE);									#关闭文件

	#页面输出
	$output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post" id="1">
<input type="hidden" name="action" value="delete">
<input type="hidden" name="forum" value="$inforum">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="7%" $catbackpic align="center">
		</td>
		<td bgcolor="$titlecolor" width="*" $catbackpic align="center">
			<font color="$titlefontcolor"><b>标题</b></font>
		</td>
		<td bgcolor="$titlecolor" width="10%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>发布者</b></font>
		</td>
		<td bgcolor="$titlecolor" width="20%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>发布时间</b></font>
		</td>
		<td bgcolor="$titlecolor" width="15%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>内容字节数</b></font>
		</td>
		<td bgcolor="$titlecolor" width="3%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>选</b></font>
		</td>
	</tr>~;
	#输出数据
	my $i = 0;	#编号
	foreach my $line(@xzbdata)
	{	#回圈处理数据 loop 1
		#   没用   , 标题   , 发布者  , 内容 , 发布时间
		my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);		#分割数据
		#背景色
		if ($i%2 == 0) {
			$postbackcolor = $postcolorone;
		} else {
			$postbackcolor = $postcolortwo;
		}
		my $admini		= qq~<div align="right"><font color="$titlecolor">|<a href="$thisprog?action=edit&forum=$inforum&xzbid=$posttime"><font color="$titlecolor">编辑</font></a>|<a href="$thisprog?action=delete&forum=$inforum&xzbid=$posttime"><font color="$titlecolor">删除</font></a>|</font></div>~;		#管理连结
		my $postdate		= &dateformat($posttime+$addtimes);						#发布时间
		my $msgbytes	= length($msg);												#字节数
		my $startedby	= uri_escape($postid);		#会员名
		$iuu = $i + 1;
		$output .= qq~
	<tr>
		<td bgcolor="$postbackcolor" width="7%" align="center">
			<font color="$postfontcolorone">No.<i>$iuu</i></font>
		</td>
		<td bgcolor="$postbackcolor" width="*" align="left">
			&nbsp;&nbsp;<font color="$postfontcolorone">$title</font>$admini
		</td>
		<td bgcolor="$postbackcolor" width="10%" align="center">
			<font color="$postfontcolorone"><span style=cursor:hand onClick=javascript:O9('$startedby')>$postid</span></font>
		</td>
		<td bgcolor="$postbackcolor" width="20%" align="center">
			<font color="$postfontcolorone">$postdate</font>
		</td>
		<td bgcolor="$postbackcolor" width="15%" align="center">
			<font color="$postfontcolorone"><i>$msgbytes</i> byte(s)</font>
		</td>
		<td bgcolor="$postbackcolor" width="3%" align="center">
			<input type="checkbox" name="xzbid" value="$posttime">
		</td>
	</tr>~;
		$i++;																		#编号递增
	}#loop 1 end
	#页面输出
	$output .= qq~
	</table>
	</td>
</tr>
</table><SCRIPT>valignend()</SCRIPT>
<table cellpadding="0" cellspacing="2" width="$tablewidth" align="center" border="0">
<tr>
	<td align="right" width="75%">
		<input type="submit" value="删除选择">
	</td>
</form id="1 end">
<form action="$thisprog" method="post" id="2">
<input type="hidden" name="action" value="deleteover">
<input type="hidden" name="forum" value="$inforum">
	<td align="right">
		<input type="submit" value="删除超过４８小时的小字报">
	</td>
</tr>
</form id="2 end">
</table><BR>~;
}
sub editxzb
{	#模式 -> 编辑
	#输出页面头
	&mischeader("编辑小字报");
	#找寻要编辑的小字报
	my $findresult	= -1;	#初始化
	my @xzbdata		= ();
	my $xzbno		= 0;
	open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");	#开启文件
	while (my $line = <FILE>)
	{	#每次读取一行内容 loop 1
		chomp $line;															#去掉换行符
		my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);	#分割数据
		if ($posttime eq $xzbid)
		{	#就是这个
			$findresult = $xzbno;		#激活找寻结果
		}
		elsif ($findresult == -1)
		{	#不是的时候
			$xzbno++;				#编号递增
		}
		push(@xzbdata,$line);													#放进数据 ARRAY
	}#loop 1 end
	close(FILE);
	if ($findresult == -1)
	{	#找不到
		&error("编辑小字报&找不到目标小字报！");										#输出错误页
	}
	if ($checked ne 'yes')
	{	#未进行确认
		#目前数据
		#   没用   , 标题   , 发布者  , 内容 , 发布时间
		my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$xzbdata[$xzbno]);	#分割数据
	    $msg =~ s/\<p\>/\n\n/ig;															#字串处理
	    $msg =~ s/\<br\>/\n/ig;
		my $startedby	=  uri_escape($postid);				#会员名
		#页面输出
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post" id="1">
<input type="hidden" name="action" value="edit">
<input type="hidden" name="checked" value="yes">
<input type="hidden" name="forum" value="$inforum">
<input type="hidden" name="xzbid" value="$posttime">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center" colspan="2">
			<font color="$titlefontcolor"><b>编辑所选小字报</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolortwo" alin="center" colspan="2">
			<table cellpadding="0" cellspacing="0" width="100%" bgcolor="$tablebordercolor" align="center" border="0">
			<tr>
				<td>
					<table cellpadding="3" cellspacing="1" border="0" width="100%">
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
					<tr>
						<td bgcolor=$miscbackone valign=top>
							<font color="$fontcolormisc"><b>小字报发布者</b></font>
						</td>
						<td bgcolor="$miscbackone">
							<font color="$postfontcolorone"><u><span style=cursor:hand onClick=javascript:O9('$startedby')>$postid</span></u></font>
						</td>
					</tr>
					<tr>
						<td bgcolor=$miscbackone valign=top>
							<font color="$fontcolormisc"><b>小字报标题</b> (最大 80 字)</font>
						</td>
						<td bgcolor="$miscbackone">
							<input type="text" maxlength="80" name=inpost onkeydown=ctlent() value="$title" size=80>
						</td>
					</tr>
					<tr>
						<td bgcolor=$miscbacktwo valign=top>
							<font color="$fontcolormisc"><b>小字报内容</b> (最多 $hownews 字)<p>
							在此论坛中：
							<li>HTML 标签: <b>不可用</b>
							<li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS 标签</a>: <b>可用</b></font>
						</td>
						<td bgcolor=$miscbacktwo valign=top>
							<TEXTAREA cols=58 name=message rows=6 wrap=soft onkeydown=ctlent()>$msg</TEXTAREA>
						</td>
					</tr>
					</table>
				</td>
			</tr>
			</table>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="right" width="51%">
			<input type="submit" value="提交编辑">&nbsp;
		</td>
</form id="1">
<form action="$thisprog" method="get" id="2">
<input type="hidden" name="forum" value="$inforum">
		<td bgcolor="$postcolorone" align="left">
			&nbsp;<input type="submit" value="返回主页面">
		</td>
</form id="2">
	</tr>
	</table>
	</td>
</tr>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
	else
	{	#已进行确认
		#驗證處理
		if ($inpost eq "")
		{
			&error("编辑小字报&必须输入标题！");									#输出错误页
		}
		elsif (length($inpost) > 82)
		{
			&error("编辑小字报&标题过长！");										#输出错误页
		}
		elsif (length($message) > $hownews)
		{
			&error("编辑小字报&内容过长！");										#输出错误页
		}
		#编辑处理
		my $newfile	= '';									#初始化文件
		foreach my $line (@xzbdata)
		{	#每次读取一行内容 loop 1
			chomp $line;			#去掉换行符
			my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);		#分割数据
			if($posttime eq $xzbid)
			{	#编辑目标
				$line = "＃—＃—·\t$inpost\t$inmembername\t$message\t$posttime\t";	#新行
			}
			$newfile .= $line."\n";														#放入新文件内
		}#loop 1 end
		open(FILE,'>'."${lbdir}boarddata/xzb$inforum.cgi");	#开启只写文件
		print FILE $newfile;								#写入新文件内容
		close(FILE);										#关闭文件
		#页面输出
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="get">
<input type="hidden" name="forum" value="$inforum">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>已经编辑该小字报内容</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="center">
			<input type="submit" value="返回主页面">
		</td>
	</tr>
	</table>
	</td>
</tr>
</form>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
}
sub deletexzb
{	#模式 -> 删除
	#输出页面头
	&mischeader("删除小字报");
	#读取复选数据
	my @noarray		= ();	#初始化
	my %nohash		= ();
	my $xzbidcount	= 0;
	my $novalue		= '';	# HIDDEN 的输入栏
	if ($xzbid ne "")
	{	#有定义第一个 ID
		@noarray = $query->param('xzbid');	#所有 ID
		foreach my $xzbid(@noarray)
		{	#处理所有 ID loop 1
			$novalue .= '<input type="hidden" name="xzbid" value="'.$xzbid.'">'."\n";	#增加栏位
			$nohash{$xzbid} = $xzbid;													#放入 HASH
			$xzbidcount++;																#数目递增
		}#loop 1 end 
		chomp $novalue;						#去除最後换行
	}
	if ($xzbidcount == 0)
	{	#没选任何小字报
		&error("删除小字报&没有选任何小字报！");			#输出错误页
	}

	if ($checked ne 'yes')
	{	#未进行确认
		#页面输出
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post" id="1">
<input type="hidden" name="action" value="delete">
<input type="hidden" name="checked" value="yes">
<input type="hidden" name="forum" value="$inforum">
$novalue
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center" colspan="2">
			<font color="$titlefontcolor"><b>确认删除所选的 $xzbidcount 个小字报？</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="right" width="51%">
			<input type="submit" value="确认删除">&nbsp;
		</td>
</form id="1">
<form action="$thisprog" method="get" id="2">
<input type="hidden" name="forum" value="$inforum">
		<td bgcolor="$postcolorone" align="left">
			&nbsp;<input type="submit" value="返回主页面">
		</td>
</form id="2">
	</tr>
	</table>
	</td>
</tr>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
	else
	{	#已进行确认
		#删除处理
		my $newfile	= '';									#初始化文件
		my $delbyte	= '';									#删除的字节
		open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");		#开启文件
		while (my $line = <FILE>)
		{	#每次读取一行内容 loop 1
			chomp $line;			#去掉换行符
			my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);		#分割数据
			if(($line eq "") || (defined $nohash{$posttime}))
			{	#空白行或删除目录
				$delbyte += length($line);	#加上删除的字节
				next;						#跳过
			}
			$newfile .= $line."\n";														#放入新文件内
		}#loop 1 end
		close(FILE);										#关闭文件
		open(FILE,'>'."${lbdir}boarddata/xzb$inforum.cgi");	#开启只写文件
		print FILE $newfile;								#写入新文件内容
		close(FILE);										#关闭文件
		#页面输出
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="get">
<input type="hidden" name="forum" value="$inforum">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>所选的 $xzbidcount 个小字报已被删除</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolortwo" align="center">
			总共删除 $delbyte  byte(s)
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="center">
			<input type="submit" value="返回主页面">
		</td>
	</tr>
	</table>
	</td>
</tr>
</form>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
}
sub deleteoverxzb
{	#模式 -> 删除 2
	#输出页面头
	&mischeader("删除小字报");
	#读取超时资料
	my @delxzbid	= ();	#初始化
	if($checked ne 'yes')
	{	#未进行确认
		open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");	#开启文件
		while (my $line = <FILE>)
		{	#每次读取一行内容 loop 1
			chomp $line;															#去掉换行符
			my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);	#分割数据
			if ($currenttime-$posttime > 3600*48)
			{	#超过４８小时
				push(@delxzbid,$posttime);		#放到需删 ID
			}
		}#loop 1 end
		close(FILE);									#关闭文件
	}
	else
	{	#已进行确认
		@delxzbid = $query->param('xzbid');				#需删 ID
	}
	if (@delxzbid == 0)
	{	#没任何小字报需要删
		&error("删除小字报&没有小字报需要删除！");			#输出错误页
	}
	#读取复选数据
	my %nohash		= ();
	my $xzbidcount	= 0;
	my $novalue		= '';	# HIDDEN 的输入栏
	foreach my $xzbid(@delxzbid)
	{	#处理所有 ID loop 1
		unless ($currenttime-$posttime > 3600*48)
		{	#再检查时间，不通过
			next;		#跳过
		}
		$novalue .= '<input type="hidden" name="xzbid" value="'.$xzbid.'">'."\n";	#增加栏位
		$nohash{$xzbid} = $xzbid;													#放入 HASH
		$xzbidcount++;																#数目递增
	}#loop 1 end 
	chomp $novalue;						#去除最後换行
	
	if ($checked ne 'yes')
	{	#未进行确认
		#页面输出
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post">
<input type="hidden" name="action" value="delete">
<input type="hidden" name="checked" value="yes">
<input type="hidden" name="forum" value="$inforum">
$novalue
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>确认删除所选的 $xzbidcount 个小字报？</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="center">
			<input type="submit" value="确认删除">
		</td>
	</tr>
	</table>
	</td>
</tr>
</form>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
}