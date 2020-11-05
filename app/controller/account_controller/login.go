package account_controller

import (
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
)

func LoginAction(c *gin.Context) {

	c.HTML(200, "account/login.html",
		pongo2.Context{"hello": "world"})
}
