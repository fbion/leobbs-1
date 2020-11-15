package  controller

import (
	"gitee.com/leobbs/leobbs/app/service/forum_service"
	"gitee.com/leobbs/leobbs/app/skins"
	"gitee.com/leobbs/leobbs/app/vo"
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
	is_admin := safeSess.Get("is_admin")
	if is_admin == nil {
		is_admin = false
	}

	var forumOutList []vo.Forum_out_vo
	forumList , err := forum_service.GetForumList()
	if err != nil {
		common.Sugar.Error(err)
	}
	if forumList != nil {

		for _, tmpForum := range forumList {
			var tmpForumOut vo.Forum_out_vo
			tmpForumOut.ID = tmpForum.ID
			tmpForumOut.ForumName = tmpForum.Name
			tmpForumOut.ForumDesc = tmpForum.Description
			forumOutList = append(forumOutList, tmpForumOut)
		}

	}

	pongoContext := pongo2.Context{
		"imagesurl":   "/assets",
		"skin":        "leobbs",
		"hello":       "world",
		"lu_username": luUsername,
		"is_admin": is_admin,
		"forumsList": forumOutList,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "index.html", pongoContext)
}