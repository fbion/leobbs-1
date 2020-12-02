package member_admin_controller

import (
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/app/service/account_service"
	"gitee.com/leobbs/leobbs/app/skins"
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
)

func IndexAction(c *gin.Context) {

	currentMethod := "IndexAction@forum_controller"

	luUsername, luUid, isAdmin := account_service.AuthGetLoginUinfo(c)

	if isAdmin == nil || isAdmin == false {
		common.Sugar.Infof(currentMethod + " bad access: username: %v, uid: %v, isAdmin: %v", luUsername, luUid, isAdmin);
		common.ShowMessage(c, &common.Msg{
			"您没有权限",
		})
		return;
	}
	var members []orm_model.Member
	result := common.DB.Find(&members)
	if result.Error != nil {
		common.Sugar.Error(currentMethod + " err: %v", result.Error)
	}


	pongoContext := pongo2.Context{
		"imagesurl":   "/assets",
		"skin":        "leobbs",
		"hello":       "world",
		"lu_username": luUsername,
		"lu_uid": luUid,
		"isAdmin": isAdmin,
		"memberList": members,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "admin/member/index.html", pongoContext)
	return
}
