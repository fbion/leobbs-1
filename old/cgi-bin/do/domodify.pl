#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

use strict;
use warnings;
use diagnostics;

require "cleanolddata.pl";
    &cleanolddata2;
    $helpurl = &helpfiles("遗忘密码");
    $helpurl = qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;

    if ("$userregistered" eq "no") {&error("修改资料&没有此用户名！"); }
    if ("$in_password" ne "$password") {&error("修改资料&论坛密码错误！请重新登录后修改！"); }
    if (("$passwordverification" eq "yes") && ("$emailfunctions" ne "off")) {
	$newpassneeded = "<br><B>如果您修改了邮件地址，一个新的论坛密码将通过邮件发给您。</B>";
	undef $newpasswordaddon;
    }
    $newpasswordaddon = qq~
<tr><td bgcolor=$miscbackone width=40%><font color=$fontcolormisc><b>论坛密码：</b> 请输入修改论坛密码，区分大小写<br>只能使用大小写字母和数字的组合,不得少于８位</td>
<td bgcolor=$miscbackone width=60%><input type=password name="newpassword1" maxlength=20>　$helpurl</td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>论坛密码： (至少8位)</b><br>再输一遍，以便确定！</td>
<td bgcolor=$miscbackone><input type=password name="newpassword2" maxlength=20>　$helpurl</td>
</tr><tr>
<td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
<font color=$fonthighlight><b>如果你不想修改论坛密码，请保持上面空白！</b></font></td></tr>
~;

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        &whosonline("$in_member_name\t个人资料\tnone\t修改<b>$in_member_name</b>的个人资料\t");
    }

    if ($avatars eq "on") {
        if ($arrowavaupload eq "on") {
            $avaupload = qq~<br>上传头像： <input type="file" size=20 name="addme">　上传自定义头像。<br>~;
        }
        else { undef $avaupload; }

    open (FILE, "${lbdir}data/lbava.cgi");
    my @images = <FILE>;
    close (FILE);
    chomp @images;

    $selecthtml .= qq~<option value="noavatar" selected>不要头像</option>\n~;
    $currentface = "noavatar";
    foreach (@images) {
	$totleavator=@images -1;
        $cleanavatar =  $_;
        $cleanavatar =~ s/\.(gif|jpg)$//i;
        if (($cleanavatar =~ /admin_/) && ($member_code eq "me")) { next; }
        if ($cleanavatar eq "$useravatar") {
	    $selecthtml .= qq~<option value="$cleanavatar" selected>$cleanavatar</option>\n~;
            $currentface = "$cleanavatar";
        }
        elsif (($cleanavatar eq "noavatar") && (!$useravatar)) {
        }
	else {
            $selecthtml .= qq~<option value="$cleanavatar">$cleanavatar</option>\n~;
        }
    }
	    
    $personalavatar =~ s/\$imagesurl/${imagesurl}/o;
    $avatarhtml = qq~
<script>
function showimage(){document.images.useravatars.src="$imagesurl/avatars/"+document.creator.useravatar.options[document.creator.useravatar.selectedIndex].value+".gif";}
</script>
<tr>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>个性图片：</b><br>您可以选择一个个性图片，当你发表时将显示在您的名字下方。<BR>如果你填写了下面的自定义头像部分，那么你的头像以自定义的为准。否则，请你留空自定义头像的所有栏目！<BR>
<br><b>关于自定义头像</b>：<br>你也可以在这里给出你自定义头像的 URL 地址，头像的高度和宽度(像素)。 如果不想要自定义头像，请将相应栏目全部留空！<BR>如果不填写头像的高度和宽度，则系统将自动判断并填入。<BR><BR>
<br><b>如果你不想要任何的头像，那么请首先在菜单上选“noavatar”，然后留空所有自定义头像的部分！</b><BR><br>
<BR>您也可以用虚拟形象功能来打造丰富多彩的个人形象，<a href=face.cgi><font color=$fonthighlight>请按此进入</font></a>。<BR>
</td>
<td bgcolor=$miscbackone valign=top>总头像个数： $totleavator 个。　<a href=viewavatars.cgi target=_blank><B>按此查看</B></a>所有头像名称列表。<BR>
<select name="useravatar" size=1 onChange="showimage()">
$selecthtml
</select>
<img src=$imagesurl/avatars/$currentface.gif name="useravatars" width=32 height=32 hspace=15><br><br><br>
$avaupload
<br>图像位置： <input type="text" name="newpersonalavatar" size="26" value="$personalavatar">　输入完整的 URL 路径。<br>
<br>图像宽度： <input type="text" name="newpersonalwidth" size="2" maxlength=3 value="$personalwidth">　必须是 20 -- $maxposticonwidth 之间的一个整数。<br>
<br>图像高度： <input type="text" name="newpersonalheight" size="2" maxlength=3 value="$personalheight">　必须是 20 -- $maxposticonheight 之间的一个整数。<br></td>
</td></tr>
~;
    }
    $userflag = "blank" if ($userflag eq "");
    $flaghtml = qq~
<script language="javascript">
function showflag(){document.images.userflags.src="$imagesurl/flags/"+document.creator.userflag.options[document.creator.userflag.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc><b>所在国家:</b><br>请选择你所在的国家。</td>
<td bgcolor=$miscbackone>
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
<option value="Czech_Republic">捷克</option>
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
<option value="Russia">俄罗斯</option>
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

    my ($getpassq, $getpassa) =split(/\|/,$userquestion); 
    $getpassFORM =qq~ 
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>论坛密码提示问题：</b>用于取得忘记了的论坛密码<br>最大 20 个字符（10个汉字）</td> 
<td bgcolor=$miscbackone><input type=text name="getpassq" value="$getpassq" size=20 maxlength=20></td> 
</tr> 
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>论坛密码提示答案：</b>配合上栏使用<br>最大 20 个字符（10个汉字）</td> 
<td bgcolor=$miscbackone><input type=text name="getpassa" value="$getpassa" size=20 maxlength=20></td> 
</tr><tr> 
<td bgcolor=$miscbacktwo valign=middle colspan=2 align=center> 
<font color=$fonthighlight><b>论坛密码提示问题和答案是不能够修改的，请谨慎输入！</b></font></td></tr>~ if(($userquestion eq "")||($userquestion eq "|"));

    $signature=$signatureorigin if ($signatureorigin);
    $signature="" if (($signatureorigin eq "")&&($signaturehtml eq ""));
    $signature =~ s/\[br\]/\n/isg;
    $signature =~ s/<br>/\n/isg;
    $signature =~ s/<p>/\n/isg;
    $signature =~ s/</&lt;/g;
    $signature =~ s/>/&gt;/g;
    $signature =~ s/\&amp;/\&/isg;
    $signature =~ s/&quot\;/\"/g;
    $signature =~ s/\&nbsp;/ /isg;
    $interests =~ s/<br>/\n/isg;
    $interests =~ s/<p>/\n/isg;
    $interests =~ s/\n+/\n/isg;

    $tempoutput = "<select name=\"newshowemail\">\n<option value=\"yes\">是\n<option value=\"msn\">MSN\n<option value=\"popo\">网易泡泡\n<option value=\"no\">否\n</select>\n";
    $tempoutput =~ s/value=\"$showemail\"/value=\"$showemail\" selected/;

    $output .= qq~
<script>
function chk(){
if(!document.creator.oldpassword.value){alert('为了安全，请输入目前论坛的密码。');document.creator.oldpassword.focus();return false;}
}
</script>
<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center>
<form action="$thisprog" method=post name="creator" enctype="multipart/form-data" onsubmit="return chk()">
<input type=hidden name="action" value="process">
<input type=hidden name="oldsex" value="$sex">
<input type=hidden name="membername" value="$in_member_name">
<font color=$fontcolormisc>修改 <font color=$fonthighlight><b>$in_member_name</b></font> 的个人资料</td></tr>
<tr><td bgcolor=$miscbacktwo width=40%><font color=$fonthighlight><b>目前论坛密码：</b> <U>为了安全，请先输入您目前的论坛密码</U></td>
<td bgcolor=$miscbacktwo width=60%><input type=password name="oldpassword" maxlength=20>　<font color=$fonthighlight>*</td>
</tr>
<tr><td bgcolor=$miscbacktwo valign=middle colspan=2 align=center></td></tr>
$newpasswordaddon$getpassFORM
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>邮件地址：</b><br>请输入有效的邮件地址，这将保证您在论坛中的私人资料。$newpassneeded</td>
<td bgcolor=$miscbackone><input type=text name="newemailaddress" value="$emailaddress"></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>显示邮件地址</b><br>
您是否希望在您发表文章之后显示您的邮件？</td>
<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
</tr>
~;

    $membertitle = "" if ($membertitle =~ m/^member$/i);
    if (($editusertitleself eq "post") && ($jifen >= $needpoststitle)) { $editusertitleself = "on"; }
    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>个人头衔：</b><BR>最大 20 个字符（10个汉字）</td>
<td bgcolor=$miscbackone><input type=text name="newmembertitle" value="$membertitle" size=14 maxlength=20></td>
</tr>
~ if ($editusertitleself eq "on");

    if (($editjhmpself eq "post") && (($numberofposts + $numberofreplys) >= $needpostsjhmp)) { $editjhmpself = "on"; }
    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>江湖门派：</b><BR>最大 20 个字符（10个汉字）</td>
<td bgcolor=$miscbackone><input type=text name="newjhmp" value="$jhmp" size=14 maxlength=20></td>
</tr>
~ if ($editjhmpself eq "on");

    if ($editjhmpself eq "system") {
	my $jumpfile="$lbdir" . "data/jhmp.cgi";
	open(FILE,$jumpfile);
	my @JUMP=<FILE>;
	close(FILE);
	chomp @JUMP;
	if($member_code eq "ad" || $member_code eq "smo"){
	    @JUMP = grep(/^(.+?)\t[1|0]\t/,@JUMP);
	} else {
            @JUMP1 = grep(/^$jhmp\t0\t/,@JUMP);
	    @JUMP = grep(/^(.+?)\t1\t/,@JUMP);
	    push(@JUMP,@JUMP1);
	}
	push(@JUMP,"");
	my $JUMP=join("\n",@JUMP);
	my $temp_c=0;
	$JUMP=~s/(.+?)\t[1|0]\t(.*?)\t\n/
	my $temp=$1;
	my $temp1=$2;
	$temp=qq(<option value="$temp_c">$temp　　[创始人：$temp1]<\/option>);
	$temp_c++;
	$temp;
	/ge;
	$JUMP=qq(<option value="1000">无门无派</option>$JUMP);
	my $jhmp_c=quotemeta($jhmp);
	$JUMP=~s/<option value="([0-9]+)">$jhmp_c　　\[(.+?)\]<\/option>/<option value="$1" selected>$jhmp　　\[$2\]<\/option>/;
	$output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>江湖门派：</b><BR>请选择一个您喜欢的门派</td>
<td bgcolor=$miscbackone><select name="newjhmp">$JUMP</select></td>
</tr>
~;
    }

    $tempoutput = "<select name=\"newsex\" size=\"1\"><option value=\"no\">保密 </option><option value=\"m\">帅哥 </option><option value=\"f\">美女 </option></select>\n";
    $tempoutput =~ s/value=\"$sex\"/value=\"$sex\" selected/;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>性别：</b></td>
<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
</tr>
~;

    $tempoutput = "<select name=\"neweducation\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"小学\">小学 </option><option value=\"初中\">初中 </option><option value=\"高中\">高中</option><option value=\"中专\">中专</option><option value=\"大专\">大专</option><option value=\"本科\">本科</option><option value=\"硕士\">硕士</option><option value=\"博士\">博士</option><option value=\"博士后\">博士后</option></select>\n";
    $tempoutput =~ s/value=\"$education\"/value=\"$education\" selected/;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>最高学历：</b></td>
<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
</tr>
~;

    $tempoutput = "<select name=\"newmarry\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"未婚\">未婚 </option><option value=\"已婚\">已婚 </option><option value=\"离婚\">离婚 </option><option value=\"丧偶\">丧偶 </option></select>\n";
    $tempoutput =~ s/value=\"$marry\"/value=\"$marry\" selected/;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>婚姻状况：</b></td>
<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
</tr>
~;

    $tempoutput = "<select name=\"newwork\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"计算机业\">计算机业 </option><option value=\"金融业\">金融业 </option><option value=\"商业\">商业 </option><option value=\"服务行业\">服务行业 </option><option value=\"教育业\">教育业 </option><option value=\"学生\">学生 </option><option value=\"工程师\">工程师 </option><option value=\"主管，经理\">主管，经理 </option><option value=\"政府部门\">政府部门 </option><option value=\"制造业\">制造业 </option><option value=\"销售/广告/市场\">销售/广告/市场 </option><option value=\"失业中\">失业中 </option></select>\n";
    $tempoutput =~ s/value=\"$work\"/value=\"$work\" selected/;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>职业状况：</b></td>
<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
</tr>
~;

    ($year, $month, $day) = split(/\//, $born);
    $tempoutput1 = "<select name=\"newmonth\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option></select>\n";
    $tempoutput1 =~ s/value=\"$month\"/value=\"$month\" selected/;

    $tempoutput2 = "<select name=\"newday\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option><option value=\"13\">13</option><option value=\"14\">14</option><option value=\"15\">15</option><option value=\"16\">16</option><option value=\"17\">17</option><option value=\"18\">18</option><option value=\"19\">19</option><option value=\"20\">20</option><option value=\"21\">21</option><option value=\"22\">22</option><option value=\"23\">23</option><option value=\"24\">24</option><option value=\"25\">25</option><option value=\"26\">26</option><option value=\"27\">27</option><option value=\"28\">28</option><option value=\"29\">29</option><option value=\"30\">30</option><option value=\"31\">31</option></select>\n";
    $tempoutput2 =~ s/value=\"$day\"/value=\"$day\" selected/;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>生日：</b>如不想填写，请全部留空。此项可选</td>
<td bgcolor=$miscbackone><font color=$fontcolormisc><input type="text" name="newyear" size=4 maxlength=4 value="$year">年$tempoutput1月$tempoutput2日</font></td>
</tr>
~;

    if ($usersx eq "") {$usersx = "blank"};

    $tempoutput="<SELECT name=\"usersx\" onchange=showsx() size=\"1\"> <OPTION value=blank>保密</OPTION> <OPTION value=\"sx1\">子鼠</OPTION> <OPTION value=\"sx2\">丑牛</OPTION> <OPTION value=\"sx3\">寅虎</OPTION> <OPTION value=\"sx4\">卯兔</OPTION> <OPTION value=\"sx5\">辰龙</OPTION> <OPTION value=\"sx6\">巳蛇</OPTION> <OPTION value=\"sx7\">午马</OPTION> <OPTION value=\"sx8\">未羊</OPTION> <OPTION value=\"sx9\">申猴</OPTION> <OPTION value=\"sx10\">酉鸡</OPTION> <OPTION value=\"sx11\">戌狗</OPTION> <OPTION value=\"sx12\">亥猪</OPTION></SELECT>\n";
    $tempoutput =~ s/value=\"$usersx\"/value=\"$usersx\" selected/;

    $output.=qq~
<SCRIPT language=javascript>
function showsx(){document.images.usersxs.src="$imagesurl/sx/"+document.creator.usersx.options[document.creator.usersx.selectedIndex].value+".gif";}
</SCRIPT>
<tr><td bgcolor=$miscbackone vAlign=top><font color=$fontcolormisc><b>所属生肖：</b>请选择你所属的生肖。</td>
<td bgcolor=$miscbackone>$tempoutput<IMG border=0 name=usersxs src=$imagesurl/sx/$usersx.gif align=absmiddle>
</TD></TR>
~;
    if ($userxz eq "") {$userxz = "blank"};
    $tempoutput="<SELECT name=\"userxz\" onchange=showxz() size=\"1\"> <OPTION value=blank>保密</OPTION> <OPTION value=\"z1\">白羊座(3月21--4月19日)</OPTION> <OPTION value=\"z2\">金牛座(4月20--5月20日)</OPTION> <OPTION value=\"z3\">双子座(5月21--6月21日)</OPTION> <OPTION value=\"z4\">巨蟹座(6月22--7月22日)</OPTION> <OPTION value=\"z5\">狮子座(7月23--8月22日)</OPTION> <OPTION value=\"z6\">处女座(8月23--9月22日)</OPTION> <OPTION value=\"z7\">天秤座(9月23--10月23日)</OPTION> <OPTION value=\"z8\">天蝎座(10月24--11月21日)</OPTION> <OPTION value=\"z9\">射手座(11月22--12月21日)</OPTION> <OPTION value=\"z10\">魔羯座(12月22--1月19日)</OPTION> <OPTION value=\"z11\">水瓶座(1月20--2月18日)</OPTION> <OPTION value=\"z12\">双鱼座(2月19--3月20日)</OPTION></SELECT>\n";
    $tempoutput =~ s/value=\"$userxz\"/value=\"$userxz\" selected/;
    $output.=qq~
<SCRIPT language=javascript>
function showxz(){document.images.userxzs.src="$imagesurl/star/"+document.creator.userxz.options[document.creator.userxz.selectedIndex].value+".gif";}
</SCRIPT>
<tr><td bgcolor=$miscbackone vAlign=top><font color=$fontcolormisc><b>所属星座：</b>请选择你所属的星座。<br>如果你正确输入了生日的话，那么此项无效！</td>
<td bgcolor=$miscbackone>$tempoutput<IMG border=0 height=15 name=userxzs src=$imagesurl/star/$userxz.gif width=15 align=absmiddle>
</TD></TR>
~;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>主页地址：</b><br>如果您有主页，请输入主页地址。此项可选</td>
<td bgcolor=$miscbackone><input type=text name="newhomepage" value="$homepage"></td>
</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>OICQ 号：</b><br>如果您有 OICQ，请输入号码。此项可选</td>
<td bgcolor=$miscbackone><input type=text name="newoicqnumber" value="$oicqnumber"></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>ICQ 号：</b><br>如果您有 ICQ，请输入号码。此项可选</td>
<td bgcolor=$miscbackone><input type=text name="newicqnumber" value="$icqnumber"></td>
</tr>$flaghtml<tr>
<script src=$imagesurl/images/comefrom.js></script>
<body onload="init()">
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>来自：</b><br>请输入您所在的地方。此项可选</td>
<td bgcolor=$miscbackone>
省份 <select name="province" onChange = "select()"></select>　城市 <select name="city" onChange = "select()"></select><br>
我在 <input type=text name="newlocation" value="$location" maxlength=12 size=20 style="font-weight: bold">　不能超过12个字符（6个汉字）</td>
</tr><tr>
~;

    $timedifference = 0 if ($timedifference eq '');
    $tempoutput = "<select name=\"newtimedifference\"><option value=\"-23\">- 23</option><option value=\"-22\">- 22</option><option value=\"-21\">- 21</option><option value=\"-20\">- 20</option><option value=\"-19\">- 19</option><option value=\"-18\">- 18</option><option value=\"-17\">- 17</option><option value=\"-16\">- 16</option><option value=\"-15\">- 15</option><option value=\"-14\">- 14</option><option value=\"-13\">- 13</option><option value=\"-12\">- 12</option><option value=\"-11\">- 11</option><option value=\"-10\">- 10</option><option value=\"-9\">- 9</option><option value=\"-8\">- 8</option><option value=\"-7\">- 7</option><option value=\"-6\">- 6</option><option value=\"-5\">- 5</option><option value=\"-4\">- 4</option><option value=\"-3\">- 3</option><option value=\"-2\">- 2</option><option value=\"-1\">- 1</option><option value=\"0\">0</option><option value=\"1\">+ 1</option><option value=\"2\">+ 2</option><option value=\"3\">+ 3</option><option value=\"4\">+ 4</option><option value=\"5\">+ 5</option><option value=\"6\">+ 6</option><option value=\"7\">+ 7</option><option value=\"8\">+ 8</option><option value=\"9\">+ 9</option><option value=\"10\">+ 10</option><option value=\"11\">+ 11</option><option value=\"12\">+ 12</option><option value=\"13\">+ 13</option><option value=\"14\">+ 14</option><option value=\"15\">+ 15</option><option value=\"16\">+ 16</option><option value=\"17\">+ 17</option><option value=\"18\">+ 18</option><option value=\"19\">+ 19</option><option value=\"20\">+ 20</option><option value=\"21\">+ 21</option><option value=\"22\">+ 22</option><option value=\"23\">+ 23</select>";
    $tempoutput =~ s/value=\"$timedifference\"/value=\"$timedifference\" selected/;

    $output .= qq~
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>时差：</b><br>
服务器所在时区：$basetimes<br>如果您所在的位置和服务器有时差，请输入。<br>以后您看到所有的时间将按照您所在的地区时间显示。</td>
<td bgcolor=$miscbackone>$tempoutput</td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>自我简介： </b><BR>不能超过 <B>$maxinsline</B> 行，也不能超过 <B>$maxinslegth</B> 个字符<br><br>您可以输入您的个人简介。此项可选</td>
<td bgcolor=$miscbackone><textarea name="newinterests" cols="60" rows="5">$interests</textarea></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>签名：</b><br>不能超过 <B>$maxsignline</B> 行，也不能超过 <B>$maxsignlegth</B> 个字符
<br><br>不能使用 HTML 标签<br>可以使用 <a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS 标签</a><BR>
<li>贴图标签　: <b>$signpicstates</b><li>Flash 标签: <b>$signflashstates</b><li>音乐标签　: <b>$signsoundstates</b><li>文字大小　: <b>$signfontsizestates</b>
</td>
<td bgcolor=$miscbackone><textarea name="newsignature" cols="60" rows="8">$signature</textarea></td>
</tr>
$avatarhtml
<tr><td colspan=2 bgcolor=$miscbacktwo align=center><input type=submit value="提 交" name=submit></td>
</form></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
1;
