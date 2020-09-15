package  controller

import "github.com/gin-gonic/gin"

import  "github.com/flosch/pongo2"

func IndexAction(c *gin.Context) {

	c.HTML(200, "index.html", pongo2.Context{"hello": "world"})
}