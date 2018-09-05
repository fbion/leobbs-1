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
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";
$|++;

$thisprog = "usermanager.cgi";
$query = new LBCGI;

$action          = $query -> param('action');
$usertype        = $query -> param('usertype');
$action          = &unHTML("$action");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");       
&admintitle;
        
&getmember("$inmembername","no");
        
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / 用户分类管理</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'search' =>    \&searchusers,
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
            }
            else { &searchoptions; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        
sub searchoptions {
       my $memteam1 = qq~<option value="rz1">$defrz1(认证用户)</option>~ if ($defrz1 ne "");
       my $memteam2 = qq~<option value="rz2">$defrz2(认证用户)</option>~ if ($defrz2 ne "");
       my $memteam3 = qq~<option value="rz3">$defrz3(认证用户)</option>~ if ($defrz3 ne "");
       my $memteam4 = qq~<option value="rz4">$defrz4(认证用户)</option>~ if ($defrz4 ne "");
       my $memteam5 = qq~<option value="rz5">$defrz5(认证用户)</option>~ if ($defrz5 ne "");

    print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
	由于 <font color=red>一般用户</font> 数目较多，请到 <a href="setmembers.cgi">用户管理/排名(*)</a> 搜索。<br><br>
        <form method=get action="usermanager.cgi">
        <input type=hidden name="action" value="search">
        <div align=center>请选择需要查询的用户类型
	<select name="usertype">$memteam1$memteam2$memteam3$memteam4$memteam5
	<option value="rz">认证用户</option>
	<option value="amo">论坛副版主</option>
	<option value="mo">论坛版主</option>
        <option value="cmo">分类区总版主</option>
        <option value="smo">论坛总版主</option>
	<option value="ad">坛主</option>
        <option value="banned">禁止用户发言</option>
        <option value="masked">屏蔽此用户帖子</option>
	</select> 
        <p><input type="submit" value='确定'></p></div></form>
	</td></tr>
        ~;
        }

sub searchusers {
	unless ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
        }

        if ($usertype eq ""){
	print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>没有选择需要搜索的用户类别</font>
                    
        </td></tr>
         ~;
         }
         else {
	print qq~
        <tr>
        <td bgcolor=#FFFFFF colspan=2><br>
         ~;

	$filetoopen = "$lbdir" . "data/lbmember.cgi";
        open(FILE,"$filetoopen");
        flock (FILE, 1) if ($OS_USED eq "Unix");
        @memberfiles = <FILE>;
        close(FILE);
	$i=0;
        foreach $memtypedata (@memberfiles) {
	chomp $memtypedata;
        ($username, $membertype) = split(/\t/,$memtypedata);

       if ($membertype eq $usertype) {
       print qq~
       <a href="setmembers.cgi?action=edit&member=$username">$username</a><br><br>~;
       $i++;
       }
    }
       print qq~
       <br><br>
       <b>共找到 $i 位用户</b><br>
       </td></tr>
       ~;
       }
     }

print qq~</td></tr></table></body></html>~;
exit;
