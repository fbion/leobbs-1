package topic_controller

import (
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
	"github.com/leobbs/leobbs/app/orm_model"
	"github.com/leobbs/leobbs/app/service/account_service"
	"github.com/leobbs/leobbs/app/vo"
	"github.com/leobbs/leobbs/pkg/common"
	"github.com/russross/blackfriday/v2"
	"strings"
)

func IndexAction(c *gin.Context) {

	currentMethod := "IndexAction@topic_controller"

	luUsername, luUid, isAdmin := account_service.AuthGetLoginUinfo(c)

	var topicIndexUri vo.TopicIndexUri
	if err := c.ShouldBindUri(&topicIndexUri); err != nil {
		common.ShowUMessage(c, &common.Umsg{
			"贴子不存在",
			"/",
		})
		return
	}

	id := c.Param("id")
	if id == "" {
		common.ShowUMessage(c, &common.Umsg{
			"贴子不存在",
			"/",
		})
		return
	}

	var tmpTopic vo.Topic_out_vo

	var tmpTopicRaw orm_model.Topic

	result := common.DB.First(&tmpTopicRaw, id)
	if result.Error != nil {
		common.Sugar.Infof(currentMethod+" query Topic error: %v", result.Error)
		common.ShowUMessage(c, &common.Umsg{
			"贴子不存在",
			"/",
		})
		return
	}
	tmpTopic.ID = tmpTopicRaw.ID
	tmpTopic.Title = tmpTopicRaw.Title
	tmpTopic.ForumId = tmpTopicRaw.ForumId
	tmpTopic.AuthorUid = tmpTopicRaw.AuthorUid

	var tmpForum vo.Forum_out_vo

	var tmpForumRaw orm_model.Forum

	result = common.DB.First(&tmpForumRaw, tmpTopic.ForumId)
	if result.Error != nil {
		common.Sugar.Infof(currentMethod+" query Forum error: %v", result.Error)
		common.ShowUMessage(c, &common.Umsg{
			"论坛不存在",
			"/",
		})
		return
	}

	tmpForum.ID = tmpForumRaw.ID
	tmpForum.ForumName = tmpForumRaw.Name
	tmpForum.ForumDesc = tmpForumRaw.Description

	page, prevPage, nextPage := common.PageHelper(c)

	var tmpPostList []vo.Post_out_vo

	var rawPostList []orm_model.Post

	result = common.DB.Order("ID ASC").
		Where("topic_id = ? ", id).
		Limit(20).
		Offset(page * 20).
		Find(&rawPostList)

	if result.Error != nil {
		common.Sugar.Infof(currentMethod+" err: %v", result.Error)
	}

	for _, v := range rawPostList {
		common.Sugar.Infof(currentMethod+" post: %+v", v)
		originContent := strings.Replace(v.Content, "\r\n", "\n", -1)
		unsafeContent := blackfriday.Run([]byte(originContent))
		safeContent := string(unsafeContent[:])
		common.Sugar.Infof("safeContent: %s", safeContent)
		tmpUserInfo := account_service.GetUserInfo(v.PostUid)
		common.Sugar.Infof(currentMethod+" userInfo: %+v", tmpUserInfo)
		tmpPostList = append(tmpPostList, vo.Post_out_vo{
			UserInfo: tmpUserInfo,
			ID:       v.ID,
			Content:  safeContent,
		})
	}


	c.HTML(200, "topic/topic.html",
		common.Pongo2ContextWithVersion(pongo2.Context{
			"imagesurl":  "/assets",
			"skin":       "leobbs",
			"hello":      "world",
			"luUsername": luUsername,
			"luUid":      luUid,
			"isAdmin":    isAdmin,
			"topic":      tmpTopic,
			"forum":      tmpForum,
			"postList":   tmpPostList,
			"prevPage":   prevPage,
			"nextPage":   nextPage,
		}))

}
