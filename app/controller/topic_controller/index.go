package topic_controller

import (
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/app/service/account_service"
	"gitee.com/leobbs/leobbs/app/skins"
	"gitee.com/leobbs/leobbs/app/vo"
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
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
		common.Sugar.Infof(currentMethod + " query Topic error: %v", result.Error)
		common.ShowUMessage(c, &common.Umsg{
			"贴子不存在",
			"/",
		})
		return;
	}
	tmpTopic.ID = tmpTopicRaw.ID
	tmpTopic.Title = tmpTopicRaw.Title
	tmpTopic.ForumId = tmpTopicRaw.ForumId


	var tmpForum vo.Forum_out_vo

	var tmpForumRaw orm_model.Forum

	result = common.DB.First(&tmpForumRaw, tmpTopic.ForumId)
	if result.Error != nil {
		common.Sugar.Infof(currentMethod + " query Forum error: %v", result.Error)
		common.ShowUMessage(c, &common.Umsg{
			"论坛不存在",
			"/",
		})
		return;
	}

	tmpForum.ID = tmpForumRaw.ID
	tmpForum.ForumName = tmpForumRaw.Name
	tmpForum.ForumDesc = tmpForumRaw.Description

	var tmpPostList []vo.Post_out_vo

	var rawPostList []orm_model.Post

	result = common.DB.Order("ID ASC").
		Where("topic_id = ? ", id).
		Limit(20).
		Offset(0).
		Find(&rawPostList)

	if result.Error != nil {
		common.Sugar.Infof(currentMethod + " err: %v", result.Error)
	}

	for _, v := range rawPostList {
		tmpPostList = append(tmpPostList, vo.Post_out_vo{
			ID: v.ID,
			Content: v.Content,
		})
	}





	pongoContext := pongo2.Context{
		"imagesurl":   "/assets",
		"skin":        "leobbs",
		"hello":       "world",
		"lu_username": luUsername,
		"lu_uid": luUid,
		"isAdmin": isAdmin,
		"topic": tmpTopic,
		"forum": tmpForum,
		"postList": tmpPostList,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "topic/topic.html", pongoContext)
}