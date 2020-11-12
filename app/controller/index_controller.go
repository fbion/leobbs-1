package  controller

import (
	"gitee.com/leobbs/leobbs/app/skins"
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
)

func IndexAction(c *gin.Context) {
	currentMethod := "IndexAction"
	safeSess := sessions.Default(c)
	luUsername := safeSess.Get("lu_username")
	common.Sugar.Infof(currentMethod +  " luUsername : %v", luUsername)
	if luUsername == nil {
		luUsername = ""
	}
	pongoContext := pongo2.Context{
		"imagesurl":   "/assets",
		"skin":        "leobbs",
		"hello":       "world",
		"lu_username": luUsername,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "index.html", pongoContext)
}