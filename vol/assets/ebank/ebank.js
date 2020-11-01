<!--
function displaytime()
{
	time = new Date();
	year = time.getYear();
	month = time.getMonth() + 1;
	if (month < 10) month = "0" + month;
	day = time.getDate();
	if (day < 10) day = "0" + day;
	hour = time.getHours();
	if (hour < 10) hour = "0" + hour;
	minute = time.getMinutes();
	if (minute < 10) minute = "0" + minute;
	second = time.getSeconds();
	if (second < 10) second = "0" + second;
	showtime.innerHTML = year + "/" + month + "/" + day + " " + hour + ":" + minute + ":" + second;
	setTimeout("displaytime()", 1000);
}

function btransfriend()
{
	var friend = document.btrans.friends.options[document.btrans.friends.selectedIndex].value;
	if (friend != "") document.btrans.btransuser.value = friend;
}

function postfriend()
{
	var friend = document.post.friends.options[document.post.friends.selectedIndex].value;
	if (friend != "") document.post.postuser.value = friend;
}

clickmmtimes = 1;
function DoKiss()
{
	if (clickmmtimes > 9)
	{
		clickmmtimes = 1;
		if (confirm("干什么? 想和人家约会吗? 先给人家买束花吧...\n才 50 块钱 :) 人家可是本银行第一美女哟。"))
		{
			window.open("ebankkiss.cgi", "", "width=118, height=118, resizable=0, scrollbars=no, menubar=no, status=no");
			setTimeout("Refresh()", 2000);
		}
		else
		{
			alert("啊, 没钱还想泡本小姐? 非礼阿...\n保安, 快把这个家伙赶出去!");
			this.close();
		}
	}
	else
	{
		clickmmtimes++;
	}
}

refreshpage = 0;
function Refresh()
{
	if (refreshpage = 1) this.location.reload();
	refreshpage++;
}
-->