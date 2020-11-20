package topic_controller

import (
	"gitee.com/leobbs/leobbs/app/form"
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/app/service/forum_service"
	"gitee.com/leobbs/leobbs/app/skins"
	"gitee.com/leobbs/leobbs/app/vo"
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"strconv"
)

func NewTopicAction(c *gin.Context) {

	currentMethod := "NewTopicAction@topic_controller"
	safeSess := sessions.Default(c)
	luUsername := safeSess.Get("lu_username")
	common.Sugar.Infof(currentMethod+" luUsername : %v", luUsername)
	if luUsername == nil {
		luUsername = ""
	}
	is_admin := safeSess.Get("is_admin")
	if is_admin == nil {
		is_admin = false
	}

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
		"is_admin":    is_admin,
		"forum":       tmpForumOut,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "topic/new-topic.html", pongoContext)
}

func SaveNewTopicAction(c *gin.Context) {

	currentMethod := "SaveNewTopicAction@topic_controller"
	safeSess := sessions.Default(c)
	luUsername := safeSess.Get("lu_username")
	common.Sugar.Infof(currentMethod+" luUsername : %v", luUsername)
	if luUsername == nil {
		luUsername = ""
	}
	is_admin := safeSess.Get("is_admin")
	if is_admin == nil {
		is_admin = false
	}

	var newTopicForm form.NewTopicForm


	err := c.MustBindWith(&newTopicForm, binding.Form)
	if err != nil {
		common.LogError(err)
		common.ShowUMessage(c, &common.Umsg{Msg: "发布失败", Url: "javascript:history.go(-1);"})
		return
	}
	common.Sugar.Infof(currentMethod + " newTopicForm: %v", newTopicForm)

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
