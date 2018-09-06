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
require "data/mpic.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";

$|++;

$thisprog = "setmpic.cgi";

$query = new LBCGI;

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
	$theparam =~ s/\\/\\\\/g;
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/"//g;
        $theparam =~ s/'//g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
            $printme .= "\$" . "$_ = \'$theparam\'\;\n";
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");       
&admintitle;
        
&getmember("$inmembername","no");
        
        
        if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / 论坛图例设置</b>
            </td></tr>
            ~;
            

            if($action eq 'submit') { 
               &submit;
            }
            else { &options; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        

##################################################################################
sub submit {
	
	
        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/mpic.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=宋体 color=#333333><center><b>以下信息已经成功保存</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                print $printme;
                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=宋体 color=#333333><b>所有信息没有保存</b><br>文件或者目录不可写<br>请检测你的 data 目录和 mpic.cgi 文件的属性！
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                }
                
sub options {

   
    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>论坛图例</b>
    </td>
    </tr>          
    ~;
    print qq~
    <tr>
    <td bgcolor=#FFFFFF>
    <form action="$thisprog" method="post">
    <input type="hidden" name="action" value="submit">
    <table cellspacing=0 cellpadding=0 border=0 width=95% align=center>
    <tr><td colspan=3 height=50>注意：以下所有图片必须放在${imagesdir}images/$skin目录下，不要加url路径！</td></tr>
    
    <tr>
    <td colspan=3 bgcolor=#EEEEEE>在线名单图例　　(大小：12*11)</td></tr>
    <tr>
    <td><b>论坛坛主</b></td><td><input type="text" name="onlineadmin" value="$onlineadmin"
     onblur="document.images.i_onlineadmin.src='$imagesurl/images/'+this.value;">
    </td><td><img src="$imagesurl/images/$onlineadmin" name="i_onlineadmin"></td></tr>
    
    <tr>
    <td><b>论坛总版主</b></td><td><input type="text" name="onlinesmod" value="$onlinesmod"
     onblur="document.images.i_onlinesmod.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$onlinesmod" name="i_onlinesmod"></td></tr>
    
    <tr>
    <td><b>分类区版主</b></td><td><input type="text" name="onlinecmod" value="$onlinecmod"
     onblur="document.images.i_onlinecmod.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$onlinecmod" name="i_onlinecmod"></td></tr>

     <tr>
    <td><b>论坛版主</b></td><td><input type="text" name="onlinemod" value="$onlinemod"
     onblur="document.images.i_onlinemod.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$onlinemod" name="i_onlinemod"></td></tr>

     <tr>
    <td><b>论坛副版主</b></td><td><input type="text" name="onlineamod" value="$onlineamod"
     onblur="document.images.i_onlineamod.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$onlineamod" name="i_onlineamod"></td></tr>
     
     <tr>
    <td><b>认证会员</b></td><td><input type="text" name="onlinerz" value="$onlinerz"
     onblur="document.images.i_onlinerz.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$onlinerz" name="i_onlinerz"></td></tr>
     
     <tr>
    <td><b>普通会员</b></td><td><input type="text" name="onlinemember" value="$onlinemember"
     onblur="document.images.i_onlinemember.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$onlinemember" name="i_onlinemember"></td></tr>
     
     <tr>
     <td><b>突出显示自己的颜色</b></td><td><input type="text" name="onlineselfcolor" value="$onlineselfcolor">
     </td><td><font color=$onlineselfcolor name="i_onlineself">自己</td></tr>

     <tr>
     <td><b>男性会员名字的颜色</b></td><td><input type="text" name="mcolor" value="$mcolor">
     </td><td><font color="$mcolor" name="i_m">男性</td></tr>
     <tr>
     <td><b>女性会员名字的颜色</b></td><td><input type="text" name="fcolor" value="$fcolor">
     </td><td><font color=$fcolor name="i_f">女性</td></tr>

     <tr>
    <td><b>客人或隐身会员</b></td><td><input type="text" name="onlineguest" value="$onlineguest"
     onblur="document.images.i_onlineguest.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$onlineguest" name="i_onlineguest"></td></tr>
     <tr><td><BR></td><td></td></tr>
     
     <tr><td colspan=3 bgcolor=#EEEEEE>论坛图例　　(大小：13*16)</td></tr>
     
      <tr>
    <td><b>正规论坛 - 有新的帖子</b></td><td><input type="text" name="zg_havenew" value="$zg_havenew"
     onblur="document.images.i_zg_havenew.src='$imagesurl/images/$skin/'+this.value;">
     </td><td><img src="$imagesurl/images/$skin/$zg_havenew" name="i_zg_havenew"></td></tr>
     
      <tr>
    <td><b>正规论坛 - 没有新的帖子</b></td><td><input type="text" name="zg_nonew" value="$zg_nonew"
     onblur="document.images.i_zg_nonew.src='$imagesurl/images/$skin/'+this.value;">
     </td><td><img src="$imagesurl/images/$skin/$zg_nonew" name="i_zg_nonew"></td></tr>
     
          <tr>
    <td><b>开放论坛 - 有新的帖子</b></td><td><input type="text" name="kf_havenew" value="$kf_havenew"
     onblur="document.images.i_kf_havenew.src='$imagesurl/images/$skin/'+this.value;">
     </td><td><img src="$imagesurl/images/$skin/$kf_havenew" name="i_kf_havenew"></td></tr>
     
      <tr>
    <td><b>开放论坛 - 没有新的帖子</b></td><td><input type="text" name="kf_nonew" value="$kf_nonew"
     onblur="document.images.i_kf_nonew.src='$imagesurl/images/$skin/'+this.value;">
     </td><td><img src="$imagesurl/images/$skin/$kf_nonew" name="i_kf_nonew"></td></tr>
     
          <tr>
    <td><b>评论论坛 - 有新的帖子</b></td><td><input type="text" name="pl_havenew" value="$pl_havenew"
     onblur="document.images.i_pl_havenew.src='$imagesurl/images/$skin/'+this.value;">
     </td><td><img src="$imagesurl/images/$skin/$pl_havenew" name="i_pl_havenew"></td></tr>
     
      <tr>
    <td><b>评论论坛 - 没有新的帖子</b></td><td><input type="text" name="pl_nonew" value="$pl_nonew"
     onblur="document.images.i_pl_nonew.src='$imagesurl/images/$skin/'+this.value;">
     </td><td><img src="$imagesurl/images/$skin/$pl_nonew" name="i_pl_nonew"></td></tr>
     
          <tr>
    <td><b>保密论坛 - 有新的帖子</b></td><td><input type="text" name="bm_havenew" value="$bm_havenew"
     onblur="document.images.i_bm_havenew.src='$imagesurl/images/$skin/'+this.value;">
     </td><td><img src="$imagesurl/images/$skin/$bm_havenew" name="i_bm_havenew"></td></tr>
     
      <tr>
    <td><b>保密论坛 - 没有新的帖子</b></td><td><input type="text" name="bm_nonew" value="$bm_nonew"
     onblur="document.images.i_bm_nonew.src='$imagesurl/images/$skin/'+this.value;">
     </td><td><img src="$imagesurl/images/$skin/$bm_nonew" name="i_bm_nonew"></td></tr>
    
	       <tr>
    <td><b>认证论坛 - 有新的帖子</b></td><td><input type="text" name="rz_havenew" value="$rz_havenew"
     onblur="document.images.i_rz_havenew.src='$imagesurl/images/$skin/'+this.value;">
     </td><td><img src="$imagesurl/images/$skin/$rz_havenew" name="i_rz_havenew"></td></tr>
     
      <tr>
    <td><b>认证论坛 - 没有新的帖子</b></td><td><input type="text" name="rz_nonew" value="$rz_nonew"
     onblur="document.images.i_rz_nonew.src='$imagesurl/images/$skin/'+this.value;">
     </td><td><img src="$imagesurl/images/$skin/$rz_nonew" name="i_rz_nonew"></td></tr>

	 <tr>
    <td><b>精华区</b></td><td><input type="text" name="jh_pic" value="$jh_pic"
     onblur="document.images.i_jh_pic.src='$imagesurl/images/$skin/'+this.value;">
     </td><td><img src="$imagesurl/images/$skin/$jh_pic" name="i_jh_pic"></td></tr>
     
     <tr><td colspan=3 bgcolor=#EEEEEE>论坛按钮</td></tr>

                <tr>
                <td>
                <b>发新帖按钮图标</b>　(大小：99*25)</td>
                <td><input type=text name="newthreadlogo" value="$newthreadlogo" onblur="document.images.i_newthreadlogo.src='$imagesurl/images/$skin/'+this.value;">
                </td><td><img src=$imagesurl/images/$skin/$newthreadlogo name="i_newthreadlogo"></td>
                </tr>

                <tr>
                <td><b>发起投票按钮图标</b>　(大小：99*25)</td>
                <td>
                <input type=text name="newpolllogo" value="$newpolllogo" onblur="document.images.i_newpolllogo.src='$imagesurl/images/$skin/'+this.value;">
                </td><td><img src=$imagesurl/images/$skin/$newpolllogo name="i_newpolllogo"></td>
                </tr>

                <tr>
                <td><b>小字报按钮图标</b>　(大小：99*25)</td>
                <td>
                <input type=text name="newxzblogo" value="$newxzblogo" onblur="document.images.i_newxzblogo.src='$imagesurl/images/$skin/'+this.value;">
                </td><td><img src=$imagesurl/images/$skin/$newxzblogo name="i_newxzblogo"></td>
                </tr>

                <tr>
                <td><b>回复帖子按钮图标</b>　(大小：99*25)</td>
                <td>
                <input type=text name="newreplylogo" value="$newreplylogo" onblur="document.images.i_newreplylogo.src='$imagesurl/images/$skin/'+this.value;">
                </td><td><img src=$imagesurl/images/$skin/$newreplylogo name="i_newreplylogo"></td>
                </tr>

                <tr>
                <td><b>原窗口按钮图标</b>　(大小：74*21)</td>
                <td>
                <input type=text name="wlogo" value="$wlogo" onblur="document.images.i_wlogo.src='$imagesurl/images/$skin/'+this.value;">
                </td><td><img src=$imagesurl/images/$skin/$wlogo name="i_wlogo"></td>
                </tr>

                <tr>
                <td><b>新窗口按钮图标</b>　(大小：74*21)</td>
                <td>
                <input type=text name="nwlogo" value="$nwlogo" onblur="document.images.i_nwlogo.src='$imagesurl/images/$skin/'+this.value;">
                </td><td><img src=$imagesurl/images/$skin/$nwlogo name="i_nwlogo"></td>
                </tr>

                <tr>
                <td><b>帮助按钮图标</b>　(大小：不限)</td>
                <td>
                <input type=text name="help_blogo" value="$help_blogo" onblur="document.images.i_help_blogo.src='$imagesurl/images/'+this.value;">
                </td><td><img src=$imagesurl/images/$skin/$help_blogo name="i_help_blogo"></td>
                </tr>

                <tr>
                <td><b>新贴最后的 new 图标</b>　(大小：不限)</td>
                <td>
                <input type=text name="new_blogo" value="$new_blogo" onblur="document.images.i_new_blogo.src='$imagesurl/images/$skin/'+this.value;">
                </td><td><img src=$imagesurl/images/$skin/$new_blogo name="i_new_blogo"></td>
                </tr>
                <tr>
                <td><b>自己是发帖人的标记图示</b>　(大小：不限)</td>
                <td>
                <input type=text name="mypost_blogo" value="$mypost_blogo" onblur="document.images.i_new_mypost.src='$imagesurl/images/$skin/'+this.value;">
                </td><td><img src=$imagesurl/images/$skin/$mypost_blogo name="i_new_mypost"></td>
                </tr>

               <tr> 
               <td><b>精华帖子的标记图示</b>  (大小：不限)</td> 
               <td> 
               <input type=text name="new_JH" value="$new_JH" onblur="document.images.i_new_JH.src='$imagesurl/images/$skin/'+this.value;"> 
               </td><td><img src=$imagesurl/images/$skin/$new_JH name="i_new_JH"></td> 
               </tr> 

     
   <tr><td colspan=3 height=50 align=center><input type="submit" value="提 交"> <input type="reset" value="复 位"></td></tr>
     
    </form>
    
    </td>
    </tr>             
     ~;        
     
     } 
     
     
print qq~</td></tr></table></body></html>~;
exit;
