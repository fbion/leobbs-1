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
require "bbs.lib.pl";
$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$bgcolor = "white"; # 背景颜色
$interval = 10;   #一行几个图标
$linesperpage = 8; #一页几行

########### No need to edit below this line ###################
$thisprog = "viewavatars.cgi";

$perpage = $interval * $linesperpage;
$query = new LBCGI;

$startimage  = $query -> param ("startimage");
$endimage    = $query -> param ("endimage");
$inpage      = $query -> param ("page");

if (($startimage < 0) || ($startimage eq "") || ($endimage <= 0) || ($endimage < $startimage)) {
 $startimage = 0;
 $endimage = $perpage - 1;
}
if ($inpage eq "") { $inpage = 1; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

$inmembername   = cookie("amembernamecookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

if ((!$inmembername) or ($inmembername eq "客人")) {
  $inmembername = "客人";
} else {
#  &getmember("$inmembername");
    &getmember("$inmembername","no");
  &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}
$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");


$count = 0;

$dirtoopen = "$imagesdir" . "avatars";
opendir (DIR, "$dirtoopen");
@dirdata = readdir(DIR);
closedir (DIR);

@images = grep(/\.gif$/i,@dirdata);

foreach $image (@images) {
  if ($membercode ne 'ad') {
    if ($image =~ /admin\_/ig) {
      next;
    }
  }
  if ($image =~ /noavatar/ig) {
    next;
  } else {
    push (@cleanimages, $image);
  }
}

$totalimages = @cleanimages - 1;

if ($endimage > $totalimages) { $endimage = $totalimages; }

@imagestoshow = @cleanimages[$startimage..$endimage];

$numimages = $endimage - $startimage;
$shownimages = 0;

foreach (@imagestoshow) {
  $avatar =  $_;
  $avatar =~ s/.gif//i;
  $avatarout .= qq~<td align="center" valign="center"><img src="$imagesurl/avatars/$avatar.gif" alt="$avatar" $defaultwidth $defaultheight><br>$avatar</td>\n~;
  $count++;
  $shownimages++;

  if (($count eq $interval) && ($shownimages <= $numimages)) {
    $count = 0;
    $countdown++;
    $avatarout .= qq~</tr><tr bgcolor="$bgcolor">\n~;
  }
}


print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&title;

$output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> 在这里您可以查看到本站所有的头像</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> → <a href="viewavatars.cgi">用户头像列表</a> → 查看列表<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>

~;

$output .= qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellPadding=6 cellSpacing=1 border=0 width=100%>
<tr bgcolor="$bgcolor">
$avatarout~;

for($count; $count < $interval; $count++) {
     $output .= qq~<td>&nbsp;</td>~;
}

&splitpages;

$output .= qq~
</tr><tr><td colspan=$interval bgcolor="$bgcolor" align=center>
<center><font color=$fontcolormisc>$pagelinks</font></td></tr>
</table></td></tr>
</table><SCRIPT>valignend()</SCRIPT>
~;

&output("$boardname - 用户头像列表",\$output);

sub splitpages {
 $totalpages = @cleanimages / $perpage;
 ($pagenumbers, $decimal) = split (/\./, $totalpages);
 if ($decimal > 0) { $pagenumbers++; }

 $page = 1;
 $start = 0;
 $end = $perpage - 1;
 $pagedigit = 0;

 while ($pagenumbers > $pagedigit) {
   $pagedigit++;
   if ($inpage ne $page) {
     $pagelinks .= qq~[<a href="$thisprog?startimage=$start&endimage=$end&page=$page">第$pagedigit页</a>] ~;
   }
   else { $pagelinks .= qq~[<B>第$pagedigit页</B>] ~; }
   $start += $perpage;
   $end += $perpage;
   $page++;
 }
 $page--;
 $pagelinks = qq~本列表共有$page页　$pagelinks~;

 if ($totalpages <= 1) { 
  $pagelinks = qq~用户头像列表只有一页.~; 
 }
}
