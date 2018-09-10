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
    $startingtime = (times)[0] + (times)[1];
    foreach ($0, $ENV{'PATH_TRANSLATED'}, $ENV{'SCRIPT_FILENAME'}) {
        my $LBPATH = $_;
        next if ($LBPATH eq '');
        $LBPATH =~ s/\\/\//g;
        $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC, $LBPATH);
    }
}

use warnings;
use strict;
use diagnostics;
use LBCGI;
#use URI::Escape;
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "data/cityinfo.cgi";
require "face/config.pl";
require "facelib.pl";
$|++;
$thisprog = "setface.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
if ($COOKIE_USED eq 2 && $mycookiepath ne "") {$cookiepath = $mycookiepath;}
elsif ($COOKIE_USED eq 1) {$cookiepath = "";}
else {
    $boardurltemp = $boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
}

#&ipbanned; #封杀一些 ip
$inselectstyle = $query->cookie("selectstyle");
$inselectstyle = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~ m/\//) || ($inselectstyle =~ m/\\/) || ($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$inmembername = $query->cookie("amembernamecookie");
$inpassword = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~ m/\//) || ($inmembername =~ m/\\/) || ($inmembername =~ m/\.\./));

if ($inmembername eq "" || $inmembername eq "客人") {
    &error("不能进入 $plugname &你目前的身份是访客，请先登陆!");
    exit;
}
else {
    #    &getmember("$inmembername");
    &getmember("$inmembername", "no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
    if ($inpassword ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
}

&title;

$tempmembername = $membername;
$tempmembername =~ s/ /\_/g;
$tempmembername =~ tr/A-Z/a-z/;

$admin_user =~ s/ /\_/g;
$admin_user =~ tr/A-Z/a-z/;

if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

&error("$plugname 后台管理&只有论坛坛主与插件管理员才能进入此区！") if (($membercode ne "ad") && ($admin_user ne "$tempmembername"));

print $query->header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
$output .= qq~
<BODY>
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> 在这里您可以购买、装备、赠送、设置和管理你的虚拟形象</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> → <a href=face.cgi>$plugname</a> <img src=$imagesurl/images/fg.gif width=1 height=10> [<a href=setface.cgi>后台管理</a>]<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=2 cellspacing=1 border=0 width=100%>
<tr><td height=30 bgcolor=$titlecolor $catbackpic><font color=$titlefontcolor>
&nbsp;<B><a href=$thisprog?action=set>基本设置</a> | <a href=$thisprog?action=sortm>类别管理</a> | <a href=$thisprog?action=add_sp>增加单一商品</a> | <a href=$thisprog?action=edit>商品管理</a> | <a href=$thisprog?action=view>查看用户信息</a></b></td></table>~;

$action = $query->param('action');

my %Mode = (
    'set'       => \&bset, # 基本设置
    'sortm'     => \&sort_manage,
    'edit_sort' => \&edit_sort, # 编辑类别信息
    'putjs'     => \&putjs,     # 输出类别JS文件
    'edit_cate' => \&edit_cate, # 编辑分类
    'del_cate'  => \&del_cate,  # 删除分类
    'add_cate'  => \&add_cate,  # 增加分类
    'upmenujs'  => \&upmenujs,  # 输出分类菜单样式
    'add_sp'    => \&add_sp,    # 增加单一商品
    'view'      => \&view_user, # 查看用户信息
    'edit'      => \&edit_sp,   # 编辑与删除商品信息
);

if ($Mode{$action}) {$Mode{$action}->();}
else {&main();}


sub main {
    $output .= qq~<table cellpadding=6 cellspacing=1 width=100%>
    <tr align=middle bgcolor=$miscbacktwo><td>插 件 后 台 管 理 说 明</td></tr>
    <tr align=middle bgcolor=$forumcolortwo><td align="left" valign="top">
　　<B>欢迎您使用雷傲超级论坛虚拟形象后台管理系统！ </B><P>
　　基本设置　　　- 设置插件的基本参数、只有坛主才能进入此区；<P>
　　类别管理　　　- 增加、编辑、删除分类和套装类别，输出JavaScript代码等；<P>
　　增加单一商品　- 增加普通商品信息；<P>
　　商品管理　　　- 编辑、删除商品信息；<P>
　　查看用户信息　- 查看用户当前的装备情况。<P>
　　程序版权所有： <a href=http://www.lzeweb.com/ target=_blank>三元社区</a>　　程序编制：阿强(CPower)
    </td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}


sub bset # 基本设置
{
    &error("基本设置&此选项只有本论坛坛主才能使用！") if ($membercode ne "ad");
    my $checked = $query->param('checked');
    if ($checked eq "yes") {
        my $new1 = $query->param('plugname');    # 插件名称
        my $new2 = $query->param('close_plug');  # 插件状态
        my $newau = $query->param('admin_user'); # 插件管理员
        my $new3 = $query->param('samnum');      # 相同装备允许的数量
        my $new4 = $query->param('lognum');      # 系统记录条数
        my $new6 = $query->param('show_pagen');  # 每页显示商品数
        my $new7 = $query->param('row_num');     # 每行显示商品数
        my $new8 = $query->param('c_width');     # 每件商品的表格宽度

        my $filetomake = $lbdir . "face/config.pl";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE qq~\$admin_user = '$newau';
\$plugname = '$new1';
\$close_plug = '$new2';
\$samnum = '$new3';
\$lognum = '$new4';
\$show_pagen = '$new6';
\$row_num = '$new7';
\$c_width = '$new8';
\$td = 'td align=center';
1;~;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        $output .= qq~

<table cellPadding=6 cellSpacing=1 border=0 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>修改成功</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog?action=set">~;
    }
    else {
        $tempoutput = "<select name=\"close_plug\">\n<option value=\"open\">正常开放\n<option value=\"close\">暂时关闭\n</select>\n";
        $tempoutput =~ s/value=\"$close_plug\"/value=\"$close_plug\" selected/;

        $output .= qq~

<table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST>
<input type=hidden name=action value="set">
<input type=hidden name=checked value="yes">
<tr bgcolor=$miscbacktwo>
<td colspan=4 align=center><font color=$fontcolormisc><b>[ 参 数 设 置 ]</b></font></td>
</tr>
<tr bgcolor=$miscbackone>
<td><font color=$fontcolormisc>插件名称</font></td><td><input type=text size=15 name="plugname" value=$plugname></td>
<td><font color=$fontcolormisc>插件状态</font></td><td>$tempoutput</td>
</tr>
<tr bgcolor=$miscbackone>
<td><font color=$fontcolormisc>插件管理员</font></td><td><input type=text size=15 name="admin_user" value=$admin_user></td>
<td><font color=$fontcolormisc>相同装备允许的数量</font></td><td><input type=text size=10 name="samnum" value=$samnum></td>
</tr>
<tr bgcolor=$miscbacktwo>
<td><font color=$fontcolormisc>系统记录条数</font></td><td><input type=text size=10 name="lognum" value=$lognum></td>
<td><font color=$fontcolormisc>每页显示商品数</font></td><td><input type=text size=3 name="show_pagen" value=$show_pagen></td>
</tr>
<tr bgcolor=$miscbacktwo>
<td><font color=$fontcolormisc>每行显示商品数</font></td><td><input type=text size=2 name="row_num" value=$row_num></td>
<td><font color=$fontcolormisc>每件商品的表格宽度</font></td><td><input type=text size=5 name="c_width" value=$c_width></td>
</tr>

<tr bgcolor=$miscbacktwo><td colspan=4 align=center><input type=submit name=submit value="确 定">　　<input type=reset value=重　置></td></form></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    }
}

sub sort_manage {
    my $filetoopen = "$lbdir" . "face/category.pl"; # 大分类
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @cate = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    $filetoopen = "$lbdir" . "face/class.cgi"; # 小分类
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @sort = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    $output .= qq~
<script>
function OUTJS()
{if(!confirm("是否确定输出 JS 菜单文件？"))return false;}
function DEL()
{if(!confirm("$membername，本操作不可恢复，您是否确认删除？"))return false;}
</script>
<table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST>
<input type=hidden name=action value="set">
<input type=hidden name=checked value="yes">
<tr bgcolor=$miscbacktwo>
<td colspan=5 align=center><font color=$fontcolormisc><b>[ 类 别 管 理 ]</b></font></td>
</tr>

<tr bgcolor=$miscbackone>
<td colspan=5>[<a href="$thisprog?action=add_cate">增加新的分类</a>] - [<a href="$thisprog?action=upmenujs" onclick="return OUTJS();">输出分类菜单样式</a>]</td>
</tr>~;

    foreach (@cate) {
        chop($_);
        ($cate_id, $cate_state, $cate_name, $cate_info) = split(/\t/, $_);
        $cate_state = $cate_state eq 1 ? '<font color=blue>启用</font>' : '<font color=red>关闭</font>';
        $output .= qq~
	<tr bgcolor=#EEEEEE><td colspan=5 height=30>分类名称：$cate_name　$cate_state [<a href="$thisprog?action=edit_cate&id=$cate_id">编辑此分类</a>]  [<a href="$thisprog?action=del_cate&id=$cate_id" onclick="return DEL();">删除此分类</a>]</td></tr>
	<tr bgcolor=$miscbacktwo align=center><td width=120>类别名称</td><td width=80></td><td width=80></td><td width=50>类别状态</td><td width=320>类别描述</td></tr>~;

        foreach (@sort) {
            chomp $_;
            ($cateid, $sort_id, $sort_status, $sortname, $sortinfo) = split(/\t/, $_);

            if ($cate_id eq $cateid) {
                $status = $sort_status eq 1 ? '<font color=blue>开放</font>' : '<font color=red>关闭</font>';
                $jsinfo = $sort_status eq 1 ? "<a href=$thisprog?action=putjs&id=$sort_id>输出JS文件</a>" : "";

                $output .= qq~<tr bgcolor=$miscbackone><td>$sortname</td><td align=center>$jsinfo</td><td align=center><a href="$thisprog?action=edit_sort&id=$sort_id">编辑</a>$msort</td><td width=50 align=center>$status</td><td>$sortinfo</td></tr>~;
            }
        }
    }

    $output .= qq~<tr bgcolor=#EEEEEE><td colspan=5 height=30>分类名称：暂无</td></tr><tr bgcolor=$miscbacktwo align=center><td width=120>类别名称</td><td width=80></td><td width=80></td><td width=50>类别状态</td><td width=320>类别描述</td></tr>~;

    foreach (@sort) {
        chomp $_;
        ($cateid, $sort_id, $sort_status, $sortname, $sortinfo) = split(/\t/, $_);

        if ($cateid eq '') {
            $output .= qq~<tr bgcolor=$miscbackone><td>$sortname</td><td align=center></td><td align=center><a href="$thisprog?action=edit_sort&id=$sort_id">编辑</a>$msort</td><td width=50 align=center><font color=red>关闭</font></td><td>$sortinfo</td></tr>~;
        }
    }
    $output .= qq~</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

sub edit_sort {
    my $id = $query->param('id');
    my $edit = $query->param('edit');
    if ($edit eq 'y') {
        $new_cname = $query->param('catename');
        $new_name = $query->param('sort_name');
        $new_status = $query->param('sort_status');
        $new_explain = $query->param('sort_explain');
        &error("编辑类别&商品类别名字不能空！！") if ($new_name eq '');
        &error("编辑类别&商品类别描述不能空！！") if ($new_explain eq '');

        my $filetoopen = "$lbdir" . "face/class.cgi";
        open(FILE, "$filetoopen");
        my @sort = <FILE>;
        close(FILE);

        open(FILE, ">$filetoopen");
        for ($i = 0; $i < @sort; $i++) {
            ($cateid, $old_id, $old_status, $old_name, $old_info) = split(/\t/, @sort[$i]);

            if ($old_id eq $id) # 如果找到符合的条件，则写入新的数据
            {
                print FILE "$new_cname\t$old_id\t$new_status\t$new_name\t$new_explain\n";
            }
            else {print FILE "$cateid\t$old_id\t$old_status\t$old_name\t$old_info";}
        }
        close(FILE);
        $output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>编 辑 成 功</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="1; url=$thisprog?action=sortm">~;
    }
    else {
        my $filetoopen = "$lbdir" . "face/class.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        @sort = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        for ($i = 0; $i < @sort; $i++) {
            ($cateid, $sort_id, $sort_status, $sort_name, $sort_info) = split(/\t/, @sort[$i]);
            last if ($sort_id eq $id);
        }

        $filetoopen = "$lbdir" . "face/category.pl"; # 大分类
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        my @cate = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        foreach (@cate) {
            chop($_);
            ($cate_id, $cate_state, $cate_name, $cate_info) = split(/\t/, $_);
            $temps .= qq~<option value="$cate_id">$cate_name</option>~;
        }

        $temps =~ s/value=\"$cateid\"/value=\"$cateid\" selected/;
        $tempoutput = "<input type=radio name=sort_status value=\"1\"> 启用　<input type=radio name=sort_status value=\"0\"> 关闭";
        $tempoutput =~ s/value=\"$sort_status\"/value=\"$sort_status\" checked/;

        $output .= qq~
	<table cellPadding=6 cellSpacing=1 width=100%>
	<form action="$thisprog" method="post">
	<input type=hidden name="action" value="edit_sort">
	<input type=hidden name="edit" value="y">
	<input type=hidden name="id" value="$id">
	<tr bgcolor=$miscbacktwo>
	<td colspan=2 align=center><font color=$fontcolormisc><b>[ 修 改 类 别 ]</b></font></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>分类名称</td><td><select name=catename size=1">$temps</select></td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>类别名称</td><td><input type=text size=15 name="sort_name" maxlength=15 value="$sort_name"></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>类别状态</td><td>$tempoutput</td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>类别描述</td><td><input type=text size=40 name="sort_explain" value="$sort_info"></td>
	</tr>
	<tr bgcolor=$miscbackone><td align=center colspan=2><input type=submit value="提 交"></td></tr></form>
	</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    }
}

sub putjs {
    my $id = $query->param('id');
    my $filetoopen = "$lbdir" . "face/wpdata/$id.pl"; # 大分类
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @spdata = <FILE>;
    my $spdata = @spdata;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    foreach (@spdata) {
        chop($_);
        ($x1, $x2, $x3, $x, $x, $x5, $x6, $x7, $x, $x8) = split(/\t/, $_);
        ($x6, $x) = split(/\./, $x6);
        ($x7, $x) = split(/\./, $x7);
        $outinfo .= qq~'$x1|$x2|$x3|$x5|$x6|$x7',~;
        #商品ID,商品名称,商品价格,适用人群,商品大图,商品小图
    }
    chop($outinfo);

    open(FILE, ">${imagesdir}/face/js/$id.js");
    print FILE qq~//雷傲超级论坛虚拟形象 商品信息 ID:$id
var SPNUM = $spdata;
var SPINFO = new Array($outinfo);~;
    close(FILE);

    $output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>JavaScript 文件保存成功！</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog?action=sortm">~;
}

sub edit_cate {
    my $id = $query->param('id');
    my $edit = $query->param('edit');
    if ($edit eq 'y') {
        $new_name = $query->param('cate_name');
        $new_state = $query->param('cate_status');
        $new_explain = $query->param('cate_explain');
        &error("编辑分类&分类名字不能空！！") if ($new_name eq '');
        &error("编辑分类&分类描述不能空！！") if ($new_explain eq '');

        $/ = "";
        my $filetoopen = "$lbdir" . "face/category.pl";
        open(FILE, "$filetoopen");
        my $cate = <FILE>;
        close(FILE);
        $/ = "\n";

        $cate =~ s/$id\t(.*)/$id\t$new_state\t$new_name\t$new_explain/;
        open(FILE, ">$filetoopen");
        print FILE $cate;
        close(FILE);

        $output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>编 辑 分 类 成 功</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="1; url=$thisprog?action=sortm">~;
    }
    else {
        my $filetoopen = "$lbdir" . "face/category.pl";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        @cate = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        foreach (@cate) {
            chop($_);
            ($cate_id, $cate_state, $cate_name, $cate_info) = split(/\t/, $_);
            last if ($cate_id eq $id);
        }
        &error("编辑分类&编辑分类的ID不存在！！") if ($cate_id ne $id);

        $tempoutput = "<input type=radio name=cate_status value=\"1\"> 启用　<input type=radio name=cate_status value=\"0\"> 关闭";
        $tempoutput =~ s/value=\"$cate_state\"/value=\"$cate_state\" checked/;

        $output .= qq~
	<table cellPadding=6 cellSpacing=1 width=100%>
	<form action="$thisprog" method="post">
	<input type=hidden name="action" value="edit_cate">
	<input type=hidden name="edit" value="y">
	<input type=hidden name="id" value="$id">
	<tr bgcolor=$miscbacktwo>
	<td colspan=2 align=center><font color=$fontcolormisc><b>[ 编 辑 分 类 ]</b></font></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>分类名称</td><td><input type=text size=15 name="cate_name" maxlength=15 value="$cate_name"></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>分类状态</td><td>$tempoutput</td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>分类描述</td><td><input type=text size=40 name="cate_explain" value="$cate_info"></td>
	</tr>
	<tr bgcolor=$miscbackone><td align=center colspan=2><input type=submit value="提 交"></td></tr></form>
	</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    }
}

sub del_cate {
    my $id = $query->param('id');

    $/ = "";
    my $filetoopen = "$lbdir" . "face/category.pl";
    open(FILE, "$filetoopen");
    my $cate = <FILE>;
    close(FILE);
    $/ = "\n";

    if ($cate =~ s/$id\t(.*)\n//) # 找到指定的ID
    {
        open(FILE, ">$filetoopen");
        print FILE $cate;
        close(FILE);
    }

    $filetoopen = "$lbdir" . "face/class.cgi";
    open(FILE, "$filetoopen");
    my @sort = <FILE>;
    close(FILE);

    open(FILE, ">$filetoopen");
    foreach (@sort) {
        ($cateid, $sort_id, $sort_status, $sort_name, $sort_info) = split(/\t/, $_);
        if ($cateid ne $id) {
            print FILE $_;
        }
        else {
            print FILE "\t$sort_id\t0\t$sort_name\t$sort_info";
        }
    }
    close(FILE);

    $output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>删 除 分 类 成 功</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="1; url=$thisprog?action=sortm">~;
}

sub add_cate {
    my $add = $query->param('add');

    if ($add ne 'y') {
        $output .= qq~
	<table cellPadding=6 cellSpacing=1 width=100%>
	<form action="$thisprog" method="post">
	<input type=hidden name="action" value="add_cate">
	<input type=hidden name="add" value="y">
	<tr bgcolor=$miscbacktwo>
	<td colspan=2 align=center><font color=$fontcolormisc><b>[ 增 加 大 分 类 ]</b></font></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>分类名称</td><td><input type=text size=15 name="cate_name" maxlength=15></td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>分类描述</td><td><input type=text size=40 name="cate_explain"></td>
	</tr>
	<tr bgcolor=$miscbackone><td align=center colspan=2><input type=submit value="提 交"></td></tr></form>
	</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    }
    else {
        $cate_name = $query->param('cate_name');
        $cate_explain = $query->param('cate_explain');
        &error("增加分类&分类名字不能空！！") if ($cate_name eq '');
        &error("增加分类&分类描述不能空！！") if ($cate_explain eq '');

        my $filetoopen = "$lbdir" . "face/category.pl";
        if ((-e "$filetoopen")) {
            open(FILE, "$filetoopen");
            my @cate = <FILE>;
            close(FILE);

            foreach (@cate) {
                ($cate_num, $x, $old_name, $x) = split(/\t/, $_);
                &error("分类名称重复&已经存在相同的分类名称！") if ($cate_name eq $old_name);
            }
        }
        else {
            $cate_num = 0;
        }
        $cate_num++;

        open(FILE, ">>$filetoopen");
        print FILE "$cate_num\t0\t$cate_name\t$cate_explain\n";
        close(FILE);

        $output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>增 加 成 功</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><meta http-equiv="refresh" content="1; url=$thisprog?action=sortm">~;
    }
}

sub upmenujs {
    my $filetoopen = "$lbdir" . "face/category.pl"; # 大分类
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @cate = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    $filetoopen = "$lbdir" . "face/class.cgi"; # 小分类
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @sort = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    foreach (@cate) {
        chop($_);
        ($cate_id, $cate_state, $cate_name, $cate_info) = split(/\t/, $_);
        if ($cate_state eq '1') {
            my $menucon = "";
            foreach (@sort) {
                chomp($_);
                ($cateid, $sort_id, $sort_status, $sortname, $sortinfo) = split(/\t/, $_);
                if ($sort_status eq '1') {
                    $menucon .= qq~<tr onMouseOut=\\"mOutNav(this, '')\\" onMouseOver=\\"mOverNav(this, '1')\\" bgcolor='$miscbackone'><td> <span onClick=DispSubMenu('$sort_id'); onMouseOver=DispSubMenu1('$sort_id'); style=cursor:hand; title='$sortinfo'>$sortname</span></td></tr>~ if ($cate_id eq $cateid);
                }
            }

            $outjs .= qq~//$cate_name\nvar MENU$cate_id = "$menucon"\n\n~;                                                                             # 下拉菜单选项
            $smenun .= qq~<td><span style='width=80;cursor: hand;' onMouseOver='ShowMenu(MENU$cate_id,80)' title='$cate_info'>$cate_name</span></td>~; # 子菜单名
        }
    }

    open(FILE, ">${imagesdir}/face/js/catemenu.js");
    print FILE qq~//3FACE 商品分类下拉菜单代码
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
	{navTD.style.backgroundColor='$miscbacktwo';}
}
function mOutNav(navTD, caption)
{
	if (!navTD.contains(event.toElement))
	{navTD.style.backgroundColor='$miscbackone';}
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
	vMnuCode = "<table id='submenu' cellspacing=1 cellpadding=3 style='width:"+tWidth+"' bgcolor=$tablebordercolor border=0 onmouseout='_HideMenu()'>" + vMnuCode + "</table>";

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

$outjs

function displayMenu()
{
    s = "<table cellspacing=0 cellpadding=0 border=0><tr align=center>$smenun</tr></table>";
    document.write(s);
}
~;
    close(FILE);
    $output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>分类菜单 JavaScript 文件更新成功！</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog?action=sortm">~;
}


sub add_sp {
    my $add = $query->param('add');
    if ($add ne 'y') {
        $filetoopen = "$lbdir" . "face/class.cgi"; # 商品类别
        open(FILE, "$filetoopen");
        my @sort = <FILE>;
        close(FILE);
        my $id = $query->param('id');
        foreach (@sort) {
            ($cateid, $sort_id, $x, $sort_name, $x) = split(/\t/, $_);
            $temps = qq~$temps<option value="$sort_id">$sort_name</option>~ if ($sort_id =~ /^[0-9]/);
            $temps =~ s/value=\"$id\"/value=\"$id\" selected/;
        }

        if ($id ne '') {
            &error("这里只能增加单一的商品&单一商品和套装商品的增加是不一样的！") if ($id eq 't');
            opendir(DIR, "${imagesdir}face/$id");
            @thd = readdir(DIR);
            closedir(DIR);
            $myimages = "";
            $topiccount = @thd;
            @thd = sort @thd;
            for (my $i = 0; $i < $topiccount; $i++) {
                next if (($thd[$i] eq ".") || ($thd[$i] eq ".."));
                $myimages .= qq~<option value="$thd[$i]">$thd[$i]~;
            }
            $myimages =~ s/value=\"$action\"/value=\"$action\" selected/;
        }

        $output .= qq~
	<table cellPadding=6 cellSpacing=1 width=100%>
	<form action="$thisprog" method="post" name=FORM>
	<input type=hidden name="action" value="add_sp">
	<input type=hidden name="add" value="y">
	<tr bgcolor=$miscbacktwo>
	<td colspan=4 align=center><font color=$fontcolormisc><b>[ 增 加 单 一 商 品 ]</b></font></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>商品分类</td><td><SCRIPT language=javascript>
function select_class(){
window.open("$thisprog?action=add_sp&id="+document.FORM.file_name.options[document.FORM.file_name.selectedIndex].value,"_self");
}
function select(){
document.FORM.m_graphic.value=FORM.image.value;
document.bbsimg.src = "$imagesurl/face/$id/"+FORM.image.value;}
function select1(){
document.FORM.sx_graphic.value=FORM.sximage.value;
document.sxdemo.src = "$imagesurl/face/$id/"+FORM.sximage.value;}
</SCRIPT>
  <select name=file_name size=1" onchange=select_class()>
  <option value=blank>== 选择分类 ==</option>
  $temps
  </select></td><td rowspan="5" height=226 width=240><IMG border=1 name=bbsimg src="$imagesurl/face/blank.gif" align="absmiddle"> <IMG name=sxdemo src="$imagesurl/face/blank.gif" border=1 width=84 hegiht=84></td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>商品名称</td><td><input type=text size=20 name="m_name" maxlength=20></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>商品价格</td><td><input type=text size=10 name="m_money"> $moneyname</td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>商品描述</td><td><input type=text size=40 name="m_description"></td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>适合人群</td><td><input type="radio" name="fit_herd" value="m">男 <input type="radio" name="fit_herd" value="f">女 <input type="radio" name="fit_herd" value="t"> 通用</td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>商品图片地址</td><td><input type=text size=40 name="m_graphic"></td><td><select name="image" onChange=select()><option value="blank.gif">选择图片$myimages</select></td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>商品缩小图片地址</td><td><input type=text size=40 name="sx_graphic"></td><td><select name="sximage" onChange=select1()><option value="blank.gif">选择图片$myimages</select></td>
	</tr>

	<tr bgcolor=$miscbackone><td align=center colspan=3><input type=submit value="提 交"></td></tr></form>
	</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;

        #	<tr bgcolor=$miscbackone>
        #	<td>商品耐久度</td><td><input type=text size=5 name="m_wear"> 点</td>
        #	</tr>
    }
    else {
        $sp_name = $query->param('m_name');
        $file_name = $query->param('file_name');
        $sp_money = $query->param('m_money');
        $sp_description = $query->param('m_description');
        $sp_wear = $query->param('m_wear');
        $sp_fitherd = $query->param('fit_herd');
        $sp_graphic = $query->param('m_graphic');
        $sp_sxgraphic = $query->param('sx_graphic');

        &error("增加单一商品&商品名字不能空！！") if ($sp_name eq "");
        &error("增加单一商品&请选择商品的类别！！") if ($file_name eq "blank");
        &error("增加单一商品&商品价格不能空！！") if ($sp_money eq "");
        &error("增加单一商品&商品描述不能空！！") if ($sp_description eq "");
        #	&error("增加单一商品&商品耐久度不能空！！") if ($sp_wear eq "");
        &error("增加单一商品&商品图片不能空！！") if ($sp_graphic eq "");
        &error("增加单一商品&商品缩小图片不能空！！") if ($sp_sxgraphic eq "");
        &error("增加单一商品&请选择商品的适合人群！！") if ($sp_fitherd eq "");

        $currenttime = time();

        my $filetoopen = "$lbdir" . "face/wpdata/$file_name.pl";
        open(FILE, ">>$filetoopen");
        print FILE "$currenttime\t$sp_name\t$sp_money\t$sp_description\t$sp_wear\t$sp_fitherd\t$sp_graphic\t$sp_sxgraphic\t\t\n";
        close(FILE);
        $output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>商 品 增 加 成 功！</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog?action=add_sp">~;
    }
}

sub view_user {
    my $id = $query->param('id');

    my $filetoopen = "$lbdir" . "face/totaluser.cgi";
    open(FILE, "$filetoopen");
    my $totaluser = <FILE>;
    close(FILE);
    my @membernum = split(/\t/, $totaluser);
    $membernum = @membernum;
    foreach (@membernum) {
        $userinfo = qq~$userinfo<option value="$_">$_</option>~;
        $userinfo =~ s/value=\"$id\"/value=\"$_\" selected/;
    }
    if ($id ne "") {
        &readface("$id", 1);
        $loadface = "没设置" if ($loadface eq "");
        $loadface = "虚拟形象做为论坛头像" if ($loadface eq "y");
        $loadface = "论坛普通形象(查看个人资料时候显示)" if ($loadface eq "n");
    }

    $output .= qq~<SCRIPT language=javascript>
function select_user(){
window.open("$thisprog?action=view&id="+document.FORM.file_name.options[document.FORM.file_name.selectedIndex].value,"_self");
}</SCRIPT>
<table cellPadding=6 cellSpacing=1 width=100%>
<form action="$thisprog" method="post" name=FORM>
<tr bgcolor=$miscbacktwo>
<td colspan=3 align=center><font color=$fontcolormisc><b>[ 查 看 用 户 信 息 - 总共有：$membernum 名 ]</b></font></td>
</tr>
<tr bgcolor=$miscbackone>
<td rowspan="8" width=150><DIV id="SHOW" style='padding:0;position:relative;top:0;left:0;width:140;height:226'></div></td>
<td width=550></td>
<td rowspan="8" width=150><select name=file_name size=16 onchange=select_user()>$userinfo</select></td></tr>~;

    if ($id ne '') {
        for ($i = 1; $i < 26; $i++) {
            @tempsp = split(/\_/, @buy_sp[$i]);
            next if (@tempsp eq "");
            for ($j = 0; $j < @tempsp; $j++) {
                ($info1, $info2) = split(/\,/, @tempsp[$j]);

                $/ = "";
                my $filetoopen = "$lbdir" . "face/wpdata/$i.pl";
                open(FILE, "$filetoopen");
                my $sort = <FILE>;
                close(FILE);
                $/ = "\n";

                if ($sort !~ /$info1\t(.*)/) # 找不到指定的商品ID
                {
                    $ladesign = $info2 eq 'Y' ? 1 : 0;
                    $outinfo .= qq~'$info1|$info2||||$i|$j',~;
                    $outinfo1 .= qq~'$ladesign',~;
                    $outinfo2 .= qq~'$i',~;
                }
                else {
                    my ($sp_name, $sp_money, $x, $sp_wear, $sp_fitherd, $sp_graphic, $sp_sxgraphic, $sp_suit, $sp_suitid) = split(/\t/, $1);
                    $ladesign = $info2 eq 'Y' ? 1 : 0;
                    $outinfo .= qq~'$sp_name|$info2|$sp_fitherd|$sp_graphic|$sp_sxgraphic|$sp_suitid|$j',~;
                    $outinfo1 .= qq~'$ladesign',~;
                    $outinfo2 .= qq~'$i',~;
                    $outmoney += $sp_money;
                }
            }
        }

        chop($outinfo);
        chop($outinfo1);
        chop($outinfo2);
        $outmoney = 0 if ($outmoney eq "");
        $output .= qq~
<SCRIPT LANGUAGE="JavaScript">
// 3FACE JS
var currface = "$currequip";
var showArray = currface.split('-');


var s="";
for (var i=0; i<=25; i++)
{
   if(showArray[i] != '0')
   {
	s+="<IMG src=$imagesurl/face/"+i+"/"+showArray[i]+".gif style='padding:0;position:absolute;top:0;left:0;width:140;height:226;z-index:"+i+";'>";
   }
}
s+="<IMG src=$imagesurl/face/blank.gif style='padding:0;position:absolute;top:0;left:0;width:140;height:226;z-index:50;'>";
SHOW.innerHTML=s;
</script>
  <tr bgcolor=$miscbackone> 
    <td>当前用户名：$id</td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td>虚拟形象使用方式：$loadface</td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td></td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td></td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td>当前装备总金额：$outmoney $moneyname</td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td></td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td></td>
  </tr>

<script>
var AllArray = new Array($outinfo);
var LadeSign = new Array($outinfo1);
var SortArray = new Array($outinfo2);

function DispInfo(Sign)
{
    var Info = "<table border=0 cellPadding=3 cellSpacing=0 width=84 bgcolor=$tablebordercolor align=left>";
    var jj=0;

    for(i=0;i<AllArray.length;i++)
    {
	if(Sign == LadeSign[i])
	{
	    var UTemp = AllArray[i].split('|');	// 分解商品信息

	    if(UTemp[2] == 'f')
		SPSEX = '女'
	    else if(UTemp[2] == 'm')
	        SPSEX = '男'
	    else
	        SPSEX = '通用'

	    if(jj == 0)
	        Info += "<tr>";
	    Info += "<td width=84 bgColor=$miscbackone>";

	    if(UTemp[2] == '')
		Info += "<img src=$imagesurl/face/images/abate.gif width=84 height=84 border=0' alt='无效商品\\n商品类别："+UTemp[5]+"\\n商品ID号："+UTemp[0]+"'></td>";
	    else
		Info += "<img src=$imagesurl/face/"+SortArray[i]+"/"+UTemp[4]+" width=84 height=84 border=0 alt='商品名称："+UTemp[0]+"\\n适用性别："+SPSEX+"'></td>";

	    if(jj == 7)
	        Info += "</tr>";
	    if(jj < 7)
	        jj++;
	    else
	        jj = 0;
	}
    }
    k = 8 - jj;
    Info += "<td colspan="+k+" bgColor=$miscbackone></td></tr></table>";
    if(Sign == 1)
	LoadArea.innerHTML = Info;
    else
	ULoadArea.innerHTML = Info;
}
</script>

<tr><td colspan=3 bgcolor=$miscbacktwo height=20><font color=$titlefont size=2><B>当前配带物品</B></font></td></tr>
<tr><td colspan=3 bgcolor=$miscbackone>
<div id=LoadArea><script>DispInfo(1);</script></div>
</td></tr>
<tr><td colspan=3 bgcolor=$miscbacktwo height=20><font color=$titlefont size=2><B>未配带物品</B></font></td></tr>
<tr><td colspan=3 bgcolor=$miscbackone>
<div id=ULoadArea><script>DispInfo(0);</script></div>
<div id=Area></div>
</td></tr>~;
    }

    $output .= qq~</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

sub edit_sp {
    my $filetoopen = "$lbdir" . "face/class.cgi"; # 商品类别
    open(FILE, "$filetoopen");
    my @sort = <FILE>;
    close(FILE);
    my $id = $query->param('id');

    foreach (@sort) {
        ($cateid, $sort_id, $sort_status, $sort_name, $sort_info) = split(/\t/, $_);
        $mainid .= qq~<option value="$sort_id">$sort_name</option>~;
        $mainid =~ s/value=\"$id\"/value=\"$id\" selected/;
    }

    $output .= qq~
<SCRIPT language=javascript>
function select_sort(){
window.open("$thisprog?action=edit&id="+document.FORM.sort.options[document.FORM.sort.selectedIndex].value,"_self");
}
</SCRIPT>
<table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST name=FORM>
<tr bgcolor=$miscbacktwo>
<td align=center><font color=$fontcolormisc><b>[ 商 品 管 理 ]</b></font></td>
</tr>
<tr bgcolor=#EEEEEE><td height=30>选择商品类别：<select name=sort size=1" onchange=select_sort()><option value=''>== 选择类别 ==</option>$mainid</select></td></tr></form>~;

    if ($id ne '') {
        $filetoopen = "$lbdir" . "face/wpdata/$id.pl";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, "$filetoopen");
        my @sort = <FILE>;
        close(FILE);
        $sort = @sort;
        if ($sort eq '0') {
            $output .= qq~
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>本类暂无任何商品！</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
            return;
        }
        $numid = $id;
        $output .= qq~
<script language="JavaScript" type="text/javascript">
function editface(forumid,countid,action){
var Win=window.open("editface.cgi?action="+action+"&num="+forumid+"&id="+countid,"FACE",'width=500,height=280,resizable=0,scrollbars=0,menubar=0,status=1');
}
function check(){if(!confirm("继续下去的操作将不可恢复，是否确认删除？"))return false;}
</script>
<tr bgcolor=$miscbackone><td>
<TABLE border=0 cellPadding=0 cellSpacing=1 width=100% align=center>~;

        my $page = $query->param('page');
        $page = 1 if ($page eq "");
        my $allnum = @sort;
        my $temp = $allnum / 9;
        my $allpages = int($temp);
        $allpages++ if ($allpages != $temp);
        $page = 1 if ($page < 1);
        $page = $allpages if ($page > $allpages);
        my $showpage = "";
        if (!$allpages) {$showpage .= "当前没有记录";}
        elsif ($allpages == 1) {$showpage .= "当前记录只有 <B>1</B> 页";}
        else {
            $showpage = "总共 <b>$allpages</b> 页，<b>$sort</b> 件商品：[";
            $i = $page - 3;
            $showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i title='第 $i 页'>←</a>~ if ($i > 0);
            $i++;
            $showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i>$i</a>~ if ($i > 0);
            $i++;
            $showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i>$i</a>~ if ($i > 0);
            $i++;
            $showpage .= qq~ <font color=#990000><B>$i</B></font>~;
            $i++;
            $showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i>$i</a>~ unless ($i > $allpages);
            $i++;
            $showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i>$i</a>~ unless ($i > $allpages);
            $i++;
            $showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i title='第 $i 页'>→</a>~ unless ($i > $allpages);
            $showpage .= " ]";
        }

        for ($i = $allnum - $page * 9 + 9 - 1; $i >= $allnum - $page * 9 && $i >= 0; $i--) {
            ($sp_id, $sp_name, $sp_money, $x, $sp_wear, $sp_fitherd, $sp_graphic, $sp_sxgraphic, $sp_suit, $sp_suitid) = split(/\t/, @sort[$i]);

            if ($sp_suit eq 'Y') {
                chop($sp_suitid);
                @taoinfo = split(/\_/, $sp_suitid);
                $numid = @taoinfo[0];
            }
            $sp_fitherd = '男' if ($sp_fitherd eq 'm');
            $sp_fitherd = '女' if ($sp_fitherd eq 'f');
            $sp_fitherd = '男女' if ($sp_fitherd eq 't');

            $output .= qq~<tr>~ if ($ii == 0);

            $output .= qq~
<td width=33%>
<table border=0 cellPadding=0 cellSpacing=2 width=100%><TBODY>
<TR><TD bgColor=#eeeeee height=84 rowSpan=5 width=84><img src=$imagesurl/face/$numid/$sp_sxgraphic width=84 hegiht=84></TD>
<TD bgColor=#eeeeee height=20>$sp_name</TD></TR>
<TR><TD bgColor=#eeeeee height=20>单　价：$sp_money.00</TD></TR>
<TR><TD bgColor=#eeeeee height=20>适　用：$sp_fitherd</TD></TR>
<TR><TD bgColor=#eeeeee height=20 align=center><a href="javascript:editface('$id','$sp_id','edit_sp')">[修改]</a>　　<a href="javascript:editface('$id','$sp_id','del_sp')" onclick="return check();">[删除]</a></TD></TR>
</TBODY></TABLE>
</TD><TD width=10>&nbsp;</TD>~;

            #<TR><TD bgColor=#eeeeee height=20>耐久度：$sp_wear</TD></TR>

            $output .= qq~</tr>~ if ($ii == 2);
            if ($ii < 2) {$ii++;}
            else {$ii = 0;}
        }
        $output .= qq~</table></td></tr>
<form action=$thisprog method=POST name="Jump">
<input type=hidden name="action" value="edit">
<input type=hidden name="id" value="$id">
<input type=hidden name=page value="">
<script>
function Page_Jump()
{
     document.Jump.page.value = document.Jump.N_Page.value;
}
</script>
<tr bgcolor=$miscbacktwo><td align=center><font color=$menufontcolor>$showpage</font> 跳到 <input type="text" name="N_Page" size="3" maxlength="3">  <input type="submit" name="Submit" value="确定" onClick="return Page_Jump();"></td></tr></form>~;
    }
    $output .= qq~</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

&output("$plugname - 后台管理", \$output);
