package topic_controller

import (
	"fmt"
	"gitee.com/leobbs/leobbs/app/form"
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/app/service/account_service"
	"gitee.com/leobbs/leobbs/app/service/forum_service"
	"gitee.com/leobbs/leobbs/app/skins"
	"gitee.com/leobbs/leobbs/app/vo"
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"strconv"
)

func NewTopicAction(c *gin.Context) {

	currentMethod := "NewTopicAction@topic_controller"
	luUsername, luUid, isAdmin := account_service.AuthGetLoginUinfo(c)

	common.Sugar.Infof(currentMethod+" params: %v", c.Params)

	id := c.Query("id")
	if id == "" {
		common.ShowUMessage(c, &common.Umsg{
			"论坛id不存在",
			"/",
		})
		return
	}
	idVal, err := strconv.ParseInt(id, 10, 64)
	common.Sugar.Infof(currentMethod+" idVal: %d", idVal)
	if err != nil {
		common.ShowUMessage(c, &common.Umsg{
			"论坛id不存在",
			"/",
		})
		return
	}
	forum, err := forum_service.GetForum(idVal)
	if err != nil {
		common.Sugar.Error(err)
	}

	var tmpForumOut vo.Forum_out_vo

	if forum != nil {

		tmpForumOut.ID = forum.ID
		tmpForumOut.ForumName = forum.Name
		tmpForumOut.ForumDesc = forum.Description

	}

	pongoContext := pongo2.Context{
		"imagesurl":   "/assets",
		"skin":        "leobbs",
		"hello":       "world",
		"lu_username": luUsername,
		"lu_uid": luUid,
		"isAdmin":    isAdmin,
		"forum":       tmpForumOut,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "topic/new-topic.html", pongoContext)
}

func SaveNewTopicAction(c *gin.Context) {

	currentMethod := "SaveNewTopicAction@topic_controller"
	_, luUid, _ := account_service.AuthGetLoginUinfo(c)

	var newTopicForm form.NewTopicForm


	err := c.MustBindWith(&newTopicForm, binding.Form)
	if err != nil {
		common.LogError(err)
		common.ShowUMessage(c, &common.Umsg{Msg: "发布失败", Url: "javascript:history.go(-1);"})
		return
	}
	common.Sugar.Infof(currentMethod + " newTopicForm: %v", newTopicForm)

	//TODO 先创建Topic，然后发帖子
	var tmpTopic orm_model.Topic

	tmpTopic.Title = newTopicForm.Title
	tmpTopic.ForumId = newTopicForm.Fid
	tmpTopic.AuthorUid = luUid.(int64)



	result := common.DB.Create(&tmpTopic)
	if result.Error != nil {
		common.LogError(err)
		common.ShowUMessage(c, &common.Umsg{Msg: "发布失败", Url: "javascript:history.go(-1);"})
		return
	}
	var tmpPost orm_model.Post

	tmpPost.TopicId = tmpTopic.ID
	tmpPost.Content = newTopicForm.Content
	tmpPost.PostUid = luUid.(int64)

	result = common.DB.Create(&tmpPost)
	if result.Error != nil {

		common.LogError(err)
		common.ShowUMessage(c, &common.Umsg{Msg: "发布失败", Url: "javascript:history.go(-1);"})
		return
	}


	common.LogError(err)
	common.ShowUMessage(c, &common.Umsg{
		Msg: "发布成功",
		Url: fmt.Sprintf("/topic/%d", tmpTopic.ID),
	})
}
