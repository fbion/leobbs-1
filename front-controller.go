package main

import (
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
	"github.com/gorilla/websocket"
	"github.com/rs/zerolog/log"
	"net/http"
)

type FrontController struct {
}

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

func echo(w http.ResponseWriter, r *http.Request) {
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		common.LogError(err)
		return
	}
	defer c.Close()
	for {
		mt, message, err := c.ReadMessage()
		if err != nil {
			common.LogError(err)
			break
		}
		log.Info().Msgf("recv: %s", message)
		err = c.WriteMessage(mt, message)
		if err != nil {
			common.LogError(err)
			break
		}
	}
}
func (fc *FrontController) WsCtr(c *gin.Context) {

	echo(c.Writer, c.Request)

}
func (fc *FrontController) HomeCtr(c *gin.Context) {
	c.JSON(200, "[]")
}
