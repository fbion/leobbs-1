function setCookie (name, value) {
  var exp = new Date();exp.setTime(exp.getTime() + 2*60*60*1000);
  document.cookie = name + "=" + escape(value) + "; expires=" + exp.toGMTString() +"; path=/";
}

function getCookie(name) {
  var search;
  search = name + "="
  offset = document.cookie.indexOf(search) 
  if (offset != -1) {
    offset += search.length ;
    end = document.cookie.indexOf(";", offset) ;
    if (end == -1)
      end = document.cookie.length;
    return unescape(document.cookie.substring(offset, end));
  }
  else
    return "";
}

function deleteCookie(name) {
  setCookie(name, "");
}

function getItemsInfo(i)
{
	eval("var itemsinfo = getCookie('items["+i+"]');");
	var infoArray= itemsinfo.split('|');
	if(infoArray.length != 6)
		return -1;
	return infoArray;
}

function saveItemsinfo(infoArray, i)
{
	var itemsinfo = infoArray[0];
	for (var j = 1; j< 6; j ++)
	{
		itemsinfo = itemsinfo + '|' + infoArray[j];
	}
      	eval("setCookie('items["+i+"]', itemsinfo );");
	return;
}

function checkExistItem(infoArray, cartLength)
{
  var tmpArray = new Array;

  for (var i = 0; i < cartLength; i++) 
  {
    tmpArray = getItemsInfo(i);
    if (tmpArray[1] == infoArray[1] && tmpArray[2] == infoArray[2])
	return i;
  }
  if (i == cartLength)
	return -1;
}

function addItemQuantity(name,typeid,num,price)
{
	var infoArray = new Array;

	var cartLength = getCookie('cartLength');

	if(cartLength  == "") 
	{
	    cartLength = 0;
	    setCookie('cartLength', cartLength);
	}
	if(cartLength == 8)
	{
	    alert("您的购物车已满，请支付后继续购物！");
	    setCookie('cartLength', cartLength);
	    return;
	}
	infoArray[1] = typeid;
	infoArray[2] = num;
	var i = checkExistItem(infoArray, cartLength);

	if(i != -1)
	{
	    infoArray = getItemsInfo(i); 
	    var count = infoArray[3];
	    if(count >= 10)
	    {alert("每件商品一次购买数量只允许10个");	return;}
	    count ++;
	    infoArray[3] = count;
	    saveItemsinfo(infoArray, i);
	    openCart();
	    return;
	}

	infoArray[0] = name;
	infoArray[1] = typeid;
	infoArray[2] = num;
	infoArray[3] = 1;
	infoArray[4] = price;
	saveItemsinfo(infoArray, cartLength);

	cartLength ++;
	setCookie('cartLength', cartLength);
	openCart();
	return ;
}
