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
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
use MAILPROG qw(sendmail);
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";
require "code.cgi";
require "data/cityinfo.cgi";
$|++;

$thisprog = "setmembers.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$action = $query->param('action');
$box = $query->param('box');
$checkaction = $query->param('checkaction');
$inletter = $query->param('letter');
$inmember = $query->param('member');
$inmember = &unHTML("$inmember");
$action = &unHTML("$action");

$indellast = $query->param('dellast');
$indellast = &unHTML("$indellast");
$indelposts = $query->param('delposts');
$indelposts = &unHTML("$indelposts");
$indeltime = $query->param('deltime');
$indeltime = &unHTML("$indeltime");
$delusetype = $query->param('delusetype');
$delusetype = &unHTML("$delusetype");
$indelcdrom = $query->param('delcdrom');
$indelcdrom = &unHTML("$indelcdrom");
$undelname = $query->param('undelname');
$undelname = &unHTML("$undelname");

$in_member_name = $query->cookie("adminname");
$in_password = $query->cookie("adminpass");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&admintitle;

&getmember("$in_member_name", "no");

if ((($member_code eq "ad") || ($member_code eq "smo")) && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {

    print qq~
	<script>
	function openScript(url, width, height){var Win = window.open(url,"openScript",'width=' + width + ',height=' + height + ',resizable=1,scrollbars=yes,menubar=yes,status=yes' );}
	</script>
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / 用户管理</b>
            </td></tr>
            ~;

    my %Mode = (

        'viewletter'     => \&viewletter,
        'edit'           => \&edit,
        'deletemember'   => \&deletemember,
        'unban'          => \&unban,
        'delnopost'      => \&delnopost,
        'canceldel'      => \&canceldel,
        'deleteavatar'   => \&deleteavatar,
        'boxaction'      => \&boxaction,
        'delok'          => \&delok,
        'viewip'         => \&viewip,
        'viewdelmembers' => \&viewdelmembers,
        'undelmember'    => \&undelmember
    );

    if ($Mode{$action}) {
        $Mode{$action}->();
    }
    else {&memberoptions;}

    print qq~</table></td></tr></table>~;
}
else {
    &adminlogin;
}


############### delete member

sub deleteavatar {

    $oldmembercode = $member_code;
    &getmember("$inmember");
    if ((($member_code eq "ad") || ($member_code eq "smo") || ($member_code eq "cmo") || ($member_code eq "mo") || ($member_code eq "amo")) && ($oldmembercode eq "smo")) {
        print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>总斑竹无权删除坛主和斑竹资料！</b></td></tr>";
        exit;
    }
    $inmember = $inmember;
    $inmember =~ y/ /_/;
    $inmember =~ tr/A-Z/a-z/;

    unlink("${imagesdir}usravatars/$inmember.gif");
    unlink("${imagesdir}usravatars/$inmember.png");
    unlink("${imagesdir}usravatars/$inmember.jpg");
    unlink("${imagesdir}usravatars/$inmember.jpeg");
    unlink("${imagesdir}usravatars/$inmember.swf");
    unlink("${imagesdir}usravatars/$inmember.bmp");
    $memberfiletitletemp = unpack("H*", "$inmember");
    unlink("${imagesdir}usravatars/$memberfiletitletemp.gif");
    unlink("${imagesdir}usravatars/$memberfiletitletemp.png");
    unlink("${imagesdir}usravatars/$memberfiletitletemp.jpg");
    unlink("${imagesdir}usravatars/$memberfiletitletemp.swf");
    unlink("${imagesdir}usravatars/$memberfiletitletemp.bmp");

    unlink("${lbdir}cache/meminfo/$inmember.pl");

    print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>用户头像已经删除了</b>
        </td></tr>
         ~;

} # end routine

##################################################################################
######## Subroutes (forum list)


sub memberoptions {
    %iplist = ();
    %lettlerlist = ();
    open(FILE, "$lbdir/data/lbmember4.cgi");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @file = <FILE>;
    close(FILE);
    chomp @file;
    @file = sort @file;
    $nowcount_a = 0;
    $nowcount_b = 0;
    foreach (@file) {
        my ($getmembername, $getip) = split(/\t/, $_);
        my $fr;
        ($getip, $getip2) = split(/, /, $getip);
        $getip = $getip2 if (($getip2 ne "") && ($getip2 ne "unknown"));
        $getip =~ s/\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$//;
        unless (defined($iplist{$getip})) {
            $iplist{$getip} = "$_";
            $ipshow = sprintf("% 3s", $getip);
            $ipshow =~ s/\s/\&nbsp\;/g;
            $tempoutput2 .= qq~<br>~ if ($nowcount_b % 15 == 0);
            $tempoutput2 .= qq~ <a href="$thisprog?action=viewip&letter=$getip">$ipshow</a> ~;
            $nowcount_b++;
        }
        if ($getmembername =~ /^[\w\-]/) {
            $fr = substr($getmembername, 0, 1);
            $fr =~ tr/a-z/A-Z/;
            $frshow = sprintf("%- 2s", $fr);
            $frshow =~ s/\s/\&nbsp\;/g;
        }
        else {
            $fr = substr($getmembername, 0, 2);
            $frshow = $fr;
        }
        unless (defined(($lettlerlist{$fr}))) {
            $lettlerlist{$fr} = "$_";
            $tempoutput .= qq~<br>~ if ($nowcount_a % 15 == 0);
            $tempoutput .= qq~ <a href="$thisprog?action=viewletter&letter=~ . uri_escape($fr) . qq~">$frshow</a> ~;
            $nowcount_a++;
        }
        last if ($nowcount_a >= 300);
    }

    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>请选择一项</b>
    </td>
    </tr>          
    ~;
    if ($member_code eq "ad") {
        print qq~

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="foruminit.cgi?action=uptop">更新用户排名</a></b><br>
    用户排名其实不会自动更新的，除非你在这儿更新一下。<BR><BR>
    </td>
    </tr>
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="foruminit.cgi?action=updatecount">重新计算用户总数</a></b><br>
    将更新首页显示的用户数，这样可以用来恢复正确总用户数。<BR><BR>
    </td>
    </tr>
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b>删除符合条件的用户</b>(同时会自动更新用户排名)<BR>
    预删除并不会真正删除用户，只是做一个统计。斑竹和坛主是不允许在这里删除的。<BR>
    预删除和真正删除期间，如果用户访问了论坛，那么在真正删除的时候，此用户资料将被保留。<BR>
    真正删除后，用户的所有资料都会丢失，除非你做过备份，否则是无法恢复的。
	<form action="setmembers.cgi" method=POST>
        <input type=hidden name="action" value="delnopost">
        <select name="deltime">
        <option value="30" >一个月内没访问 
        <option value="60" >二个月内没访问 
        <option value="90" >三个月内没访问
        <option value="121">四个月内没访问
        <option value="151">五个月内没访问
        <option value="182">六个月内没访问
        <option value="212">七个月内没访问
        <option value="243">八个月内没访问
        <option value="273">九个月内没访问
        <option value="304">十个月内没访问
        <option value="365">一年之内没访问
        <option value="730">两年之内没访问
        </select> 且 
        <select name="delposts">
		<option value="9999999999">不管发贴总数 
        <option value="0"   >没有发过贴子
        <option value="10"  >总发贴少于 10
        <option value="50"  >总发贴少于 50
        <option value="100" >总发贴少于 100
        <option value="200" >总发贴少于 200
        <option value="300" >总发贴少于 300
        <option value="500" >总发贴少于 500
        <option value="800" >总发贴少于 800
        <option value="1000">总发贴少于 1000
        </select> 且 
        <select name="dellast">
        <option value="no"  >不管访问次数
        <option value="5"   >访问少于 5 次
        <option value="10"  >访问少于 10 次
        <option value="20"  >访问少于 20 次
        <option value="50"  >访问少于 50 次
        <option value="80"  >访问少于 80 次
        <option value="100" >访问少于 100 次
        <option value="200" >访问少于 200 次
        <option value="500" >访问少于 500 次
        </select> 且 
       <select name="delcdrom"> 
       <option value="30" >一个月内没发言 
       <option value="60" >二个月内没发言 
       <option value="90" >三个月内没发言 
       <option value="121">四个月内没发言 
       <option value="151">五个月内没发言 
       <option value="182">六个月内没发言 
       <option value="212">七个月内没发言 
       <option value="243">八个月内没发言 
       <option value="273">九个月内没发言 
       <option value="304">十个月内没发言 
       <option value="365">一年之内没发言 
       <option value="730">两年之内没发言 
       </select><BR>符合方式 
      <select name="delusetype"> 
      <option value="And">AND(所有资料符合)
      <option value="OR">OR(某一资料符合)
      </select> <BR>输入每次进行处理的用户数 <input type=text name="users" size=4 maxlength=4 value=500> 如果无法正常完成，请尽量减少这个数目，延长处理时间<BR>

        <input type=submit value="预 删 除">
        </form>
        ~;
        if (-e "${lbdir}data/delmember.cgi") {
            open(FILE, "${lbdir}data/delmember.cgi");
            @delmembers = <FILE>;
            close(FILE);
            $delmembersize = @delmembers;
            $delmembersize--;
            $pretime = $delmembers[0];
            if ($delmembersize ne "0") {
                chomp $pretime;
                $nowtime = time;
                $nowtime = $nowtime - 3 * 24 * 3600;
                if ($nowtime > $pretime) {
                    $oooput = qq~距离上次预删除时间已经超过３天了 [<a href=$thisprog?action=delok>确定删除</a>]~;
                }
                else {
                    $oooput = qq~距离上次预删除时间还未到３天 [<a href=$thisprog?action=delok>不管，强制删除</a>]~;
                }
                $pretime = &dateformat($pretime);
                print qq~
        	上次预删除时间：$pretime (预删除用户个数： $delmembersize ) [<a href=$thisprog?action=canceldel>取消预删除</a>]<BR>
        	$oooput [<a href=$thisprog?action=viewdelmembers>查看预删除会员列表</a>]
    	    ~;
            }
            else {
                #預刪除會員為 0 時自動取消
                unlink("${lbdir}data/delmember.cgi");
                print qq~
			预删除文件不存在，现在可以进行预删除。 
			~;
            }

        }
        else {
            print qq~
        	预删除文件不存在，现在可以进行预删除。
    	    ~;
        }
        print qq~
    <BR><BR>
    </td>
    </tr>
    ~;
    }
    print qq~
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b>查看、编辑、删除、禁止用户</b><br>
    点击下面的字母你可以查看到用户详细资料， 并可编辑、改变用户的信息。<br>
    禁止用户：只要简单的点击“编辑用户”，然后在“用户属性”中选择“禁止用户”就可以。<br>
    删除用户：只要找到用户，点击删除就可以。<br>
	<form action="setmembers.cgi" method=POST>
        <input type=hidden name="action" value="edit">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="快速定位">
        </form>
    
    ~;

    print qq~
    注册用户大致列表：<br>$tempoutput
<P><a href=$thisprog?action=viewip>寻找以特定ＩＰ注册的用户</a>
    <p>注册ＩＰ大致列表：<br>$tempoutput2
    </td>
    </tr>           
                
                
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><BR>
    <b>注意事项：</b><p>
    如果您希望给您的用户一个自定义的头衔，只要编辑他（她）的资料。<br>
    这个论坛利用储存的发贴数来确定他们的成员身份.<br>
    如果您任命一个用户为版主，而他本身却没有自定义的头衔，那么就会自动添加一个版主头衔。
    如果他已有自定义的等级，那么他的原头衔将被保留。<br>
    版主只能够管理自己的论坛，但是他们也可以在其他论坛中使用 #Moderation Mode 下的功能。<br>
    请确保您所提升的版主是可靠的。<br>
    版主也和坛主一样，不受灌水预防机制限制。<br>
    只有坛主才能够进入管理中心。<br><br>
    如果你禁止了一个用户，那么也同时禁止了用他们原名称、邮件重新注册的可能。
    </td>
    </tr>             
     ~;

} # end routne


##################################################################################
######## Subroutes (Do member count)  
sub canceldel {

    unless (($member_code eq "ad") && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
    }
    else {
        unlink("${lbdir}data/delmember.cgi");
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>取消预删除</b><p>
        <font color=#333333>预删除已经被取消！</font>
        </td></tr>
         ~;
    }
}
sub delnopost {
    $step = $query->param('step');
    $step = 1 unless ($step);
    $size1 = $query->param('size1');
    $size1 = 0 unless ($size1);
    $users = $query->param('users');
    $users = 500 unless ($users);

    opendir(DIR, "${lbdir}$memdir/old");
    @files = readdir(DIR);
    closedir(DIR);
    @memberfiles = grep (/\.cgi$/i, @files);
    $size = @memberfiles;

    $currenttime = time;

    if (-e "${lbdir}data/delmember.cgi" && $step == 1) {
        print qq~
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000>
<b>计算用户排名</b><p>
<font color=#333333>预删除文件存在，不可重复预删除！</font>
</td></tr>~;
    }
    else {
        if ($step == 1) {
            open(FILE, ">${lbdir}data/delmember.cgi");
            print FILE "$currenttime\t\n";
            close(FILE);
            unlink("${lbdir}data/lbmember.cgi");
        }

        $sendtoemail = "";
        open(MEMFILE, ">>${lbdir}data/lbmember.cgi");
        flock(MEMFILE, 2) if ($OS_USED eq "Unix");
        for ($i = ($step - 1) * $users; $i < $step * $users && $i < $size; $i++) {
            ($nametocheck, $no) = split(/\./, $memberfiles[$i]);
            my $namenumber = &getnamenumber($nametocheck);
            &checkmemfile($nametocheck, $namenumber);
            $memberfile = $memberfiles[$i];
            $usrname = "${lbdir}$memdir/$namenumber/$memberfile";
            open(FILE, "$usrname");
            flock(FILE, 2) if ($OS_USED eq "Unix");
            $line = <FILE>;
            close(FILE);
            undef $joineddate;
            undef $lastgone;
            undef $anzahl;
            undef $lastpostdate;
            undef $userad;
            undef $visitno;
            undef $anzahl1;
            undef $anzahl2;
            undef $emailaddr;
            undef $membername;

            ($membername, $no, $no, $userad, $anzahl, $emailaddr, $no, $no, $no, $no, $no, $no, $no, $joineddate, $lastpostdate, $no, $timedifference, $no, $no, $no, $no, $no, $no, $no, $no, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $line);

            ($anzahl1, $anzahl2) = split(/\|/, $anzahl);
            $anzahl = $anzahl1 + $anzahl2;
            ($lastpost, $posturl, $posttopic) = split(/\%\%\%/, $lastpostdate);

            $lastgone = $lastpost if ($lastpost > $lastgone);
            $lastgone = $joineddate if ($joineddate > $lastgone);

            $lastposttime = $lastpost;
            $lastposttime = $joineddate if ($joineddate > $lastposttime);
            $lastposttime1 = $lastposttime + $indelcdrom * 3600 * 24;

            $lastgone1 = $lastgone + $indeltime * 3600 * 24;

            $DelThisMember = "no";
            if ($delusetype eq "And") {
                $DelThisMember = "yes" if (($lastgone1 <= $currenttime) && ($anzahl <= $indelposts) && ($lastposttime1 <= $currenttime));
            }
            else {
                $DelThisMember = "yes" if (($lastgone1 <= $currenttime) || ($anzahl <= $indelposts && $indelposts ne 9999999999) || ($lastposttime1 <= $currenttime));
            }
            $DelThisMember = "no" if (($userad eq "ad") || ($userad eq "mo") || ($userad eq "smo") || ($userad eq "cmo") || ($userad eq "amo") || ($userad =~ /^rz/) || ($useradd5 eq "1"));
            if ($DelThisMember eq "yes") {
                if ($indellast ne "no") {
                    if (($visitno <= $indellast) || ($delusetype eq "OR")) {
                        open(FILE, ">>${lbdir}data/delmember.cgi");
                        flock(FILE, 2) if ($OS_USED eq "Unix");
                        print FILE "$memberfile\t$lastgone\t\n";
                        close(FILE);
                        $size1++;
                        if ($sendtoemail eq "") {$sendtoemail = "$emailaddr";}
                        else {$sendtoemail = "$sendtoemail, $emailaddr";}
                    }
                }
                else {
                    open(FILE, ">>${lbdir}data/delmember.cgi");
                    flock(FILE, 2) if ($OS_USED eq "Unix");
                    print FILE "$memberfile\t$lastgone\t\n";
                    close(FILE);
                    $size1++;
                    if ($sendtoemail eq "") {$sendtoemail = "$emailaddr";}
                    else {$sendtoemail = "$sendtoemail, $emailaddr";}
                }
            }
            print MEMFILE "$membername\t$userad\t$anzahl\t$joineddate\t\n";
        }
        close(MEMFILE);

        if ($sendtoemail ne "" && $emailfunctions eq "on") {
            $from = "$adminemail_out";
            $subject = "来自$board_name的重要邮件！！";
            $message = "";
            $message .= "\n";
            $message .= "$board_name <br>\n";
            $message .= "$boardurl/leobbs.cgi <br>\n";
            $message .= "------------------------------------------\n<br><br>\n";
            $message .= "系统发现你已经长时间未访问本论坛并发言了， <br>\n";
            $message .= "为了释放空间，你的用户名将在３日后删除。 <br>\n";
            $message .= "如果你想保留你的用户名，请登录本论坛一次。 <br>\n";
            $message .= "------------------------------------------<br>\n";
            $message .= "LeoBBS 由 www.leobbs.com 荣誉出品。<br>\n";
            &sendmail($from, $from, $sendtoemail, $subject, $message);
        }

        if ($i < $size - 1) {
            $step++;
            print qq~<meta http-equiv="refresh" Content="0; url=$thisprog?action=delnopost&deltime=$indeltime&delposts=$indelposts&dellast=$indellast&delcdrom=$indelcdrom&delusetype=$delusetype&size1=$size1&step=$step&users=$users">
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#333333><br>　如果你的浏览器没有自动前进，请<a href=$thisprog?action=delnopost&deltime=$indeltime&delposts=$indelposts&dellast=$indellast&delcdrom=$indelcdrom&delusetype=$delusetype&size1=$size1&step=$step&users=$users>点击继续</a>
</td></tr>
~;
        }
        else {
            if ($size1 == 0) {
                $delwarn = "<BR><BR><font color=red><B>当前没有符合删除条件的注册会员！<B></font>";
            }
            elsif ($emailfunctions ne "on") {
                $delwarn = "<BR><BR><font color=red><B>邮件功能没有打开，所以用户无法接收预删除信息！<B></font>";
            }
            else {
                $delwarn = "";
            }

            unlink("${lbdir}data/delmember.cgi") if ($size1 eq 0);
            print qq~
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000>
<b>计算用户排名</b><p>
<font color=#333333>当前共有 $size 个注册用户，排名数据已经更新！</font><BR>
<font color=#333333>预删除 $size1 个注册用户，排名数据已经更新，３天后可以进入管理区进行真正删除！</font>
$delwarn
</td></tr>~;
        }
    }
} # end routine

sub delok {

    unless (($member_code eq "ad") && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
    }
    else {

        if ($checkaction eq "yes") {
            $step = $query->param('step');
            $step = 0 unless ($step);
            $users = $query->param('users');
            $users = 200 unless ($users);
            $delno = $query->param('delno');
            $delno = 0 unless ($delno);

            open(FILE, "${lbdir}data/delmember.cgi");
            @alldelname = <FILE>;
            close(FILE);
            $delsize = @alldelname;

            opendir(DIRS, "$lbdir");
            my @files = readdir(DIRS);
            closedir(DIRS);
            @files = grep (/^\w+?$/i, @files);
            my @recorddir = grep (/^record/i, @files);
            $recorddir = $recorddir[0];
            my @memfavdir = grep (/^memfav/i, @files);
            $memfavdir = $memfavdir[0];
            $from = "$adminemail_out";
            $subject = "来自$board_name的重要邮件！！";
            $message = "";
            $message .= "\n";
            $message .= "$board_name <br>\n";
            $message .= "$boardurl/leobbs.cgi <br>\n";
            $message .= "------------------------------------------\n<br><br>\n";
            $message .= "系统发现你已经长时间未访问本论坛并发言了， <br>\n";
            $message .= "为了释放空间，你的用户名已经被完全删除。 <br>\n";
            $message .= "您被释放的用户名为：membername。 <br>\n";
            $message .= "------------------------------------------<br>\n";
            $sendtoemail = "";

            if ($step * $users < $delsize) {
                for ($i = $step * $users; $i <= ($step + 1) * $users; $i++) {
                    last if ($i > $delsize);
                    ($memberfile, $deltime) = split(/\t/, $alldelname[$i]);

                    ($nametocheck, $no) = split(/\./, $memberfile);
                    my $namenumber = &getnamenumber($nametocheck);
                    &checkmemfile($nametocheck, $namenumber);
                    $usrname = "${lbdir}$memdir/$namenumber/$memberfile";
                    open(FILE, "$usrname");
                    $line = <FILE>;
                    close(FILE);
                    undef $joineddate;
                    undef $lastgone;
                    undef $anzahl;
                    undef $lastpostdate;
                    undef $userad;
                    undef $visitno;
                    undef $anzahl1;
                    undef $anzahl2;
                    undef $emailaddr;
                    undef $membername;

                    ($membername, $no, $no, $userad, $anzahl, $emailaddr, $no, $no, $no, $no, $no, $no, $no, $joineddate, $lastpostdate, $no, $timedifference, $no, $no, $no, $no, $no, $no, $no, $no, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $line);
                    $messageto = $message;
                    $messageto =~ s/membername/$membername/isg;
                    ($anzahl1, $anzahl2) = split(/\|/, $anzahl);
                    $anzahl = $anzahl1 + $anzahl2;
                    ($lastpost, $posturl, $posttopic) = split(/\%\%\%/, $lastpostdate);
                    $lastgone = $lastpost if ($lastpost > $lastgone);
                    $lastgone = $joineddate if ($joineddate > $lastgone);

                    $delbankno = 0;
                    $delbanksaves = 0;
                    if ($lastgone <= $deltime) {
                        $membername =~ s/ /\_/isg;
                        $membername =~ tr/A-Z/a-z/;
                        my $namenumber = &getnamenumber($membername);
                        &checkmemfile($membername, $namenumber);
                        unlink("${lbdir}$memdir/$namenumber/$membername.cgi");
                        unlink("${lbdir}$memdir/old/$membername.cgi");
                        unlink("${lbdir}$msgdir/in/${membername}_msg.cgi");
                        unlink("${lbdir}$msgdir/out/${membername}_out.cgi");
                        unlink("${lbdir}$msgdir/main/${membername}_mian.cgi");
                        unlink("${lbdir}$memfavdir/$membername.cgi");
                        unlink("${lbdir}$memfavdir/open/$membername.cgi");
                        unlink("${lbdir}$memfavdir/close/$membername.cgi");
                        unlink("${lbdir}memfriend/$membername.cgi");
                        unlink("${lbdir}$recorddir/post/$membername.cgi");
                        unlink("${lbdir}$recorddir/reply/$membername.cgi");
                        unlink("${lbdir}memblock/$membername.cgi");
                        unlink("${lbdir}cache/myinfo/$membername.cgi");
                        unlink("${lbdir}cache/meminfo/$membername.cgi");
                        unlink("${lbdir}cache/id/$membername.cgi");
                        unlink("${imagesdir}usravatars/$membername.gif");
                        unlink("${imagesdir}usravatars/$membername.png");
                        unlink("${imagesdir}usravatars/$membername.jpg");
                        unlink("${imagesdir}usravatars/$membername.swf");
                        unlink("${imagesdir}usravatars/$membername.bmp");
                        $memberfiletitletemp = unpack("H*", "$membername");
                        unlink("${imagesdir}usravatars/$memberfiletitletemp.gif");
                        unlink("${imagesdir}usravatars/$memberfiletitletemp.png");
                        unlink("${imagesdir}usravatars/$memberfiletitletemp.jpg");
                        unlink("${imagesdir}usravatars/$memberfiletitletemp.swf");
                        unlink("${imagesdir}usravatars/$memberfiletitletemp.bmp");
                        unlink("${lbdir}ebankdata/log/" . $membername . ".cgi");
                        my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $bankadd1, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
                        if ($mystatus) {
                            $delbankno++;
                            $delbanksaves += $mysaves;
                        }

                        $delno++;
                        if ($sendtoemail eq "") {$sendtoemail = $emailaddr;}
                        else {$sendtoemail = "$sendtoemail, $emailaddr";}
                    }
                    &updateallsave(-$delbankno, -$delbanksaves);
                }

                if (($emailfunctions eq "on") && ($sendtoemail ne "")) {
                    &sendmail($from, $from, $sendtoemail, $subject, $messageto);
                }
                $step++;
                print qq~<meta http-equiv="refresh" Content="0; url=$thisprog?action=delok&checkaction=yes&delno=$delno&step=$step&users=$users">
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#333333><br>　如果你的浏览器没有自动前进，请<a href=$thisprog?action=delok&checkaction=yes&delno=$delno&step=$step&users=$users>点击继续</a>
</td></tr>
			~;

            }
            else {

                require "$lbdir" . "data/boardstats.cgi";

                $filetomake = "$lbdir" . "data/boardstats.cgi";
                $totalmembers = $totalmembers - $delno;
                &winlock($filetomake) if ($OS_USED eq "Nt");
                open(FILE, ">$filetomake");
                flock(FILE, 2) if ($OS_USED eq "Unix");
                print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
                print FILE "\$totalmembers = \'$totalmembers\'\;\n";
                print FILE "\$totalthreads = \'$totalthreads\'\;\n";
                print FILE "\$totalposts = \'$totalposts\'\;\n";
                print FILE "\n1\;";
                close(FILE);
                &winunlock($filetomake) if ($OS_USED eq "Nt");

                # Delete the database for the member

                unlink("${lbdir}data/delmember.cgi");

                print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>$delno 个过期注册用户已经被完整删除<BR>
        用户库已经全部更新</b><br><Br><a href=foruminit.cgi?action=uptop>点这儿更新用户排名一次</a><br>
        </td></tr>
         ~;
            }
        }
        else {
            print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>警告！！</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>完全删除所有符合条件的预删除用户，点击下面的链接继续。<BR>
        在预删除期间访问过论坛的用户不会被删除<p>
        <p>
        >> <a href="$thisprog?action=delok&checkaction=yes">开始删除</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
        }
    }
} # end routine

sub viewletter {

    open(FILE, "$lbdir/data/lbmember1.cgi");
    my @membernames = <FILE>;
    close(FILE);
    undef @sortedfile;
    foreach (@membernames) {
        chomp $_;
        ($no, $names) = split(/\t/, $_);
        push(@sortedfile, $names);
    }

    @sortedfile = sort alphabetically(@sortedfile);

    foreach (@sortedfile) {
        if ($_ =~ /^[\w\-]/) {
            $fr = substr($_, 0, 1);
            $fr =~ tr/a-z/A-Z/;
        }
        else {
            $fr = substr($_, 0, 2);
        }
        push(@letters, $fr);
    }
    @sortedletters = sort (@letters);

    print qq~
    <tr>
    <td bgcolor=#EEEEEE colspan=2><center>
    <font color=#990000><b>查看所有以 "$inletter" 开头的用户</b><p>
	<form action="setmembers.cgi" method=POST>
        <input type=hidden name="action" value="edit">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="快速定位">
        </form>
</center>
    ~;

    print qq~
    </td>
    </tr>          
    <tr>
    <td bgcolor=#FFFFFF align=center colspan=2>
    &nbsp;
    </td>
    </tr>          
    ~;

    foreach (@sortedfile) {
        if ($_ =~ /^[\w\-]/) {
            $frr = substr($_, 0, 1);
            $frr =~ tr/a-z/A-Z/;
        }
        else {
            $frr = substr($_, 0, 2);
        }
        if ($inletter eq $frr) {
            $_ =~ s/\.cgi$//;
            $member = $_;
            &getmember("$member");
            &showmember;
        }
    }

} # end route

sub viewip {
    unless ($inletter eq "findsame") {
        $inletters = $inletter;
        $inletter = ($inletter !~ /\./) ? $inletter . "." : $inletter;
        $inletter =~ s/\./\\\./g;
    }
    %iplist = ();
    %sameiplist = ();
    @thatiplist = ();
    open(FILE, "$lbdir/data/lbmember4.cgi");
    my @ipfile = <FILE>;
    close(FILE);
    chomp @ipfile;
    foreach (@ipfile) {
        (my $membername, my $getip) = split(/\t/, $_);
        if ($inletter ne "findsame") {
            push(@thatiplist, $membername) if ($getip =~ /^$inletter/);
        }
        else {
            $sameiplist{$getip} = "" unless (defined($sameiplist{$getip}));
            $sameiplist{$getip} .= qq(<a href="$thisprog?action=edit&member=$membername">$membername</a>,);
        }
        ($getip, $getip2) = split(/, /, $getip);
        $getip = $getip2 if (($getip2 ne "") && ($getip2 ne "unknown"));
        $getip =~ s/\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$//;
        $iplist{$getip} = "$getip" unless (defined($iplist{$getip}));
    }
    @iplist = keys %iplist;
    @iplist = sort (@iplist);

    print qq~
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>寻找以特定ＩＰ注册的用户</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=left colspan=2>　　　　　　　　　　<b>说明:</b><br>
　　　　　　　　　　你如果要寻找一个 IP，可以直接输入 IP 地址在这里，比如： 202.100.200.100。<br>
　　　　　　　　　　如果你要寻找一个 C 类网，那么你可以不输入 IP 的最后一位，比如：202.100.200. <br>
　　　　　　　　　　如果你要寻找一个 B 类网，那么你可以不输入 IP 的最后两位，比如：202.100. <br>
　　　　　　　　　　注意上面的写法，如果寻找的是一个 C 类或者 B 类网，请最后保留点号(.)，切记！</td></tr>
    <tr>
    <form action="setmembers.cgi" method=POST><input type=hidden name="action" value="viewip"><td bgcolor=#EEEEEE align=center colspan=2><input type=text name="letter" size20 maxlength=16> <input type=submit value="寻找用户"></td></form></tr>
    <tr>
    <form action="setmembers.cgi" method=POST><input type=hidden name="action" value="viewip"><input type=hidden name="letter" value="findsame"><td bgcolor=#EEEEEE align=center colspan=2><input type=submit value="寻找所有相同ＩＰ的用户"></td></form></tr>
    <tr><td bgcolor=#FFFFFF align=center colspan=2 height="20"></td></tr>
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>注册ＩＰ大致列表</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=left colspan=2>　　　　　　　　　　~;

    $nowcount = 0;
    foreach (@iplist) {
        $ipshow = sprintf("% 3s", $_);
        $ipshow =~ s/\s/\&nbsp\;/g;
        print qq~<br>　　　　　　　　　　~ if ($nowcount == int($nowcount / 15) * 15);
        print qq~ <a href="$thisprog?action=viewip&letter=$_">$ipshow</a> ~;
        $nowcount++;
    }

    print qq~$tempoutput</td></tr>
    <tr><td bgcolor=#FFFFFF align=center colspan=2 height="20"></td></tr>~;
    if ($inletter ne "findsame") {
        print qq~
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>所有ＩＰ以 "$inletters" 开头的用户</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=center colspan=2 height="20"></td></tr>
    ~;
        foreach (@thatiplist) {
            $member = $_;
            &getmember("$member");
            &showmember;
        }
    }
    else {
        print qq~
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>所有相同ＩＰ的用户</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=left colspan=2>　　　　　　　　　　<b>注意:</b><br>
　　　　　　　　　　相同ＩＰ不一定代表是同一人。<br></td></tr>
    ~;
        while (($ip, $thisiplist) = each(%sameiplist)) {
            my @listofthisip = split(/\,/, $thisiplist);
            my $listofthisipc = @listofthisip;
            next if ($listofthisipc <= 1);
            $listofthisip = join(",", @listofthisip);
            print qq~
    <tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>ＩＰ为 "<font color=#990000>$ip</font>" 的用户</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF colspan=2 align=left>$listofthisip</td></tr>
    <tr><td bgcolor=#FFFFFF> </td><td bgcolor=#FFFFFF> </td></tr>
    ~;
        }
    }
}


##################################################################################
######## Subroutes (Show member) 


sub showmember {

    $joineddate = &longdate("$joineddate");

    $cleanmember = $member;
    $cleanmember =~ s/\_/ /g;

    ## Sort last post, and where

    ($postdate, $posturl, $posttopic) = split(/\%%%/, $lastpostdate);

    if ($postdate ne "没有发表过") {
        $postdate = &longdate("$postdate");
        $lastpostdetails = qq~最后发表 <a href="$posturl">$posttopic</a> 在 $postdate~;
    }
    else {
        $lastpostdetails = "没有发表过";
    }

    if ($member_code eq "banned") {
        $unbanlink = qq~ | [<a href="$thisprog?action=unban&member=~ . uri_escape($member) . qq~">取消禁止发言</a>]~;
    }
    $totlepostandreply = $numberofposts + $numberofreplys;
    print qq~
    <tr>
    <td bgcolor=#EEEEEE colspan=2 align=center><font face=$font color=$fontcolormisc><b><font color=$fonthighlight>"$cleanmember"</b> 的详细资料 　 [ <a href="$thisprog?action=edit&member=~ . uri_escape($member) . qq~">编辑</a> ] | [ <a href="$thisprog?action=deletemember&member=~ . uri_escape($member) . qq~">删除</a> ]$unbanlink</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF width=30%><font color=#333333><b>注册时间：</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF width=30%><font color=#333333><b>注册ＩＰ：</b></font></td>
    <td bgcolor=#FFFFFF><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$ipaddress',420,320)" title="LB WHOIS信息"><font color=#333333>$ipaddress</font></span> (<a href="$thisprog?action=viewip&letter=$ipaddress">找相同ＩＰ的用户</a>)</td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>用户头衔：</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$membertitle</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>最后发表：</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastpostdetails</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>发表总数：</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$totlepostandreply</font> 篇</td></tr>
    <tr>
    <td bgcolor=#FFFFFF>&nbsp;</td>
    <td bgcolor=#FFFFFF>&nbsp;</td></tr>
    
    ~;
    $unbanlink = "";
} # end routine


##################################################################################
######## Subroutes (Edit member) 


sub edit {
    $oldmembercode = $member_code;

    if ($checkaction eq "yes") {

        $innewpassword = $query->param('password');
        $innewpassword = &cleanarea("$innewpassword");
        $inrating = $query->param('rating');
        $inmembertitle = $query->param('membertitle');
        $inmembertitle = &cleanarea("$inmembertitle");
        $inemailaddress = $query->param('emailaddress');
        $inhomepage = $query->param('homepage');
        $inoicqnumber = $query->param('oicqnumber');
        $inicqnumber = $query->param('icqnumber');
        $inlocation = $query->param('location');
        $innumberofposts = $query->param('numberofposts');
        $innumberofreplys = $query->param('numberofreplys');
        $intimedifference = $query->param('timedifference');
        $inmembercode = $query->param('membercode');
        $inmembercode = &cleaninput("$inmembercode");
        $invisitno = $query->param('visitno');
        $injhmp = $query->param('jhmp');
        $injifen = $query->param('jifen');
        $inmymoney = $query->param('mymoney');
        $insex = $query->param('sex');
        $ineducation = $query->param('education');
        $inmarry = $query->param('marry');
        $inwork = $query->param('work');
        $inyear = $query->param('year');
        $inmonth = $query->param('month');
        $inday = $query->param('day');
        $inpostdel = $query->param('postdel');
        $newsignature = $query->param('newsignature');
        $notshowsignature = ($query->param('notshowsignature') eq "yes") ? "yes" : "no";
        $inuserflag = $query->param('userflag');
        $inusersx = $query->param('usersx');
        $inuserxz = $query->param('userxz');
        $injoineddate = $query->param('joineddate');
        $newsignature = &unHTML("$newsignature");
        $newsignature = &cleanarea("$newsignature");

        $inlocation = &cleaninput("$inlocation");
        $inonlinetime = $query->param('onlinetime');

        $inuseradd1 = $query->param('useradd1');
        $tinuseradd1 = $query->param('tuseradd1');
        $tinuseradd2 = $query->param('tuseradd2');
        $tinuseradd3 = $query->param('tuseradd3');
        $tinuseradd4 = $query->param('tuseradd4');
        $tinuseradd5 = $query->param('tuseradd5');
        $tinuseradd6 = $query->param('tuseradd6');

        $inawards = ("$tinuseradd1:$tinuseradd2:$tinuseradd3:$tinuseradd4:$tinuseradd5:$tinuseradd6");

        $inyear =~ s/\D//g;
        if (($inyear eq "") || ($inmonth eq "") || ($inday eq "")) {
            $inyear = "";
            $inmonth = "";
            $inday = "";
        }
        $inborn = "$inyear/$inmonth/$inday";

        if ($inborn ne "//") { #开始自动判断星座
            if ($inmonth eq "01") {
                if (($inday >= 1) && ($inday <= 19)) {
                    $inuserxz = "z10";
                }
                else {
                    $inuserxz = "z11";
                }
            }
            elsif ($inmonth eq "02") {
                if (($inday >= 1) && ($inday <= 18)) {
                    $inuserxz = "z11";
                }
                else {
                    $inuserxz = "z12";
                }
            }
            elsif ($inmonth eq "03") {
                if (($inday >= 1) && ($inday <= 20)) {
                    $inuserxz = "z12";
                }
                else {
                    $inuserxz = "z1";
                }

            }
            elsif ($inmonth eq "04") {
                if (($inday >= 1) && ($inday <= 19)) {
                    $inuserxz = "z1";
                }
                else {
                    $inuserxz = "z2";
                }
            }
            elsif ($inmonth eq "05") {
                if (($inday >= 1) && ($inday <= 20)) {
                    $inuserxz = "z2";
                }
                else {
                    $inuserxz = "z3";
                }
            }
            elsif ($inmonth eq "06") {
                if (($inday >= 1) && ($inday <= 21)) {
                    $inuserxz = "z3";
                }
                else {
                    $inuserxz = "z4";
                }
            }
            elsif ($inmonth eq "07") {
                if (($inday >= 1) && ($inday <= 22)) {
                    $inuserxz = "z4";
                }
                else {
                    $inuserxz = "z5";
                }
            }
            elsif ($inmonth eq "08") {
                if (($inday >= 1) && ($inday <= 22)) {
                    $inuserxz = "z5";
                }
                else {
                    $inuserxz = "z6";
                }
            }
            elsif ($inmonth eq "09") {
                if (($inday >= 1) && ($inday <= 22)) {
                    $inuserxz = "z6";
                }
                else {
                    $inuserxz = "z7";
                }
            }
            elsif ($inmonth eq "10") {
                if (($inday >= 1) && ($inday <= 23)) {
                    $inuserxz = "z7";
                }
                else {
                    $inuserxz = "z8";
                }
            }
            elsif ($inmonth eq "11") {
                if (($inday >= 1) && ($inday <= 21)) {
                    $inuserxz = "z8";
                }
                else {
                    $inuserxz = "z9";
                }
            }
            elsif ($inmonth eq "12") {
                if (($inday >= 1) && ($inday <= 21)) {
                    $inuserxz = "z9";
                }
                else {
                    $inuserxz = "z10";
                }
            }

        }

        $inmembertitle = "Member" if ($inmembertitle eq "");

        if (length($injhmp) > 21) {
            print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>江湖门派的输入请控制在20个字符（10个汉字）内。</b></font></td></tr>
        ~;
            print qq~</td></tr></table></body></html>~;
            exit;
        }
        if (length($inmembertitle) > 21) {
            print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>个人头衔的输入请控制在20个字符（10个汉字）内。</b></font></td></tr>
        ~;
            print qq~</td></tr></table></body></html>~;
            exit;
        }
        if (length($inlocation) > 12) {
            print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>来自的输入请控制在12个字符（6个汉字）内。</b></font></td></tr>
        ~;
            print qq~</td></tr></table></body></html>~;
            exit;
        }

        if ($injhmp eq "") {$jhmp = "无门无派";}
        else {$jhmp = ($jhmp);}
        if ($inrating eq "") {$inrating = 0;}
        elsif ($inrating > $maxweiwang) {$inrating = $maxweiwang;}
        elsif ($inrating < -6) {
            $inrating = -6;
            $inmembercode = "banned";
        }

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        open(FILE, "$filetoopen");
        @forums = <FILE>;
        close(FILE);

        foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $trash) = split(/\t/, $forum);
            $namekey = "allow" . "$forumid";
            $tocheck = $query->param("$namekey");
            if ($tocheck eq "yes") {
                $allowedforums2 .= "$forumid=$tocheck&";
            }
        }

        &getmember("$inmember");
        if ($innewpassword eq "") {$innewpassword = $password;}
        else {

            if ($innewpassword =~ /[^a-zA-Z0-9]/) {
                print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>密码只允许大小写字母和数字的组合！！</b></td></tr>";
                exit;
            }
            if ($innewpassword =~ /^lEO/) {
                print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>密码不允许是 lEO 开头，请更换！！</b></td></tr>";
                exit;
            }
            if (length($innewpassword) < 8) {
                print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>密码太短了，请更换！密码必须 8 位以上！</b></td></tr>";
                exit;
            }
            if ($innewpassword ne "") {
                eval {$innewpassword = md5_hex($innewpassword);};
                if ($@) {eval('use Digest::MD5 qw(md5_hex);$innewpassword = md5_hex($innewpassword);');}
                unless ($@) {$innewpassword = "lEO$innewpassword";}
            }
        }

        if ((($inmembercode eq "ad") || ($inmembercode eq "smo") || ($inmembercode eq "cmo") || ($inmembercode eq "amo") || ($inmembercode eq "mo")) && ($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>总斑竹无权提升任何人为坛主和斑竹！</b></td></tr>";
            exit;
        }

        $memberfiletitle = $inmember;
        $memberfiletitle =~ s/ /\_/isg;
        $memberfiletitle =~ tr/A-Z/a-z/;
        unlink("${lbdir}cache/meminfo/$memberfiletitle.pl");
        unlink("${lbdir}cache/myinfo/$memberfiletitle.pl");

        if ($inmembercode eq "banned") {
            $filetoopen = "$lbdir" . "data/banemaillist.cgi";
            open(FILE, ">>$filetoopen");
            print FILE "$inemailaddress\t";
            close(FILE);
            $filetoopen = "$lbdir" . "data/baniplist.cgi";
            open(FILE, ">>$filetoopen");
            print FILE "$ipaddress\t";
            close(FILE);
            $banresult = "禁止 $membername 发言成功";
        }
        if ($oldmembercode eq "smo") {
            $innumberofposts = $numberofposts;
            $innumberofreplys = $numberofreplys;
            $inpostdel = $postdel;
            $inmymoney = $mymoney;
            $invisitno = $visitno;
            $inawards = $awards;
        }
        if ($newsignature) {
            $newsignature =~ s/\t//g;
            $newsignature =~ s/\r//g;
            $newsignature =~ s/  / /g;
            $newsignature =~ s/\&amp;nbsp;/\&nbsp;/g;
            $newsignature =~ s/\n\n/\n\&nbsp;\n/isg;
            $newsignature =~ s/\n/\[br\]/isg;
            $newsignature =~ s/\[br\]\[br\]/\[br\]\&nbsp;\[br\]/isg;
        }
        require "dosignlbcode.pl";
        $signature1 = &signlbcode($newsignature);
        $newsignature = $newsignature . "aShDFSiod" . $signature1;
        $onlinetime = ($inonlinetime =~ /[^0-9]/) ? $onlinetime : $inonlinetime;
        my $namenumber = &getnamenumber($memberfiletitle);
        &checkmemfile($memberfiletitle, $namenumber);
        unless ((-e "${lbdir}$memdir/$namenumber/$memberfiletitle.cgi") || (-e "${lbdir}$memdir/old/$memberfiletitle.cgi")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>该用户不存在！</b></td></tr>";
            exit;
        }
        $filetomake = "$lbdir" . "$memdir/$namenumber/$memberfiletitle.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$innewpassword\t$inmembertitle\t$inmembercode\t$innumberofposts|$innumberofreplys\t$inemailaddress\t$showemail\t$ipaddress\t$inhomepage\t$inoicqnumber\t$inicqnumber\t$inlocation\t$interests\t$injoineddate\t$lastpostdate\t$newsignature\t$intimedifference\t$allowedforums2\t$useravatar\t$inuserflag\t$inuserxz\t$inusersx\t$personalavatar\t$personalwidth\t$personalheight\t$inrating\t$lastgone\t$invisitno\t$inuseradd04\t$inuseradd02\t$inmymoney\t$inpostdel\t$insex\t$ineducation\t$inmarry\t$inwork\t$inborn\t$chatlevel\t$chattime\t$injhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$inawards\t$injifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
        open(FILE, ">${lbdir}$memdir/old/$memberfiletitle.cgi");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$innewpassword\t$inmembertitle\t$inmembercode\t$innumberofposts|$innumberofreplys\t$inemailaddress\t$showemail\t$ipaddress\t$inhomepage\t$inoicqnumber\t$inicqnumber\t$inlocation\t$interests\t$injoineddate\t$lastpostdate\t$newsignature\t$intimedifference\t$allowedforums2\t$useravatar\t$inuserflag\t$inuserxz\t$inusersx\t$personalavatar\t$personalwidth\t$personalheight\t$inrating\t$lastgone\t$invisitno\t$inuseradd04\t$inuseradd02\t$inmymoney\t$inpostdel\t$insex\t$ineducation\t$inmarry\t$inwork\t$inborn\t$chatlevel\t$chattime\t$injhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$inawards\t$injifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        if ($oldmembercode ne "smo") {
            my $notshowsignaturefile = "$lbdir" . "data/notshowsignature.cgi";
            if (open(FILE, "$notshowsignaturefile")) {
                $notshowsignaturemember = <FILE>;
                close(FILE);
            }
            $notshowsignaturemember1 = $notshowsignaturemember;
            $notshowsignaturemember1 =~ s/^\t//;
            $notshowsignaturemember1 =~ s/\t$//;
            $notshowsignaturemember1 = "\t$notshowsignaturemember\t";
            if ($notshowsignature eq "yes") {
                if ($notshowsignaturemember1 !~ /\t$membername\t/) {
                    open(FILE, ">$notshowsignaturefile");
                    print FILE "$notshowsignaturemember$membername\t";
                    close(FILE);
                    $banresult .= "<br>屏蔽 $membername 签名成功";
                }
            }
            else {
                if ($notshowsignaturemember1 =~ /\t$membername\t/) {
                    $notshowsignaturemember =~ s/$membername\t//i;
                    open(FILE, ">$notshowsignaturefile");
                    print FILE "$notshowsignaturemember";
                    close(FILE);
                    $banresult .= "<br>开放 $membername 签名成功";
                }
            }
        }

        opendir(CATDIR, "${lbdir}cache");
        @dirdata = readdir(CATDIR);
        closedir(CATDIR);
        @dirdata1 = grep (/^forumstopic/, @dirdata);
        foreach (@dirdata1) {unlink("${lbdir}cache/$_");}

        print qq~
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>所有信息已经保存</b><br><br>$banresult<br>
                </td></tr>
                ~;

    }
    else {

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        open(FILE, "$filetoopen");
        @forums = <FILE>;
        close(FILE);

        foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc, $forum_pass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $forum);
            if ($privateforum eq "yes") {
                $grab = "$forumid\t$forumname";
                push(@newforums, $grab);
            }
        }
        $cleanmember = $inmember;
        $cleanmember =~ s/\_/ /g;

        &getmember("$inmember");
        $inmemberencode = uri_escape($inmember);
        $signature = $signatureorigin if ($signatureorigin);
        $signature = "" if (($signatureorigin eq "") && ($signaturehtml eq ""));
        $signature =~ s/\[br\]/\n/isg;
        $signature =~ s/<br>/\n/isg;
        $signature =~ s/<p>/\n/isg;
        $signature =~ s/</&lt;/g;
        $signature =~ s/>/&gt;/g;
        $signature =~ s/\&amp;/\&/isg;
        $signature =~ s/&quot\;/\"/g;
        $signature =~ s/\&nbsp;/ /isg;
        if ($privateforums) {
            @private = split(/&/, $privateforums);
            foreach $accessallowed (@private) {
                chomp $accessallowed;
                ($access, $value) = split(/=/, $accessallowed);
                $allowed_entry2{$access} = $value;
            }
        }

        @allowedforums = sort alphabetically(@newforums);
        foreach $line (@allowedforums) {
            ($forumid, $forumname) = split(/\t/, $line);
            if ($allowed_entry2{$forumid} eq "yes") {$checked = " checked";}
            else {$checked = "";}
            $privateoutput .= qq~<input type="checkbox" name="allow$forumid" value="yes" $checked>$forumname<br>\n~;
        }

        my $memteam1 = qq~<option value="rz1">$defrz1(认证用户)~ if ($defrz1 ne "");
        my $memteam2 = qq~<option value="rz2">$defrz2(认证用户)~ if ($defrz2 ne "");
        my $memteam3 = qq~<option value="rz3">$defrz3(认证用户)~ if ($defrz3 ne "");
        my $memteam4 = qq~<option value="rz4">$defrz4(认证用户)~ if ($defrz4 ne "");
        my $memteam5 = qq~<option value="rz5">$defrz5(认证用户)~ if ($defrz5 ne "");
        $memberstateoutput = qq~<select name="membercode"><option value="me">一般用户$memteam1$memteam2$memteam3$memteam4$memteam5<option value="rz">认证用户<option value="banned">禁止此用户发言<option value="masked">屏蔽此用户贴子<option value="mo">论坛版主<option value="amo">论坛副版主<option value="cmo">分类区版主<option value="smo">论坛总版主 *<option value="ad">坛主 **</select>~;

        $memberstateoutput =~ s/value=\"$member_code\"/value=\"$member_code\" selected/g;
        if ($userregistered eq "no") {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>无此用户！</b></td></tr>";
            exit;
        }

        if ((($member_code eq "ad") || ($member_code eq "smo") || ($member_code eq "cmo") || ($member_code eq "amo") || ($member_code eq "mo")) && ($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>总斑竹无权查看坛主和斑竹资料！</b></td></tr>";
            exit;
        }
        $userflag = "blank" if ($userflag eq "");
        $flaghtml = qq~
<script language="javascript">
function showflag(){document.images.userflags.src="$imagesurl/flags/"+document.creator.userflag.options[document.creator.userflag.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>所在国家:</b></td>
<td bgcolor=#ffffff>
<select name="userflag" size=1 onChange="showflag()">
<option value="blank">保密</option>
<option value="China">中国</option>
<option value="Angola">安哥拉</option>
<option value="Antigua">安提瓜</option>
<option value="Argentina">阿根廷</option>
<option value="Armenia">亚美尼亚</option>
<option value="Australia">澳大利亚</option>
<option value="Austria">奥地利</option>
<option value="Bahamas">巴哈马</option>
<option value="Bahrain">巴林</option>
<option value="Bangladesh">孟加拉</option>
<option value="Barbados">巴巴多斯</option>
<option value="Belgium">比利时</option>
<option value="Bermuda">百慕大</option>
<option value="Bolivia">玻利维亚</option>
<option value="Brazil">巴西</option>
<option value="Brunei">文莱</option>
<option value="Canada">加拿大</option>
<option value="Chile">智利</option>
<option value="Colombia">哥伦比亚</option>
<option value="Croatia">克罗地亚</option>
<option value="Cuba">古巴</option>
<option value="Cyprus">塞浦路斯</option>
<option value="Czech_Republic">捷克斯洛伐克</option>
<option value="Denmark">丹麦</option>
<option value="Dominican_Republic">多米尼加</option>
<option value="Ecuador">厄瓜多尔</option>
<option value="Egypt">埃及</option>
<option value="Estonia">爱沙尼亚</option>
<option value="Finland">芬兰</option>
<option value="France">法国</option>
<option value="Germany">德国</option>
<option value="Great_Britain">英国</option>
<option value="Greece">希腊</option>
<option value="Guatemala">危地马拉</option>
<option value="Honduras">洪都拉斯</option>
<option value="Hungary">匈牙利</option>
<option value="Iceland">冰岛</option>
<option value="India">印度</option>
<option value="Indonesia">印度尼西亚</option>
<option value="Iran">伊朗</option>
<option value="Iraq">伊拉克</option>
<option value="Ireland">爱尔兰</option>
<option value="Israel">以色列</option>
<option value="Italy">意大利</option>
<option value="Jamaica">牙买加</option>
<option value="Japan">日本</option>
<option value="Jordan">约旦</option>
<option value="Kazakstan">哈萨克</option>
<option value="Kenya">肯尼亚</option>
<option value="Kuwait">科威特</option>
<option value="Latvia">拉脱维亚</option>
<option value="Lebanon">黎巴嫩</option>
<option value="Lithuania">立陶宛</option>
<option value="Malaysia">马来西亚</option>
<option value="Malawi">马拉维</option>
<option value="Malta">马耳他</option>
<option value="Mauritius">毛里求斯</option>
<option value="Morocco">摩洛哥</option>
<option value="Mozambique">莫桑比克</option>
<option value="Netherlands">荷兰</option>
<option value="New_Zealand">新西兰</option>
<option value="Nicaragua">尼加拉瓜</option>
<option value="Nigeria">尼日利亚</option>
<option value="Norway">挪威</option>
<option value="Pakistan">巴基斯坦</option>
<option value="Panama">巴拿马</option>
<option value="Paraguay">巴拉圭</option>
<option value="Peru">秘鲁</option>
<option value="Poland">波兰</option>
<option value="Portugal">葡萄牙</option>
<option value="Romania">罗马尼亚</option>
<option value="Russia">俄国</option>
<option value="Saudi_Arabia">沙特阿拉伯</option>
<option value="Singapore">新加坡</option>
<option value="Slovakia">斯洛伐克</option>
<option value="Slovenia">斯洛文尼亚</option>
<option value="Solomon_Islands">所罗门</option>
<option value="Somalia">索马里</option>
<option value="South_Africa">南非</option>
<option value="South_Korea">韩国</option>
<option value="Spain">西班牙</option>
<option value="Sri_Lanka">印度</option>
<option value="Surinam">苏里南</option>
<option value="Sweden">瑞典</option>
<option value="Switzerland">瑞士</option>
<option value="Thailand">泰国</option>
<option value="Trinidad_Tobago">多巴哥</option>
<option value="Turkey">土耳其</option>
<option value="Ukraine">乌克兰</option>
<option value="United_Arab_Emirates">阿拉伯联合酋长国</option>
<option value="United_States">美国</option>
<option value="Uruguay">乌拉圭</option>
<option value="Venezuela">委内瑞拉</option>
<option value="Yugoslavia">南斯拉夫</option>
<option value="Zambia">赞比亚</option>
<option value="Zimbabwe">津巴布韦</option>
</select>
<img src="$imagesurl/flags/$userflag.gif" name="userflags" border=0 height=14 width=21>
</td></tr>
~;
        $flaghtml =~ s/value=\"$userflag\"/value=\"$userflag\" selected/;

        if ($userxz eq "") {$userxz = "blank"};
        $xzhtml = qq~
        <SCRIPT language=javascript>
        function showxz(){document.images.userxzs.src="$imagesurl/star/"+document.creator.userxz.options[document.creator.userxz.selectedIndex].value+".gif";}
        </SCRIPT>
	<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>所属星座：</b>请选择你所属的星座。<br>如果输入了生日的话，那么此项无效！</td>
	<td bgcolor=#ffffff>
        <SELECT name=\"userxz\" onchange=showxz() size=\"1\"> <OPTION value=blank>保密</OPTION> <OPTION value=\"z1\">白羊座(3月21--4月19日)</OPTION> <OPTION value=\"z2\">金牛座(4月20--5月20日)</OPTION> <OPTION value=\"z3\">双子座(5月21--6月21日)</OPTION> <OPTION value=\"z4\">巨蟹座(6月22--7月22日)</OPTION> <OPTION value=\"z5\">狮子座(7月23--8月22日)</OPTION> <OPTION value=\"z6\">处女座(8月23--9月22日)</OPTION> <OPTION value=\"z7\">天秤座(9月23--10月23日)</OPTION> <OPTION value=\"z8\">天蝎座(10月24--11月21日)</OPTION> <OPTION value=\"z9\">射手座(11月22--12月21日)</OPTION> <OPTION value=\"z10\">魔羯座(12月22--1月19日)</OPTION> <OPTION value=\"z11\">水瓶座(1月20--2月18日)</OPTION> <OPTION value=\"z12\">双鱼座(2月19--3月20日)</OPTION></SELECT> <IMG border=0 height=15 name=userxzs src=$imagesurl/star/$userxz.gif width=15 align=absmiddle>
        </TD></TR>
	~;
        $xzhtml =~ s/value=\"$userxz\"/value=\"$userxz\" selected/;

        if ($usersx eq "") {$usersx = "blank"};
        $sxhtml = qq~
        <SCRIPT language=javascript>
        function showsx(){document.images.usersxs.src="$imagesurl/sx/"+document.creator.usersx.options[document.creator.usersx.selectedIndex].value+".gif";}
        </SCRIPT>
	<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>所属生肖：</b>请选择你所属的生肖。</td>
	<td bgcolor=#ffffff>
        <SELECT name=\"usersx\" onchange=showsx() size=\"1\"> <OPTION value=blank>保密</OPTION> <OPTION value=\"sx1\">子鼠</OPTION> <OPTION value=\"sx2\">丑牛</OPTION> <OPTION value=\"sx3\">寅虎</OPTION> <OPTION value=\"sx4\">卯兔</OPTION> <OPTION value=\"sx5\">辰龙</OPTION> <OPTION value=\"sx6\">巳蛇</OPTION> <OPTION value=\"sx7\">午马</OPTION> <OPTION value=\"sx8\">未羊</OPTION> <OPTION value=\"sx9\">申猴</OPTION> <OPTION value=\"sx10\">酉鸡</OPTION> <OPTION value=\"sx11\">戌狗</OPTION> <OPTION value=\"sx12\">亥猪</OPTION></SELECT> <IMG border=0 name=usersxs src=$imagesurl/sx/$usersx.gif align=absmiddle>
        </TD></TR>
	~;
        $sxhtml =~ s/value=\"$usersx\"/value=\"$usersx\" selected/;
        if ($avatars eq "on") {
            if (($personalavatar) && ($personalwidth) && ($personalheight)) {
                #自定义头像存在
                $personalavatar =~ s/\$imagesurl/${imagesurl}/o;
                if (($personalavatar =~ /\.swf$/i) && ($flashavatar eq "yes")) {
                    $personalavatar = uri_escape($personalavatar);
                    $useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>　[ <a href="$thisprog?action=deleteavatar&member=$inmemberencode">删 除 头 像</a> ]);
                }
                else {
                    $personalavatar = uri_escape($personalavatar);
                    $useravatar = qq(<br>&nbsp; <img src=$personalavatar border=0 width=$personalwidth height=$personalheight>　[ <a href="$thisprog?action=deleteavatar&member=$inmemberencode">删 除 头 像</a> ]);
                }
            }
            elsif (($useravatar ne "noavatar") && ($useravatar)) {
                $useravatar = uri_escape($useravatar);
                $useravatar = qq(<br>&nbsp; <img src="$imagesurl/avatars/$useravatar.gif" border=0 $defaultwidth $defaultheight>);
            }
            else {$useravatar = "没有";}
        }
        $inmembert = $inmember;
        $inmembert =~ tr/A-Z/a-z/;
        $inbox = "${lbdir}$msgdir/in/$inmembert\_msg.cgi";
        open(FILE, "$inbox");
        @inboxmsg = <FILE>;
        close(FILE);
        $inboxmsg = @inboxmsg;
        $outbox = "${lbdir}$msgdir/out/$inmembert\_out.cgi";
        open(FILE, "$outbox");
        @outboxmsg = <FILE>;
        close(FILE);
        $outboxmsg = @outboxmsg;

        $signature =~ s/<br>/\n/g;
        if ($oldmembercode eq "ad") {
            my $notshowsignaturefile = "$lbdir" . "data/notshowsignature.cgi";
            if (open(FILE, "$notshowsignaturefile")) {
                $notshowsignaturemember = <FILE>;
                close(FILE);
            }
            $notshowsignaturemember =~ s/^\t//;
            $notshowsignaturemember =~ s/\t$//;
            $notshowsignaturemember = "\t$notshowsignaturemember\t";
            $nsscheck = ($notshowsignaturemember !~ /\t$inmember\t/i) ? "" : " checked";
            print qq~
    <form action="$thisprog" method=post name="creator">
    <input type=hidden name="action" value="edit">
    <input type=hidden name="checkaction" value="yes">
    <input type=hidden name="member" value="$inmember">
    <tr>
    <td bgcolor=#EEEEEE colspan=2><font color=#333333><b>要编辑的用户名称： </b>$membername</td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>用户头衔：</b><br>您可以自定义一个头衔，<br>默认 Member 表示无头衔</td>
    <td bgcolor=#FFFFFF><input type=text name="membertitle" value="$membertitle" maxlength=20></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>发表总数：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="numberofposts" value="$numberofposts"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>回复总数：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="numberofreplys" value="$numberofreplys"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>贴子被删除数：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="postdel" value="$postdel"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>密码(如不修改请留空)：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="password"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>邮件地址/MSN地址：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="emailaddress" value="$emailaddress"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>主页地址：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="homepage" value="$homepage"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>OICQ 号：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="oicqnumber" value="$oicqnumber"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ICQ 号：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="icqnumber" value="$icqnumber"></td>
    </tr>$flaghtml<tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>来自何方：</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="location" value="$location" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>江湖门派:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="jhmp" value="$jhmp" maxlength=20></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>个人威望:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="rating" value="$rating" maxlength=2> (-5 到 $maxweiwang 之间)</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>积分:</b></td>
    <td bgcolor=#FFFFFF><input type=text name="jifen" value="$jifen" maxlength=12 size=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>个人签名：</b></td>
    <td bgcolor=#FFFFFF><textarea name="newsignature" cols="60" rows="8">$signature</textarea><br><input type="checkbox" name="notshowsignature" value="yes" $nsscheck>屏蔽此用户签名？</td>
    </tr><tr>
	~;

            $tempoutput = "<select name=\"sex\" size=\"1\"><option value=\"no\">保密 </option><option value=\"m\">帅哥 </option><option value=\"f\">美女 </option></select>\n";
            $tempoutput =~ s/value=\"$sex\"/value=\"$sex\" selected/;

            print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>性别：</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

            $tempoutput = "<select name=\"education\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"小学\">小学 </option><option value=\"初中\">初中 </option><option value=\"高中\">高中</option><option value=\"中专\">中专</option><option value=\"大专\">大专</option><option value=\"本科\">本科</option><option value=\"硕士\">硕士</option><option value=\"博士\">博士</option><option value=\"博士后\">博士后</option></select>\n";
            $tempoutput =~ s/value=\"$education\"/value=\"$education\" selected/;

            print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>最高学历：</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

            $tempoutput = "<select name=\"marry\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"未婚\">未婚 </option><option value=\"已婚\">已婚 </option><option value=\"离婚\">离婚 </option><option value=\"丧偶\">丧偶 </option></select>\n";
            $tempoutput =~ s/value=\"$marry\"/value=\"$marry\" selected/;

            print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>婚姻状况：</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

            $tempoutput = "<select name=\"work\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"计算机业\">计算机业 </option><option value=\"金融业\">金融业 </option><option value=\"商业\">商业 </option><option value=\"服务行业\">服务行业 </option><option value=\"教育业\">教育业 </option><option value=\"学生\">学生 </option><option value=\"工程师\">工程师 </option><option value=\"主管，经理\">主管，经理 </option><option value=\"政府部门\">政府部门 </option><option value=\"制造业\">制造业 </option><option value=\"销售/广告/市场\">销售/广告/市场 </option><option value=\"失业中\">失业中 </option></select>\n";
            $tempoutput =~ s/value=\"$work\"/value=\"$work\" selected/;

            print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>职业状况：</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;
            ($year, $month, $day) = split(/\//, $born);
            $tempoutput1 = "<select name=\"month\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option></select>\n";
            $tempoutput1 =~ s/value=\"$month\"/value=\"$month\" selected/;

            $tempoutput2 = "<select name=\"day\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option><option value=\"13\">13</option><option value=\"14\">14</option><option value=\"15\">15</option><option value=\"16\">16</option><option value=\"17\">17</option><option value=\"18\">18</option><option value=\"19\">19</option><option value=\"20\">20</option><option value=\"21\">21</option><option value=\"22\">22</option><option value=\"23\">23</option><option value=\"24\">24</option><option value=\"25\">25</option><option value=\"26\">26</option><option value=\"27\">27</option><option value=\"28\">28</option><option value=\"29\">29</option><option value=\"30\">30</option><option value=\"31\">31</option></select>\n";
            $tempoutput2 =~ s/value=\"$day\"/value=\"$day\" selected/;

            print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>生日：</b>如不想填写，请全部留空。</td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><input type="text" name="year" size=4 maxlength=4 value="$year">年$tempoutput1月$tempoutput2日</font></td>
	</tr>$xzhtml
        </tr>$sxhtml
	~;
            if (open(FILE2, "${lbdir}data/cityawards.cgi")) {
                @tempawards = <FILE2>;
                close(FILE2);
                foreach $tempaward (@tempawards) {
                    chomp $tempaward;
                    next if ($tempaward eq "");
                    ($tempawardname, $tempawardurl, $tempawardinfo, $tempawardorder, $tempawardpic) = split(/\t/, $tempaward);
                    $awardselect1 .= qq~<option value="$tempawardname">$tempawardname~;
                    $awardselect2 .= qq~<option value="$tempawardname">$tempawardname~;
                    $awardselect3 .= qq~<option value="$tempawardname">$tempawardname~;
                    $awardselect4 .= qq~<option value="$tempawardname">$tempawardname~;
                    $awardselect5 .= qq~<option value="$tempawardname">$tempawardname~;
                    $awardselect6 .= qq~<option value="$tempawardname">$tempawardname~;
                }
                ($tuseradd1, $tuseradd2, $tuseradd3, $tuseradd4, $tuseradd5, $tuseradd6) = split(/:/, $awards);
                $awardselect1 =~ s/value=\"$tuseradd1\"/value=\"$tuseradd1\" selected/;
                $awardselect2 =~ s/value=\"$tuseradd2\"/value=\"$tuseradd2\" selected/;
                $awardselect3 =~ s/value=\"$tuseradd3\"/value=\"$tuseradd3\" selected/;
                $awardselect4 =~ s/value=\"$tuseradd4\"/value=\"$tuseradd4\" selected/;
                $awardselect5 =~ s/value=\"$tuseradd5\"/value=\"$tuseradd5\" selected/;
                $awardselect6 =~ s/value=\"$tuseradd6\"/value=\"$tuseradd6\" selected/;
            }
            undef @tempawards;
            print qq~
   <td bgcolor=#FFFFFF><font color=#333333><b>论坛勋章：</b></td>
   <td bgcolor=#FFFFFF>勋章一：
   <select name="tuseradd1">
   <option value="">没有勋章
   $awardselect1
   </select> 勋章二：
   <select name="tuseradd2">
   <option value="">没有勋章
   $awardselect2
   </select><br>勋章三：
   <select name="tuseradd3">
   <option value="">没有勋章
   $awardselect3
   </select> 勋章四：
   <select name="tuseradd4">
   <option value="">没有勋章
   $awardselect4
   </select><br>勋章五：
   <select name="tuseradd5">
   <option value="">没有勋章
   $awardselect5
   </select> 勋章六：
   <select name="tuseradd6">
   <option value="">没有勋章
   $awardselect6
    </select></td>
   </tr><tr>
   ~;
            $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

            print qq~
    <td bgcolor=#FFFFFF><font color=#333333><b>额外金钱：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="mymoney" value="$mymoney" maxlength=12 size=12> 目前现金：$mymoney1 $moneyname</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>访问次数：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="visitno" value="$visitno" maxlength=7 size=7></td>
    </tr><tr>
    ~;
            $timedifference = 0 if ($timedifference eq '');
            $tempoutput = "<select name=\"timedifference\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\">0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
            $tempoutput =~ s/value=\"$timedifference\"/value=\"$timedifference\" selected/;
            $joineddate = $lastgone if ($joineddate eq "");
            $joineddate1 = $joineddate;
            $joineddate = &dateformat($joineddate);
            if ($lastgone ne "") {$lastgone = &dateformat($lastgone);}
            else {$lastgone = $joineddate;}
            print qq~
    <td bgcolor=#FFFFFF><font color=#333333><b>时差：</b></td>
    <td bgcolor=#FFFFFF>$tempoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF colspan=2><font color=#333333><b>私有论坛访问权限：</b><br>
    $privateoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>用户类型：</b><br>注意：坛主为论坛管理员，有绝对高的权限。<br>所以务必少添加此类型的用户。<br>总版主在任何论坛都具有版主权限，<br>在管理中心只有一定权限。</td>
    <td bgcolor=#FFFFFF>$memberstateoutput</td>
    </tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>注册时间：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>注册时的 IP 地址：</b></td>
    <td bgcolor=#FFFFFF><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$ipaddress',420,320)" title="LB WHOIS信息"><font color=#333333>$ipaddress</font></span> (<a href="$thisprog?action=viewip&letter=$ipaddress">找相同ＩＰ的用户</a>)</td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>最后访问时间：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastgone</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>在线时间：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333><input type=text size=12 name="onlinetime" value="$onlinetime" maxlength=12> 秒</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>用户头像：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$useravatar</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>用户短讯息：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>
      收件箱共 $inboxmsg 条　[ <a href="$thisprog?action=boxaction&box=inbox&checkaction=delete&member=$inmemberencode">删除收件箱</a> ]　[ <a href="$thisprog?action=boxaction&box=inbox&checkaction=viewbox&member=$inmemberencode">检视收件箱</a> ]<br>
      发件箱共 $outboxmsg 条　[ <a href="$thisprog?action=boxaction&box=outbox&checkaction=delete&member=$inmemberencode">删除发件箱</a> ]　[ <a href="$thisprog?action=boxaction&box=outbox&checkaction=viewbox&member=$inmemberencode">检视发件箱</a> ]</font></td></tr>

    <input type=hidden name="joineddate" value="$joineddate1">
    <tr>
    <td colspan=2 bgcolor=#FFFFFF align=center>[ <a href="$thisprog?action=deletemember&member=$inmemberencode">删 除 此 用 户</a> ]</td>
    </tr>
    <tr>
    <td colspan=2 bgcolor=#EEEEEE align=center><input type=submit value="提 交" name=submit></form></td>
    </tr>
    ~;
        }
        else {
            my $memteam1 = qq~<option value="rz1">$defrz1(认证用户)~ if ($defrz1 ne "");
            my $memteam2 = qq~<option value="rz2">$defrz2(认证用户)~ if ($defrz2 ne "");
            my $memteam3 = qq~<option value="rz3">$defrz3(认证用户)~ if ($defrz3 ne "");
            my $memteam4 = qq~<option value="rz4">$defrz4(认证用户)~ if ($defrz4 ne "");
            my $memteam5 = qq~<option value="rz5">$defrz5(认证用户)~ if ($defrz5 ne "");
            $memberstateoutput = qq~<select name="membercode"><option value="me">一般用户$memteam1$memteam2$memteam3$memteam4$memteam5<option value="rz">认证用户<option value="banned">禁止此用户发言<option value="masked">屏蔽此用户贴子</select>~;
            $memberstateoutput =~ s/value=\"$member_code\"/value=\"$member_code\" selected/g;
            ($year, $month, $day) = split(/\//, $born);
            if ($lastgone ne "") {$lastgone = &dateformat($lastgone);}
            else {$lastgone = $joineddate;}
            $joineddate = $lastgone if ($joineddate eq "");
            $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
            print qq~
    <form action="$thisprog" method=post>
    <input type=hidden name="action" value="edit">
    <input type=hidden name="checkaction" value="yes">
    <input type=hidden name="member" value="$inmember">
    <input type=hidden name="numberofposts" value="$numberofposts">
    <input type=hidden name="numberofreplys" value="$numberofreplys">
    <input type=hidden name="postdel" value="$postdel">
    <input type=hidden name="emailaddress" value="$emailaddress">
    <input type=hidden name="homepage" value="$homepage">
    <input type=hidden name="oicqnumber" value="$oicqnumber">
    <input type=hidden name="icqnumber" value="$icqnumber">
    <input type=hidden name="location" value="$location">
    <input type=hidden name="sex" value="$sex">
    <input type=hidden name="education" value="$education">
    <input type=hidden name="marry" value="$marry">
    <input type=hidden name="work" value="$work">
    <input type=hidden name="month" value="$month">
    <input type=hidden name="day" value="$day">
    <input type=hidden name="year" value="$year">
    <input type=hidden name="visitno" value="$visitno">
    <input type=hidden name="mymoney" value="$mymoney">
    <input type=hidden name="joineddate" value="$joineddate">
    <input type=hidden name="userflag" value="$userflag">
    <input type=hidden name="usersx" value="$usersx">
    <input type=hidden name="userxz" value="$userxz">
    <input type=hidden name="timedifference" value="$timedifference">
    <input type=hidden name="jifen" value="$jifen">

    <tr>
    <td bgcolor=#EEEEEE colspan=2><font color=#333333><b>要编辑的用户名称： </b>$membername</td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>用户头衔：</b><br>您可以自定义一个头衔，<br>默认 Member 表示无头衔</td>
    <td bgcolor=#FFFFFF><input type=text name="membertitle" value="$membertitle" maxlength=20></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>密码(如不修改请留空)：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="password"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>江湖门派:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="jhmp" value="$jhmp" maxlength=20></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>个人威望:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="rating" value="$rating" maxlength=2> (-5 到 $maxweiwang 之间)</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>个人签名：</b></td>
    <td bgcolor=#FFFFFF><textarea name="newsignature" cols="60" rows="8">$signature</textarea></td>
    </tr><tr>
    ~;
            $joineddate = &dateformat($joineddate);
            print qq~
    <td bgcolor=#FFFFFF colspan=2><font color=#333333><b>私有论坛访问权限：</b><br>
    $privateoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>用户类型：</b></td>
    <td bgcolor=#FFFFFF>$memberstateoutput</td>
    </tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>注册时间：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>注册时的 IP 地址：</b></td>
    <td bgcolor=#FFFFFF><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$ipaddress',420,320)" title="LB WHOIS信息"><font color=#333333>$ipaddress</font></span> (<a href="$thisprog?action=viewip&letter=$ipaddress">找相同ＩＰ的用户</a>)</td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>最后访问时间：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastgone</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>在线时间：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333><input type=text size=10 name="onlinetime" value="$onlinetime" maxlength=10> 秒</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>用户头像：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$useravatar</font></td></tr>
    <tr>
    <td colspan=2 bgcolor=#FFFFFF align=center>[ <a href="$thisprog?action=deletemember&member=$inmemberencode">删 除 此 用 户</a> ]</td>
    </tr>

    <tr>
    <td colspan=2 bgcolor=#EEEEEE align=center><input type=submit value="提 交" name=submit></form></td>
    </tr>
    ~;

        }
    } # end else

} # endroute


############### delete member

sub deletemember {

    $oldmembercode = $member_code;
    &getmember("$inmember");
    my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $bankadd1, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);

    if ((($member_code eq "ad") || ($member_code eq "smo") || ($member_code eq "cmo") || ($member_code eq "amo") || ($member_code eq "mo")) && ($oldmembercode eq "smo")) {
        print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>总斑竹无权删除坛主和斑竹资料！</b></td></tr>";
        exit;
    }
    if ($in_member_name eq $inmember) {
        print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>自己不能删除自己的资料哟！</b></td></tr>";
        exit;
    }

    if ($checkaction eq "yes") {
        ####################################################
        # Check to see if they were the last member to register

        require "$lbdir" . "data/boardstats.cgi";

        if ($inmember eq "$lastregisteredmember") {
            #start

            $dirtoopen = "$lbdir" . "$memdir";
            opendir(DIR, "$dirtoopen");
            @filedata = readdir(DIR);
            closedir(DIR);
            @inmembers = grep (/cgi$/i, @filedata);

            local ($highest) = 0;

            foreach (@inmembers) {
                $_ =~ s/\.cgi$//g;
                &getmember("$_");
                if (($joineddate > $highest) && ($inmember ne $membername)) {
                    $highest = $joineddate;
                    $memberkeep = $membername;
                }
            }

            $filetomake = "$lbdir" . "data/boardstats.cgi";
            $totalmembers--;
            &winlock($filetomake) if ($OS_USED eq "Nt");
            open(FILE, ">$filetomake");
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE "\$lastregisteredmember = \'$memberkeep\'\;\n";
            print FILE "\$totalmembers = \'$totalmembers\'\;\n";
            print FILE "\$totalthreads = \'$totalthreads\'\;\n";
            print FILE "\$totalposts = \'$totalposts\'\;\n";
            print FILE "\n1\;";
            close(FILE);
            &winunlock($filetomake) if ($OS_USED eq "Nt");
        } # end if new/delete member

        else {
            require "$lbdir" . "data/boardstats.cgi";

            $filetomake = "$lbdir" . "data/boardstats.cgi";
            $totalmembers--;
            &winlock($filetomake) if ($OS_USED eq "Nt");
            open(FILE, ">$filetomake");
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
            print FILE "\$totalmembers = \'$totalmembers\'\;\n";
            print FILE "\$totalthreads = \'$totalthreads\'\;\n";
            print FILE "\$totalposts = \'$totalposts\'\;\n";
            print FILE "\n1\;";
            close(FILE);
            &winunlock($filetomake) if ($OS_USED eq "Nt");
        } # end if else

        opendir(DIRS, "$lbdir");
        my @files = readdir(DIRS);
        closedir(DIRS);
        @files = grep (/^\w+?$/i, @files);
        my @recorddir = grep (/^record/i, @files);
        $recorddir = $recorddir[0];
        my @memfavdir = grep (/^memfav/i, @files);
        $memfavdir = $memfavdir[0];
        my @searchdir = grep (/^search/i, @files);
        $searchdir = $searchdir[0];

        &getmember("$inmember", "no");

        $in_member_name = $inmember;
        $in_member_name =~ s/ /\_/isg;
        $in_member_name =~ tr/A-Z/a-z/;

        # Delete the database for the member
        my $namenumber = &getnamenumber($in_member_name);
        &checkmemfile($in_member_name, $namenumber);
        unlink("${lbdir}$searchdir/$in_member_name\_sch.cgi");
        unlink("${lbdir}$searchdir/$in_member_name\_sav.cgi");
        unlink("${lbdir}$memdir/$namenumber/$in_member_name.cgi");
        unlink("${lbdir}$memdir/old/$in_member_name.cgi");
        unlink("${lbdir}$msgdir/in/${inmembername}_msg.cgi");
        unlink("${lbdir}$msgdir/out/${inmembername}_out.cgi");
        unlink("${lbdir}$msgdir/main/${inmembername}_mian.cgi");
        unlink("${lbdir}$memfavdir/$in_member_name.cgi");
        unlink("${lbdir}$memfavdir/open/$in_member_name.cgi");
        unlink("${lbdir}$memfavdir/close/$in_member_name.cgi");
        unlink("${lbdir}memfriend/$in_member_name.cgi");
        unlink("${lbdir}$recorddir/post/$in_member_name.cgi");
        unlink("${lbdir}$recorddir/reply/$in_member_name.cgi");
        unlink("${lbdir}memblock/$in_member_name.cgi");
        unlink("${imagesdir}usravatars/$in_member_name.gif");
        unlink("${imagesdir}usravatars/$in_member_name.png");
        unlink("${imagesdir}usravatars/$in_member_name.jpg");
        unlink("${imagesdir}usravatars/$in_member_name.swf");
        unlink("${imagesdir}usravatars/$in_member_name.bmp");
        unlink("${lbdir}ebankdata/log/" . $in_member_name . ".cgi");
        unlink("${lbdir}cache/meminfo/$in_member_name.pl");
        unlink("${lbdir}cache/myinfo/$in_member_name.pl");
        unlink("${lbdir}cache/id/$in_member_name.pl");
        $memberfiletitletemp = unpack("H*", "$in_member_name");
        unlink("${imagesdir}usravatars/$memberfiletitletemp.gif");
        unlink("${imagesdir}usravatars/$memberfiletitletemp.png");
        unlink("${imagesdir}usravatars/$memberfiletitletemp.jpg");
        unlink("${imagesdir}usravatars/$memberfiletitletemp.swf");
        unlink("${imagesdir}usravatars/$memberfiletitletemp.bmp");

        &updateallsave(-1, -$mysaves) if ($mystatus);

        my $charone = substr($emailaddress, 0, 1);
        $charone = lc($charone);
        $charone = ord($charone);

        $/ = "";
        open(MEMFILE, "${lbdir}data/lbemail/$charone.cgi");
        my $allmemberemails = <MEMFILE>;
        close(MEMFILE);
        $/ = "\n";
        $allmemberemails =~ s/$emailaddress\t.+?\n//isg;
        if (open(MEMFILE, ">${lbdir}data/lbemail/$charone.cgi")) {
            print MEMFILE "$allmemberemails";
            close(MEMFILE);
        }

        $filetoopen = "$lbdir" . "data/banemaillist.cgi";
        open(FILE, "$filetoopen");
        $emaildata = <FILE>;
        close(FILE);
        @emaildata = split(/\t/, $emaildata);
        open(FILE, ">$filetoopen");
        foreach (@emaildata) {
            chomp $_;
            print FILE "$_\t" if ($emailaddress ne $_);
        }
        close(FILE);

        $filetoopen = "$lbdir" . "data/baniplist.cgi";
        open(FILE, "$filetoopen");
        $ipdata = <FILE>;
        close(FILE);
        @ipdata = split(/\t/, $ipdata);
        open(FILE, ">$filetoopen");
        foreach (@ipdata) {
            chomp $_;
            print FILE "$_\t" if ($ipaddress ne $_);
        }
        close(FILE);

        open(FILE, "${lbdir}data/lbmember.cgi");
        @members = <FILE>;
        close(FILE);
        open(FILE, ">${lbdir}data/lbmember.cgi");
        foreach (@members) {
            chomp $_;
            my ($usernamerbak, $no) = split(/\t/, $_);
            print FILE "$_\n" if ($usernamerbak ne $inmember);
        }
        close(FILE);
        open(FILE, "${lbdir}data/lbmember3.cgi");
        @members = <FILE>;
        close(FILE);
        open(FILE, ">${lbdir}data/lbmember3.cgi");
        foreach (@members) {
            chomp $_;
            my ($usernamerbak, $no) = split(/\t/, $_);
            print FILE "$_\n" if ($usernamerbak ne $inmember);
        }
        close(FILE);
        open(FILE, "${lbdir}data/lbmember4.cgi");
        @members = <FILE>;
        close(FILE);
        open(FILE, ">${lbdir}data/lbmember4.cgi");
        foreach (@members) {
            chomp $_;
            my ($usernamerbak, $no) = split(/\t/, $_);
            print FILE "$_\n" if ($usernamerbak ne $inmember);
        }
        close(FILE);

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>用户已经从数据库中完全删除了</b>
        </td></tr>
         ~;

    } # end checkaction else

    else {

        $cleanedmember = $inmember;
        $cleanedmember =~ s/\_/ /g;
        $inmember = uri_escape($inmember);

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>警告！！</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>只有点击下面的链接才可以删除用户<b>"$cleanedmember"</b><p>
        >> <a href="$thisprog?action=deletemember&checkaction=yes&member=$inmember">删除用户</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
    }

} # end routine

sub unban {

    &getmember("$inmember");

    if ($member_code ne "banned") {
        print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>$inmember 没有被禁止发言啊！</b></td></tr>";
        exit;
    }

    $memberfiletitle = $inmember;
    $memberfiletitle =~ s/ /\_/isg;
    $memberfiletitle =~ tr/A-Z/a-z/;
    unlink("${lbdir}cache/meminfo/$memberfiletitle.pl");

    # Remove from ban lists

    $filetoopen = "$lbdir" . "data/banemaillist.cgi";
    open(FILE, "$filetoopen");
    $emaildata = <FILE>;
    close(FILE);
    @emaildata = split(/\t/, $emaildata);
    open(FILE, ">$filetoopen");
    foreach (@emaildata) {
        chomp $_;
        print FILE "$_\t" if ($emailaddress ne $_);
    }
    close(FILE);

    $filetoopen = "$lbdir" . "data/baniplist.cgi";
    open(FILE, "$filetoopen");
    $ipdata = <FILE>;
    close(FILE);
    @ipdata = split(/\t/, $ipdata);
    open(FILE, ">$filetoopen");
    foreach (@ipdata) {
        chomp $_;
        print FILE "$_\t" if ($ipaddress ne $_);
    }
    close(FILE);

    my $namenumber = &getnamenumber($memberfiletitle);
    &checkmemfile($memberfiletitle, $namenumber);
    $filetomake = "$lbdir" . "$memdir/$memberfiletitle.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    open(FILE, ">$filetomake");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "$membername\t$password\t$membertitle\tme\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$allowedforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
    close(FILE);
    &winunlock($filetomake) if ($OS_USED eq "Nt");

    print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>$membername 已经取消禁止发言</b>
        </td></tr>
        ~;

} # end route

sub viewdelmembers {
    unless ((($member_code eq "ad") || ($member_code eq "smo")) && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {
        print qq~
<tr> 
<td bgcolor=#FFFFFF align=center colspan=2> 
<font color=#990000> 
<b>错误</b><p> 
<font color=#333333>你没有权限使用这个功能！</font> 
</td> 
</tr> 
~;
        exit;
    }
    print qq~
<tr> 
<td bgcolor=#FFFFFF colspan=2><br> 
~;

    $filetoopen = "$lbdir" . "data/delmember.cgi";
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @memberfiles = <FILE>;
    close(FILE);
    $i = -1;
    print qq~
<table width=100% border=0> 
<tr>~;
    foreach $memtypedata (@memberfiles) {
        if ($i > -1) {
            chomp $memtypedata;
            ($username, $membertype) = split(/\t/, $memtypedata);
            $username =~ s/.cgi//isg;
            &getmember("$username");
            $membername = $username if ($membername eq "");
            print qq~
<td width=10%><a href="setmembers.cgi?action=undelmember&undelname=$membername" title="将会员 $membername 从预删除中取消">$membername</a></td>~; ### 這行昨天弄錯已修改 , 之前有修改過的人請更新一下 
        }
        $i++;
        if ($i / 5 eq int($i / 5)) {print qq~</tr><tr>~;
        }
    }
    print qq~</table>
<br><br> 
<b><center>共有 $i 名会员符合预删除资格</center></b><br> 
</td></tr> 
~;
}

sub undelmember {
    unless ((($member_code eq "ad") || ($member_code eq "smo")) && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {
        print qq~
<tr> 
<td bgcolor=#FFFFFF align=center colspan=2> 
<font color=#990000> 
<b>错误</b><p> 
<font color=#333333>你没有权限使用这个功能！</font> 
</td> 
</tr> 
~;
        exit;
    }
    print qq~
<tr> 
<td bgcolor=#FFFFFF colspan=2><br> 
~;
    $filetoopen = "$lbdir" . "data/delmember.cgi";
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @memberfiles = <FILE>;
    close(FILE);
    $pretime = $memberfiles[0];
    $i = 0;
    open(FILE, ">${lbdir}data/delmember.cgi");
    print FILE "$pretime";
    close(FILE);
    foreach $memtypedata (@memberfiles) {
        if ($i > "0") {
            chomp $memtypedata;
            ($username, $membertype) = split(/\t/, $memtypedata);
            $username =~ s/.cgi//isg;
            &getmember("$username");
            if ($undelname ne $membername) {
                open(FILE, ">>${lbdir}data/delmember.cgi");
                flock(FILE, 1) if ($OS_USED eq "Unix");
                print FILE "$username\t$membertype\t\n";
                close(FILE);
            }
        }
        $i++;
    }
    close(FILE);
    print qq~</table>
<br><br> 
<b><center>会员 $undelname 已从预删除名单中取消</center></b><br> 
</td></tr> 
~;
}

sub boxaction {

    $oldmembercode = $member_code;
    &getmember("$inmember");
    if ((($member_code eq "ad") || ($member_code eq "smo") || ($member_code eq "cmo") || ($member_code eq "amo") || ($member_code eq "mo")) && ($oldmembercode eq "smo")) {
        print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>总斑竹无权查看坛主和斑竹资料！</b></td></tr>";
        exit;
    }
    $inmembert = $inmember;
    $inmembert =~ tr/A-Z/a-z/;
    if ($box eq "inbox") {
        $filepath = "${lbdir}$msgdir/in/$inmembert\_msg.cgi";
        $boxname = "收件箱";
    }
    else {
        $filepath = "${lbdir}$msgdir/out/$inmembert\_out.cgi";
        $boxname = "发件箱";
    }
    if ($checkaction eq "delete") {
        unlink $filepath;
        print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>用户$boxname已经删除了</b>
    </td></tr>
    ~;
    }
    else {
        open(FILE, "$filepath");
        my @messanges = <FILE>;
        close(FILE);
        print qq~
<script>function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
</script>
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>用户$boxname的讯息</b></td></tr>
    <tr>
    <form name="form2"><td bgcolor=#FFFFFF align=center colspan=2>
    <TEXTAREA name=inpost rows=12 style="width:90%">~;
        $current_time = localtime;
        foreach (@messanges) {
            $messangeswords = $_;
            ($usrname, $msgread, $msgtime, $msgtitle, $msgwords) = split(/\t/, $_);
            $usrname =~ s/^＊＃！＆＊//isg;
            $usrname =~ s/ /\_/g;
            $usrname =~ tr/A-Z/a-z/;
            $msgwords =~ s/\r//ig;
            $msgwords =~ s/ / /g;
            $msgwords =~ s/"/\&quot;/g;
            $msgwords =~ s/\s+/ /g;
            $msgwords =~ s/<br>/\n/g;
            $msgwords =~ s/<p>/\n/g;
            $msgtime = $msgtime + ($timedifferencevalue * 3600) + ($timezone * 3600);
            $msgtime = &dateformat("$msgtime");
            print qq~[收发对象]：$usrname\n[收发时间]：$msgtime\n[短信标题]：$msgtitle\n[短信内容]：$msgwords\n\n~;
        }
        print qq~</TEXTAREA><br>>> <a href="javascript:HighlightAll('form2.inpost')">复制到剪贴板 <<</a></td></form></tr>~;
    }

}

sub updateallsave #利用变化量来更新总量信息
{
    my ($callusers, $callsaves) = @_;

    my $filetoopen = $lbdir . "ebankdata/allsaves.cgi";
    my $allusers = 0;
    my $allsaves = 0;
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    if (-e $filetoopen) {
        open(FILE, $lbdir . "ebankdata/allsaves.cgi");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        my $allinfo = <FILE>;
        close(FILE);
        chomp($allinfo);
        ($allusers, $allsaves) = split(/,/, $allinfo);
    }

    $allusers += $callusers;
    $allsaves += $callsaves;

    if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$allusers,$allsaves";
        close(FILE);
    }
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    return;
}

print qq~</td></tr></table></body></html>~;
exit;
