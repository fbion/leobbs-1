package controller

import (
	"fmt"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
	"github.com/leobbs/leobbs/app/service/account_service"
	"github.com/leobbs/leobbs/app/service/forum_service"
	"github.com/leobbs/leobbs/app/vo"
	"github.com/leobbs/leobbs/pkg/common"
)

func IndexAction(c *gin.Context) {
	luUsername, luUid, isAdmin := account_service.AuthGetLoginUinfo(c)

	var forumOutList []vo.Forum_out_vo
	forumList, err := forum_service.GetForumList()
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

	common.Sugar.Infof("ForumList: %+v", forumOutList)
	cnt := account_service.CountRegMember()

	c.HTML(200, "index.html",
		common.Pongo2ContextWithVersion(pongo2.Context{

			"imagesurl":        "/assets",
			"skin":             "leobbs",
			"hello":            "world",
			"luUsername":       luUsername,
			"luUid":            luUid,
			"isAdmin":          isAdmin,
			"forumsList":       forumOutList,
			"memberTotalCount": fmt.Sprintf("%d", cnt),
		}))
}
