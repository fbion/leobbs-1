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
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setvariables.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;');

$query = new LBCGI;
#&ipbanned; #封杀一些 ip

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);

        if (($_ eq 'adfoot')||($_ eq 'adscript')||($_ eq 'adscriptmain')||($_ eq 'adlinks')||($_ eq 'topicad')) {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g
	}
	$theparam = &unHTML("$theparam");

	$theparam  = sprintf("%02d",$theparam) if (($_ eq 'createmon')||($_ eq 'createday'));
	if ($_ eq 'createyear') { $theparam = sprintf("%02d", $theparam); $theparam = 1900+$theparam if ($theparam<100); }

	${$_} = $theparam;
        if ($_ ne 'action') {
            $theparam =~ s/[\a\f\n\e\0\r]//isg;
            $printme .= "\$" . "$_ = \'$theparam\'\;\n" if ($_ ne "");
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");
        
$maxweiwang = 5 if (($maxweiwang < 5)||($maxweiwang eq ""));

if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {

    if ($action eq "process") {

        
        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/boardinfo.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

$lbdirbak = $lbdir ;

eval{ require "data/boardinfo.cgi"; };
if ($@) {

    open(FILE,"${lbdirbak}data/boardinfobak.cgi");
    my @ddd = <FILE>;
    close(FILE);
    open(FILE,">${lbdirbak}data/boardinfo.cgi");
    foreach (@ddd) {
    	chomp $_;
        print FILE "$_\n";
    }
    close(FILE);

                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 变量设置</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=宋体 color=#333333><b>所有信息没有保存</b><br>你输入的数据中，有非正常的内容，导致数据出错，请排查！
                    </td></tr></table></td></tr></table>
                    ~;
		print qq~</td></tr></table></body></html>~;
		exit;
}

        $filetomake = "$lbdir" . "data/boardinfobak.cgi";
        open(FILE,">$filetomake");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);

    opendir (DIRS, "${lbdir}cache/id");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	$_ =~ s/\.cgi//isg;
    	unlink ("${lbdir}cache/id/$_\.cgi");
    }

        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 变量结构</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=宋体 color=#333333><center><b>以下信息已经成功保存</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                $printme =~ s/\\\'/\'/g;
                print $printme;
                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 变量设置</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=宋体 color=#333333><b>所有信息没有保存</b><br>文件或者目录不可写<br>请检测你的 data 目录和 boardinfo.cgi 文件的属性！
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 变量设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>论坛变量设置</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                <input type=hidden name="noads" value="$noads">
                <input type=hidden name="regerid" value="$regerid">
                ~;
                $tempoutput1 = "<select name=\"mainoff\">\n<option value=\"0\">论坛开放\n<option value=\"1\">论坛关闭\n<option value=\"2\">自动定期开放\n</select>\n";
                $tempoutput1 =~ s/value=\"$mainoff\"/value=\"$mainoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333 ><b>论坛状态</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1</td>
                </tr>
                ~;
	$tempoutput1 = "<select name=\"mainauto\">\n<option value=\"day\">每天\n<option value=\"week\">每星期\n<option value=\"month\">每月\n</select>\n";
        $tempoutput1 =~ s/value=\"$mainauto\"/value=\"$mainauto\" selected/;
      	print qq~
              <tr>
              <td bgcolor=#FFFFFF width=40%>
              <font face=宋体 color=#333333 ><b>自动开放论坛于</b><br>(只有选择自动定期开放此项有效)</font></td>
              <td bgcolor=#FFFFFF>
              $tempoutput1 <input name=mainautovalue value="$mainautovalue" size=8><br>注: 可以使用单一数字或是范围，如每天6, 每天0-6, 每星期6, 每月10-15</td>
              </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333 ><b>维护说明</b> (支持 HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="line1" cols="40">$line1</textarea><BR><BR></td>
                </tr>
                ~;
                $tempoutput1 = "<select name=\"regonoff\">\n<option value=\"0\">允许用户注册\n<option value=\"1\">不允许用户注册\n<option value=\"2\">自动定期开放\n</select>\n";
                $tempoutput1 =~ s/value=\"$regonoff\"/value=\"$regonoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333 ><b>是否允许用户注册</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1<BR><BR></td>
                </tr>
                ~;
		$tempoutput1 = "<select name=\"regauto\">\n<option value=\"day\">每天\n<option value=\"week\">每星期\n<option value=\"month\">每月\n</select>\n";
		$tempoutput1 =~ s/value=\"$regauto\"/value=\"$regauto\" selected/;
		print qq~
               <tr>
               <td bgcolor=#FFFFFF width=40%>
               <font face=宋体 color=#333333 ><b>自动开放注册于</b><br>(只有上面选择自动定期开放此项才有效)</font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput1 <input name=regautovalue value="$regautovalue" size=8><br>注: 可以使用单一数字或是范围，如每天6, 每天0-6, 每星期6, 每月10-15</td>
               </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333 ><b>不允许注册说明</b> (支持 HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="noregwhynot" cols="40">$noregwhynot</textarea><BR><BR></td>
                </tr>
                ~;
                $tempoutput1 = "<select name=\"regdisptime\">\n<option value=\"15\">15\n<option value=\"1\">1\n<option value=\"3\">3\n<option value=\"5\">5\n<option value=\"8\">8\n<option value=\"10\">10\n<option value=\"12\">12\n<option value=\"17\">17\n<option value=\"20\">20\n<option value=\"25\">25\n<option value=\"30\">30\n<option value=\"40\">40\n<option value=\"45\">45\n<option value=\"50\">50\n<option value=\"60\">60\n<option value=\"90\">90\n<option value=\"120\">120\n<option value=\"150\">150\n<option value=\"200\">200\n</select> 秒\n";
                $tempoutput1 =~ s/value=\"$regdisptime\"/value=\"$regdisptime\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333 ><b>注册声明时间显示多少秒后才能确定</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1<BR><BR></td>
                </tr>
                ~;

                $tempoutput1 = "<select name=\"regpuonoff\">\n<option value=\"ontop\">首页弹出\n<option value=\"oneach\">每页弹出\n<option value=\"off\">不弹出\n</select>\n";
                $tempoutput1 =~ s/value=\"$regpuonoff\"/value=\"$regpuonoff\" selected/;
                if(!$popupmsg){$popupmsg=qq~请先注册以避免此视窗出现~;}
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333 ><b>是否弹出提醒注册视窗</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1<BR><BR></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333 ><b>提醒访客注册视窗内容</b> (支援 HTML,不需要注册画面的连结)<BR><BR></font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="popupmsg" cols="40">$popupmsg</textarea><BR><BR></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛名称</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boardname" value="$boardname"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛描述</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boarddescription" value="$boarddescription"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛 LOGO</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boardlogos" value="$boardlogos"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛 URL 地址</b><br>结尾不要加 "/"，更不要加 leobbs.cgi 之类的哦</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boardurl" value="$boardurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>主页名称</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="homename" value="$homename"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>版权信息</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="copyrightinfo" value="$copyrightinfo"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛备案信息，只需填入编号就可以，<BR>不要填其他多余的内容，如果没有请留空！</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=18 name="beian" value="$beian" maxlength=18> 比如：沪ICP备05023323号</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛状态栏显示</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="statusbar" value="$statusbar"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>主页地址</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="homeurl" value="$homeurl"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>图片目录 URL</b><br>在结尾不要加 "/images"</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="imagesurl" value="$imagesurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>图片绝对路径</b><br>结尾加 "/"</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="imagesdir" value="$imagesdir"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>程序绝对路径</b><br>结尾加 "/"</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="lbdir" value="$lbdir"></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emoticons\">\n<option value=\"off\">不使用\n<option value=\"on\">使用\n</select>\n";
                $tempoutput =~ s/value=\"$emoticons\"/value=\"$emoticons\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否使用表情字符转换？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"canchgfont\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
                $tempoutput =~ s/value=\"$canchgfont\"/value=\"$canchgfont\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否使用文字字体转换？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"avatars\">\n<option value=\"off\">不使用\n<option value=\"on\">使用\n</select>\n";
                $tempoutput =~ s/value=\"$avatars\"/value=\"$avatars\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否使用个性图片</b><br>使用个性化图片，每个用户将拥有有自己特色的头像。</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛关键字</b><br>输入和你论坛相关的关键字，每个关键字之间用英文的逗号隔开 ！</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newkeywords" value="$newkeywords" size=40 maxlength=100></td>
                </tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>短消息功能</b>
                </font></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"allowusemsg\">\n<option value=\"on\">使用\n<option value=\"off\">不使用\n</select>";
                $tempoutput =~ s/value=\"$allowusemsg\"/value=\"$allowusemsg\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否开启论坛短消息功能？</b><br>开启短消息功能，可使您及您的会员便于互相沟通。</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>一次群发讯息最高数量</font></b><br>如不限制，请留空</td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="maxsend" value="$maxsend" maxlength=3> 此功能对版主和坛主无效</td>
                </tr>                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>短消息收件箱消息条数限制</font></b><br>如不限制，请留空</td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="maxmsgno" value="$maxmsgno" maxlength=3> 此功能对版主和坛主无效</td>
                </tr>                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>每页显示多少短消息</font></b></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="maxthread" value="$maxthread" maxlength=3> 默认: 9 </td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>自动刷新短消息窗口时间</font></b></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="infofreshtime" value="$infofreshtime" maxlength=3> 秒(留空为不需要)</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"allowmsgattachment\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>";
                $tempoutput =~ s/value=\"$allowmsgattachment\"/value=\"$allowmsgattachment\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否开启论坛短消息附件功能？</b><br>附件最大 60KB，不可设。</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>邮件功能</b>
                </font></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emailfunctions\">\n<option value=\"off\">不使用\n<option value=\"on\">使用\n</select>\n";
                $tempoutput =~ s/value=\"$emailfunctions\"/value=\"$emailfunctions\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否使用邮件功能？</b><br>推荐你使用</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
		$sendmailprog = mailprogram();

                $tempoutput = "<select name=\"emailtype\">\n<option value=\"smtp_mail\">SMTP\n<option value=\"esmtp_mail\">ESMTP\n<option value=\"directmail\">94cool 特快专递\n<option value=\"send_mail\">Sendmail\n<option value=\"blat_mail\">Blat\n</select>\n";
                $tempoutput =~ s/value=\"$emailtype\"/value=\"$emailtype\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>请选择一个可以使用的邮件协议</b><br>推荐使用 SMTP，可以同时在 NT 和 UNIX 下使用。而 SENDMAIL 只能在 UNIX 中用，Blat 只能在 NT 中用。你也可以用 94cool 特快专递，他可以直接把信件提交到对方信箱，类似 Foxmail 的特快专递，速度相当快(注意的是，如果你主机有限制，可能会无法使用该功能，请测试后再确定)。</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>发送邮件程序位置</b><br>如果您使用的不是 Sendmail，请不要填写</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=30 name="SEND_MAIL" value="$SEND_MAIL"> 测试结果：$sendmailprog</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>SMTP 的位置</b><br>如果您使用的不是 SMTP，请不要填写，一般填写你 ISP 提供的发信服务器地址</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="SMTP_SERVER" value="$SMTP_SERVER"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>SMTP 的端口</b><br>如果您使用的不是 SMTP，请不要填写，默认为 25</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=6 name="SMTP_PORT" value="$SMTP_PORT" maxlength=6></td>
                </tr>
				
				<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>ESMTP 的用户名</b><br>如果您使用的不是 ESMTP，请不要填写</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="SMTPUSER" value="$SMTPUSER"></td>
                </tr>
                <tr>
				<td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>ESMTP 的密码</b><br>如果您使用的不是 ESMTP，请不要填写</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="SMTPPASS" value="$SMTPPASS"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>坛主接收邮件使用的信箱</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adminemail_in" value="$adminemail_in"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>坛主发送邮件使用的信箱</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adminemail_out" value="$adminemail_out"></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"passwordverification\">\n<option value=\"no\">否\n<option value=\"yes\">是\n</select>\n";
                $tempoutput =~ s/value=\"$passwordverification\"/value=\"$passwordverification\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否用邮件通知用户密码？</b><br>建议不使用。若要使用，请确定打开了上面的“是否使用邮件功能？”，并保证你发送邮件是没有问题的。</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"adminverification\">\n<option value=\"no\">否\n<option value=\"yes\">是\n</select>\n";
                $tempoutput =~ s/value=\"$adminverification\"/value=\"$adminverification\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>新用户注册，是否必须管理员认证？</b><br>建议不使用。若要使用，1,请确定打开了上面的“是否使用邮件功能？”，并保证你发送邮件是没有问题的。2,确认已经打开上面的邮件通知用户密码!</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"newusernotify\">\n<option value=\"no\">否\n<option value=\"yes\">是\n</select>\n";
                $tempoutput =~ s/value=\"$newusernotify\"/value=\"$newusernotify\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>有新用户注册是否用邮件通知您？</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"oneaccountperemail\">\n<option value=\"no\">否\n<option value=\"yes\">是\n</select>\n";
                $tempoutput =~ s/value=\"$oneaccountperemail\"/value=\"$oneaccountperemail\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>一个 Email 只能注册一个账号？</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>广告选项</b>
                </font></td>
                </tr>
		~;
	$adscript   =~ s/\[br\]/\n/isg;
	$adscriptmain   =~ s/\[br\]/\n/isg;
	$adfoot   =~ s/\[br\]/\n/isg;

               $tempoutput = "<select name=\"useadscript\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n"; 
               $tempoutput =~ s/value=\"$useadscript\"/value=\"$useadscript\" selected/; 
               print qq~ 
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页独立广告书写(如果没有，请留空)</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adscriptmain" rows="5" cols="40">$adscriptmain</textarea>
                </td>
                </tr>
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=宋体 color=#333333><b>是否使用论坛首页广告</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页广告书写</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adscript" rows="5" cols="40">$adscript</textarea>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"useadfoot\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n"; 
               $tempoutput =~ s/value=\"$useadfoot\"/value=\"$useadfoot\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=宋体 color=#333333><b>是否使用论坛首页尾部代码</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页尾部代码书写</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adfoot" rows="5" cols="40">$adfoot</textarea><BR><BR>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"useimagead\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimagead\"/value=\"$useimagead\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=宋体 color=#333333><b>是否使用论坛首页浮动广告</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页浮动广告图片(Flash) URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage" value="$adimage"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页浮动广告连接目标网址</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink" value="$adimagelink"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页浮动广告图片宽度</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth" value="$adimagewidth" maxlength=3>&nbsp;像素</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页浮动广告图片高度</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight" value="$adimageheight" maxlength=3>&nbsp;像素</td>
                </tr>
                ~;
                
               $tempoutput = "<select name=\"useimageadforum\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimageadforum\"/value=\"$useimageadforum\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=宋体 color=#333333><b>分论坛是否使用此浮动广告</b><BR>如果分论坛有自定义的浮动广告，<BR>那么此选项无效</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput<BR><BR></td> 
               </tr>
		~;
               
               $tempoutput = "<select name=\"useimagead1\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimagead1\"/value=\"$useimagead1\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=宋体 color=#333333><b>是否使用论坛首页右下固定广告</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页右下固定广告图片(Flash) URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage1" value="$adimage1"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页右下固定广告连接目标网址</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink1" value="$adimagelink1"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页右下固定广告图片宽度</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth1" value="$adimagewidth1" maxlength=3>&nbsp;像素</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页右下固定广告图片高度</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight1" value="$adimageheight1" maxlength=3>&nbsp;像素</td>
                </tr>
                ~;
                
               $tempoutput = "<select name=\"useimageadforum1\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimageadforum1\"/value=\"$useimageadforum1\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=宋体 color=#333333><b>分论坛是否使用此右下固定广告</b><BR>如果分论坛有自定义的右下固定广告，<BR>那么此选项无效</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>其他选项</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>支持上传的附件类型</b><br>用,分割</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="addtype" value="$addtype"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>最大每次上传几个附件</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=2 name="maxaddnum" value="$maxaddnum"> 建议不要超过10。</td>
                </tr>
                
                ~;
                $tempoutput = "<select name=\"COOKIE_USED\">\n<option value=\"0\">完整路径模式\n<option value=\"1\">根目录模式\n<option value=\"2\">固定模式\n</select>\n";
                #<option value=\"0\">自动侦测目录模式\n
                $tempoutput =~ s/value=\"$COOKIE_USED\"/value=\"$COOKIE_USED\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>请选择 Cookie 使用方式！</B><br>默认使用完整路径模式，如果你发现论坛<BR>用户登录后还是客人的话，请使用<BR>根目录模式或固定模式(固定模式必须配合下面一个参数使用)。</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>Cookie 固定模式内容</b><br>输入固定的域名和路径，只有当上面选项设置为固定模式才有效</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=20 name="mycookiepath" value="$mycookiepath"> <BR>(域名前不要加 http://，最后不要加 / 号，例如：www.abc.com )</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"EXP_MODE\">\n<option value=\"\">标准模式\n<option value=\"0\">增强模式\n</select>\n";
                $tempoutput =~ s/value=\"$EXP_MODE\"/value=\"$EXP_MODE\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>请选择页面更新方式！</B><br>默认使用标准模式，如果你发现论坛私密区进入时，<BR>输入正确密码后还必须刷新的话，请修改为增强模式。<BR>但如果设置为增强模式后发现一些奇怪的现象，请改回！</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"CACHE_MODES\">\n<option value=\"\">开放模式\n<option value=\"no\">拒绝模式\n</select>\n";
                $tempoutput =~ s/value=\"$CACHE_MODES\"/value=\"$CACHE_MODES\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>请选择页面是否保持缓存！</B><br>默认使用开放模式，如果发现论坛出现奇怪的混乱现象，<BR>必须手工刷新才能解决的话，请修改为拒绝模式。<BR>但如果设置为拒绝模式后发现一些奇怪的现象，请改回！</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

    unless (WebGzip::getStatus()) {
	$gzipfunc = qq~Gzip 模块可以使用~;
    }
    else {
    	$e = WebGzip::getStatus();
    	$gzipfunc = qq~<BR><font color=#FF0000>Gzip 模块不可用！</font> $e~ 
    }

                $tempoutput = "<select name=\"usegzip\">\n<option value=\"no\">关闭\n<option value=\"yes\">打开\n</select>\n 测试结果：$gzipfunc";
                $tempoutput =~ s/value=\"$usegzip\"/value=\"$usegzip\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>请选择是否采用Gzip压缩！</B><br>默认开放，Gzip 可以有效的压缩传输的页面，让页面传输的更快，但也会多消耗部分资源！如果你对资源要求很严，那么请选择关闭！</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"complevel\">\n<option value=\"9\">9\n<option value=\"8\">8\n<option value=\"7\">7\n<option value=\"6\">6\n<option value=\"5\">5\n<option value=\"4\">4\n<option value=\"3\">3\n<option value=\"2\">2\n<option value=\"1\">1\n</select>\n";
                $tempoutput =~ s/value=\"$complevel\"/value=\"$complevel\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>请选择Gzip压缩级别！</B><br>9 表示压缩率最高，1表示压缩率最低，配合上面选项使用！</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"OS_USED\">\n<option value=\"Nt\">Windows 系列\n<option value=\"Unix\">Unix 系列\n<option value=\"No\">不加锁\n</select>\n";
                $tempoutput =~ s/value=\"$OS_USED\"/value=\"$OS_USED\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>请选择操作系统平台用于文件加锁</b><BR>请千万不要选错，如果你不能确定，请选择 Windows 系列！！<BR>文件加锁可以有效的防止贴子数据丢失等问题，但会影响速度，请自己衡量！<br></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"canotherlink\">\n<option value=\"no\">不允许外部连接\n<option value=\"yes\">允许外部连接\n</select>\n";
                $tempoutput =~ s/value=\"$canotherlink\"/value=\"$canotherlink\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否禁止外部连接程序对论坛操作</b><BR>打开的话，可有效防止外部连接的程序灌水轰炸机的骚扰，但有可能会和防火墙冲突<br></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"useverify\">\n<option value=\"no\">不允许使用\n<option value=\"yes\">允许使用\n</select>\n";
                $tempoutput =~ s/value=\"$useverify\"/value=\"$useverify\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否使用验证码校验</b><br></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

eval ('use GD;');
if ($@) {
    $gdfunc = 0;
}
else {
    $gdfunc = 1;
}
if ($gdfunc eq "1") {
                $tempoutput = "<select name=\"verifyusegd\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
                $tempoutput =~ s/value=\"$verifyusegd\"/value=\"$verifyusegd\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否使用 GD 来显示验证码</b><br></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
} else {
	print qq~<input type=hidden name="verifyusegd" value="no">~;
}

                $tempoutput = "<select name=\"floodcontrol\">\n<option value=\"off\">否\n<option value=\"on\">是\n</select>\n";
                $tempoutput =~ s/value=\"$floodcontrol\"/value=\"$floodcontrol\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否灌水预防机制？</b><br>强烈推荐使用</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>用户发贴的相隔时间</b><br>灌水预防机制不会影响到坛主或版主</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=5 name="floodcontrollimit" value="$floodcontrollimit" maxlength=4> 秒 (一般设置 30 左右)</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>同 IP 的注册最小相隔时间</b><br>可以有效防止灌水注册机</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=5 name="regcontrollimit" value="$regcontrollimit" maxlength=4> 秒 (一般设置 30 左右)</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>显示编辑计数的最小时间</b><br>在该时间内对贴子的编辑不计数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=6 name="noaddedittime" value="$noaddedittime" maxlength=5> 秒 (默认 60 秒)</td>
                </tr>
                
               <tr>
               <td bgcolor=#FFFFFF width=40%>
               <font face=宋体 color=#333333><b>超过多少小时的贴子不允许再编辑</b><br>版主以上级别不限制</font></td>
               <td bgcolor=#FFFFFF>
               <input type=text size=3 name="noedittime" value="$noedittime" maxlength=2> 小时 (留空不限制)</td>
               </tr>
               
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>删贴率在多少以上的会员不允许发表新主题</b><br>此设定不会影响到坛主或版主</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="deletepercent" value="$deletepercent" maxlength=3> % (一般设置 20% 左右，若不想限制，则设置 0 或空白)</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛允许的最大在线人数</b><br>可以控制服务器的资源使用</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=6 name="arrowonlinemax" value="$arrowonlinemax" maxlength=5> 人 (一般设 500 左右，若不想限制，则设置 99999)</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"timezone\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\">0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
                $tempoutput =~ s/value=\"$timezone\"/value=\"$timezone\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>服务器时差</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>所在的时区</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="basetimes" value="$basetimes"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>用户威望最大多少？</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=4 name="maxweiwang" value="$maxweiwang" maxlength=3> 默认: 10(不能小于5)</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>在多少区发送相同贴子就查封？</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=4 name="maxadpost" value="$maxadpost" maxlength=3> 默认: 4(不能小于3)，如果要取消，请设置 999</td>
                </tr>
                ~;
		
		$tempoutput = "<select name=\"coolclickdisp\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n";
		$tempoutput =~ s/value=\"$coolclickdisp\"/value=\"$coolclickdisp\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF width=40%>
		<font face=宋体 color=#333333><b>是否使用 LeoBBS 点击风格？使用的话，点击将会先显示一个进程条！</font></td>
		<td bgcolor=#FFFFFF>
		$tempoutput</td>
		</tr>
		~;
		
		$tempoutput = "<select name=\"friendonlinepop\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
		$tempoutput =~ s/value=\"$friendonlinepop\"/value=\"$friendonlinepop\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF width=40%>
		<font face=宋体 color=#333333><b>好友上线是否通知？</font></td>
		<td bgcolor=#FFFFFF>
		$tempoutput</td>
		</tr>
		~;

		$tempoutput = "<select name=\"cpudisp\">\n<option value=\"0\">不显示\n<option value=\"1\">显示\n</select>\n";
		$tempoutput =~ s/value=\"$cpudisp\"/value=\"$cpudisp\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF width=40%>
		<font face=宋体 color=#333333><b>是否显示论坛 CPU 占用时间。(此设置对坛主无效)</font></td>
		<td bgcolor=#FFFFFF>
		$tempoutput</td>
		</tr>
		
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>显示论坛 CPU 占用时间的字体颜色</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=8 maxlength=7 name="cpudispcolor" value="$cpudispcolor"> 默认：#c0c0c0</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"useemote\">\n<option value=\"no\">不使用\n<option value=\"yes\">使用\n</select>\n";
                $tempoutput =~ s/value=\"$useemote\"/value=\"$useemote\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否使用 EMOTE 标签</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"announcements\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
                $tempoutput =~ s/value=\"$announcements\"/value=\"$announcements\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否使用论坛公告</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
		
                $tempoutput = "<select name=\"refreshurl\">\n<option value=\"0\">自动返回当前论坛\n<option value=\"1\">自动返回当前贴子\n</select>\n";
                $tempoutput =~ s/value=\"$refreshurl\"/value=\"$refreshurl\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>发表、回复贴子后自动转移到？</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"dispboardonline\">\n<option value=\"no\">不显示\n<option value=\"yes\">显示\n</select>\n";
                $tempoutput =~ s/value=\"$dispboardonline\"/value=\"$dispboardonline\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否在首页显示分论坛详细在线情况</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"adminstyle\">\n<option value=\"2\">下拉菜单显示\n<option value=\"1\">平板显示\n<option value=\"3\">自动判断\n</select>\n";
                $tempoutput =~ s/value=\"$adminstyle\"/value=\"$adminstyle\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛版主显示样式</b><BR>如果选择平板显示，只能显示前３个版主，设置后，需要清空缓存一次</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"disphideboard\">\n<option value=\"no\">不显示\n<option value=\"yes\">显示\n</select>\n";
                $tempoutput =~ s/value=\"$disphideboard\"/value=\"$disphideboard\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>跳转论坛栏中是否显示隐含论坛</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispchildjump\">\n<option value=\"no\">不显示\n<option value=\"yes\">显示\n</select>\n";
                $tempoutput =~ s/value=\"$dispchildjump\"/value=\"$dispchildjump\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>跳转论坛栏中是否显示子论坛</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispboardsm\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$dispboardsm\"/value=\"$dispboardsm\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否在最下面显示论坛声明</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"dispborn\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n<option value=\"auto\">有才显示，无则不显示\n</select>\n";
                $tempoutput =~ s/value=\"$dispborn\"/value=\"$dispborn\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>首页是否显示当天生日用户</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"sendtobirthday\">\n<option value=\"no\">不发送\n<option value=\"yes\">发送\n</select>\n";
                $tempoutput =~ s/value=\"$sendtobirthday\"/value=\"$sendtobirthday\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否给当天生日用户发送祝贺信息</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
		$tempoutput = "<select name=\"usetodaypostreply\">\n<option value=\"yes\">是的，记录\n<option value=\"no\">不，不记录\n</select>\n";
                $tempoutput =~ s/value=\"$usetodaypostreply\"/value=\"$usetodaypostreply\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否把回复也记录在每日发贴数上</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"dispinfos\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$dispinfos\"/value=\"$dispinfos\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>首页是否显示个人状态或者快速登录</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"displink\">\n<option value=\"no\">不显示\n<option value=\"yes\">显示\n</select>\n";
                $tempoutput =~ s/value=\"$displink\"/value=\"$displink\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>首页是否显示首页连接</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"displinkaddr\">\n<option value=\"1\">首页下方\n<option value=\"2\">首页上方\n</select>\n";
                $tempoutput =~ s/value=\"$displinkaddr\"/value=\"$displinkaddr\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>显示首页连接的位置</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>首页连接</b><br>用 HTML 语法书写！</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="links" cols="40" rows="6">$links</textarea><BR>
                </td>
                </tr>
                ~;

	$adlinks   =~ s/\[br\]/\n/isg;

		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛广告区</b><br>用 HTML 语法书写！</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adlinks" cols="40" rows="10">$adlinks</textarea><BR>
                </td>
                </tr>
                ~;


	$topicad   =~ s/\[br\]/\n/isg;

		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>看贴广告区</b><br>用 HTML 语法书写！</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="topicad" cols="40" rows="10">$topicad</textarea><BR>
                </td>
                </tr>
                ~;

		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛创建的日期</b><BR>请填写完整，年月日不可缺任何一个！</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="createyear" value="$createyear" size=4>年<input type=text name="createmon" value="$createmon" size=2>月<input type=text name="createday" value="$createday" size=2>日。(请用标准年月日格式，年用四位表示)</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"dispprofile\">\n<option value=\"yes\">允许\n<option value=\"no\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$dispprofile\"/value=\"$dispprofile\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否允许客人查看用户资料</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"forumnamedisp\">\n<option value=\"0\">不显示\n<option value=\"1\">显示\n</select>\n";
                $tempoutput =~ s/value=\"$forumnamedisp\"/value=\"$forumnamedisp\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛首页是否显示直接发贴按钮</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"canhidden\">\n<option value=\"yes\">允许\n<option value=\"no\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$canhidden\"/value=\"$canhidden\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛是否允许用户隐身？</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispguest\">\n<option value=\"1\">视系统负荷而定\n<option value=\"2\">永远显示\n<option value=\"3\">永远不显示\n</select>\n";
                $tempoutput =~ s/value=\"$dispguest\"/value=\"$dispguest\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>在线列表中是否显示客人？</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"userincert\">\n<option value=\"yes\">允许\n<option value=\"no\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$userincert\"/value=\"$userincert\" selected/;
                print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>访问论坛的最大客人数(超过此数目的客人将必须注册才可以访问。打开此功能后，记得在默认风格设置中把“是否允许搜索引擎直接访问？”开放，否则搜索引擎可能会因为客人数超过导致无法对你论坛进行正确的索引)</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=4 maxlength=4 name="maxguests" value="$maxguests"> 如不需要此功能，请设置为空或0</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>认证论坛是否允许普通用户进入？</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispmememail\">\n<option value=\"yes\">根据用户设置要求决定显示\n<option value=\"no\">强制不显示所有的 Email 地址\n</select>\n";
                $tempoutput =~ s/value=\"$dispmememail\"/value=\"$dispmememail\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>论坛中是否保密所有的用户 Email ？</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"flashavatar\">\n<option value=\"no\">不支持\n<option value=\"yes\">支持\n</select>\n";
                $tempoutput =~ s/value=\"$flashavatar\"/value=\"$flashavatar\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>上传头像是否支持 FLASH 格式</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>上传头像文件允许的最大值(单位：KB)</b><br>默认允许最大 200KB ！</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxuploadava" value="$maxuploadava" size=5 maxlength=5>　不要加 KB，建议不要超过 200</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333><b>论坛首页音乐名称</b>(如果没有请留空)<br>请输入背景音乐名称，背景音乐<BR>应上传于 non-cgi/midi 目录下。<br><b>不要包含 URL 地址或绝对路径！</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=20 name="midiaddr2" value="$midiaddr2">~;
                $midiabsaddr = "$imagesdir" . "midi/$midiaddr2";
                print qq~　<EMBED src="$imagesurl/midi/$midiaddr2" autostart="false" width=70 height=25 loop="true" align=absmiddle>~ if ((-e "$midiabsaddr")&&($midiaddr2 ne ""));
                print qq~
                </td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>只允许进入论坛的地区</b><br>非允许地区的 IP 将无法进入论坛，由于利用的是论坛内部的 IP 地址库，有误判断的可能性，<B>而且此选项还受 IP 禁止的约束</B>！</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="arrowformwhere" value="$arrowformwhere" size=20>　多个地区用逗号隔开，以市或省为单位</td>
                </tr>
		~;

                $tempoutput = "<select name=\"usefake\">\n<option value=\"no\">不使用\n<option value=\"yes\">使用\n</select>\n";
                $tempoutput =~ s/value=\"$usefake\"/value=\"$usefake\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=宋体 color=#333333><b>是否采用伪静态方式（具体看说明，服务器不支持的话，千万不要用）</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput <a href=leobbs.htm target=_blank>按此测试</a>，如果能看到论坛首页，说明服务器设置正确！<BR>如提示文件没有找到，那就说明未设置正确，请参考说明文档重新设置！</td>
                </tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
                ~;
                
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;

# 测试 SENDMAIL 路径
sub mailprogram
{
    $mailprogram='/usr/sbin/sendmail';
    if (!(-e $mailprogram)) {$mailprogram='/usr/bin/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/bin/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/lib/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/usr/slib/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/usr/lib/sendmail';};
    if (!(-e $mailprogram)) {$mailprogram='perlmail';}; 
    if (!(-e $mailprogram)) {$mailprogram="Unknow";};
    return $mailprogram;
}