package topic_controller

import (
	"fmt"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"github.com/leobbs/leobbs/app/form"
	"github.com/leobbs/leobbs/app/orm_model"
	"github.com/leobbs/leobbs/app/service/account_service"
	"github.com/leobbs/leobbs/app/service/forum_service"
	"github.com/leobbs/leobbs/app/vo"
	"github.com/leobbs/leobbs/pkg/common"
	"strconv"
)

func NewTopicAction(c *gin.Context) {

	currentMethod := "NewTopicAction@topic_controller"
	luUsername, luUid, isAdmin := account_service.AuthGetLoginUinfo(c)

	common.Sugar.Infof(currentMethod+" params: %v", c.Params)

	id := c.Query("fid")
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
		common.ShowUMessage(c, &common.Umsg{
			"论坛不存在",
			"/",
		})
		return
	}

	var tmpForumOut vo.Forum_out_vo

	if forum != nil {

		tmpForumOut.ID = forum.ID
		tmpForumOut.ForumName = forum.Name
		tmpForumOut.ForumDesc = forum.Description

	}

	c.HTML(200, "topic/new-topic.html",
		common.Pongo2ContextWithVersion(pongo2.Context{
			"imagesurl":  "/assets",
			"skin":       "leobbs",
			"hello":      "world",
			"luUsername": luUsername,
			"luUid":      luUid,
			"isAdmin":    isAdmin,
			"forum":      tmpForumOut,
		}))
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
	common.Sugar.Infof(currentMethod+" newTopicForm: %v", newTopicForm)

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

	tmpTopic.PostId = tmpPost.ID
	//记录PostId到Topic表
	common.DB.Save(&tmpTopic)

	common.LogError(err)
	common.ShowUMessage(c, &common.Umsg{
		Msg: "发布成功",
		Url: fmt.Sprintf("/topic/%d", tmpTopic.ID),
	})
}
