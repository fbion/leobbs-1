package topic_controller

import (
	"fmt"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"github.com/leobbs/leobbs/app/form"
	"github.com/leobbs/leobbs/app/orm_model"
	"github.com/leobbs/leobbs/app/service/account_service"
	"github.com/leobbs/leobbs/app/skins"
	"github.com/leobbs/leobbs/app/vo"
	"github.com/leobbs/leobbs/pkg/common"
)

func NewPostAction(c *gin.Context) {

	currentMethod := "NewPostAction@topic_controller"
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
			"贴子不存在",
			"/",
		})
		return
	}

	var tmpTopic vo.Topic_out_vo

	var topicModel orm_model.Topic
	result := common.DB.Where("id = ?", tid).
		Find(&topicModel)

	if result.Error != nil {
		common.Sugar.Infof(currentMethod+" err: %v", result.Error)
	}

	tmpTopic.ForumId = topicModel.ForumId
	tmpTopic.ID = topicModel.ID

	pongoContext := pongo2.Context{
		"imagesurl":  "/assets",
		"skin":       "leobbs",
		"hello":      "world",
		"luUsername": luUsername,
		"isAdmin":    isAdmin,
		"topic":      tmpTopic,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "topic/new-post.html", pongoContext)
}

func SaveNewPostAction(c *gin.Context) {

	currentMethod := "SaveNewPostAction@topic_controller"
	_, luUid, _ := account_service.AuthGetLoginUinfo(c)

	var newPostForm form.NewPostForm

	err := c.MustBindWith(&newPostForm, binding.Form)
	if err != nil {
		common.LogError(err)
		common.ShowUMessage(c, &common.Umsg{Msg: "发布失败", Url: "javascript:history.go(-1);"})
		return
	}
	common.Sugar.Infof(currentMethod+" newPostForm: %v", newPostForm)

	var tmpPost orm_model.Post

	tmpPost.TopicId = newPostForm.Tid
	tmpPost.Content = newPostForm.Content
	tmpPost.PostUid = luUid.(int64)

	result := common.DB.Create(&tmpPost)
	if result.Error != nil {

		common.LogError(err)
		common.ShowUMessage(c, &common.Umsg{Msg: "发布失败", Url: "javascript:history.go(-1);"})
		return
	}

	common.LogError(err)
	common.ShowUMessage(c, &common.Umsg{
		Msg: "发布成功",
		Url: fmt.Sprintf("/topic/%d", newPostForm.Tid),
	})
}
