package member_admin_controller

import (
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/app/service/account_service"
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/gin-gonic/gin"
	"net/http"
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
	c.JSON(http.StatusOK, members)
	return
}
