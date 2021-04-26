package account_controller

import (
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
	"github.com/leobbs/leobbs/pkg/common"
)

func LogoutAction(c *gin.Context) {
	safeSess := sessions.Default(c)
	safeSess.Delete("luUsername")
	safeSess.Delete("lu_isAdmin")
	_ = safeSess.Save()
	common.ShowUMessage(c, &common.Umsg{Msg: "退出成功", Url: "/"})
}
