package  controller

import (
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
)

func IndexAction(c *gin.Context) {

	c.HTML(200, "index.html", pongo2.Context{"hello": "world"})
}