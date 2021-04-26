package member_admin_controller

import (
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
	"github.com/leobbs/leobbs/app/orm_model"
	"github.com/leobbs/leobbs/app/service/account_service"
	"github.com/leobbs/leobbs/app/skins"
	"github.com/leobbs/leobbs/pkg/common"
)

func IndexAction(c *gin.Context) {

	currentMethod := "IndexAction@forum_controller"

	luUsername, luUid, isAdmin := account_service.AuthGetLoginUinfo(c)

	if isAdmin == nil || isAdmin == false {
		common.Sugar.Infof(currentMethod+" bad access: username: %v, uid: %v, isAdmin: %v", luUsername, luUid, isAdmin)
		common.ShowMessage(c, &common.Msg{
			"您没有权限",
		})
		return
	}

	page, prevPage, nextPage := common.PageHelper(c)

	var members []orm_model.Member
	result := common.DB.Limit(20).
		Offset(page * 20).
		Find(&members)
	if result.Error != nil {
		common.Sugar.Error(currentMethod+" err: %v", result.Error)
	}

	pongoContext := pongo2.Context{
		"imagesurl":  "/assets",
		"skin":       "leobbs",
		"hello":      "world",
		"luUsername": luUsername,
		"luUid":      luUid,
		"isAdmin":    isAdmin,
		"memberList": members,
		"prevPage":   prevPage,
		"nextPage":   nextPage,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "admin/member/index.html", pongoContext)
	return
}
