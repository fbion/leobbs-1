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
$LBCGI::POST_MAX=1024*150;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";
require "code.cgi"; 
$|++;

$thisprog = "setawards.cgi";

$query = new LBCGI;

&ipbanned; #封杀一些 ip

@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        	$theparam = &cleaninput("$theparam");
		$PARAM{$param} = $theparam;
	    }


    $action          =  $PARAM{'action'};
    $awardid         =  $PARAM{'award'};
    $new_awardname   =  $PARAM{'awardname'};
    $new_awardurl    =  $PARAM{'awardurl'};
    $new_awardinfo   =  $PARAM{'awardinfo'};
    $new_awardorder  =  $PARAM{'awardorder'};
    $new_weblogo     =  $PARAM{'weblogo'}; 
    $checkaction     =  $PARAM{'checkaction'};
    $oldaward        =  $PARAM{'oldaward'};
    $oawardname	     =  $PARAM{'oawardname'};
    $action          = &unHTML("$action");
    
$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>"UTF-8");
&admintitle;
        
&getmember("$inmembername","no");
        
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
            
           my %Mode = ( 

            'addaward'            =>    \&addaward,
            'processnew'          =>    \&createaward,
            'edit'                =>    \&editaward,
            'doedit'              =>    \&doedit,       
             );


            if($Mode{$action}) {$Mode{$action}->();}
            elsif (($action eq "delete") && ($checkaction ne "yes")) { &warning; }
            elsif (($action eq "delete") && ($checkaction eq "yes")) { &deleteaward; }
            else { &awardlist; }            
            }                
else {&adminlogin;}
        
sub awardlist {
    $highest = 0;
    print qq~
    <tr><td bgcolor=#2159C9 colspan=3><font face=宋体 color=#FFFFFF>
    <b>欢迎来到论坛管理中心 / 社区勋章管理</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font face=宋体 color=#333333>
    <b>注意事项：</b><br><br>
    在下面，您将看到目前所有的社区勋章。您可以编辑社区勋章名或是增加一个新的社区勋章。 
    也可以编辑或删除目前存在的社区勋章。<br>
    </td></tr>
    ~;

    $filetoopen = "$lbdir" . "data/cityawards.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @awards = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    foreach $award (@awards) { #start foreach @awards
        chomp $award;
	next if ($award eq "");
        ($awardname, $awardurl, $awardinfo, $awardorder, $awardpic) = split(/\t/,$award);
        $rearrange = ("$awardname\t$awardurl\t$awardinfo\t$awardorder\t$awardpic");
        push (@rearrangedawards, $rearrange);

    } # end foreach (@awards)

         print qq~
            <tr>
            <td bgcolor=#FFFFFF colspan=3 ><font face=宋体 color=#333333><hr noshade>
            </td></tr>
            <tr>
            <td bgcolor=#EEEEEE width=20% nowrap><font face=宋体 color=#333333>
       <a href="$thisprog?action=addaward">增加新的社区勋章</a></font></td>
            </td></tr>
       
       ~;
    @finalsortedawards = @rearrangedawards;
    $awardnamenum = 0;
    foreach $sortedawards (@finalsortedawards) { #start foreach @finalsortedawards

        ($awardname, $awardurl, $awardinfo, $awardorder, $awardpic) = split(/\t/,$sortedawards);
        $awardnamenum++;
       
               print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=3 align=left><hr noshade width=70%><font face=宋体 color=#333333>
                <b>社区勋章名称</b>： $awardname<BR><b>社区勋章图片</b>： <img src=$imagesurl/awards/$awardpic><br><b>社区勋章简介</b>： $awardinfo<br>
                <br><a href="$thisprog?action=edit&award=$awardnamenum">编辑此社区勋章</a> | <font face=宋体 color=#333333><a href="$thisprog?action=delete&award=$awardnamenum&oawardname=$awardname">删除此社区勋章</a> </td>
                </font></td></tr>
                ~;
       
            } # end foreach
    
               
        print qq~
        <td bgcolor=#FFFFFF colspan=3 ><font face=宋体 color=#333333><hr noshade>
        </td></tr>
             <tr>
            <td bgcolor=#EEEEEE width=20% nowrap><font face=宋体 color=#333333>
       <a href="$thisprog?action=addaward">增加新的社区勋章</a></font></td>
            </td></tr>
        </tr></table></td></tr></table>~;
    
} # end routine.

sub addaward {

        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 增加社区勋章</b>
        </td></tr>
        ~;

 
        print qq~
        
                     
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="processnew">       
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>社区勋章名称</b><br>请输入新社区勋章的名称<BR>(请控制在 20 个汉字内)</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="awardname" maxlength=40></td>
        </tr>
        <input type=hidden size=40 name="awardurl" value="">
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>奖励图片名称</b><br>请输入图片名称(放在non-cgi/images/awards目录下)</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="weblogo"></td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>奖励描述</b><br>请输入新奖励的描述</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="awardinfo"></td>
        </tr>   
        
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
        ~;
        
}

sub createaward {   
		
		&errorout("对不起，论坛名字过长，请控制在 20 个汉字内！") if (length($new_awardname) >40);
		&errorout("奖励描述不能空！！") if ($new_awardinfo eq "");
                
                $filetoopen = "$lbdir" . "data/cityawards.cgi";
	        &winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE, "$filetoopen");
  	        flock(FILE, 1) if ($OS_USED eq "Unix");
                my @awards = <FILE>;
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                # Create a new number for the new award folder, and files.

                open(FILE, ">$filetoopen");
                flock(FILE, 2) if ($OS_USED eq "Unix");
                foreach $line (@awards) {
                    chomp $line;
                    print FILE "$line\n";
                    }
                print FILE "$new_awardname\t$new_awardurl\t$new_awardinfo\t$new_awardorder\t$new_weblogo\t";
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");
                
                print qq~
                <tr><td bgcolor=#2159C9" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 增加社区勋章结果</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                <font face=宋体 color=#333333>
                ~;

                print "<b>详细资料</b><p>\n";
                print "<ul>\n";
               
                print "新社区勋章 <B>$new_awardname</b> 已经建立！";
                print "<a href=\"$thisprog?action=awardlist\">返回</a> ";             
                print "</ul></td></tr></table></td></tr></table>\n";

}

sub warning { #start

        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 删除社区勋章</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=宋体 color=#990000><b>警告！！</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <font face=宋体 color=#333333>如果您确定要删除社区勋章 $oawardname，那么请点击下面链接<p>
        >> <a href="$thisprog?action=delete&checkaction=yes&award=$awardid&oawardname=$oawardname">删除社区勋章</a> <<
        <br><br>>> <a href=\"$thisprog?action=awardlist\">算了,再考虑一下</a> <<
        </td></tr>
        </table></td></tr></table>
        
        ~;
        
}
sub deleteaward {

         $filetoopen = "$lbdir" . "data/cityawards.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         my @awards = <FILE>;
         close(FILE);

         open(FILE,">$filetoopen");
         flock(FILE,2) if ($OS_USED eq "Unix");
         $awardname = 0;
         foreach $award (@awards) {
         chomp $award;
	 next if ($award eq "");
	 $awardname ++;
                unless ($awardid eq $awardname) {
                    print FILE "$award\n";
                    }
                }
         close(FILE);
         &winunlock($filetoopen) if ($OS_USED eq "Nt");

       
                    print qq~
                    <tr><td bgcolor=#2159C9" colspan=2><font face=宋体 color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 删除社区勋章结果</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                    <font face=宋体 color=#990000>
                    
                    <center><b>社区勋章 <B>$oawardname</B> 已被删除</b>，请刷新社区勋章管理页后再继续操作！</center><p>
                    
                  
                                    
                    </td></tr></table>
                    <center>>> <a href=\"$thisprog?action=awardlist\">从这里返回</a> <<</center></td></tr></table>
                    ~;


}

sub editaward {

         $filetoopen = "$lbdir" . "data/cityawards.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
         flock(FILE, 2) if ($OS_USED eq "Unix");
         @awards = <FILE>;
         close(FILE);
         &winunlock($filetoopen) if ($OS_USED eq "Nt");
         ($awardname,$awardurl,$awardinfo,$awardorder,$awardpic) = split(/\t/,$awards[$awardid-1]);   
         
        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 编辑社区勋章</b>
        </td></tr>
       
                
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="doedit">
        <input type=hidden name="award" value="$awardid">
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>社区勋章名称</b><br>请输入社区勋章名称<BR>(请控制在 20 个汉字内)</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="awardname" value="$awardname"  maxlength=40></td>
        </tr>
        <input type=hidden size=40 name="awardurl" value="">
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>社区勋章图片</b><br>请输入社区勋章图片(放在non-cgi/images/awards目录下)</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="weblogo" value="$awardpic"></td>
        </tr> 
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>社区勋章描述</b><br>请输入社区勋章描述</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="awardinfo" value="$awardinfo"></td>
        </tr>   
        
            
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
        ~;
        
}

sub doedit {
        
	&errorout("对不起，奖励名字过长，请控制在 20 个汉字内！") if (length($new_awardname) >40);
	&errorout("奖励描述不能空！！") if ($new_awardinfo eq "");
       
         $filetoopen = "$lbdir" . "data/cityawards.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
	 open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         my @awards = <FILE>;
         close(FILE);

                $editedline = "$new_awardname\t$new_awardurl\t$new_awardinfo\t$new_awardorder\t$new_weblogo\t";
                chomp $editedline;

                $filetoopen = "$lbdir" . "data/cityawards.cgi";
                open(FILE,">$filetoopen");
                flock(FILE,2) if ($OS_USED eq "Unix");
                $tempawardid = 0;
                foreach $award (@awards) {
                chomp $award;
                $tempawardid ++;
                    if ($tempawardid eq $awardid) {
                        print FILE "$editedline\n";
                        }
                        else {
                            print FILE "$award\n";
                            }
                    }
                close (FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");


                 print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 编辑社区勋章结果</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333><b>所有信息已经保存</b><p>
               
                </td></tr></table>
                <center><a href=\"$thisprog?action=awardlist\">返回</a></center> 
                </td></tr></table>
                ~;
                
            }



print qq~</td></tr></table></body></html>~;
exit;

sub errorout {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 发生错误</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                <font face=宋体 color=#333333>
                <font face=宋体 color=#333333><b>$_[0]</b>
                </td></tr></table></td></tr></table>
                ~;
exit;	
}
