package admin_controller

import (
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
	"github.com/leobbs/leobbs/pkg/common"
)

func LoginAction(c *gin.Context) {

	c.HTML(200, "admin/login.html",
		common.Pongo2ContextWithVersion(pongo2.Context{

			"imagesurl":        "/assets",
			"skin":             "leobbs",
			"hello":            "world",
		}))
}
