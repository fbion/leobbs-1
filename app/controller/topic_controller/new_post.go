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

func NewPostAction(c *gin.Context) {

		currentMethod := "NewPostAction@topic_controller"
		safeSess := sessions.Default(c)
		luUsername := safeSess.Get("lu_username")
		common.Sugar.Infof(currentMethod +  " luUsername : %v", luUsername)
		if luUsername == nil {
			luUsername = ""
		}
		isAdmin := safeSess.Get("isAdmin")
		if isAdmin == nil {
			isAdmin = false
		}

		var tmpPostList []vo.Post_out_vo

		var rawPostList []orm_model.Post

		result := common.DB.Order("ID ASC").
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
			"isAdmin": isAdmin,
			"postList": tmpPostList,
		}

		for tmpKey, tmpV := range skins.GetLeobbsSkin() {
			pongoContext[tmpKey] = tmpV
		}
		c.HTML(200, "topic/new-topic.html", pongoContext)
}


func SaveNewPostAction(c *gin.Context) {

	currentMethod := "SaveNewPostAction@topic_controller"
	safeSess := sessions.Default(c)
	luUsername := safeSess.Get("lu_username")
	common.Sugar.Infof(currentMethod +  " luUsername : %v", luUsername)
	if luUsername == nil {
		luUsername = ""
	}
	isAdmin := safeSess.Get("isAdmin")
	if isAdmin == nil {
		isAdmin = false
	}


	//TODO 先创建Post，然后发帖子
	var tmpPostList []vo.Post_out_vo

	var rawPostList []orm_model.Post

	result := common.DB.Order("ID ASC").
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
}