package account_controller

import (
	"gitee.com/leobbs/leobbs/app/form"
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/app/skins"
	"gitee.com/leobbs/leobbs/pkg/common"
	"gitee.com/leobbs/leobbs/pkg/passwd_utils"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
)

func RegisterAction(c *gin.Context) {
	pongoContext := pongo2.Context{
		"imagesurl": "/assets",
		"skin":      "leobbs",
		"hello":     "world",
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "account/register.html",
		pongoContext)
}

func FinishRegAction(c *gin.Context) {
	currentMethod := "FinishRegAction"

	var regForm form.RegisterForm
	err := c.MustBindWith(&regForm, binding.Form)
	if err != nil {
		common.LogError(err)
		common.ShowUMessage(c, &common.Umsg{Msg: "注册失败", Url: "javascript:history.go(-1);"})
		return
	}


	if regForm.Password != regForm.Password2 {
		common.ShowUMessage(c, &common.Umsg{Msg: "两次输入密码不匹配", Url: "javascript:history.go(-1);"})
		return
	}

	var mm orm_model.Member

	result := common.DB.Where(" username = ? ", regForm.Username).Find(&mm)
	if result.Error != nil {
		common.Sugar.Info(currentMethod + " error: %v", result.Error)
	} else {
		if mm.Username == regForm.Username {
			common.ShowUMessage(c, &common.Umsg{
				Msg: "用户名已存在",
				Url: "javascript:history.go(-1);",
			})
			return
		}
	}
	result = common.DB.Where(" email = ? ", regForm.Email).Find(&mm)
	if result.Error != nil {
		common.Sugar.Info(currentMethod + " error: %v", result.Error)
	} else {
		if mm.Email == regForm.Email {
			common.ShowUMessage(c, &common.Umsg{
				Msg: "邮箱已存在",
				Url: "javascript:history.go(-1);",
			})
			return
		}
	}



	hashStr, passwdStr, err := passwd_utils.HashPassword(regForm.Password)
	if err != nil {
		common.Sugar.Error(currentMethod + " error: %v", err)
		common.ShowUMessage(c, &common.Umsg{
			"生成密码Hash错误",
			"javascript:history.go(-1);",
		})
		return
	}
	mm.Salt = hashStr
	mm.Password = passwdStr
	mm.Username = regForm.Username
	mm.Email = regForm.Email

	result = common.DB.Create(&mm)
	if result.Error != nil {
		common.Sugar.Errorf(currentMethod + " error: %v", err)
		common.ShowUMessage(c, &common.Umsg{
			"注册失败",
			"javascript:history.go(-1);",
		})
		return
	}


	if mm.ID > 0 {
		common.ShowUMessage(c, &common.Umsg{
			"注册成功,请登录吧",
			"/",
		})
		return
	}
	common.ShowUMessage(c, &common.Umsg{
		"注册失败",
		"javascript:history.go(-1);",
	})
}

