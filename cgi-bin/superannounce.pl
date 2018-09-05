#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################
sub superanndo {
$superannounce=&HTML($superannounce); $superannounce =~ s/\n/<BR>/isg; $superannounce =~ s/\t/\n/isg;
$superannouncedisp = "oncepersession" if ($superannouncedisp eq "");
$superannouncehide = "yes" if ($superannouncehide eq "");
$output .= qq~
<style type="text/css">
#fadeinbox{position:absolute;width:350px;left:0;top:-400px;border:2px $titleborder;background-color:$menubackground;padding:4px;z-index:100;visibility:hidden;}
</style>
<script>
var ie55="";
var agent=navigator.userAgent.toLowerCase();
if (document.all){var version=parseFloat(agent.substr(agent.indexOf("msie")+5,3));
if (version>=5.5) ie55="yes";
}
var displaymode="$superannouncedisp"
var autohidebox=["$superannouncehide",20]
var showonscroll="yes"
var enablefade="yes"
var IEfadelength=1
var Mozfadedegree=0.05
if (parseInt(displaymode)!=NaN)
var random_num=Math.floor(Math.random()*displaymode)
function displayfadeinbox(){
var ie=document.all && !window.opera
var dom=document.getElementById
iebody=(document.compatMode=="CSS1Compat")? document.documentElement:document.body
objref=(dom)? document.getElementById("fadeinbox"):document.all.fadeinbox
var scroll_top=(ie)? iebody.scrollTop:window.pageYOffset
var docwidth=(ie)? iebody.clientWidth:window.innerWidth
docheight=(ie)? iebody.clientHeight: window.innerHeight
var objwidth=objref.offsetWidth
objheight=objref.offsetHeight
objref.style.left=docwidth/2-objwidth/2+"px"
objref.style.top=scroll_top+docheight/2-objheight/2+"px"
if (showonscroll=="yes") showonscrollvar=setInterval("staticfadebox()",50)
if (ie55=="yes" && enablefade=="yes" && objref.filters){
eval(objref.filters[0].duration=IEfadelength)
eval(objref.filters[0].Apply())
eval(objref.filters[0].Play())
}
objref.style.visibility="visible"
if (objref.style.MozOpacity){
if (enablefade=="yes")
mozfadevar=setInterval("mozfadefx()",90)
else{
objref.style.MozOpacity=1
controlledhidebox()
}}
else
controlledhidebox()
}
function mozfadefx(){
if (parseFloat(objref.style.MozOpacity)<1)
objref.style.MozOpacity=parseFloat(objref.style.MozOpacity)+Mozfadedegree
else{
clearInterval(mozfadevar)
controlledhidebox()
}}
function staticfadebox(){
var ie=document.all && !window.opera
var scroll_top=(ie)? iebody.scrollTop:window.pageYOffset
objref.style.top=scroll_top+docheight/2-objheight/2+"px"
}
function hidefadebox(){
objref.style.visibility="hidden"
if (typeof showonscrollvar!="undefined")
clearInterval(showonscrollvar)
document.cookie="fadedin=no"
}
function controlledhidebox(){
if (autohidebox[0]=="yes"){
var delayvar=(enablefade=="yes" && objref.filters)? (autohidebox[1]+objref.filters[0].duration)*1000:autohidebox[1]*1000
setTimeout("hidefadebox()",delayvar)
}}
function initfunction(){
setTimeout("displayfadeinbox()",100)
}
function get_cookie(Name) {
var search=Name+"="
var returnvalue=""
if (document.cookie.length>0) {
offset=document.cookie.indexOf(search)
if (offset != -1) {
offset+=search.length
end=document.cookie.indexOf(";",offset)
if (end == -1)
end=document.cookie.length;
returnvalue=unescape(document.cookie.substring(offset, end))
}}
return returnvalue;
}
if (displaymode=="oncepersession" && get_cookie("fadedin")=="" || displaymode=="always" && get_cookie("fadedin")!="no" || parseInt(displaymode)!=NaN && random_num==0 && get_cookie("fadedin")!="no"){
if (window.addEventListener)
window.addEventListener("load",initfunction,false)
else if (window.attachEvent)
window.attachEvent("onload",initfunction)
else if (document.getElementById)
window.onload=initfunction
document.cookie="fadedin=yes"
}
</script>
<DIV id=fadeinbox style="filter:progid:DXImageTransform.Microsoft.RandomDissolve(duration=1) progid:DXImageTransform.Microsoft.Shadow(color=gray,direction=135) ; -moz-opacity:0">
<table border=0 width=350 cellspacing=0 cellpadding=2 bgcolor=$titleborder><tr><td width=100%><table border=0 width=100% bgcolor=$menubackground cellspacing=4 cellpadding=2>
<tr><td width=100%><center><B><font color=$fonthighlight>* 超 级 公 告 *</font></B></center><img src="" width=0 height=3><BR>
$superannounce<BR><BR>
<div align=right><span style=cursor:hand onClick="hidefadebox();return false">[关闭显示] </span></div>
</td></tr></table></td></tr></table></div>
~;
}
1;
