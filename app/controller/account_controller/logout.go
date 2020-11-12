package account_controller

import (
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
)

func LogoutAction(c *gin.Context) {
	safeSess := sessions.Default(c)
	safeSess.Delete("lu_username")
	safeSess.Delete("lu_is_admin")
	_ = safeSess.Save()
	common.ShowUMessage(c, &common.Umsg{Msg: "退出成功", Url: "/"})
}
