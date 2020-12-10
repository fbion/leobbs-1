package topic_controller

import (
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/app/skins"
	"gitee.com/leobbs/leobbs/app/vo"
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
)

func EditTopicAction(c *gin.Context) {

	currentMethod := "EditTopicAction@topic_controller"
	safeSess := sessions.Default(c)
	luUsername := safeSess.Get("luUsername")
	common.Sugar.Infof(currentMethod+" luUsername : %v", luUsername)
	if luUsername == nil {
		luUsername = ""
	}
	isAdmin := safeSess.Get("isAdmin")
	if isAdmin == nil {
		isAdmin = false
	}

	tid := c.Query("tid")
	if tid == "" {
		common.ShowUMessage(c, &common.Umsg{
			"贴子不存在, E-1",
			"/",
		})
		return
	}

	var tmpTopic vo.Topic_out_vo
	var rawTopic orm_model.Topic

	result := common.DB.
		Where("id = ? ", tid).
		Find(&rawTopic)

	if result.Error != nil {
		common.Sugar.Infof(currentMethod+" err: %v", result.Error)
		common.ShowUMessage(c, &common.Umsg{
			"贴子不存在, E2",
			"/",
		})
		return
	}
	tmpTopic = vo.Topic_out_vo{
		ID:        rawTopic.ID,
		ForumId:   rawTopic.ForumId,
		PostId:    rawTopic.PostId,
		AuthorUid: rawTopic.AuthorUid,
	}
	common.Sugar.Infof(currentMethod+" tmpTopic: %v", tmpTopic)

	var tmpPost vo.Post_out_vo

	var rawPost orm_model.Post

	if tmpTopic.PostId > 0 {
		result = common.DB.Order("ID ASC").
			Limit(1).
			Offset(0).
			Where("topic_id = ?", tmpTopic.ID).
			Where("id = ?", tmpTopic.PostId).
			Find(&rawPost)
	} else {
		result = common.DB.Order("ID ASC").
			Limit(1).
			Offset(0).
			Where("topic_id = ?", tmpTopic.ID).
			Find(&rawPost)
	}

	if result.Error != nil {
		common.Sugar.Infof(currentMethod+" err: %v", result.Error)
		common.ShowUMessage(c, &common.Umsg{
			"贴子不存在",
			"/",
		})
		return
	}

	tmpPost = vo.Post_out_vo{
		ID:      rawPost.ID,
		Content: rawPost.Content,
	}
	pongoContext := pongo2.Context{
		"imagesurl":  "/assets",
		"skin":       "leobbs",
		"hello":      "world",
		"luUsername": luUsername,
		"isAdmin":    isAdmin,
		"topic":      tmpTopic,
		"post":       tmpPost,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "topic/edit-topic.html", pongoContext)
}

func SaveEditTopicAction(c *gin.Context) {

	currentMethod := "SaveEditTopicAction@topic_controller"
	safeSess := sessions.Default(c)
	luUsername := safeSess.Get("luUsername")
	common.Sugar.Infof(currentMethod+" luUsername : %v", luUsername)
	if luUsername == nil {
		luUsername = ""
	}
	isAdmin := safeSess.Get("isAdmin")
	if isAdmin == nil {
		isAdmin = false
	}

	//TODO 先创建Topic，然后发帖子
	var tmpPostList []vo.Post_out_vo

	var rawPostList []orm_model.Post

	result := common.DB.Order("ID ASC").
		Limit(20).
		Offset(0).
		Find(&rawPostList)

	if result.Error != nil {
		common.Sugar.Infof(currentMethod+" err: %v", result.Error)
	}

	for _, v := range rawPostList {
		tmpPostList = append(tmpPostList, vo.Post_out_vo{
			ID:      v.ID,
			Content: v.Content,
		})
	}
}
