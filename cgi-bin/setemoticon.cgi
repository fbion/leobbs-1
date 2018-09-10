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

$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "setemoticon.cgi";
$query = new LBCGI;

$addme = $query->param('addme');

for ('action', 'emoticonid', 'emoticonname', 'emoticonurl', 'emoticoninfo') {
    my $theparam = $query->param($_);
    $theparam = &cleaninput("$theparam");
    ${$_} = $theparam;
}
$checkaction = ($query->param('checkaction') eq "yes") ? "yes" : "no";

$inmembername = $query->cookie("adminname");
$inpassword = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

my %Mode = ('createnew' => \&createnew,
    'processnew'        => \&createaction,
    'edit'              => \&editemot,
    'editaction'        => \&editaction,
    'delete'            => \&deleteaction
);

&getadmincheck;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&admintitle;
&getmember("$inmembername", "no");
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
    print qq~
    <tr><td bgcolor="#2159C9" colspan=2><font color=#FFFFFF>
    <b>欢迎来到论坛管理中心 / 表情转换设置管理器</b>
    </td></tr>~;
    if ($Mode{$action}) {
        $Mode{$action}->();
    }
    else {
        &emoticonlist;
    }
    print qq~</table></td></tr></table>~;
}
else {
    &adminlogin;
}

sub emoticonlist {
    print qq~<tr><td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>注意事项</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=2 align=center>
    　　在下面，您将看到目前所有的 EMOT 图片。您可以增加一个新的 EMOT 图片。也可以编辑或删除目前存在的 EMOT 图片。<p>
    <table width=80% align=center>
    <tr><td>
    <li><u>图片名称</u> 为正在使用的图片,把滑鼠移上後可看到图片的文件名称。<p>
    <li><u>转换代码</u> 为转换时使用的代码,在文章内容输入代码後便会显示相关的 EMOT 图片。<p>
    <li><u>表情描述</u> 为转换後图片的文字注解。<p>
    </td></tr>
    </table>
    </td></tr>
~;

    $filetoopen = "${lbdir}data/emoticons.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @emoticons = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    print qq~
    <tr><td bgcolor=#FFFFFF align=center colspan=2><table width=90% cellspacing="0" cellpadding="2">
    <tr><td align="center" colspan="4" bgcolor="#EEEEEE">|| <a href="$thisprog?action=createnew">增加新 EMOT 图片</a> ||</td></tr>
    <tr><td align="center" bgcolor=$catback><BR><b style="color:blue">图片名称</b></td><td align="center" width="20%" bgcolor=$catback><b style="color:blue">转换代码</b></td><td align="center" width="20%" bgcolor=$catback><b style="color:blue">表情描述</b></td><td align="center" width="30%" bgcolor=$catback><b style="color:blue">相关操作</b></td></tr>
~;

    $emoticonnum = 0;
    foreach $emoticon (@emoticons) {
        chomp $emoticon;
        next if ($emoticon eq "");
        ($emoticonname, $emoticonurl, $emoticoninfo) = split(/\t/, $emoticon);
        $emoticonurl =~ s/\\//g;
        $emoticonnum++;
        print qq~<tr><td align="left">　　<img src="$imagesurl/emoticons/$emoticonname" align="absmiddle" border=0>$emoticonname</td><td align="right"><input type="text" value="$emoticonurl" maxlength="10" style="width:100%"></td><td align="right"><input type="text" value="$emoticoninfo"  style="width:100%"></td><td align="center"><a href="$thisprog?action=edit&emoticonid=$emoticonnum">[编辑]</a> <a href="$thisprog?action=delete&emoticonid=$emoticonnum">[删除]</a></td></tr>\n~;
    }
    print qq~<tr><td align="center" colspan="4" bgcolor="#EEEEEE">共有 EMOT 图片 $emoticonnum 个 </td></tr></table>~;
}

sub createnew {
    opendir(DIR, "${imagesdir}emoticons");
    @emoticon = readdir(DIR);
    closedir(DIR);
    chomp @emoticon;
    @emoticon = grep (/.[gif|jpg|png|bmp]$/, @emoticon);
    @emoticon = sort @emoticon;
    $emoticon = join("\t", @emoticon);
    $emoticon =~ s/^\t//;
    $emoticon = "<option>" . $emoticon . "</option>";
    $emoticon =~ s/\t/<\/option><option>/isg;
    $emoticon =~ s/<option><\/option>//isg;
    print qq~
<script>
function selectimg(oj,fm) {
    img =oj.options[oj.selectedIndex].text;
    fm.emoticonname.value=img;
    document.emotimg.src = "$imagesurl/emoticons/"+img;
}
</script>
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="processnew">    
    <tr><td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b> EMOT 图片名称</b><br>请输入新 EMOT 图片的文件名称<BR></font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="emoticonname" value=""><select name="image" onChange="selectimg(this,this.form)">$emoticon</select><img name=emotimg src="$imagesurl/images/none.gif" align="absmiddle" border=0></td>
    </tr>
    <tr><td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>表情转换代码</b><br>请输入新 EMOT 图片的转换代码<BR>(只限半形英文,数字和符号)</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=40 name="emoticonurl" value="" maxlength="10"></td>
    </tr>
    <tr><td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font  color=#333333><b> EMOT 图片描述</b><br>请输入 EMOT 图片的描述</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=40 name="emoticoninfo"></td>
    </tr>
    <tr><td bgcolor=#FFFFFF valign=middle align=center colspan=2>
    <input type=submit value="提 交"></form>
    </td>
    </tr>
    <tr><td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td>
    </tr>
    ~;
}

sub editemot {
    $filetoopen = "$lbdir" . "data/emoticons.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @emoticons = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    ($emoticonname, $emoticonurl, $emoticoninfo) = split(/\t/, $emoticons[$emoticonid - 1]);
    $emoticonurl =~ s/\\//g;
    opendir(DIR, "${imagesdir}emoticons");
    @emoticon = readdir(DIR);
    closedir(DIR);
    chomp @emoticon;
    @emoticon = grep (/.[gif|jpg|png|bmp]$/, @emoticon);
    @emoticon = sort @emoticon;
    $emoticon = join("\t", @emoticon);
    $emoticon =~ s/^\t//;
    $emoticon = "<option>" . $emoticon . "</option>";
    $emoticon =~ s/\t/<\/option><option>/isg;
    $emoticon =~ s/<option><\/option>//isg;
    $emoticon =~ s/<option>$emoticonname<\/option>/<option selected>$emoticonname<\/option>/;
    print qq~
<script>
function selectimg(oj,fm){
	img =oj.options[oj.selectedIndex].text;
	fm.emoticonname.value=img;
	document.emotimg.src = "$imagesurl/emoticons/"+img;
}
</script>
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="editaction">
    <input type=hidden name="emoticonid" value="$emoticonid">
    <input type=hidden name="emoticon" value="$emoticonname">
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b> EMOT 图片名称</b><br>请输入新的 EMOT 图片文件名称<BR></font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="emoticonname" value="$emoticonname"><select name="image" onChange="selectimg(this,this.form)">$emoticon</select><img name=emotimg src="$imagesurl/emoticons/$emoticonname" align="absmiddle" border=0></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>表情转换代码</b><br>请输入新的 EMOT 图片转换代码<BR>(只限半形英文,数字和符号)</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=40 name="emoticonurl" value="$emoticonurl" maxlength="10"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font  color=#333333><b> EMOT 图片描述</b><br>请输入新的 EMOT 图片描述</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=40 name="emoticoninfo" value="$emoticoninfo"></td>
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
    if ($emoticonname eq "" || $emoticonurl eq "") {
        &errorout(" EMOT 图片名称及表情转换代码不能为空！");
        return;
    }
    $emoticonurl = &decode($emoticonurl);
    if ($errorout == 1) {
        &errorout("表情转换代码不容许使用英文,数字和符号以外的字串！");
        return;
    }
    $filetoopen = "$lbdir" . "data/emoticons.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @emoticons = <FILE>;
    close(FILE);

    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    foreach $emoticon (@emoticons) {
        next if ($emoticon eq "");
        chomp $emoticon;
        print FILE "$emoticon\n";
    }
    print FILE "$emoticonname\t$emoticonurl\t$emoticoninfo\t\n";
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    &doemote;

    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#333333><b>增加结果</b><p>
    <li>新 EMOT 图片 <B>$emoticonname</b> 已经建立！
    <br><BR><a href=$thisprog?action=createnew>继续增加 EMOT 图片</a>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td>
    </tr>
    ~;
}
sub editaction {
    if ($emoticonname eq "" || $emoticonurl eq "") {
        &errorout(" EMOT 图片名称及表情转换代码不能为空！");
        return;
    }
    $emoticonurl = &decode($emoticonurl);
    if ($errorout == 1) {
        &errorout("表情转换代码不容许使用英文,数字和符号以外的字串！");
        return;
    }
    $filetoopen = "$lbdir" . "data/emoticons.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @emoticons = <FILE>;
    close(FILE);
    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    $emoticonnum = 0;
    foreach $emoticon (@emoticons) {
        next if ($emoticon eq "");
        chomp $emoticon;
        $emoticonnum++;
        if ($emoticonid eq $emoticonnum) {
            ($oldemoticonname, undef, undef) = split(/\t/, $emoticon);
            print FILE "$emoticonname\t$emoticonurl\t$emoticoninfo\t\n";
        }
        else {
            print FILE "$emoticon\n";
        }
    }
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    &doemote;

    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#333333><b>编辑结果</b><p>
    <li> EMOT 图片 <B>$oldemoticonname</b> 已经更新！
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td>
    </tr>
    ~;
}

sub deleteaction {
    if ($checkaction ne "yes") {
        print qq~<tr>
    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
    <font color=#990000><b>警告！！</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
    <font color=#333333>如果您确定要删除 EMOT 图片 $emoticon，那么请点击下面链接<p>
    >> <a href="$thisprog?action=delete&checkaction=yes&emoticonid=$emoticonid">删除 EMOT 图片</a> <<
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td>
    </tr>
    ~;
        return;
    }
    $filetoopen = "$lbdir" . "data/emoticons.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @emoticons = <FILE>;
    close(FILE);

    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    $emoticonnum = 0;
    foreach $emoticon (@emoticons) {
        next if ($emoticon eq "");
        chomp $emoticon;
        $emoticonnum++;
        if ($emoticonid eq $emoticonnum) {
            ($oldemoticonname, undef, undef) = split(/\t/, $emoticon);
        }
        else {
            print FILE "$emoticon\n";
        }
    }
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    &doemote;

    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#333333><b>删除结果</b><p>
    <li> EMOT 图片 <B>$oldemoticonname</B> 已被删除！
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td>
    </tr>
    ~;
}

sub errorout {
    my ($errortype, $errormsg) = @_;
    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>$errortype</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF align="center" colspan=2><font color=red>$errormsg</font></td></tr>
    <tr><td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">返回</a> --</td></tr>
    ~;
}

sub decode {
    my $str = shift;
    my @strarr = split(//, $str);
    chomp @strarr;
    my $strlen = length($str);
    $str = "";
    for ($i = 0; $i < $strlen; $i++) {
        my $binchar = vec($str, $i, 8);
        if ($binchar > 126) {
            $errorout = 1;
            last;
        }
        if ($strarr[$i] =~ /[^a-zA-Z0-9]/) {
            $str .= "\\$strarr[$i]";
        }
        else {
            $str .= $strarr[$i];
        }
    }
    return $str;
}
sub doemote {
    $subsmilecode = '';
    open(FILE, "${lbdir}data/emoticons.cgi");
    my @emoticonsdata = <FILE>;
    close(FILE);
    foreach (@emoticonsdata) {
        chomp;
        next if ($_ eq "");
        my ($emoticonname, $emoticonurl, $emoticoninfo) = split(/\t/, $_);
        $subsmilecode .= "\$\$post =~ s/(^|\\s|\\>|\\;)$emoticonurl(\\s|\$|\\<)/\$1<img src=\${imagesurl}\\/emoticons\\/$emoticonname alt=\"$emoticoninfo\">\$2/isg;\n";
    }

    open(FILE, ">${lbdir}data/emoticons.pl");
    print FILE $subsmilecode;
    close(FILE);
}
