package account_controller

import (
	"gitee.com/leobbs/leobbs/app/skins"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
)

func LoginAction(c *gin.Context) {
	pongoContext := pongo2.Context{
		"imagesurl": "/assets",
		"skin":      "leobbs",
		"hello":     "world",
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "account/login.html",
		pongoContext)
}


func DoLoginAction(c *gin.Context) {





	pongoContext := pongo2.Context{
		"imagesurl": "/assets",
		"skin":      "leobbs",
		"hello":     "world",
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "account/login.html",
		pongoContext)
}
