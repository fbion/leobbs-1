package admin_controller

import (
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
	"github.com/leobbs/leobbs/app/service/account_service"
	"github.com/leobbs/leobbs/app/skins"
)

func Index(c *gin.Context) {
	luUsername, luUid, isAdmin := account_service.AuthGetLoginUinfo(c)

	pongoContext := pongo2.Context{
		"imagesurl":  "/assets",
		"skin":       "leobbs",
		"hello":      "world",
		"luUsername": luUsername,
		"luUid":      luUid,
		"isAdmin":    isAdmin,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "admin/index.html", pongoContext)
}
