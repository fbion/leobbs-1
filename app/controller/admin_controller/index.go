package admin_controller

import (
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
)

func Index(c *gin.Context) {

	c.HTML(200, "admin/index.html", pongo2.Context{"hello": "world"})
}

func Login(c *gin.Context) {

	c.HTML(200, "admin/login.html",
		pongo2.Context{"hello": "world"})
}

