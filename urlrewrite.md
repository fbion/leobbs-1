LeoBBS X �װ�������̳˵���ĵ� A:visited{TEXT-DECORATION: none} A:active{TEXT-DECORATION: none} A:hover{TEXT-DECORATION: underline overline} A:link{text-decoration: none;} .h { font-family: ����; font-size: 12px; color: #FF0000 } .t { font-family: ����; font-size: 11px; color: #000003 } .ti { font-family: ����; font-size: 12px; color: #000003; font-weight: bold } .l { font-family: ����; font-size: 14px; font-weight: bold; color: #FFFFFF } BODY{FONT-FAMILY: ����; FONT-SIZE: 9pt;} caption,TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: ����; FONT-SIZE: 9pt} INPUT,textarea, SUBMIT { font-family: ����; font-size: 9pt; font-family: ����; vertical-align:middle; background-color: #efefef; } a:active, a:link, a:visited { color:#000099 }

�װ����ᳬ����̳ LeoBBS X ˵���ĵ�

.

  
**α��̬��ʵ�֣�**  
  
  
һ. APACHE 1.3.x & 2.X  
  
  
  
������ͨ������£��� addon Ŀ¼�µ� .htaccrss �ļ����Ƶ��� cgi-bin �£��� CGI �����ļ���һ��Ȼ��ֱ�ӿ��ڡ��������輴�ɣ��������������Բ��ɹ�����ô�밴������Ĳ����ֹ����ã�  
  
  
����1. �� apache/conf/httpd.conf �ļ����������������У�����������ǰ��� # ȥ��(����ڶ��е������Ҳ��������Թ�)��  
  
#LoadModule rewrite\_module modules/mod\_rewrite.so  
#AddModule mod\_rewrite.c  
  
  
����2. �������������������������ݣ����ڰ�װ·����ͬ�����ܻ��в��죬����ϸ����һ�£���  
  
<Directory "d:/Apache/htdocs/cgi-bin">  
  
�ڴ�����ֱ�������������  
  
AddHandler cgi-script .cgi .md .pl  
  
����Ȼ�󿴽���ȥ�ļ��У������� None �ĳ� All��������������ӣ�����һ�¾Ϳ����ˣ���  
  
AllowOverride All  
  
Options All  
  
  
  
  
  
����3. �ڴ��ļ���������������Ρ�  
  
RewriteEngine On  
  
RewriteRule ^(.\*)/topic-(\[0-9\]+)-(\[0-9\]+)-(\[0-9\]+)-(\[0-9\]+)-(.\*)\\.md$ $1/topic\\.cgi\\?forum=$2&topic=$3&start=$4&show=$5&replynum=$6  
  
RewriteRule ^(.\*)/leobbs\\.md$ $1/leobbs\\.cgi  
  
RewriteRule ^(.\*)/leobbs-(.+)\\.md$ $1/leobbs\\.cgi?action=$2  
  
RewriteRule ^(.\*)/announcements\\.md$ $1/announcements\\.cgi  
  
RewriteRule ^(.\*)/announcements-(.+)\\.md$ $1/announcements\\.cgi?forum=$2  
  
RewriteRule ^(.\*)/profile-(.\*)\\.md$ $1/profile\\.cgi\\?action=show&member=$2  
  
RewriteRule ^(.\*)/view-(\[0-9\]+)-(\[0-9\]+)\\.md$ $1/view\\.cgi\\?forum=$2&topic=$3  
  
RewriteRule ^(.\*)/forums-(\[0-9\]+)-(\[0-9\]+)\\.md$ $1/forums\\.cgi\\?forum=$2&show=$3  
  
RewriteRule ^(.\*)/printpage-(\[0-9\]+)-(\[0-9\]+)\\.md$ $1/printpage\\.cgi\\?forum=$2&topic=$3  
  
  
  
����4. �������� Apache ����ֻҪû����ʾ����α��̬�ķ������˰�װ��������ˡ�  
  
  
  
��. IIS 5.0 & 6.0  
  
  
  
����1. �� addon Ŀ¼�µ� Rewrite.rar ��ѹ����Ŀ¼�� Rewrite �¡�  
  
  
  
����2. �� Rewrite Ŀ¼������������ĳ·���¡�  
  
  
  
����3. �򿪡�������塱���������ߡ�����IIS��Ϣ�����������������վ����������վ�㡱�������ԡ���  
  
  
  
����4. �ڡ�ISAPIɸѡ������������ӡ���ɸѡ���������� Rewrite����ִ���ļ�Ϊ Rewrite Ŀ¼�µ� Rewrite.dll��ͨ���������ָ�����Ե�ַ����  
  
  
  
����5. ���� IIS��ֻҪû����ʾ����α��̬�ķ������˰�װ��������ˡ�  
  
  
  
��.�������е����ã�  
  
  
  
�������ڷ����������ú�α��̬���ǲ����ģ������ڳ����д�α��̬��֧�ֿ��أ���¼�װ���̳�Ĺ��������ڡ������������á�����󣬡��Ƿ����α��̬��ʽ�����к��棬�㡰���˲��ԡ����������������̳��ҳ����˵�����óɹ���Ȼ�����Ŀѡ��ʹ�á������漴�ɣ������ʾ���ǡ��ļ�û���ҵ�����404���󡱣��Ǿ�˵�����ô������������ã�  
  
  
  
ע�������������û�о������ã����ߡ����˲��ԡ���ʱ��û�п�����������̳��ҳ����ôǧ��Ҫ�ڳ���˴�α��̬��ʽ��������̳���޷�����ʹ�ã�  
  
  
  

  
  

* * *

��Ȩ���У�[�װ��Ƽ�](http://www.leobbs.com) & [�װ����ᳬ����̳](http://bbs.leobbs.com)����Copyright 2000-2005