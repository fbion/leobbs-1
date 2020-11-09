package account_controller

import (
	"gitee.com/leobbs/leobbs/app/skins"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
)

func RegisterAction(c *gin.Context) {
	pongoContext := pongo2.Context{
		"imagesurl": "/assets",
		"skin":      "leobbs",
		"hello":     "world",
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "account/register.html",
		pongoContext)
}