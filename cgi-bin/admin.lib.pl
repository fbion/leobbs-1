#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

use strict;
use warnings;
use diagnostics;

sub getadmincheck {
    my $currenttime = time;
    $memberfilename = $inmembername;
    $memberfilename =~ y/ /_/;
    $memberfilename =~ tr/A-Z/a-z/;
    $memberfilename = "${lbdir}verifynum/login/$memberfilename.cgi";

    if (-e $memberfilename) {
        open(FILE, "$memberfilename");
        my $logintime = <FILE>;
        close(FILE);
        chomp $logintime;
        if ($currenttime > $logintime + 900) {
            # 管理员登录如果15分钟未做任何操作，需要重新登录
            unlink("$memberfilename");
            print "Set-Cookie: adminpass=\"\"\n";
            $inpassword = "";
        }
        else {
            open(FILE, ">$memberfilename");
            print FILE "$currenttime\n";
            close(FILE);
        }

    }
    else {
        print "Set-Cookie: adminpass=\"\"\n";
        $inpassword = "";
    }
}

sub adminlogin {
    $inmembername =~ s/\_/ /g;
    if ($useverify eq "yes") {

        if ($verifyusegd ne "no") {
            eval ('use GD;');
            if ($@) {
                $verifyusegd = "no";
            }
        }
        if ($verifyusegd eq "no") {
            $houzhui = "bmp";
        }
        else {
            $houzhui = "png";
        }

        require 'verifynum.cgi';
    }
    $loginprog = $thisprog if ($loginprog eq "");
    print qq~
<tr><td bgcolor="#2159C9" colspan=2><font color=#FFFFFF>
<b>欢迎来到 LeoBBS 论坛管理中心</b>
</td></tr>
<form action=admin.cgi method=post>
<input type=hidden name=action value=login>
<input type=hidden name=loginprog value=$loginprog>
<tr><td bgcolor=#EEEEEE valign=middle colspan=2 align=center><font color=#333333><b>请输入您的用户名、密码登录</b></font></td></tr>
<tr><td bgcolor=#FFFFFF valign=middle width=40% align=right><BR><font color=#555555>请输入您的用户名</font></td>
<td bgcolor=#FFFFFF valign=middle><BR><input type=text name=membername value="$inmembername" maxlength=15></td></tr>
<tr><td bgcolor=#FFFFFF valign=middle width=40% align=right><font color=#555555>请输入您的密码</font></td>
<td bgcolor=#FFFFFF valign=middle><input type=password name=password maxlength=20></td></tr>
~;
    print qq~<tr><td bgcolor=#FFFFFF valign=middle width=40% align=right><font color=#555555>请输入右边图片的数字</font></td><td bgcolor=#FFFFFF valign=middle><input type=hidden name=sessionid value="$sessionid"><input type=text name="verifynum" size=4 maxlength=4>　　<img src=$imagesurl/verifynum/$sessionid.$houzhui border=0 align=absmiddle> 如果看不清，请刷新本页</td></tr>~ if ($useverify eq "yes");
    print qq~<tr><td bgcolor=#FFFFFF valign=middle colspan=2 align=center><BR><input type=submit name=submit value="登 录"></form></td></tr>
<tr><td bgcolor=#FFFFFF valign=middle align=left colspan=2><font color=#555555>
<blockquote><b>请注意:</b><p><b>只有论坛的坛主才能登录论坛管理中心。未经过授权的尝试登录行为将会被记录在案！</b><p>在进入论坛管理中心前，请确定你的浏览器打开了 Cookie 选项。<br> Cookie 只会存在于当前的浏览器进程中。为了安全起见，当你关闭了浏览器后，Cookie 会失效并被自动删除。</blockquote>
</td></tr></table></td></tr></table>
~;
}

sub admintitle {
    print qq~
<html>
<head>
<title>LeoBBS - 论坛管理中心</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style>
BODY {BACKGROUND: #799ae1; FONT: 9pt 宋体;}
TABLE {BORDER-BOTTOM: 0px; BORDER-LEFT: 0px; BORDER-RIGHT: 0px; BORDER-TOP: 0px}
TD {FONT: 12px 宋体}
IMG {BORDER-BOTTOM: 0px; BORDER-LEFT: 0px; BORDER-RIGHT: 0px; BORDER-TOP: 0px;}
A {COLOR: #215dc6; FONT: 12px 宋体; TEXT-DECORATION: none}
A:hover {COLOR: #428eff}
.sec_menu {BACKGROUND: #d6dff7; BORDER-BOTTOM: white 1px solid; BORDER-LEFT: white 1px solid; BORDER-RIGHT: white 1px solid; OVERFLOW: hidden}
.menu_title {}
.menu_title SPAN {COLOR: #215dc6; FONT-WEIGHT: bold; LEFT: 8px; POSITION: relative; TOP: 2px}
.menu_title2 {}
.menu_title2 SPAN {COLOR: #428eff; FONT-WEIGHT: bold; LEFT: 8px; POSITION: relative; TOP: 2px}
</STYLE>
<script language="javascript"> 
function save_changes() { document.the_form.process.value="true"; } 
function preview_template() {document.the_form.target="_blank"; document.the_form.process.value="preview template";}
</script>

</head>
<body alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=2>

<table width=97% cellpadding=0 cellspacing=0 bgcolor=#483D95 align=center valign=top>
<tr><td>
  <table width=100% cellpadding=0 cellspacing=0>
  <tr><td width=17% valign=top bgcolor=#799ae1>
    <table width=100% cellpadding=6 cellspacing=0>
	<tr><td bgcolor=#799ae1>
	<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <tr>
          <TD vAlign=top><IMG src="$imagesurl/images/title.gif" width=200 height=38><BR>
	  <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=20 align=center><font color=#336333><b>注：总斑竹可操作带 (*) 的项目</b></TD></TR>
	  </TABLE>
	</TD></TR>
 	</TABLE>
        </td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● 管理导航</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="admin.cgi">管理中心首页(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="leobbs.cgi">进入您的论坛(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="indexshow.cgi">首页JavaScript调用向导</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="admin.cgi?action=logout">退出管理中心(*)</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● 用户管理</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="setmembers.cgi">用户管理/排名(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="usermanager.cgi">用户分类/管理(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="cansale.cgi">帖子买卖用户管理(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setmemberbak.cgi">用户库备份/还原</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="resetusr.cgi">用户数据清空重置</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● 注册管理</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="noreg.cgi">保留特殊用户名(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="noregemail.cgi">保留特殊 Email(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setallowemail.cgi">限制(允许)可注册的邮箱名(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="noregip.cgi">禁止特殊 IP 注册用户(*)</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● 论坛管理</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="setforums.cgi">论坛设置和管理</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setcatedisplay.cgi">论坛区信息排列模式</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="merge.cgi">合并论坛</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="adbackup.cgi">论坛备份到本地/还原</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="shareforums.cgi">联盟论坛管理</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="rebuildall.cgi">重建所有论坛</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="rebuildmain.cgi">重新建立论坛主界面(*)</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● 设置管理</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="foruminit.cgi">初始化论坛数据</a> <B>(注)</B></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setstyles.cgi">默认风格设置</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setvariables.cgi">基本变量设置</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setmpic.cgi">论坛颜色&图片设置</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setbank.cgi">社区银行设置</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setcity.cgi">社区货币设置</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setawards.cgi">社区勋章管理</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setmembertitles.cgi">用户等级设置</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setjhmp.cgi">社区门派管理器</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setemoticon.cgi">表情转换设置管理</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setemotes.cgi">EMOTE 设置</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setad.cgi">帖子随机广告管理器</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● 限制管理</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="setbadwords.cgi">词语自动转换</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setfilter.cgi">不良词语过滤(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setipbans.cgi">IP 禁止(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setidbans.cgi">ID 禁止(*)</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● 特殊功能</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="exportemail.cgi">导出会员 Email 地址</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="massmsg.cgi">短消息广播</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="mailmembers.cgi">Email 群发</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="filemanage.cgi">论坛文件超级管理器</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setplugin.cgi">论坛插件设定</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setskin.cgi">管理区插件设定</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● 论坛编辑</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="setregrules.cgi">修改注册声明</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setregmsg.cgi">修改短消息欢迎信息</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="settemplate.cgi">编辑论坛模板</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setcss.cgi">论坛 CSS 代码生成</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="newstyles.cgi">新建/修改风格文件</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● 其它设置</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="userratinglog.cgi">用户威望积分操作日志(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="baddellogs.cgi">论坛安全日志</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="adminloginlogs.cgi">管理区安全日志</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="sizecount.cgi">统计论坛占用空间</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="vercheck.cgi">论坛版本/更新</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>
    ~;

    if (-e "${lbdir}data/leoskin.cgi") {
        eval {require "${lbdir}data/leoskin.cgi";};
        if ($@) {
        }
        else {
            if ($skin1name ne "") {
                print qq~
<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● 论坛插件</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
	~;
                print qq~<TR><TD height=18>&nbsp;>> <a href="$skin1url">$skin1name</a></TD></TR>~ if ($skin1name ne "");
                print qq~<TR><TD height=18>&nbsp;>> <a href="$skin2url">$skin2name</a></TD></TR>~ if ($skin2name ne "");
                print qq~<TR><TD height=18>&nbsp;>> <a href="$skin3url">$skin3name</a></TD></TR>~ if ($skin3name ne "");
                print qq~<TR><TD height=18>&nbsp;>> <a href="$skin4url">$skin4name</a></TD></TR>~ if ($skin4name ne "");
                print qq~<TR><TD height=18>&nbsp;>> <a href="$skin5url">$skin5name</a></TD></TR>~ if ($skin5name ne "");
                print qq~<TR><TD height=18>&nbsp;>> <a href="$skin6url">$skin6name</a></TD></TR>~ if ($skin6name ne "");
                print qq~<TR><TD height=18>&nbsp;>> <a href="$skin7url">$skin7name</a></TD></TR>~ if ($skin7name ne "");
                print qq~<TR><TD height=18>&nbsp;>> <a href="$skin8url">$skin8name</a></TD></TR>~ if ($skin8name ne "");
                print qq~<TR><TD height=18>&nbsp;>> <a href="$skin9url">$skin9name</a></TD></TR>~ if ($skin9name ne "");
                print qq~<TR><TD height=18>&nbsp;>> <a href="$skin10url">$skin10name</a></TD></TR>~ if ($skin10name ne "");
                print qq~</TABLE></TD></TR></TABLE></td></tr>~;
            }
        }
    }

    print qq~
<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● 管理导航</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="admin.cgi">管理中心首页(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="leobbs.cgi">进入您的论坛(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="admin.cgi?action=logout">退出管理中心(*)</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>● LeoBBS 信息</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;程序版本: $versionnumber</TD></TR>
              <TR><TD height=18>&nbsp;版权所有: 山鹰(糊)、花无缺</TD></TR>
              <TR><TD height=18>&nbsp;技术支持: <a href="http://bbs.leobbs.com/" target=_blank>极酷超级论坛</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

</table>
    </td><td width=70% valign=top bgcolor=#ffffff>
    <table width=100% cellpadding=5 cellspacing=0><tr><td bgcolor=#799ae1><img src=$imagesurl/images/none.gif width=0 height=6></td></tr></table><table width=100% cellpadding=6 cellspacing=0><tr><td bgcolor=#799ae1>
    ~;
}
1;  
