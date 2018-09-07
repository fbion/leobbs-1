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
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setjhmp.cgi";
$query = new LBCGI;
#&ipbanned; #封杀一些 ip

$addme=$query->param('addme');

for('action','jhmpid','jhmpname','jhmpstatus','jhmporganiger'){
	my $theparam = $query->param($_);
    $theparam = &cleaninput("$theparam");
	${$_} = $theparam;
}
$checkaction    =  ($query->param('checkaction') eq "yes")?"yes":"no";

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

my %Mode = ('createform' => \&createform,
            'processnew' => \&createaction,
	    'edit'       => \&editform,
	    'processedit'=> \&editaction,
	    'delete'     => \&deleteaction
	  );

print header(-charset=>utf8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;
&getmember("$inmembername","no");
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
    print qq~
    <tr><td bgcolor="#2159C9" colspan=2><font color=#FFFFFF>
    <b>欢迎来到论坛管理中心 / 门派管理器</b>
    </td></tr>~;
    if ($Mode{$action}) { 
        $Mode{$action}->();
    } else {
        &jhmplist;
    }
    print qq~</table></td></tr></table>~;
} else {
    &adminlogin;
}

sub jhmplist {
    print qq~
    <script language="javascript">
	function O9(id) {if(id!="")window.open("profile.cgi?action=show&member="+id);}
	</script>
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>注意事项</b>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2 align=center>
    　　在下面，您将看到目前所有的门派。您可以增加一个新的门派。也可以编辑或删除目前存在门派。<p>
    </td>
    </tr>
    ~;

    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);

	print qq~
    <tr>
    <td bgcolor=#FFFFFF align=center colspan=2><table width=90% cellspacing="0" cellpadding="2">
	<tr><td align="center" colspan="4" bgcolor="#EEEEEE">|| <a href="$thisprog?action=createform">增加新门派</a> ||</td></tr>
	<tr><td align="center" bgcolor=$catback><b style="color:blue">门派名称</b></td><td align="center" width="20%" bgcolor=$catback><b style="color:blue">门派创立人</b></td><td align="center" width="10%" bgcolor=$catback><b style="color:blue">门派状态</b></td><td align="center" width="30%" bgcolor=$catback><b style="color:blue">相关操作</b></td></tr>
	~;
    $jhmpnum = 0;
    foreach $jhmp (@jhmp) {
    	chomp $jhmp;
    	next if($jhmp eq "");
		($jhmpname, $jhmpstatus, $jhmporganiger) = split(/\t/,$jhmp);
		$jhmpurl=~s/\\//g;
		$jhmpnum++;
		$jhmpstatus=($jhmpstatus)?"开放门派":"隐藏门派";
		print qq~
		<tr><td align="left">　　<b>$jhmpname</b></td><td align="center"><span style="cursor:hand" onClick="javascript:O9('$jhmporganiger')"><font color="#333333"><u>$jhmporganiger</u></font></span></td><td align="center"><u>$jhmpstatus</u></td><td align="center"><a href="$thisprog?action=edit&jhmpid=$jhmpnum">[编辑]</a> <a href="$thisprog?action=delete&jhmpid=$jhmpnum">[删除]</a></td></tr>
	    ~;
	}
    
    
	print qq~
	<tr><td align="center" colspan="4" bgcolor="#EEEEEE">共有门派 $jhmpnum 个 </td></tr></table>
	~;
}
sub createform{
    print qq~
    <script language="javascript">
	function O9(id) {if(id!="")window.open("profile.cgi?action=show&member="+id);}
	</script>
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="processnew">    
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>门派名称</b><br>请输入新门派的名称<BR></font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="jhmpname" value=""></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>门派状态码</b><br>请选择门派的开放状态</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <select name="jhmpstatus"><option value="1">开放，允许自由加入</option><option value="0">隐藏，不允许自由加入</option></select>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font  color=#333333><b>门派创立人</b><br>请输入门派的创立人</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="jhmporganiger" value="$inmembername"> <input type=button value="检查" onClick="O9(this.form.jhmporganiger.value)"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
    <input type=submit value="提 交"></form>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td>
    </tr>
    ~;
}
sub editform {
    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);
    unless (defined $jhmp[$jhmpid-1]){&errorout("该门派不存在！"); return;}
    ($jhmpname,$jhmpstatus,$jhmporganiger) = split(/\t/,$jhmp[$jhmpid-1]);   
    $jhmpurl=~s/\\//g;
	$jhmpstatus_select=qq(<option value="1">开放，允许自由加入</option><option value="0">隐藏，不允许自由加入</option>);
	$jhmpstatus_select=~s/ value="$jhmpstatus">/ value="$jhmpstatus" selected>/;
    print qq~
    <script language="javascript">
	function O9(id) {if(id!="")window.open("profile.cgi?action=show&member="+id);}
	</script>
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="processedit">
    <input type=hidden name="jhmpid" value="$jhmpid">
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>门派名称</b><br>请输入新门派的名称<BR></font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="jhmpname" value="$jhmpname"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>门派状态码</b><br>请选择门派的开放状态</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <select name="jhmpstatus">$jhmpstatus_select</select>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font  color=#333333><b>门派创立人</b><br>请输入门派的创立人</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="jhmporganiger" value="$jhmporganiger"> <input type=button value="检查" onClick="O9(this.form.jhmporganiger.value)"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
    <input type=submit value="提 交"></form>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td>
    </tr>
    ~;
}
sub createaction {
    if ($jhmpname eq "" || $jhmporganiger eq ""){&errorout("门派名称及创立人不能为空！"); return;}
    if(length($jhmpname)>21) {&errorout("江湖门派过长，请不要超过20个字符（10个汉字）！"); return;}
    $jhmpstatus=($jhmpstatus)?1:0;
    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);
	@exisjhmp = grep(/^$jhmpname\t[1|0]\t/,@jhmp);
    if (@exisjhmp){&errorout("该门派名称已被使用！"); return;}
	
    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "########################################\n";
    print FILE "# LeoBBS auto-generated config file    #\n";
    print FILE "# Do not change anything in this file! #\n";
    print FILE "########################################\n";
	foreach $jhmp (@jhmp) {
    next if ($jhmp eq "");
	chomp $jhmp;
    print FILE "$jhmp\n";
    }
    print FILE "$jhmpname\t$jhmpstatus\t$jhmporganiger\t\n";
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    
    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#2159C9><b>增加结果</b><p>
    <li>新门派 <B>$jhmpname</b> 已经建立！
    <br><BR><a href=$thisprog?action=createform>继续增加门派</a>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td>
    </tr>
    ~;
}
sub editaction {
    if ($jhmpname eq "" || $jhmporganiger eq ""){&errorout("门派名称及创立人不能为空！"); return;}
    if(length($jhmpname)>21) {&errorout("江湖门派过长，请不要超过20个字符（10个汉字）！"); return;}
    $jhmpstatus=($jhmpstatus)?1:0;
    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);
    unless (defined $jhmp[$jhmpid-1]){&errorout("该门派不存在！"); return;}
	@exisjhmp = grep(/^$jhmpname\t[1|0]\t/,@jhmp);
#    if (@exisjhmp){&errorout("该门派名称已被使用！"); return;}
    
    open(FILE,">$filetoopen");
    flock(FILE,2) if ($OS_USED eq "Unix");
    print FILE "########################################\n";
    print FILE "# LeoBBS auto-generated config file    #\n";
    print FILE "# Do not change anything in this file! #\n";
    print FILE "########################################\n";
	$jhmpnum = 0;
	foreach $jhmp (@jhmp) {
    next if ($jhmp eq "");
	chomp $jhmp;
    $jhmpnum ++;
		if ($jhmpid eq $jhmpnum) {
	($oldjhmpname,undef,undef)=split(/\t/,$jhmp);
    print FILE "$jhmpname\t$jhmpstatus\t$jhmporganiger\t\n";
		} else {
	print FILE "$jhmp\n";
		}
	}
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    
    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#2159C9><b>编辑结果</b><p>
    <li>门派 <B>$oldjhmpname</b> 已经更新！
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td>
    </tr>
    ~;
}
sub deleteaction {
	if($checkaction ne "yes"){
    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);
    unless (defined $jhmp[$jhmpid-1]){&errorout("该门派不存在！"); return;}
    ($jhmpname,$jhmpstatus,$jhmporganiger) = split(/\t/,$jhmp[$jhmpid-1]);   
    print qq~
    <tr>
    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
    <font color=#990000><b>警告！！</b>
    </td></tr>
    
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
    <font color=#333333>如果您确定要删除门派 <u>$jhmpname</u>，那么请点击下面链接<p>
    >> <a href="$thisprog?action=delete&checkaction=yes&jhmpid=$jhmpid">删除门派</a> <<
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td>
    </tr>
    ~;
    return;
	}
    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);
    unless (defined $jhmp[$jhmpid-1]){&errorout("该门派不存在！"); return;}

    open(FILE,">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "########################################\n";
    print FILE "# LeoBBS auto-generated config file    #\n";
    print FILE "# Do not change anything in this file! #\n";
    print FILE "########################################\n";
	$jhmpnum = 0;
	foreach $jhmp (@jhmp) {
    next if ($jhmp eq "");
	chomp $jhmp;
    $jhmpnum ++;
		if ($jhmpid eq $jhmpnum) {
	($oldjhmpname,undef,undef)=split(/\t/,$jhmp);
		}else{
	print FILE "$jhmp\n";
		}
	}
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#2159C9><b>删除结果</b><p>
    <li>门派 <B>$oldjhmpname</B> 已被删除！
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td>
    </tr>
    ~;
}
sub errorout{
	#sub errorout v2.0
	my $errormsg=shift;
    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>管理程式出