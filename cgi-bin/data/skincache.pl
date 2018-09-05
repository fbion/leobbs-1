$pluginadd = qq~
<script>
linkset[2]='<center><div class="menuitems"><a href="http://www.leobbs.com/plugin/rili.htm" target=_blank><font color=#000000>社区日历</font></a></div><div class="menuitems"><a href="http://www.leobbs.com/plugin/tfk.htm" target=_blank><font color=#000000>填方块</font></a></div><div class="menuitems"><a href="http://www.leobbs.com/plugin/elsfk.htm" target=_blank><font color=#000000>俄罗斯方块</font></a></div><div class="menuitems"><a href="http://www.leobbs.com/plugin/mary/mary.htm" target=_blank><font color=#000000>超级玛丽</font></a></div><div class="menuitems"><a href="http://www.leobbs.com/plugin/ppl/index.html" target=_blank><font color=#000000>泡泡龙</font></a></div></center>'
</script>
~;
$loggedinas .= qq~<img src=$imagesurl/images/fg.gif width=1> <span style=cursor:hand onMouseover="showmenu(event,linkset[2])" onMouseout="delayhidemenu()">插件&nbsp;</span>~;
1;
