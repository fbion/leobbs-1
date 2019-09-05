package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gorilla/websocket"
	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
	"github.com/rs/zerolog/log"
	"html/template"
	"net/http"
	"strconv"
	"strings"
	"time"
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
		log.Print("upgrade:", err)
		return
	}
	defer c.Close()
	for {
		mt, message, err := c.ReadMessage()
		if err != nil {
			LogError(err)
			break
		}
		log.Printf("recv: %s", message)
		err = c.WriteMessage(mt, message)
		if err != nil {
			LogError(err)
			break
		}
	}
}
func (fc *FrontController) WsCtr(c *gin.Context) {

	echo(c.Writer, c.Request)


}
func (fc *FrontController) HomeCtr(c *gin.Context) {

	var (
		aid          int
		content      sql.NullString
		images       sql.NullString
		imagesList   []string
		publish_time sql.NullString
	)
	session := sessions.Default(c)
	username := session.Get("username")
	if username == nil {
		(&umsg{"You have no permission", "/admin/login"}).ShowMessage(c)
		return
	}
	page, err := strconv.Atoi(c.DefaultQuery("page", "1"))
	if err != nil {
		fmt.Println(err)
	}
	page -= 1
	if page < 0 {
		page = 0
	}

	prevPage := page
	if prevPage < 1 {
		prevPage = 1
	}
	nextPage := page + 2

	rpp := 20
	offset := page * rpp
	var blogList string
	rows, err := DB.Query("Select aid, content, images, publish_time from article where publish_status = 1 order by aid desc limit ? , ? ", &offset, &rpp)
	if err != nil {
		fmt.Println(err)
	}
	defer CloseRowsDefer(rows)
	for rows.Next() {
		err := rows.Scan(&aid, &content, &images, &publish_time)
		if err != nil {
			fmt.Println(err)
		}
		imagesHtml := ""
		if images.Valid {
			imagesStr := strings.ReplaceAll(images.String, "\\", "")
			log.Info().Msg(imagesStr)
			err = json.Unmarshal([]byte(imagesStr), &imagesList)
			if err != nil {
				LogError(err)
			} else {
				for i := range imagesList {
					if len(imagesList[i]) > 0 {
						imagesHtml += "<img src=\"" + imagesList[i] + "?act=resize&x=640\" />"
					}
				}
			}
		}
		tmInt, err := strconv.ParseInt(publish_time.String, 10, 64)
		if err == nil {
			tmStr := time.Unix(tmInt, 0)
			blogList += fmt.Sprintf(
				"<div>%s <br />%s<span class=\"post_time\">%s</span><hr /></div>",
				content.String,
				imagesHtml,
				tmStr.Format("2006-01-02 15:04:05"),
			)
		} else {
			LogError(err)
		}
	}
	err = rows.Err()
	if err != nil {
		fmt.Println(err)
	}
	c.HTML(http.StatusOK, "index.html", gin.H{
		"content":          content,
		"site_name":        Config.Site_name,
		"site_description": Config.Site_description,
		"bloglist":         template.HTML(blogList),
		"username":         username,
		"prev_page":        prevPage,
		"next_page":        nextPage,
	})
}
