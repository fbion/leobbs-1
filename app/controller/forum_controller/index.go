package forum_controller

import (
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/app/service/forum_service"
	"gitee.com/leobbs/leobbs/app/skins"
	"gitee.com/leobbs/leobbs/app/vo"
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
	"strconv"
)




func IndexAction(c *gin.Context) {
	currentMethod := "IndexAction@forum_controller"
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

	common.Sugar.Infof(currentMethod + " params: %v", c.Params)

	var forumIndexUri vo.ForumIndexUri
	if err:= c.ShouldBindUri(&forumIndexUri); err != nil {
		common.ShowUMessage(c, &common.Umsg{
			"论坛不存在",
			"/",
		})
		return
	}

	id := c.Param("id")
	if id == "" {
		common.ShowUMessage(c, &common.Umsg{
			"论坛id不存在",
			"/",
		})
		return
	}
	idVal, err := strconv.ParseInt(id, 10, 64)
	common.Sugar.Infof(currentMethod + " idVal: %d", idVal)
	if err != nil {
		common.ShowUMessage(c, &common.Umsg{
			"论坛id不存在",
			"/",
		})
		return
	}
	forum , err := forum_service.GetForum(idVal)
	if err != nil {
		common.Sugar.Error(err)
	}


	var tmpForumOut vo.Forum_out_vo

	if forum != nil {

			tmpForumOut.ID = forum.ID
			tmpForumOut.ForumName = forum.Name
			tmpForumOut.ForumDesc = forum.Description

	}

	//处理论坛发帖

	var tmpTopicList []vo.Topic_out_vo

	var rawTopicList []orm_model.Topic

	result := common.DB.Order("ID desc").
		Limit(20).
		Offset(0).
		Find(&rawTopicList)

	if result.Error != nil {
		common.Sugar.Infof(currentMethod + " err: %v", result.Error)
	}

	for _, v := range rawTopicList {
		tmpTopicList = append(tmpTopicList, vo.Topic_out_vo{
			ID: v.ID,
			Title: v.Title,
		})
	}


	common.Sugar.Infof(currentMethod + " topicList: %v", tmpTopicList)
	pongoContext := pongo2.Context{
		"imagesurl":   "/assets",
		"skin":        "leobbs",
		"hello":       "world",
		"lu_username": luUsername,
		"is_admin": is_admin,
		"forum": tmpForumOut,
		"topicList": tmpTopicList,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "forum.html", pongoContext)
}
